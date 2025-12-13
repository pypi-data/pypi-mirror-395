from adaptive_harmony import (
    JobNotifier,
    Logger,
    StageNotifier,
    StringThread,
    TrainingModel,
)
from adaptive_harmony.common.callbacks import RecipeCallback
from adaptive_harmony.common.grpo import GRPO, Sample
from adaptive_harmony.graders import Grader
from adaptive_harmony.metric_logger import StdoutLogger


class GSPO(GRPO):  # grpo already logs args so we don't do it here
    def __init__(
        self,
        dataset: list[StringThread],
        model: TrainingModel,
        grader: Grader,
        logger: Logger = StdoutLogger(),
        stage_notifier: StageNotifier = JobNotifier().stage_notifier("GRPO Training"),
        callbacks: list[RecipeCallback] = [],
        max_num_gspo_steps: int | None = None,
        completions_per_sample=8,
        lr: float = 7.5e-7,
        samples_per_batch=128,
        samples_per_mini_batch=128,
        mini_epochs_per_batch=1,
        max_grad_norm=1.0,
        # wildly different defaults than GRPO because we are looking at the
        # entire sequence at once, I tried the number from the GSPO paper but
        # it was skipping ~60% of the samples. I had good success with 0.01 but
        # it's not properly swept yet.
        clip_range=0.01,
        kl_beta=0.01,
        weight_decay=0,
    ):
        super().__init__(
            dataset,
            model,
            grader,
            logger,
            stage_notifier,
            callbacks,
            max_num_grpo_steps=max_num_gspo_steps,
            completions_per_sample=completions_per_sample,
            lr=lr,
            samples_per_batch=samples_per_batch,
            samples_per_mini_batch=samples_per_mini_batch,
            mini_epochs_per_batch=mini_epochs_per_batch,
            max_grad_norm=max_grad_norm,
            clip_range=clip_range,
            kl_beta=kl_beta,
            weight_decay=weight_decay,
        )

    async def train_sample(self, sample: Sample):
        await self.model.train_gspo(
            sample.sample,
            sample.logprobs,
            sample.ref_logprobs,
            [sample.advantage],  # only diff with grpo is we train with a single advantage
            self.clip_range,
            self.clip_range,
            self.kl_beta,
        )
