import json
from typing import Any
from uuid import UUID

import aiofiles
from loguru import logger
from pydantic import BaseModel, model_serializer, model_validator

from adaptive_harmony import StringThread
from adaptive_harmony.parameters import dataset_kinds
from adaptive_harmony.parameters.dataset_kinds import DatasetKind
from adaptive_harmony.parameters.model_kinds import ModelKind
from adaptive_harmony.runtime.context import RecipeContext
from adaptive_harmony.runtime.dto.DatasetSampleFormats import SampleMetadata


class Dataset[T: DatasetKind](BaseModel):
    dataset_key: str
    feedback_key: str | None = None
    local_file_path: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_from_json(cls, data):
        """Handle deserialization from JSON - accepts dict with dataset_key."""
        # If it's a string, convert it to the expected dict format
        if isinstance(data, str):
            return {"dataset_key": data, "feedback_key": None}
        return data

    async def load(self, ctx: RecipeContext | None = None) -> list[StringThread]:
        """
        Load dataset samples from the Harmony service.

        Args:
            ctx: RecipeContext with client and file_storage

        Returns:
            list of StringThread objects
        """

        def with_metadata(thread: StringThread, metadata: SampleMetadata):
            if metadata.external_data:
                thread.metadata = {**metadata.model_dump(exclude_none=True), **metadata.external_data}
            else:
                thread.metadata = metadata.model_dump()

        async def parse_internal_format(line_dict: Any) -> StringThread | None:
            thread = None

            format: type[dataset_kinds.DtoBaseModel] | None = None
            match T:
                case dataset_kinds.Prompt:
                    format = dataset_kinds.DatasetPromptSample
                case dataset_kinds.Completion:
                    format = dataset_kinds.DatasetSample
                case dataset_kinds.Metric:
                    format = dataset_kinds.DatasetMetricSample
                case dataset_kinds.Preference:
                    format = dataset_kinds.DatasetPreferenceSample
                case _:  # Mixed dataset case
                    # order is important here: try the most constrained formats first
                    formats: list[type[dataset_kinds.DtoBaseModel]] = [
                        dataset_kinds.DatasetPreferenceSample,
                        dataset_kinds.DatasetMetricSample,
                        dataset_kinds.DatasetSample,
                        dataset_kinds.DatasetPromptSample,
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
                case dataset_kinds.DatasetPromptSample:
                    sample = format.model_validate(line_dict)
                    thread = await StringThread.from_dataset(
                        [(turn.root[0], turn.root[1]) for turn in sample.prompt], None
                    )
                    with_metadata(thread, sample.metadata)
                case dataset_kinds.DatasetSample:
                    sample = format.model_validate(line_dict)
                    thread = await StringThread.from_dataset(
                        [(turn.root[0], turn.root[1]) for turn in sample.prompt], None
                    )
                    thread = thread.assistant(sample.completion.root[1])
                    with_metadata(thread, sample.metadata)
                case dataset_kinds.DatasetMetricSample:
                    sample = dataset_kinds.DatasetMetricSample.model_validate(line_dict)
                    thread = await StringThread.from_dataset(
                        [(turn.root[0], turn.root[1]) for turn in sample.prompt], None
                    )
                    thread = thread.assistant(sample.completion.root[1])
                    with_metadata(thread, sample.metadata)
                    if self.feedback_key and sample.metrics:
                        # put metric value in "res" key in the metadata
                        thread.metadata["res"] = sample.metrics.get(self.feedback_key)

                case dataset_kinds.DatasetPreferenceSample:
                    sample = dataset_kinds.DatasetPreferenceSample.model_validate(line_dict)
                    thread = await StringThread.from_dataset(
                        [(turn.root[0], turn.root[1]) for turn in sample.prompt], None
                    )
                    with_metadata(thread, sample.metadata)
                    thread.metadata["other_completion"] = sample.bad_completion.root[1]
                    thread.metadata["preferred_completion"] = sample.good_completion.root[1]

            return thread

        async def parse_external_format(line_dict: Any) -> StringThread | None:
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
            config_response = await ctx.client.get_dataset_config(self.dataset_key)
            lines = ctx.file_storage.read(config_response.file_path, use_raw_path=True).decode("utf-8").splitlines()
        else:
            assert self.local_file_path is not None, "Local file path is required when ctx is not provided"
            lines = []
            async with aiofiles.open(self.local_file_path, encoding="utf-8") as f:
                async for line in f:
                    lines.append(line.rstrip("\n"))

        threads = []
        parse_function = None
        for line in lines:
            if len(line.strip()) == 0:
                continue
            line_dict = json.loads(line)

            if parse_function is None:
                try:
                    thread = await parse_internal_format(line_dict)
                    parse_function = parse_internal_format
                except Exception as e:
                    logger.warning("Could not read dataset as internal format, falling back to external format {}", e)
                    thread = await parse_external_format(line_dict)
                    parse_function = parse_external_format
            else:
                thread = await parse_function(line_dict)

            if thread is not None:
                threads.append(thread)

        if len(threads) == 0:
            raise ValueError("Did not find any valid format samples in the dataset")
        return threads

    def __hash__(self):
        """Make Dataset hashable based on its keys."""
        return hash((self.dataset_key, self.feedback_key))


class Model[T: ModelKind](BaseModel):
    model_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_from_json(cls, data):
        """Handle deserialization - accepts string or dict."""
        if isinstance(data, str):
            return {"model_key": data}
        return data

    @model_serializer
    def serialize_model(self) -> str:
        """Serialize as just the model_key string."""
        return self.model_key

    async def to_builder(
        self,
        ctx,
        kv_cache_len: int | None = None,
        tokens_to_generate: int | None = None,
        tp: int | None = None,
    ):
        """
        Create a ModelBuilder instance configured with this model's parameters.

        Args:
            ctx: RecipeContext with client
            kv_cache_len (int | None, optional): KV cache length override
            tokens_to_generate (int | None, optional): Tokens to generate override
            tp (int | None, optional): Tensor parallelism override

        Returns:
            ModelBuilder: A configured model builder instance ready for use
        """
        config_response = await ctx.client.get_model_config(self.model_key)

        kwargs = {}
        if config_response.kv_cache_len is not None:
            kwargs["kv_cache_len"] = config_response.kv_cache_len
        if config_response.max_seq_len is not None:
            kwargs["tokens_to_generate"] = config_response.max_seq_len

        if kv_cache_len:
            kwargs["kv_cache_len"] = kv_cache_len
        if tokens_to_generate:
            kwargs["tokens_to_generate"] = tokens_to_generate

        builder = ctx.client.model(config_response.path, **kwargs)

        if config_response.tp:
            builder = builder.tp(config_response.tp)
        if tp:
            builder = builder.tp(tp)

        return builder

    def __hash__(self):
        """Make Model hashable based on its key."""
        return hash(self.model_key)


class Grader(BaseModel):
    grader_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_from_json(cls, data):
        """Handle deserialization - accepts string or dict."""
        if isinstance(data, str):
            return {"grader_key": data}
        return data

    @model_serializer
    def serialize_model(self) -> str:
        """Serialize as just the grader_key string."""
        return self.grader_key

    async def load(
        self,
        ctx,
        tp: int | None = None,
        kv_cache_len: int | None = None,
    ):
        """
        Load a grader instance configured with this grader's parameters.

        Args:
            ctx: RecipeContext with client
            tp (int | None, optional): Tensor parallelism override
            kv_cache_len (int | None, optional): KV cache length override

        Returns:
            Grader: A configured grader instance ready for use
        """
        from adaptive_harmony.graders import Grader as GraderImpl
        from adaptive_harmony.runtime.data import AdaptiveGrader

        config_response = await ctx.client.get_grader_config(self.grader_key)
        grader_config_data = json.loads(config_response.grader_config_json)

        grader_config = AdaptiveGrader(
            grader_id=config_response.grader_id,
            key=config_response.key,
            metric_id=UUID("00000000-0000-0000-0000-000000000000"),  # unused in from_config
            name=config_response.name,
            config=grader_config_data,
        )

        return GraderImpl.from_config(
            grader_config=grader_config,
            client=ctx.client,
            tp=tp,
            kv_cache_len=kv_cache_len,
        )

    def __hash__(self):
        """Make Grader hashable based on its key."""
        return hash(self.grader_key)
