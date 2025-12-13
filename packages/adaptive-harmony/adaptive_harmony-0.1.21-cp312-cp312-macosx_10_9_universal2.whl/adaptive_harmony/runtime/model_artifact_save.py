from collections.abc import Awaitable, Callable

from adaptive_harmony import TrainingModel
from adaptive_harmony.artifacts.model_artifact import ModelArtifact
from adaptive_harmony.runtime import RecipeContext


async def save_with_artifact(
    model: TrainingModel,
    model_name: str,
    ctx: RecipeContext | None = None,
    original_save_method: Callable[[TrainingModel, str], Awaitable[str]] | None = None,
) -> str:
    if original_save_method is None:
        raise ValueError("original_save_method must be provided")

    real_model_key = await original_save_method(model, model_name)

    if ctx is not None:
        ModelArtifact(real_model_key, ctx)

    return real_model_key
