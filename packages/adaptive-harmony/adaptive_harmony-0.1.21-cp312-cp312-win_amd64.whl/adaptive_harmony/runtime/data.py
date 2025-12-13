import json
import re
import types
from typing import Annotated, Any, Literal, Self, Union, get_args, get_origin

from loguru import logger
from pydantic import BaseModel, Field

from adaptive_harmony.adaptive_harmony import HarmonyClient, ModelBuilder, StringThread
from adaptive_harmony.runtime.context import RecipeContext


class InputConfig(BaseModel):
    def __init_subclass__(cls, **kwargs):
        # Add union_variant BEFORE calling super (before Pydantic processes it)
        if not hasattr(cls, "__annotations__"):
            cls.__annotations__ = {}
        if "union_variant" not in cls.__annotations__:
            cls.__annotations__["union_variant"] = Annotated[Literal[cls.__name__], Field(default=cls.__name__)]
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "__annotations__"):
            for field_name, field_type in cls.__annotations__.items():
                origin = get_origin(field_type)
                if origin is Union or origin is types.UnionType:
                    # Add discriminator to the union annotation
                    cls.__annotations__[field_name] = Annotated[field_type, Field(discriminator="union_variant")]

                    # Add union_variant field to each variant class
                    variant_types = get_args(field_type)
                    for variant_type in variant_types:
                        # Skip None (for Optional types)
                        if variant_type is type(None):
                            continue

                        # Add union_variant: Literal["ClassName"] to the variant
                        # if not already present
                        if (
                            hasattr(variant_type, "__annotations__")
                            and "union_variant" not in variant_type.__annotations__
                        ):
                            variant_type.__annotations__["union_variant"] = Literal[variant_type.__name__]
                            # Set default value
                            setattr(variant_type, "union_variant", variant_type.__name__)

    @classmethod
    def load_from_file(cls, json_file) -> Self:
        with open(json_file) as f:
            data = json.load(f)
        return cls.model_validate(data)


from .dto import DatasetSampleFormats
from .dto.AdaptiveDataset import AdaptiveDataset as DtoDataset
from .dto.AdaptiveDataset import AdaptiveDatasetKind
from .dto.AdaptiveGrader import (
    AdaptiveGrader as DtoGrader,
)
from .dto.AdaptiveGrader import (
    Judge as CustomJudge,
)
from .dto.AdaptiveGrader import (
    JudgeExample as CustomJudgeExample,
)
from .dto.AdaptiveGrader import (
    Prebuilt as PrebuiltJudge,
)
from .dto.AdaptiveGrader import (
    PrebuiltConfigKey,
)
from .dto.AdaptiveGrader import (
    Remote as RemoteRewardEndpoint,
)
from .dto.AdaptiveModel import AdaptiveModel as DtoModel

__all__ = [
    "InputConfig",
    "AdaptiveDataset",
    "AdaptiveDatasetKind",
    "AdaptiveModel",
    "AdaptiveGrader",
    "CustomJudge",
    "CustomJudgeExample",
    "PrebuiltJudge",
    "PrebuiltConfigKey",
    "RemoteRewardEndpoint",
]


# Patches for generated dto objects
class AdaptiveModel(DtoModel):
    def to_builder(
        self,
        client: HarmonyClient,
        kv_cache_len: int | None = None,
        tokens_to_generate: int | None = None,
        tp: int | None = None,
    ) -> ModelBuilder:
        """
        Create a ModelBuilder instance configured with this model's parameters.
        Applies configuration from both the model's stored parameters and any override parameters
        provided as arguments. Override parameters take precedence over stored parameters.

        Args:
            client (HarmonyClient): The client instance used to create the model builder
            kv_cache_len (int | None, optional)
            tokens_to_generate (int | None, optional)
            tp (int | None, optional)

        Returns:
            ModelBuilder: A configured model builder instance ready for use

        Note:
            The method maps self.params.max_seq_len to the tokens_to_generate parameter
            in the builder configuration.
        """
        kwargs = {}
        if self.params:
            if self.params.kv_cache_len is not None:
                kwargs["kv_cache_len"] = self.params.kv_cache_len
            if self.params.max_seq_len is not None:
                kwargs["tokens_to_generate"] = self.params.max_seq_len

        if kv_cache_len:
            kwargs["kv_cache_len"] = kv_cache_len
        if tokens_to_generate:
            kwargs["tokens_to_generate"] = tokens_to_generate
        builder = client.model(self.path, **kwargs)
        if self.params and self.params.tp:
            builder = builder.tp(self.params.tp)
        if tp:
            builder = builder.tp(tp)
        return builder

    def __repr__(self) -> str:
        # Redact api_key in the path if present, show only last 3 chars
        def redact_api_key(match):
            key = match.group(2)
            if len(key) > 3:
                redacted = "<REDACTED>" + key[-3:]
            else:
                redacted = "<REDACTED>"
            return f"{match.group(1)}{redacted}"

        redacted_path = re.sub(r"(api_key=)([^&]+)", redact_api_key, self.path)
        return f"AdaptiveModel(path='{redacted_path}')"

    def __hash__(self) -> int:
        return hash(self.path) + hash(self.model_key)


