import asyncio
import importlib.machinery
import importlib.util
import inspect
import os
import re
import site
import subprocess
import sys
import traceback
import types
from pathlib import Path
from typing import Any, Optional

import tomli
from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from adaptive_harmony.runtime.context import RecipeConfig, RecipeContext
from adaptive_harmony.runtime.data import InputConfig


class RunnerArgs(RecipeConfig, BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ADAPTIVE_", cli_parse_args=True, cli_kebab_case=True)

    recipe_file: Optional[str] = Field(default=None, description="the python recipe file to execute")
    recipe_file_url: Optional[str] = Field(
        default=None, description="Url of recipe in zip format to download and extract to execute"
    )


def main():
    runner_args = RunnerArgs()  # type: ignore
    context = asyncio.run(RecipeContext.from_config(runner_args))
    logger.trace("Loaded config: {}", context.config)
    try:
        if runner_args.recipe_file:
            _load_and_run_recipe(context, runner_args.recipe_file)
        elif runner_args.recipe_file_url:
            recipe_folder = _download_and_extract_recipe(context, runner_args.recipe_file_url)
            _load_and_run_recipe(context, recipe_folder)
        else:
            raise ValueError("recipe_file or recipe_file_url must be provided")
    except Exception as e:
        stack_trace = traceback.format_exc()
        recipe_source = runner_args.recipe_file if runner_args.recipe_file else runner_args.recipe_file_url
        logger.exception(f"Error while running recipe file {recipe_source}", exception=e)
        context.job.report_error(stack_trace)
        sys.exit(1)


def _load_and_run_recipe(context: RecipeContext, recipe_path: str):
    entry = Path(recipe_path).resolve()

    _install_recipe_dependencies(entry)
    # Reload site to pick up .pth files created by editable install
    importlib.reload(site)

    if entry.is_dir():
        entry_file = entry / "main.py"
        if not entry_file.exists():
            raise FileNotFoundError(f"main.py not found in {entry}")
        pkg_dir = entry
        module_name = "main"
    else:
        if entry.suffix != ".py":
            raise ValueError(f"Expected a Python file or directory, got: {entry}")
        entry_file = entry
        pkg_dir = entry.parent
        module_name = entry.stem

    # Create a stable synthetic package name tied to the directory
    synthetic_pkg = f"_adhoc_recipe_{abs(hash(str(pkg_dir))) & 0xFFFFFFFF:x}"

    # Clear any previous loads of this synthetic package in the current process
    for key in list(sys.modules.keys()):
        if key == synthetic_pkg or key.startswith(synthetic_pkg + "."):
            del sys.modules[key]

    # Build a synthetic namespace package pointing at pkg_dir
    pkg_mod = types.ModuleType(synthetic_pkg)
    pkg_mod.__path__ = [str(pkg_dir)]  # allow submodule search in this directory
    pkg_mod.__package__ = synthetic_pkg
    spec_pkg = importlib.machinery.ModuleSpec(synthetic_pkg, loader=None, is_package=True)
    spec_pkg.submodule_search_locations = [str(pkg_dir)]
    pkg_mod.__spec__ = spec_pkg
    sys.modules[synthetic_pkg] = pkg_mod

    # Load the entry file as a submodule of the synthetic package
    fullname = f"{synthetic_pkg}.{module_name}"
    spec = importlib.util.spec_from_file_location(fullname, str(entry_file))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load spec for {entry_file}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[fullname] = module
    spec.loader.exec_module(module)

    # get recipe_main function
    functions = inspect.getmembers(module, inspect.isfunction)
    recipe_main_functions = [(name, func) for name, func in functions if getattr(func, "is_recipe_main", False)]

    if len(recipe_main_functions) == 0:
        logger.warning("No function annotated with @recipe_main")
        return

    if len(recipe_main_functions) != 1:
        names = [name for (name, _) in recipe_main_functions]
        raise ValueError(f"You must have only one function annotated with @recipe_main. Found {names}")

    (func_name, func) = recipe_main_functions[0]
    logger.trace("Getting recipe function parameters")
    args = _get_params(func, context)

    logger.info(f"Executing recipe function {func_name}")
    if inspect.iscoroutinefunction(func):
        asyncio.run(func(*args))
    else:
        func(*args)
    logger.info(f"Recipe {func_name} completed successfully.")
    # Give time for any pending notifications (like register_artifact) to be sent
    import time

    time.sleep(0.1)


def _download_and_extract_recipe(context: RecipeContext, file_url: str) -> str:
    import tempfile
    import zipfile

    assert file_url.endswith(".zip"), "Recipe url must point to a zip file"

    # Download the zip file to a temporary location
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_zip:
        temp_zip_path = temp_zip.name
        context.file_storage.download_locally(file_url, temp_zip_path, use_raw_path=True)

    # Extract to a temporary directory
    temp_dir = tempfile.mkdtemp(prefix="user_recipe")
    with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # Clean up the temp zip file
    os.unlink(temp_zip_path)

    recipe_files = [f for f in os.listdir(temp_dir) if f.endswith(".py")]
    if not recipe_files:
        raise FileNotFoundError("No Python recipe file found in the extracted zip")
    main_files = [f for f in recipe_files if f == "main.py"]
    if len(main_files) == 0:
        raise RuntimeError("Recipe zip file must contain a main.py file")

    return temp_dir


def _parse_script_metadata(file_path: Path) -> Optional[list[str]]:
    """Parse metadata block from a Python script to extract dependencies.
    cf. [python doc](https://packaging.python.org/en/latest/specifications/inline-script-metadata)

    Args:
        file_path: Path to the Python file to parse

    Returns:
        List of dependencies if found, None otherwise
    """
    try:
        content = file_path.read_text()
    except Exception as e:
        logger.warning(f"Failed to read file {file_path} for metadata parsing: {e}")
        return None

    # Regex pattern to match metadata blocks
    metadata_pattern = r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+?)^# ///$"
    matches = list(re.finditer(metadata_pattern, content))

    for match in matches:
        metadata_type = match.group("type")
        if metadata_type != "adaptive":
            continue
        metadata_content = match.group("content")
        # Clean up metadata content by removing leading '#' and whitespaces from each line
        cleaned_lines = []
        for line in metadata_content.split("\n"):
            line = line.lstrip("#").strip()
            if line:
                cleaned_lines.append(line)
        metadata_content = "\n".join(cleaned_lines)

        # Parse metadata content as TOML
        try:
            metadata_dict = tomli.loads(metadata_content)
        except Exception as e:
            logger.warning(f"Failed to parse metadata as TOML: {e}")
            metadata_dict = None
        if metadata_dict and "dependencies" in metadata_dict:
            deps = metadata_dict["dependencies"]
            if isinstance(deps, list):
                return deps

    return None


