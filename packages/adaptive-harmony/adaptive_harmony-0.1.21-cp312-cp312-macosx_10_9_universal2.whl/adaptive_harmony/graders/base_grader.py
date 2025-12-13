import statistics
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, cast

from adaptive_harmony import Grade, HarmonyClient, StringThread
from adaptive_harmony.graders.utils import FailedJudgeLog, SuccessJudgeLog
from adaptive_harmony.logging_table import Table
from adaptive_harmony.runtime.data import (
    AdaptiveGrader,
    CustomJudge,
    PrebuiltConfigKey,
    PrebuiltJudge,
    RemoteRewardEndpoint,
)


class Grader[LogType](ABC):
    """
    Base Grader to inherit from when building a scoring function.
    """

    def __init__(self, grader_key: str):
        self._logs: list[LogType] = []
        self.grader_key = grader_key

    @abstractmethod
    async def grade(self, sample: StringThread) -> Grade:
        """
        Grade a single sample.
        Returns a single float score, with optional metadata.
        Metadata can be useful for evals when LLM reasoning regarding the score is available.
        """
        pass

    @abstractmethod
    async def setup(self) -> None:
        """
        Setup the grader.
        """
        pass

    @abstractmethod
    async def teardown(self) -> None:
        """
        Teardown the grader.
        """
        pass

    async def score_float_value(self, sample: StringThread) -> float:
        """Returns only the float score from .score"""
        return (await self.grade(sample)).value

    def add_log(self, log_data: LogType) -> None:
        """Add a log entry to the scorer's log collection."""
        self._logs.append(log_data)

    def get_logs(self, clear: bool = False, log_all_samples: bool = False) -> dict[str, float | Table]:
        """
        Get aggregated logs from all score calls.
        Base implementation computes statistics for "score" keys in individual logs.
        If there are none, returns empty dict.
        """
        if not self._logs:
            return {}

        scores = [s for s in [cast(dict[str, Any], log).get("score") for log in self._logs] if s is not None]
        logs = {}
        if scores:
            logs.update(
                dict(
                    **{
                        f"score/{key}": value
                        for key, value in dict(
                            mean=statistics.mean(scores),
                            std=statistics.stdev(scores) if len(scores) > 1 else 0.0,
                            min=min(scores),
                            max=max(scores),
                            count=len(scores),
                        ).items()
                    },
                )
            )
        if clear:
            self.clear_logs()
        return logs

    def clear_logs(self) -> None:
        """
        Clear all accumulated logs.
        """
        self._logs.clear()

    def get_sample_tables(
        self, successful_samples: list[SuccessJudgeLog], failed_samples: list[FailedJudgeLog] | None = None
    ):
        table_logs = {}
        scored_samples = (
            Table()
            .add_column("Prompt", [log["prompt"] for log in successful_samples])
            .add_column("Reasoning", [log.get("reasoning") for log in successful_samples])
            .add_column("Score", [float(log["score"]) for log in successful_samples])
        )
        if failed_samples:
            unscored_samples = (
                Table()
                .add_column("Prompt", [log.get("prompt") for log in failed_samples])
                .add_column("Error", [str(log["error"]) for log in failed_samples])
            )
            table_logs["score/unscored_samples"] = unscored_samples
        table_logs["score/scored_samples"] = scored_samples
        table_logs["score/unscored_samples_count"] = len(failed_samples) if failed_samples else 0
        table_logs["score/scored_samples_count"] = len(successful_samples)
        return table_logs

    @classmethod
    def from_function(
        cls, grader_key: str, async_fn: Callable[[StringThread], Awaitable[float]]
    ) -> "Grader[dict[str, Any]]":
        class FunctionScorer(Grader[dict[str, float]]):
            def __init__(self):
                super().__init__(grader_key)

            async def grade(self, sample: StringThread) -> Grade:
                result = await async_fn(sample)
                grade = Grade(value=result, grader_key=self.grader_key)
                self.add_log({"score": result})
                return grade

            async def setup(self) -> None:
                pass

            async def teardown(self) -> None:
                pass

        return FunctionScorer()

    @classmethod
    async def load(
        cls,
        grader_key: str,
        client: HarmonyClient,
        tp: int | None = None,
        kv_cache_len: int | None = None,
    ) -> "Grader[dict[str, Any]]":
        """
        Load a grader from the Adaptive platform using the internal API.

        Args:
            grader_key: Key of the grader to load
            client: HarmonyClient for inference
            tp: Tensor parallelism
            kv_cache_len: KV cache length

        Returns:
            Configured Grader instance ready for use
        """
        import json
        from uuid import UUID

        from adaptive_harmony.runtime.data import AdaptiveGrader

        conf = await client.get_model_config("gpt-4")
        conf = await client.get_dataset_config("hh-sft.jsonl-1760034249283")
        print(conf)
        exit()

        # Fetch grader config via internal API (uses client's stored use_case)
        config_json = await client.get_grader_config(grader_key)
        config = json.loads(config_json)

        # Parse the grader_config_json field and use Pydantic's discriminated union to deserialize
        grader_config_data = json.loads(config["grader_config_json"])

        # Build AdaptiveGrader from the response
        # Pydantic will automatically parse the config into the correct type (Judge/Prebuilt/Remote)
        # based on the "type" discriminator field
        grader_config = AdaptiveGrader(
            grader_id=UUID(config["grader_id"]),
            key=config["key"],
            metric_id=UUID("00000000-0000-0000-0000-000000000000"),  # Not used in from_config
            name=config["name"],
            config=grader_config_data,  # Pydantic will handle the Union type automatically
        )

        # Create grader instance
        return cls.from_config(
            grader_config=grader_config,
            client=client,
            tp=tp,
            kv_cache_len=kv_cache_len,
        )

    @classmethod
    def from_config(
        cls,
        grader_config: AdaptiveGrader,
        client: HarmonyClient,
        tp: int | None = None,
        kv_cache_len: int | None = None,
    ) -> "Grader[dict[str, Any]]":
        match grader_config.config.type:
            case "Judge":
                config = cast(CustomJudge, grader_config.config)
                return cls.from_templated_judge(
                    grader_config.key, str(grader_config.grader_id), config, client, tp, kv_cache_len
                )
            case "Prebuilt":
                config = cast(PrebuiltJudge, grader_config.config)
                return cls.from_prebuilt_judge(
                    grader_config.key, str(grader_config.grader_id), config, client, tp, kv_cache_len
                )
            case "Remote":
                config = cast(RemoteRewardEndpoint, grader_config.config)
                return cls.from_remote_reward_endpoint(grader_config.key, str(grader_config.grader_id), config)
            case _:
                raise ValueError(f"Invalid grader type: {grader_config.config.type}")

    @classmethod
    def from_templated_judge(
        cls,
        grader_key: str,
        grader_id: str,
        config: CustomJudge,
        client: HarmonyClient,
        tp: int | None = None,
        kv_cache_len: int | None = None,
    ) -> "Grader[dict[str, Any]]":
        # Import here to avoid circular dependency
        from adaptive_harmony.graders.templated_prompt_judge import (
            BinaryJudgeOutput,
            TemplatedPromptJudgeGrader,
        )

        # Convert examples to template variables
        examples = []
        for example in config.examples:
            examples.append(
                {
                    "context_str": (
                        "\n".join(f"{msg.role}:\n{msg.content}" for msg in example.input[:-1])
                        if len(example.input) > 1
                        else ""
                    ),
                    "user_question": example.input[-1].content if example.input else "",
                    "completion": example.output,
                    "output_json": f'{{"reasoning": "{example.reasoning or ""}", "score": "{"PASS" if example.pass_ else "FAIL"}"}}',
                }
            )

        template_vars = {
            "criteria": config.criteria,
            "examples": examples,
        }

        return TemplatedPromptJudgeGrader(
            grader_key=grader_key,
            grader_id=grader_id,
            model_key=config.model_uri,
            client=client,
            system_template=config.system_template,
            user_template=config.user_template,
            output_model=BinaryJudgeOutput,
            template_variables=template_vars,
            tp=tp,
            kv_cache_len=kv_cache_len,
        )  # type: ignore[return-value]

    @classmethod
    def from_prebuilt_judge(
        cls,
        grader_key: str,
        grader_id: str,
        config: PrebuiltJudge,
        client: HarmonyClient,
        tp: int | None = None,
        kv_cache_len: int | None = None,
    ) -> "Grader[dict[str, Any]]":
        match config.prebuilt_config_key:
            case PrebuiltConfigKey.Faithfulness:
                # Import here to avoid circular dependency
                from adaptive_harmony.graders.faithfulness_judge.faithfulness_judge import FaithfulnessGrader

                return FaithfulnessGrader(
                    grader_key=grader_key,
                    grader_id=grader_id,
                    model_key=config.model_uri,
                    client=client,
                    tp=tp,
                    kv_cache_len=kv_cache_len,
                )
            case PrebuiltConfigKey.AnswerRelevancy:
                # Import here to avoid circular dependency
                from adaptive_harmony.graders.answer_relevancy_judge.answer_relevancy_judge import AnswerRelevancyGrader

                return AnswerRelevancyGrader(
                    grader_key=grader_key,
                    grader_id=grader_id,
                    model_key=config.model_uri,
                    client=client,
                    tp=tp,
                    kv_cache_len=kv_cache_len,
                )
            case PrebuiltConfigKey.ContextRelevancy:
                # Import here to avoid circular dependency
                from adaptive_harmony.graders.context_relevancy_judge.context_relevancy_judge import (
                    ContextRelevancyGrader,
                )

                return ContextRelevancyGrader(
                    grader_key=grader_key,
                    grader_id=grader_id,
                    model_key=config.model_uri,
                    client=client,
                    tp=tp,
                    kv_cache_len=kv_cache_len,
                )
            case _:
                raise ValueError(f"Invalid prebuilt judge type: {config.prebuilt_config_key}")

    @classmethod
    def from_remote_reward_endpoint(
        cls, grader_key: str, grader_id: str, config: RemoteRewardEndpoint
    ) -> "Grader[dict[str, Any]]":
        # Import here to avoid circular dependency
        from adaptive_harmony.graders.reward_server_grader import RewardServerGrader

        return RewardServerGrader(grader_key=grader_key, grader_id=grader_id, reward_server_ip=config.url)
