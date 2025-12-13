import html
import json
import os
import tempfile
from abc import ABC, abstractmethod
from collections import defaultdict
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any, Mapping

from loguru import logger as loguru
from rich.pretty import pprint

from adaptive_harmony.logging_table import Table


class Logger(ABC):
    @abstractmethod
    def __call__(self, metrics: Mapping[str, str | int | float | Table]): ...

    @abstractmethod
    def log_config(self, config: dict[str, Any]): ...

    @staticmethod
    @abstractmethod
    def is_available() -> bool: ...

    @property
    def training_monitoring_link(self) -> str | None:
        return None

    def close(self):
        pass


class MLFlowLogger(Logger):
    def __init__(
        self,
        project_name: str,
        run_name: str,
        tracking_uri: str,
        monitoring_link: str | None = None,
        experiment_tags: dict[str, str] | None = None,
        run_tags: dict[str, str] | None = None,
        min_table_logging_step_interval: int = 5,
    ):
        try:
            import mlflow
        except ImportError:
            raise ImportError(
                "MLFlow is not available."
                "To install adaptive-harmony with MLFlow support, install `adaptive-harmony[mlflow]`"
            )

        self._mlflow = mlflow
        mlflow.set_tracking_uri(tracking_uri)
        _ = mlflow.set_experiment(project_name)
        if experiment_tags:
            _ = mlflow.set_experiment_tags(experiment_tags)
        self.run = mlflow.start_run(run_name=run_name, log_system_metrics=None, tags=run_tags)
        self.monitoring_link = monitoring_link
        self.step = 0
        self.last_logged_tables_step = 0
        self.min_table_logging_step_interval = min_table_logging_step_interval
        self._log_tables_as_artifacts: bool = False

    @staticmethod
    def is_available() -> bool:
        try:
            import mlflow  # noqa: F401

            return True
        except ImportError:
            return False

    def __call__(self, metrics: Mapping[str, str | int | float | Table]):
        metric_logs: dict[str, float] = {}
        str_logs: dict[str, str] = {}
        tables: dict[str, Table] = {}
        for entry, data in metrics.items():
            if isinstance(data, int) or isinstance(data, float):
                metric_logs.update({entry: float(data)})
            elif isinstance(data, Table):
                tables.update({entry: data})
            elif isinstance(data, str):
                str_logs.update({entry: data})
            else:
                print(f"MLFlow logger does not support type: {type(data)}")
        self._mlflow.log_metrics(metric_logs, step=self.step, synchronous=True)
        self._mlflow.log_params(str_logs)

        if self.step == 0 or (self.step - self.last_logged_tables_step > self.min_table_logging_step_interval):
            for table_entry, table in tables.items():
                headers, rows = table.export()
                # Transpose rows to columns for MLflow
                if rows:
                    columns = list(zip(*rows))
                    table_dict = {header: list(column) for header, column in zip(headers, columns)}
                    table_file_name = f"{table_entry}/step_{self.step}.json"
                    if not self._log_tables_as_artifacts:
                        try:
                            self._mlflow.log_table(data=table_dict, artifact_file=table_file_name)
                        except JSONDecodeError:
                            loguru.warning(
                                f"Reached limit of # tables that can be logged to a single run at step {self.step}"
                                "logging tables as artifacts from now on"
                            )
                            self._log_tables_as_artifacts = True
                    else:
                        with tempfile.TemporaryDirectory() as tmp_dir:
                            path = Path(tmp_dir, table_file_name.replace("/", "_"))
                            path.parent.mkdir(parents=True, exist_ok=True)
                            path.write_text(json.dumps(table_dict))
                            self._mlflow.log_artifact(local_path=str(path))
            self.last_logged_tables_step = self.step

        self.step += 1

    def log_config(self, config: dict[str, Any]):
        for key, value in config.items():
            try:
                # MLflow handles params differently - convert to string for complex types
                if isinstance(value, (dict, list)):
                    self._mlflow.log_param(key, json.dumps(value))
                else:
                    self._mlflow.log_param(key, value)
            except Exception as e:
                print(
                    f"Warning: Argument '{key}' with value '{str(value)[:100]}...' "
                    f"(type: {type(value).__name__}) could not be logged to mlflow. Error: {e}"
                )

    @property
    def training_monitoring_link(self) -> str:
        return self.monitoring_link or self._mlflow.get_tracking_uri()

    def close(self):
        self._mlflow.end_run()