INSTALL_TIMEOUT_SECS = int(os.getenv("ADAPTIVE_INSTALL_TIMEOUT_SECS", "300"))  # Default 5 minutes


def _install_recipe_dependencies(entry: Path):
    """Install Python dependencies from pyproject.toml, requirements.txt, requirements.in, or script metadata.

    Args:
        entry: Path to a file or directory. If it's a directory, looks for dependency files.
               If it's a file, parses metadata block for dependencies.
    """
    # Check for pyproject.toml first, then requirements.txt/requirements.in
    pyproject_file = entry / "pyproject.toml"
    requirements_file = entry / "requirements.txt"
    requirements_in_file = entry / "requirements.in"

    install_kwargs = {
        "check": True,
        "timeout": INSTALL_TIMEOUT_SECS,
        "capture_output": True,
        "text": True,
    }

    if pyproject_file.exists():
        logger.info(
            f"Found pyproject.toml in {entry}, installing dependencies with uv pip (timeout: {INSTALL_TIMEOUT_SECS}s)"
        )
        try:
            result = subprocess.run(
                ["uv", "pip", "install", "-e", str(entry)],
                **install_kwargs,
            )
            if result.stdout:
                logger.debug(f"Install output: {result.stdout}")
            logger.info("Successfully installed dependencies from pyproject.toml")
        except subprocess.TimeoutExpired as e:
            logger.error(f"Timeout ({INSTALL_TIMEOUT_SECS}s) installing dependencies from pyproject.toml")
            if e.stdout:
                logger.debug(f"Partial stdout: {e.stdout}")
            if e.stderr:
                logger.debug(f"Partial stderr: {e.stderr}")
            raise
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies from pyproject.toml: {e.stderr}")
            if e.stdout:
                logger.debug(f"stdout: {e.stdout}")
            raise
    elif requirements_file.exists():
        logger.info(
            f"Found requirements.txt in {entry}, installing dependencies with uv pip (timeout: {INSTALL_TIMEOUT_SECS}s)"
        )
        try:
            result = subprocess.run(
                ["uv", "pip", "install", "--verbose", "-r", str(requirements_file)], **install_kwargs
            )
            if result.stdout:
                logger.debug(f"Install output: {result.stdout}")
            logger.info("Successfully installed dependencies from requirements.txt")
        except subprocess.TimeoutExpired as e:
            logger.error(f"Timeout ({INSTALL_TIMEOUT_SECS}s) installing dependencies from requirements.txt")
            if e.stdout:
                logger.debug(f"Partial stdout: {e.stdout}")
            if e.stderr:
                logger.debug(f"Partial stderr: {e.stderr}")
            raise
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies from requirements.txt: {e.stderr}")
            if e.stdout:
                logger.debug(f"stdout: {e.stdout}")
            raise
    elif requirements_in_file.exists():
        logger.info(
            f"Found requirements.in in {entry}, compiling to requirements.txt with uv pip (timeout: {INSTALL_TIMEOUT_SECS}s)"
        )
        try:
            # Compile requirements.in to requirements.txt
            result = subprocess.run(
                ["uv", "pip", "compile", str(requirements_in_file), "-o", str(requirements_file)], **install_kwargs
            )
            if result.stdout:
                logger.debug(f"Compile output: {result.stdout}")
            logger.debug("Successfully compiled requirements.in to requirements.txt")
            result = subprocess.run(
                ["uv", "pip", "install", "-r", str(requirements_file)],
                **install_kwargs,
            )
            if result.stdout:
                logger.debug(f"Install output: {result.stdout}")
            logger.info("Successfully installed dependencies from requirements.in")
        except subprocess.TimeoutExpired as e:
            logger.error(f"Timeout ({INSTALL_TIMEOUT_SECS}s) compiling or installing dependencies from requirements.in")
            if e.stdout:
                logger.debug(f"Partial stdout: {e.stdout}")
            if e.stderr:
                logger.debug(f"Partial stderr: {e.stderr}")
            raise
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to compile or install dependencies from requirements.in: {e.stderr}")
            if e.stdout:
                logger.debug(f"stdout: {e.stdout}")
            raise
    else:
        # Check main file for script metadata
        main_file = entry if entry.is_file() else entry / "main.py"
        if main_file.is_file():
            if main_file.suffix != ".py":
                logger.debug(f"{main_file} is not a Python file, skipping dependency installation")
                return

            dependencies = _parse_script_metadata(main_file)
            if dependencies:
                logger.info(
                    f"Found {len(dependencies)} dependencies in script metadata: {dependencies}, installing them (timeout: {INSTALL_TIMEOUT_SECS}s)..."
                )
                try:
                    result = subprocess.run(["uv", "pip", "install"] + dependencies, **install_kwargs)
                    if result.stdout:
                        logger.debug(f"Install output: {result.stdout}")
                    logger.info("Successfully installed dependencies from script metadata")
                except subprocess.TimeoutExpired as e:
                    logger.error(f"Timeout ({INSTALL_TIMEOUT_SECS}s) installing dependencies from script metadata")
                    if e.stdout:
                        logger.debug(f"Partial stdout: {e.stdout}")
                    if e.stderr:
                        logger.debug(f"Partial stderr: {e.stderr}")
                    raise
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to install dependencies from script metadata: {e.stderr}")
                    if e.stdout:
                        logger.debug(f"stdout: {e.stdout}")
                    raise
            else:
                logger.debug(f"No dependencies found in script metadata for {entry}")
            return


def _get_params(func, context: RecipeContext) -> list[Any]:
    args: list[Any] = []
    sig = inspect.signature(func)
    assert len(sig.parameters.items()) <= 2, "Support only functions with 2 parameters or less"

    for _, param in sig.parameters.items():
        # Ensure param.annotation is a type before using issubclass
        if isinstance(param.annotation, type):
            if issubclass(param.annotation, RecipeContext):
                args.append(context)
            elif issubclass(param.annotation, InputConfig):
                if context.config.user_input_file:
                    user_input = param.annotation.load_from_file(context.config.user_input_file)
                else:
                    user_input = param.annotation()
                logger.trace("Loaded user input: {}", user_input)
                args.append(user_input)
        else:
            raise TypeError(f"Parameter '{param.name}' must have a type annotation.")

    return args


if __name__ == "__main__":
    main()
