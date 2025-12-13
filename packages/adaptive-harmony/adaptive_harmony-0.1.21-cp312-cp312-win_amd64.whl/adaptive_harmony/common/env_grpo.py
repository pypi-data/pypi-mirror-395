from dataclasses import dataclass
from typing import Sequence

import numpy as np

from adaptive_harmony import (
    CosineScheduler,
    DataSet,
    JobNotifier,
    Logger,
    StageNotifier,
    StringThread,
    TokenizedThread,
    TrainingModel,
)
from adaptive_harmony.common import RecipeCallback
from adaptive_harmony.core.utils import async_map, async_map_batch, get_minibatches, log_args
from adaptive_harmony.environment import EnvironmentFactory, TrajectoryScore
from adaptive_harmony.metric_logger import StdoutLogger


def compute_advantages(
    scores: list[TrajectoryScore],
    logprobs: list[list[float]],
    samples: list[TokenizedThread],
    num_generated_turns: list[int],
) -> list[list[float]]:
    def get_assistant_lengths(samples: list[TokenizedThread], num_generated_turns: list[int]) -> list[list[int]]:
        # here the +1 is because we have a loss weight on the EOD token of a turn, which is not represented when you look at the tokenized
        # Keep only the last num_generated_turns assistant turns (those with weight>0) since logprobs_per_token only returns logprobs for them
        return [
            [len(turn.content) + 1 for turn in sample.get_turns() if turn.role == "assistant"][-num_gen:]
            for sample, num_gen in zip(samples, num_generated_turns)
        ]

    # FROM https://arxiv.org/pdf/2402.03300 -> Process Supervision RL with GRPO
    # HERE PADDING DOES NOT PLAYS A ROLE IN ADVANTAGE COMPUTATION. SINCE nan are ignored.

    mapped_scores = [[turn_score.score for turn_score in score.scores] for score in scores]

    max_len = max(map(len, mapped_scores))

    # pad with np.nan instead of 0
    all_scores = np.full((len(mapped_scores), max_len), np.nan)
    for i, s in enumerate(mapped_scores):
        all_scores[i, : len(s)] = s

    # nan-aware mean and std
    mean = np.nanmean(all_scores)
    std = np.nanstd(all_scores) + 1e-8

    normalized_rewards = (all_scores - mean) / std

    # cumulative sum per row, ignoring nans
    score_level_advantage = np.where(
        np.isnan(normalized_rewards),
        np.nan,
        np.cumsum(np.nan_to_num(normalized_rewards)[:, ::-1], axis=1)[:, ::-1],
    )

    turn_level_advantage = [
        np.repeat(
            adv[: len(score.scores)],
            [turn_score.num_assistant_turns for turn_score in score.scores],
        )
        for adv, score in zip(score_level_advantage, scores)
    ]

    assistant_lengths = get_assistant_lengths(samples, num_generated_turns)
    assert all([len(lp) == sum(al) for lp, al in zip(logprobs, assistant_lengths)])

    token_level_advantage = [np.repeat(adv, al).tolist() for adv, al in zip(turn_level_advantage, assistant_lengths)]

    return token_level_advantage


@dataclass
class Sample:
    sample: TokenizedThread
    logprobs: list[float]
    ref_logprobs: list[float]
    advantage: list[float]
    kl_div: list[float]
    # for logging
    score: float
    gen_len: float