class WandbLogger(Logger):
    def __init__(
        self,
        project_name: str,
        run_name: str,
        entity: str | None = None,
    ):
        try:
            import wandb
        except ImportError:
            raise ImportError(
                "WandB is not available."
                "To install adaptive-harmony with WandB support, install `adaptive-harmony[wandb]`"
            )

        self._wandb = wandb
        self.run = wandb.init(project=project_name, name=run_name, entity=entity)
        self.step = 0

    @staticmethod
    def is_available() -> bool:
        try:
            import wandb  # noqa: F401

            return True
        except ImportError:
            return False

    def __call__(self, metrics: Mapping[str, str | int | float | Table]):
        logs = {k: self._process_metric(v) for k, v in metrics.items()}
        str_logs = {k: str(v) for k, v in logs.items() if isinstance(v, str)}
        metric_logs = {k: v for k, v in logs.items() if not isinstance(v, str)}
        self._wandb.log(metric_logs, step=self.step, commit=True)
        self.run.config.update(str_logs)
        self.step += 1

    def log_config(self, config: dict[str, Any]):
        for key, value in config.items():
            try:
                self.run.config[key] = value
            except Exception as e:
                print(
                    f"Warning: Argument '{key}' with value '{str(value)[:100]}...' "
                    f"(type: {type(value).__name__}) could not be logged to wandb. Error: {e}"
                )

    def _process_metric(self, metric: str | int | float | Table):
        if isinstance(metric, Table):
            headers, rows = metric.export()
            return self._wandb.Table(columns=headers, data=rows)
        else:
            return metric

    @property
    def training_monitoring_link(self) -> str:
        return self.run.get_url()  # type: ignore

    def close(self):
        self._wandb.finish()


class TBMetricsLogger(Logger):
    def __init__(self, run_name: str, logging_dir: str, monitoring_link: str | None = None):
        try:
            from tensorboardX import SummaryWriter
        except ImportError:
            loguru.error(
                "Tensorboard is not available."
                "To install adaptive-harmony with TB support, install `adaptive-harmony[tensorboard]"
            )
            raise

        self.monitoring_link = monitoring_link
        self.logging_dir = os.path.join(logging_dir, run_name)
        self.writer = SummaryWriter(str(self.logging_dir), flush_secs=15)
        self.step = 0

    @staticmethod
    def is_available() -> bool:
        try:
            from tensorboardX import SummaryWriter  # noqa: F401

            return True
        except ImportError:
            return False

    def __call__(self, logs: Mapping[str, str | int | float | Table]):
        modified_tables = False
        for entry, data in logs.items():
            if isinstance(data, int) or isinstance(data, float):
                self.writer.add_scalar(entry, float(data), self.step)
            elif isinstance(data, Table):
                modified_tables = True
                table_path = os.path.join(self.logging_dir, "html_tables", f"{entry}_{self.step}.html")
                os.makedirs(os.path.dirname(table_path), exist_ok=True)
                with open(table_path, "w") as f:
                    f.write(data.to_html_table())
            elif isinstance(data, str):
                self.writer.add_text(entry, data)
            else:
                print(f"TensorBoard logger does not support type: {type(data)}")

        if modified_tables:
            self.create_index_page(os.path.join(self.logging_dir, "html_tables"), sample_files=None)

        self.step += 1
        self.writer.flush()

    def log_config(self, config: dict[str, Any]):
        print("Warming: TensorBoard logger does not support logging config parameters.")

    def close(self):
        self.writer.close()

    @property
    def training_monitoring_link(self) -> str:
        return self.monitoring_link or self.logging_dir

    def create_index_page(self, root_dir: str, sample_files: list[str] | None = None):
        """
        Traverses subdirectories to find all .html files OR uses a sample list
        to create a grouped index.html file with relative links to them.

        Args:
            root_dir (str): The starting directory to search from.
                            Defaults to the current directory.
            sample_files (list, optional): A list of dummy file paths to use
                                        for a layout preview. If None, the
                                        script will search the file system.
        """
        if sample_files:
            print("Using sample data to generate layout preview.")
            html_files = sample_files
        else:
            print("Searching for HTML files...")
            html_files = []
            # os.walk is perfect for recursively exploring a directory tree
            for dirpath, _, filenames in os.walk(root_dir):
                for filename in filenames:
                    # We are looking for HTML files, but we want to ignore any
                    # index files we might have created previously.
                    if filename.endswith(".html") and filename != "index.html":
                        # Get the full path to the file
                        full_path = os.path.join(dirpath, filename)
                        # Get the path relative to the root_dir, which is what
                        # we need for the hyperlink.
                        relative_path = os.path.relpath(full_path, root_dir)
                        # On Windows, paths use backslashes. For HTML links, we need
                        # forward slashes.
                        html_files.append(relative_path.replace("\\", "/"))

        # Sort the list alphabetically for a clean, predictable order
        html_files.sort()

        # --- Group files by their parent directory ---
        grouped_files = defaultdict(list)
        for file_path in html_files:
            parent_dir = os.path.dirname(file_path)
            if not parent_dir:
                parent_dir = "Top-Level Reports"  # Group for files in root
            grouped_files[parent_dir].append(file_path)

        # --- Start Generating the HTML for the index page ---

        # A simple, clean stylesheet for the index page
        css_style = """
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 40px auto;
        padding: 0 20px;
    }
    h1 {
        color: #111;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 10px;
    }
    .group-container {
        margin-bottom: 30px;
    }
    h2 {
        font-size: 1.2rem;
        color: #444;
        margin-bottom: 10px;
        padding-bottom: 5px;
        border-bottom: 1px solid #e0e0e0;
    }
    ul {
        list-style-type: none;
        padding: 0;
    }
    li {
        margin-bottom: 10px;
        background-color: #f9f9f9;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: box-shadow 0.2s ease-in-out;
    }
    li:hover {
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
    }
    a {
        text-decoration: none;
        color: #0056b3;
        display: block;
        padding: 12px 15px;
        font-weight: 500;
    }
    a:hover {
        background-color: #f0f5fa;
        border-radius: 5px;
    }
    .file-count {
        font-size: 1rem;
        color: #666;
        margin-top: -10px;
    }
</style>
    """

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index of Reports</title>
    {css_style}
