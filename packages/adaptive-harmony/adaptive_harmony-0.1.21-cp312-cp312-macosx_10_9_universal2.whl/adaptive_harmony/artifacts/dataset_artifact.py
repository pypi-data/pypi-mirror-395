import json
import logging
import uuid
from datetime import datetime
from typing import List, Self, Sequence

from adaptive_harmony import StringThread
from adaptive_harmony.adaptive_harmony import JobArtifact
from adaptive_harmony.runtime.context import RecipeContext
from adaptive_harmony.runtime.dto.AdaptiveDataset import AdaptiveDatasetKind
from adaptive_harmony.runtime.dto.DatasetSampleFormats import (
    DatasetMetricSample,
    DatasetPreferenceSample,
    DatasetPromptSample,
    DatasetSample,
    SampleMetadata,
)

logger = logging.getLogger(__name__)

# Union type for all supported dataset sample types
DatasetSampleType = DatasetSample | DatasetPromptSample | DatasetMetricSample | DatasetPreferenceSample


class DatasetArtifact:
    """
    Artifact for saving dataset samples generated during recipe execution.

    Supports different dataset kinds (Prompt, Completion, Metric, Preference, Mixed)
    and can save samples in JSONL format compatible with the platform's dataset format.
    """

    def __init__(self, name: str, ctx: RecipeContext, kind: AdaptiveDatasetKind = AdaptiveDatasetKind.Mixed) -> None:
        """
        Initialize a dataset artifact.

        Args:
            name: Name of the dataset artifact
            ctx: Recipe context for file storage and job registration
            kind: Type of dataset (Prompt, Completion, Metric, Preference, Mixed)
        """
        artifact_id = str(uuid.uuid4())
        url = ctx.file_storage.mk_url(f"dataset_samples_{artifact_id}.jsonl")

        self._base = JobArtifact(
            id=artifact_id,
            name=name,
            kind="dataset",
            uri=url,
            # Store dataset kind and sample count in metadata
            dataset_kind=kind.value,
            sample_count=0,
        )
        self.ctx = ctx
        self.kind = kind
        self._sample_count = 0
        print(f"Registering artifact: {self._base}")
        # Register artifact with the job
        self.ctx.job.register_artifact(self._base)

    @property
    def id(self) -> str:
        """Get the artifact ID."""
        return self._base.id

    @property
    def name(self) -> str:
        """Get the artifact name."""
        return self._base.name

    @property
    def artifact_kind(self) -> str:
        """Get the artifact kind (always 'dataset')."""
        return self._base.kind

    @property
    def dataset_kind(self) -> AdaptiveDatasetKind:
        """Get the dataset kind (Prompt, Completion, etc.)."""
        return self.kind

    @property
    def uri(self) -> str:
        """Get the artifact URI."""
        assert self._base.uri is not None
        return self._base.uri

    @property
    def sample_count(self) -> int:
        """Get the number of samples added to this artifact."""
        return self._sample_count

    def add_samples_from_thread(self, threads: List[StringThread]) -> Self:
        """
        Add a dataset sample from a string thread.
        """
        return self.add_samples([self._thread_to_dataset_sample(thread) for thread in threads])

    def add_samples(self, samples: Sequence[DatasetSampleType]) -> Self:
        """
        Add dataset samples to this artifact.

        Args:
            samples: List of dataset samples to add

        Returns:
            Self for method chaining

        Raises:
            ValueError: If samples list is empty
            TypeError: If sample type doesn't match dataset kind
            Exception: If serialization or storage fails
        """
        if not samples:
            raise ValueError("Cannot add empty samples list")

        try:
            # Validate samples match the dataset kind (unless Mixed)
            if self.kind != AdaptiveDatasetKind.Mixed:
                self._validate_samples_kind(samples)

            json_lines = "\n".join([self._sample_to_json(sample) for sample in samples])
            # Convert samples to JSONL format
            self.ctx.file_storage.append((json_lines + "\n").encode("utf-8"), self.uri)

            self._sample_count += len(samples)
            logger.debug(f"Added {len(samples)} samples to dataset artifact {self.id}")
        except Exception as e:
            logger.error(f"Failed to add samples to dataset artifact {self.id}: {e}")
            raise

        return self

    def add_prompt_items(self, items: List[DatasetPromptSample]) -> Self:
        """
        Add prompt-only items to the dataset.

        Args:
            items: List of DatasetPromptSample objects

        Returns:
            Self for method chaining
        """
        return self.add_samples(items)

    def add_completion_items(self, items: List[DatasetSample]) -> Self:
        """
        Add prompt-completion items to the dataset.

        Args:
            items: List of DatasetSample objects

        Returns:
            Self for method chaining
        """
        return self.add_samples(items)

    def add_metric_items(self, items: List[DatasetMetricSample]) -> Self:
        """
        Add items with evaluation metrics to the dataset.

        Args:
            items: List of DatasetMetricSample objects

        Returns:
            Self for method chaining
        """
        return self.add_samples(items)

    def add_preference_items(self, items: List[DatasetPreferenceSample]) -> Self:
        """
        Add preference items (good vs bad completions) to the dataset.

        Args:
            items: List of DatasetPreferenceSample objects

        Returns:
            Self for method chaining
        """
        return self.add_samples(items)

    def write_jsonl(self, file_path: str) -> None:
        """
        Write the artifact contents to a local JSONL file.

        Args:
            file_path: Local path to write the JSONL file
        """
        content = self.ctx.file_storage.read(self.uri)
        with open(file_path, "wb") as f:
            f.write(content)

    def _validate_samples_kind(self, samples: Sequence[DatasetSampleType]) -> None:
        """Validate that samples match the expected dataset kind."""
        expected_type = {
            AdaptiveDatasetKind.Prompt: DatasetPromptSample,
            AdaptiveDatasetKind.Completion: DatasetSample,
            AdaptiveDatasetKind.Metric: DatasetMetricSample,
            AdaptiveDatasetKind.Preference: DatasetPreferenceSample,
        }.get(self.kind)

        if expected_type:
            for i, sample in enumerate(samples):
                if not isinstance(sample, expected_type):
                    raise TypeError(f"Sample {i} is {type(sample)}, expected {expected_type} for {self.kind} dataset")

    def _sample_to_json(self, sample: DatasetSampleType) -> str:
        """Convert a dataset sample to JSON string."""
        # Use pydantic's model_dump to get the dictionary representation
        if hasattr(sample, "model_dump"):
            sample_dict = sample.model_dump()
        else:
            # Manual conversion as fallback
            sample_dict = sample.__dict__

        return json.dumps(sample_dict, default=str)  # default=str handles UUID serialization

    def _create_default_metadata(self) -> SampleMetadata:
        """Create default metadata for a sample."""
        return SampleMetadata(
            id=uuid.uuid4(), created_at=int(datetime.now().timestamp()), model_id=None, external_data=None
        )

    def _thread_to_dataset_sample(self, thread: StringThread) -> DatasetSampleType:
        """Convert a string thread to a dataset sample."""
        print(f"Converting thread to dataset sample: {thread}")
        turns = thread.messages()
        completion_text = thread.completion()
        completion = ["assistant", completion_text] if completion_text else None
        metadata = thread.metadata
        match self.kind:
            case AdaptiveDatasetKind.Prompt:
                return DatasetPromptSample(
                    prompt=turns,  # type: ignore
                    metadata=SampleMetadata(
                        id=uuid.uuid4(),
                        created_at=int(datetime.now().timestamp()),
                        model_id=None,
                        external_data=metadata,
                    ),
                )
            case AdaptiveDatasetKind.Completion:
                return DatasetSample(
                    prompt=turns,  # type: ignore
                    completion=completion,  # type: ignore
                    metadata=SampleMetadata(
                        id=uuid.uuid4(),
                        created_at=int(datetime.now().timestamp()),
                        model_id=None,
                        external_data=metadata,
                    ),
                )
            case AdaptiveDatasetKind.Metric:
                raise ValueError("Metric dataset kind is not supported with threads")
            case AdaptiveDatasetKind.Preference:
                raise ValueError("Preference dataset kind is not supported with threads")
            case AdaptiveDatasetKind.Mixed:
                return DatasetSample(
                    prompt=turns,  # type: ignore
                    completion=completion,  # type: ignore
                    metadata=SampleMetadata(
                        id=uuid.uuid4(),
                        created_at=int(datetime.now().timestamp()),
                        model_id=None,
                        external_data=metadata,
                    ),
                )

    def __repr__(self):
        return f"DatasetArtifact(id={self.id}, name={self.name}, kind={self.dataset_kind}, samples={self.sample_count}, uri={self.uri})"
