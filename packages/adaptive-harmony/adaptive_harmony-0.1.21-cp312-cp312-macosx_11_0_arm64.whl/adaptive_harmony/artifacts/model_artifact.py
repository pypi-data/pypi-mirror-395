import uuid

from adaptive_harmony import (
    JobArtifact,
)
from adaptive_harmony.runtime.context import RecipeContext


class ModelArtifact:
    def __init__(self, key: str, ctx: RecipeContext) -> None:
        self._base = JobArtifact(
            id=str(uuid.uuid4()),
            name=key,
            kind="model",
            model_key=key,
        )
        self.ctx = ctx
        self.ctx.job.register_artifact(self._base)

    @property
    def id(self) -> str:
        return self._base.id

    @property
    def name(self) -> str:
        return self._base.name

    @property
    def kind(self) -> str:
        return self._base.kind

    @property
    def model_key(self) -> str:
        return self._base.metadata["model_key"]