class AdaptiveGrader(DtoGrader):
    def __hash__(self) -> int:
        return hash(self.grader_id)


class AdaptiveDataset(DtoDataset):
    def load_dataset(self, ctx: RecipeContext | None = None) -> list[StringThread]:
        def with_metadata(thread: StringThread, metadata: DatasetSampleFormats.SampleMetadata):
            if metadata.external_data:
                thread.metadata = {**metadata.model_dump(exclude_none=True), **metadata.external_data}
            else:
                thread.metadata = metadata.model_dump()

        def parse_internal_format(line_dict: Any) -> StringThread | None:
            thread = None

            format: type[DatasetSampleFormats.DtoBaseModel] | None = None
            match self.kind:
                case AdaptiveDatasetKind.Prompt:
                    format = DatasetSampleFormats.DatasetPromptSample
                case AdaptiveDatasetKind.Completion:
                    format = DatasetSampleFormats.DatasetSample
                case AdaptiveDatasetKind.Metric:
                    format = DatasetSampleFormats.DatasetMetricSample
                case AdaptiveDatasetKind.Preference:
                    format = DatasetSampleFormats.DatasetPreferenceSample
                case AdaptiveDatasetKind.Mixed:
                    # order is important here: try the most constrained formats first
                    formats: list[type[DatasetSampleFormats.DtoBaseModel]] = [
                        DatasetSampleFormats.DatasetPreferenceSample,
                        DatasetSampleFormats.DatasetMetricSample,
                        DatasetSampleFormats.DatasetSample,
                        DatasetSampleFormats.DatasetPromptSample,
                    ]
                    for f in formats:
                        try:
                            f.model_validate(line_dict)
                            format = f
                            break
                        except Exception:
                            pass

            if format is None:
                raise ValueError(f"Could not determine format for line in dataset. Line {line_dict}")

            match format:
                case DatasetSampleFormats.DatasetPromptSample:
                    sample = format.model_validate(line_dict)
                    thread = StringThread([(turn.root[0], turn.root[1]) for turn in sample.prompt])
                    with_metadata(thread, sample.metadata)
                case DatasetSampleFormats.DatasetSample:
                    sample = format.model_validate(line_dict)
                    thread = StringThread([(turn.root[0], turn.root[1]) for turn in sample.prompt])
                    thread = thread.assistant(sample.completion.root[1])
                    with_metadata(thread, sample.metadata)
                case DatasetSampleFormats.DatasetMetricSample:
                    sample = DatasetSampleFormats.DatasetMetricSample.model_validate(line_dict)
                    thread = StringThread([(turn.root[0], turn.root[1]) for turn in sample.prompt])
                    thread = thread.assistant(sample.completion.root[1])
                    with_metadata(thread, sample.metadata)
                    if self.feedback_key and sample.metrics:
                        # put metric value in "res" key in the metadata
                        thread.metadata["res"] = sample.metrics.get(self.feedback_key)

                case DatasetSampleFormats.DatasetPreferenceSample:
                    sample = DatasetSampleFormats.DatasetPreferenceSample.model_validate(line_dict)
                    thread = StringThread([(turn.root[0], turn.root[1]) for turn in sample.prompt])
                    with_metadata(thread, sample.metadata)
                    thread.metadata["other_completion"] = sample.bad_completion.root[1]
                    thread.metadata["preferred_completion"] = sample.good_completion.root[1]

            return thread

        def parse_external_format(line_dict: Any) -> StringThread | None:
            thread = None
            if "input" in line_dict or "messages" in line_dict:
                key = "input" if "input" in line_dict else "messages"
                thread = StringThread(
                    [(inner_turn_dict["role"], inner_turn_dict["content"]) for inner_turn_dict in line_dict[key]]
                )
                if "completion" in line_dict and line_dict["completion"]:
                    thread = thread.assistant(line_dict["completion"])
            else:
                print("Did not find `input`, or `messages` key in sample, ignoring")
            if thread is not None:
                thread.metadata = line_dict.get("metadata", {})
                if "other_completion" in line_dict and "preferred_completion" in line_dict:
                    thread.metadata["other_completion"] = line_dict["other_completion"]
                    thread.metadata["preferred_completion"] = line_dict["preferred_completion"]
            return thread

        if ctx:
            lines = ctx.file_storage.read(self.file, use_raw_path=True).decode("utf-8").splitlines()
        else:
            lines = open(self.file, encoding="utf-8").read().splitlines()
        threads = []
        parse_function = None
        for line in lines:
            if len(line.strip()) == 0:
                continue
            line_dict = json.loads(line)

            if parse_function is None:
                try:
                    thread = parse_internal_format(line_dict)
                    parse_function = parse_internal_format
                except Exception as e:
                    logger.warning("Could not read dataset as internal format, falling back to external format {}", e)
                    thread = parse_external_format(line_dict)
                    parse_function = parse_external_format
            else:
                thread = parse_function(line_dict)

            if thread is not None:
                threads.append(thread)

        if len(threads) == 0:
            raise ValueError("Did not find any valid format samples in the dataset")
        return threads
