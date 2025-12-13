from abc import abstractmethod
from typing import Any

import numpy as np
from loguru import logger

from adaptive_harmony.adaptive_harmony import (
    InferenceModel,
    StringThread,
    TrainingModel,
)
from adaptive_harmony.core.utils import async_map, async_map_fallible
from adaptive_harmony.environment import EnvironmentFactory
from adaptive_harmony.graders import Grader
from adaptive_harmony.logging_table import Table


class RecipeCallback:
    def __init__(self, frequency: float, log_key_prefix: str | None = None):
        self.frequency = frequency
        self.last_call = -1.0
        self.log_key_prefix = log_key_prefix

    async def maybe_call(self, current_percentage: float) -> dict[str, Any]:
        if current_percentage - self.last_call >= self.frequency:
            self.last_call = current_percentage
            callback_dict = await self.callback(current_percentage)
            prefixed_dict = {
                (f"{self.log_key_prefix}/{key}" if self.log_key_prefix else key): value
                for key, value in callback_dict.items()
            }
            return prefixed_dict
        return {}

    @abstractmethod
    async def callback(self, current_percentage: float) -> dict[str, Any]: ...


class GenerateSamplesCallback(RecipeCallback):
    def __init__(
        self,
        thread_set: list[StringThread],
        model: InferenceModel,
        frequency: float,
        log_key: str = "samples",
    ):
        super().__init__(frequency, log_key_prefix="generation")
        self.thread_set = thread_set
        self.model = model
        self.log_key = log_key

    async def callback(self, current_percentage: float) -> dict[str, Any]:
        logger.info("Entering generation callback...")
        generation_tokens = await async_map_fallible(self.model.generate_tokens, self.thread_set)
        generation_results = await async_map(self.model.detokenize_thread, generation_tokens)
        gen_lengths = [sample.len_last_turn() for sample in generation_tokens]

        generation_logs = {
            self.log_key: Table()
            .add_column(
                "system",
                [
                    sample.get_turns()[0].content if sample.get_turns()[0].role == "system" else ""
                    for sample in generation_results
                ],
            )
            .add_column(
                "prompt",
                [
                    repr(
                        StringThread(
                            sample.get_turns()[1:-1]
                            if (sample.get_turns() and sample.get_turns()[0].role == "system")
                            else sample.get_turns()[:-1]
                        )
                    )
                    for sample in generation_results
                ],
            )
            .add_column("response", [response.last_content() for response in generation_results]),
            "generation_length_mean": np.mean(gen_lengths).item(),
            "generation_length_std": np.std(gen_lengths).item(),
            "num_samples": len(generation_results),
        }
        return generation_logs


class ValidationLossCallback(RecipeCallback):
    def __init__(
        self,
        validation_set: list[StringThread],
        model: InferenceModel,
        frequency: float = 0.1,
        log_key: str = "loss",
    ):
        super().__init__(frequency, log_key_prefix="validation")
        self.validation_set = validation_set
        self.model = model
        self.log_key = log_key

    async def callback(self, current_percentage: float) -> dict[str, float]:
        logger.info("Entering validation loss callback...")
        losses = []
        tokens = await async_map(self.model.tokenize_thread, self.validation_set)
        logprobs = await async_map(self.model.logprobs_per_token, tokens)
        losses = [-(sum(lp) / len(lp)) for lp in logprobs]

        return {self.log_key: sum(losses) / len(losses)}


class CheckpointCallback(RecipeCallback):
    def __init__(
        self,
        model: TrainingModel,
        checkpoint_name: str,
        frequency: float = 0.2,
    ):
        super().__init__(frequency, log_key_prefix="checkpointing")
        self.last_call = 0.0  # avoid saving the model at the first period
        self.model = model
        self.model_log_name = checkpoint_name

    async def callback(self, current_percentage: float):
        logger.info(f"Saving checkpoint at {current_percentage * 100} % of training ...")
        await self.model.save(f"{self.model_log_name}-{round(current_percentage, 3)}")
        return {}


class GraderEvalCallback(RecipeCallback):
    def __init__(
        self,
        validation_set: list[StringThread],
        model: InferenceModel,
        grader: Grader,
        frequency: float,
        log_key: str = "validation",
        clear_grader_logs: bool = True,
        temperature: float = 0.0,
    ):
        super().__init__(frequency, log_key_prefix=log_key)
        self.validation_set = validation_set
        self.model = model
        self.grader = grader
        self.clear_grader_logs = clear_grader_logs
        self.temperature = temperature

    async def callback(self, current_percentage: float) -> dict[str, float | Table]:
        logger.info("Entering grader evaluation callback...")
        temp_model = self.model.temperature(self.temperature)

        tokenized_results = await async_map_fallible(temp_model.generate_tokens, self.validation_set)
        string_results = await async_map(temp_model.detokenize_thread, tokenized_results)
        grades = await async_map_fallible(self.grader.grade, string_results)
        gen_lengths = [sample.len_last_turn() for sample in tokenized_results]

        grader_logs = self.grader.get_logs(clear=self.clear_grader_logs)
        return {
            **{f"rewards/{key}": value for key, value in grader_logs.items()},
            "generation_length_mean": float(np.mean(gen_lengths).item()),
            "generation_length_std": float(np.std(gen_lengths).item()),
            "num_samples": float(len(grades)),
        }


class EnvironmentValidationCallback(RecipeCallback):
    def __init__(
        self,
        validation_set: list[StringThread],
        model: InferenceModel,
        env_factory: EnvironmentFactory,
        frequency: float,
        log_key: str = "validation",
        clear_env_logs: bool = True,
        temperature: float = 0.0,
        num_samples_log: int = 0,
    ):
        super().__init__(frequency, log_key_prefix=log_key)
        self.validation_set = validation_set
        self.model = model
        self.env_factory = env_factory
        self.clear_env_logs = clear_env_logs
        self.temperature = temperature
        self.num_samples_log = num_samples_log

    async def generate_trajectory(self, initial_thread: StringThread) -> tuple[StringThread, float, int]:
        env = self.env_factory.create_environment(initial_thread.metadata)
        temp_model = self.model.temperature(self.temperature)
        trajectory, trajectory_score = await env.generate_trajectory_and_grade(temp_model, initial_thread)
        num_turns = len([turn for turn in trajectory.get_turns() if turn.role == "assistant"])
        return trajectory, trajectory_score.cumulative_score, num_turns

    async def callback(self, current_percentage: float) -> dict[str, float | Table]:
        logger.info("Entering environment validation callback...")

        results = await async_map_fallible(self.generate_trajectory, self.validation_set)

        trajectories = [traj for traj, _, _ in results]
        scores = [score for _, score, _ in results]
        num_turns_list = [num_turns for _, _, num_turns in results]

        validation_logs = {
            "score_mean": np.mean(scores).item(),
            "score_std": np.std(scores).item(),
            "num_turns_mean": np.mean(num_turns_list).item(),
            "num_turns_std": np.std(num_turns_list).item(),
            "num_samples": len(results),
        }

        env_logs = self.env_factory.get_logs(clear=self.clear_env_logs)
        validation_logs.update({f"env/{key}": value for key, value in env_logs.items()})

        if self.num_samples_log > 0:
            samples = [repr(traj) for traj in trajectories[: self.num_samples_log]]
            samples_scores = scores[: self.num_samples_log]
            table = Table().add_column("trajectory", samples).add_column("score", samples_scores)
            validation_logs["samples"] = table

        logger.info(f"Validation Mean score: {validation_logs['score_mean']:.4f}")
        return validation_logs
