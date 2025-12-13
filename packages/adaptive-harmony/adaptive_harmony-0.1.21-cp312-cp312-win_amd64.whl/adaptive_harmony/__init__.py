# ruff: noqa: F403, F401
from typing import TYPE_CHECKING

from rich.progress import Progress, TaskID

from .adaptive_harmony import (
    EvalSample as EvalSample,
)
from .adaptive_harmony import (
    EvalSampleInteraction as EvalSampleInteraction,
)
from .adaptive_harmony import (
    Grade as Grade,
)
from .adaptive_harmony import (
    HarmonyClient as HarmonyClient,
)
from .adaptive_harmony import (
    HarmonyJobNotifier as HarmonyJobNotifier,
)
from .adaptive_harmony import (
    InferenceModel as InferenceModel,
)
from .adaptive_harmony import (
    JobArtifact as JobArtifact,
)
from .adaptive_harmony import (
    JobNotifier as JobNotifier,
)
from .adaptive_harmony import (
    ModelBuilder as ModelBuilder,
)
from .adaptive_harmony import (
    StageNotifier as StageNotifier,
)
from .adaptive_harmony import (
    StringThread as StringThread,
)
from .adaptive_harmony import (
    TokenizedThread as TokenizedThread,
)
from .adaptive_harmony import (
    TrainingModel as TrainingModel,
)
from .adaptive_harmony import (
    get_client as get_client,
)

if TYPE_CHECKING:
    from .adaptive_harmony import StringTurn as StringTurn
else:
    from typing import NamedTuple

    class StringTurn(NamedTuple):
        role: str
        content: str


import adaptive_harmony.core.rl_utils as rl_utils
from adaptive_harmony.artifacts.custom_artifact import CustomArtifact
from adaptive_harmony.artifacts.dataset_artifact import DatasetArtifact
from adaptive_harmony.core.dataset import DataSet
from adaptive_harmony.core.schedulers import CombinedSchedule, CosineScheduler, CosineSchedulerWithoutWarmup, Scheduler
from adaptive_harmony.evaluation.evaluation_artifact import EvaluationArtifact
from adaptive_harmony.file_storage import (
    FileStorage,
    FileStorageConfig,
    LocalFileStorageConfig,
    S3FileStorageConfig,
    StoredFile,
)
from adaptive_harmony.metric_logger import Logger, WandbLogger

# Ensure key classes are available at module level
__all__ = [
    "StringThread",
    "StringTurn",
    "TokenizedThread",
    "InferenceModel",
    "ModelBuilder",
    "TrainingModel",
    "HarmonyClient",
    "get_client",
    "DataSet",
    "CosineScheduler",
    "CombinedSchedule",
    "CosineSchedulerWithoutWarmup",
    "Scheduler",
    "WandbLogger",
    "Logger",
    "FileStorage",
    "FileStorageConfig",
    "LocalFileStorageConfig",
    "S3FileStorageConfig",
    "StoredFile",
    "EvaluationArtifact",
    "CustomArtifact",
    "DatasetArtifact",
    "rl_utils",
    "Grade",
    "EvalSample",
    "EvalSampleInteraction",
    "JobArtifact",
]


# Patch StringThread to use rich for display
from adaptive_harmony.core.display import _stringthread_repr, _tokenizedthread_repr
from adaptive_harmony.core.image_utils import string_thread_to_html_string

# Patch InferenceModel to have json output capabilities
from adaptive_harmony.core.structured_output import generate_and_validate, render_pydantic_model, render_schema
from adaptive_harmony.runtime.model_artifact_save import save_with_artifact

StringThread.__repr__ = _stringthread_repr  # type: ignore
TokenizedThread.__repr__ = _tokenizedthread_repr  # type: ignore
setattr(StringThread, "_repr_html_", string_thread_to_html_string)
setattr(InferenceModel, "generate_and_validate", generate_and_validate)
setattr(InferenceModel, "render_schema", staticmethod(render_schema))
setattr(InferenceModel, "render_pydantic_model", staticmethod(render_pydantic_model))

_original_training_model_save = TrainingModel.save


async def _save_with_artifact_wrapper(model: TrainingModel, model_name: str, ctx=None):
    return await save_with_artifact(model, model_name, ctx, _original_training_model_save)


setattr(TrainingModel, "save", _save_with_artifact_wrapper)


async def spawn_train(self: ModelBuilder, name: str, max_batch_size: int) -> TrainingModel:
    fut = await self.spawn_train_with_progress(name, max_batch_size)  # type:ignore

    with Progress() as pbar:
        task = pbar.add_task("Loading model", total=1000)

        while (prog := await fut._await_progress()) != 1.0:
            pbar.update(task, completed=prog, total=1.0)
        pbar.update(task, completed=1.0, total=1.0)

    return await fut.get()


async def spawn_inference(self: ModelBuilder, name: str) -> InferenceModel:
    fut = await self.spawn_inference_with_progress(name)  # type:ignore

    with Progress() as pbar:
        task = pbar.add_task("Loading model", total=1000)

        while (prog := await fut._await_progress()) != 1.0:
            pbar.update(task, completed=prog, total=1.0)
        pbar.update(task, completed=1.0, total=1.0)

    return await fut.get()


setattr(ModelBuilder, "spawn_inference", spawn_inference)
setattr(ModelBuilder, "spawn_train", spawn_train)