class ENVGRPO:
    @log_args
    def __init__(
        self,
        dataset: list[StringThread],
        model: TrainingModel,
        environment_factory: EnvironmentFactory,
        logger: Logger = StdoutLogger(),
        stage_notifier: StageNotifier = JobNotifier().stage_notifier("GRPO Training"),
        callbacks: Sequence[RecipeCallback] = [],
        validation_dataset: list[StringThread] | None = None,
        validation_frequency: float = 0.2,
        max_num_grpo_steps: int | None = None,
        completions_per_sample=8,
        lr: float = 7.5e-7,
        samples_per_batch=128,
        samples_per_mini_batch=128,
        mini_epochs_per_batch=1,
        max_grad_norm=1.0,
        clip_range=0.1,
        kl_beta=0.1,
        weight_decays: float = 0.0,
        skip_nan_gradients: bool = False,
    ):
        # Core components
        self.dataset = DataSet(dataset, allow_looping=True)
        self.model = model
        self.logger = logger
        self.stage_notifier = stage_notifier
        self.sample_index_counter = 0
        self.skip_nan_gradients = skip_nan_gradients
        # Validation data/params
        self.validation_dataset = validation_dataset
        self.validation_frequency = validation_frequency
        self.last_validation_percentage = -1.0  # Validation will run before training starts
        # GRPO HP's
        self.max_num_batches = max_num_grpo_steps
        self.completions_per_sample = completions_per_sample
        self.lr_schedule = CosineScheduler(lr)
        self.samples_per_batch = samples_per_batch // completions_per_sample
        self.samples_per_mini_batch = samples_per_mini_batch
        self.total_num_samples = (
            self.max_num_batches * self.samples_per_batch if self.max_num_batches else len(self.dataset)
        )
        self.max_grad_norm = max_grad_norm
        self.environment_factory = environment_factory
        self.clip_range = clip_range
        self.kl_beta = kl_beta
        self.weight_decays = weight_decays
        self.mini_epochs_per_batch = mini_epochs_per_batch

        self.num_batches_processed = 0
        self.callbacks = callbacks

    @property
    def completion_percentage(self):
        return (
            self.dataset.completion_percentage()
            if self.max_num_batches is None
            else min(self.num_batches_processed / self.max_num_batches, 1.0)
        )

    async def gen_data(self, sample: StringThread) -> list[Sample]:
        async def generate_trajectory(
            prompt: StringThread,
        ) -> tuple[TokenizedThread, TrajectoryScore, int]:
            # this create the environment for the first turn.
            environment = self.environment_factory.create_environment(prompt.metadata)
            prompt = await environment.bootstrap_prompt(prompt)

            # Count assistant turns in the context (before generation)
            nb_context_assistant_turns = sum(1 for turn in prompt.get_turns() if turn.role == "assistant")

            string_trajectory = await self.model.generate(prompt)  # generate the first response from the agent.
            num_generated_turns = 1
            # we loop until the environment returns a score.
            # notice how the environment can return a score or a tool or user response.
            while not isinstance(
                environment_response := await environment.react_to(string_trajectory),
                TrajectoryScore,
            ):
                for env_role, env_content in environment_response:
                    if not isinstance(env_content, str):
                        raise ValueError(f"env_content should be a str, got {env_content}")
                    if env_role == "user":
                        string_trajectory = string_trajectory.user(env_content)
                    elif env_role == "tool":
                        string_trajectory = string_trajectory.tool(env_content)
                    else:
                        raise ValueError
                string_trajectory = await self.model.generate(string_trajectory)
                num_generated_turns += 1

            tokenized_trajectory = (
                await self.model.tokenize_thread(string_trajectory)
            ).with_weight_assistant_turns_from_index(nb_context_assistant_turns)

            return tokenized_trajectory, environment_response, num_generated_turns

        assert self.model_ref is not None, "Calling `gen_data` before reference model has been set"

        trajs_and_scores = await async_map(generate_trajectory, [sample] * self.completions_per_sample)
        all_samples = [traj for traj, _, _ in trajs_and_scores]
        num_generated_turns_list = [num_turns for _, _, num_turns in trajs_and_scores]
        logprobs = await async_map(self.model.logprobs_per_token, all_samples)
        ref_logprobs = await async_map(self.model_ref.logprobs_per_token, all_samples)

        all_trajectory_scores = [score for _, score, _ in trajs_and_scores]
        advantages = compute_advantages(all_trajectory_scores, logprobs, all_samples, num_generated_turns_list)

        kl = [
            (np.array(lp, dtype=np.float32) - np.array(ref_lp, dtype=np.float32)).tolist()
            for lp, ref_lp in zip(logprobs, ref_logprobs)
        ]

        samples = []
        for i in range(len(logprobs)):
            samples.append(
                Sample(
                    sample=all_samples[i],
                    logprobs=logprobs[i],
                    ref_logprobs=ref_logprobs[i],
                    advantage=advantages[i],
                    kl_div=kl[i],
                    score=all_trajectory_scores[i].cumulative_score,
                    gen_len=all_samples[i].len_last_turn(),
                )
            )
        return samples

    async def train_sample(self, sample: Sample):
        await self.model.train_grpo(
            sample.sample,
            sample.logprobs,
            sample.ref_logprobs,
            sample.advantage,
            self.clip_range,
            self.kl_beta,
        )

    async def run(self):
        self.model_ref = await self.model.clone_inf()

        while self.completion_percentage < 1.0:
            self.stage_notifier.report_progress(
                tot_num_samples=self.total_num_samples,
                processed_num_samples=self.num_batches_processed * self.samples_per_batch,
                monitoring_link=self.logger.training_monitoring_link,
            )
            self.num_batches_processed += 1

            for callback in self.callbacks:
                if logs := await callback.maybe_call(self.completion_percentage):
                    self.logger(logs)

            # Generate training samples
            data = await async_map_batch(self.gen_data, self.dataset, self.samples_per_batch)

            completion_percentage = (
                self.dataset.completion_percentage()
                if self.max_num_batches is None
                else min(self.num_batches_processed / self.max_num_batches, 1.0)
            )
            current_lr = self.lr_schedule(completion_percentage)

            scorer_logs = {}
            for key, value in self.environment_factory.get_logs(clear=True).items():
                if "/" not in key:
                    key = f"environment/{key}"
                scorer_logs[key] = value
            batch_logs = {
                **scorer_logs,
                **self.get_train_batch_logs(data),
            }

            current_lr = self.lr_schedule(self.completion_percentage)

            # Train on generated samples
            flattened_data = sum([inner_list for inner_list in data], start=[])
            minibatches = get_minibatches(flattened_data, self.samples_per_mini_batch, self.mini_epochs_per_batch)
            for idx, mini_batch in enumerate(minibatches):
                await async_map(self.train_sample, mini_batch)
                optim_logs = await self.model.optim_step(
                    current_lr, wd=0.0, max_grad_norm=self.max_grad_norm, skip_nan_gradients=self.skip_nan_gradients
                )
                if idx == len(minibatches) - 1:
                    # only log tables and full batch-related logs on the final minibatch
                    self.logger(optim_logs | batch_logs)
                else:
                    self.logger(optim_logs)

    def get_train_batch_logs(self, data: list[list[Sample]]) -> dict:
        return {
            **dict(
                completion_percentage=self.completion_percentage,
                score_mean=np.mean([[sample.score for sample in batch] for batch in data]).item(),
                percentage_no_advantages=np.mean(
                    [all(sample.advantage == batch[0].advantage for sample in batch) for batch in data]
                ).item(),
                score_std=np.std([[sample.score for sample in batch] for batch in data]).item(),
                kl_div=np.mean([[np.mean(sample.kl_div) for sample in batch] for batch in data]).item(),
                generation_length=np.mean([np.mean([sample.gen_len for sample in batch]) for batch in data]).item(),
                logprobs=np.mean(
                    np.concatenate([np.concatenate([sample.logprobs for sample in batch]) for batch in data])
                ).item(),
                ref_logprobs=np.mean(
                    np.concatenate([np.concatenate([sample.ref_logprobs for sample in batch]) for batch in data])
                ).item(),
            ),
        }