</head>
<body>
    <h1>Index of Generated Reports</h1>
    <p class="file-count">Found {len(html_files)} report(s).</p>
"""

        if not html_files:
            html_content += "<p>No HTML reports were found in the subdirectories.</p>"
        else:
            # Iterate over the grouped dictionary
            for parent_dir, files in grouped_files.items():
                html_content += "    <div class='group-container'>\n"
                html_content += f"      <h2>{html.escape(parent_dir)}</h2>\n"
                html_content += "      <ul>\n"
                for file_path in files:
                    # We use html.escape to ensure that any special characters in the
                    # filename don't break the HTML.
                    safe_path = html.escape(file_path)
                    # Display the filename only, not the full path, as the group provides context
                    display_name = html.escape(os.path.basename(file_path))
                    html_content += f"        <li><a href='{safe_path}'>{display_name}</a></li>\n"
                html_content += "      </ul>\n"
                html_content += "    </div>\n"

        html_content += """
</body>
</html>
"""

        # Write the generated HTML to the index.html file
        index_file_path = os.path.join(root_dir, "index.html")
        try:
            with open(index_file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Successfully created index.html with {len(html_files)} links.")
        except OSError as e:
            print(f"Error writing to file {index_file_path}: {e}")


class StdoutLogger(Logger):
    def __init__(self): ...

    @staticmethod
    def is_available() -> bool:
        return True

    def __call__(self, logs: Mapping[str, str | int | float | Table]):
        pprint(logs)

    def log_config(self, config: dict[str, Any]):
        print("\n" + "=" * 50)
        pprint(config)
        print("=" * 50 + "\n")

    def close(self):
        pass


def get_prod_logger() -> Logger:
    job_id = os.environ.get("HARMONY_JOB_ID") or "unknown-job"
    use_case_id = os.environ.get("HARMONY_USE_CASE_ID") or "unknown-use-case"
    use_case_name = os.environ.get("HARMONY_USE_CASE") or "unknown-use-case"
    recipe_name = os.environ.get("HARMONY_RECIPE_NAME") or "unknown-recipe"
    run_name = os.environ.get("HARMONY_JOB_NAME") or "unknown-run"
    if os.environ.get("WANDB_API_KEY") and WandbLogger.is_available():
        return WandbLogger(project_name=use_case_name, run_name=f"{recipe_name}/{run_name}")
    elif (uri := os.environ.get("MLFLOW_TRACKING_URI")) and MLFlowLogger.is_available():
        monitoring_link = os.environ["MLFLOW_MONITORING_LINK"]
        return MLFlowLogger(
            project_name=use_case_name,
            run_name=f"{recipe_name}/{run_name}",
            tracking_uri=uri,
            monitoring_link=monitoring_link,
            experiment_tags={"adaptive.use_case_id": use_case_id},
            run_tags={"adaptive.job_id": job_id},
        )
    elif (log_dir := os.environ.get("TENSORBOARD_LOGGING_DIR")) and TBMetricsLogger.is_available():
        monitoring_link = os.path.join(os.environ["TENSORBOARD_MONITORING_LINK"], job_id)
        return TBMetricsLogger(run_name=job_id, logging_dir=log_dir, monitoring_link=monitoring_link)
    else:
        return StdoutLogger()
