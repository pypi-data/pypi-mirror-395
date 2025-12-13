from typing import Sequence

from tqdm.auto import tqdm

from adaptive_harmony import CosineScheduler, DataSet, JobNotifier, Logger, StageNotifier, StringThread, TrainingModel
from adaptive_harmony.common.callbacks import RecipeCallback
from adaptive_harmony.core.utils import async_map_batch, log_args
from adaptive_harmony.metric_logger import StdoutLogger


class SFT:
    @log_args
    def __init__(
        self,
        dataset: list[StringThread],
        model: TrainingModel,
        logger: Logger = StdoutLogger(),
        stage_notifier: StageNotifier = JobNotifier().stage_notifier("SFT Training"),
        callbacks: Sequence[RecipeCallback] = [],
        lr: float = 1e-5,
        samples_per_batch=512,  # axel magic number: "pretty well validated across different scales"
        max_grad_norm=1.0,
        epochs: int = 1,
        weight_decay: float = 0,
        skip_nan_gradients: bool = False,
    ):
        self.dataset = DataSet(dataset, allow_looping=epochs != 1)
        self.lr_schedule = CosineScheduler(lr)
        self.model = model
        self.logger = logger
        self.stage_notifier = stage_notifier
        self.callbacks = callbacks
        self.samples_per_batch = samples_per_batch
        self.max_grad_norm = max_grad_norm
        self.epochs = epochs
        self.weight_decay = weight_decay
        self.skip_nan_gradients = skip_nan_gradients

    @property
    def training_completion_percentage(self):
        return self.dataset.completion_percentage() / self.epochs

    async def run(self):
        with tqdm(total=100) as pbar:
            while self.training_completion_percentage < 1.0:
                for callback in self.callbacks:  # performs checkpointing and validation by default, if params are set
                    if logs := await callback.maybe_call(self.training_completion_percentage):
                        self.logger(logs)

                self.stage_notifier.report_progress(
                    tot_num_samples=len(self.dataset) * self.epochs,
                    processed_num_samples=self.dataset.idx,
                    monitoring_link=self.logger.training_monitoring_link,
                )

                await async_map_batch(self.model.train_language_modelling, self.dataset, self.samples_per_batch)
                cp = self.training_completion_percentage
                current_lr = self.lr_schedule(cp)
                pbar.update(cp * 100.0 - pbar.n)

                logs = await self.model.optim_step(
                    current_lr,
                    wd=self.weight_decay,
                    max_grad_norm=self.max_grad_norm,
                    skip_nan_gradients=self.skip_nan_gradients,
                )

                self.logger(logs | dict(completion_percentage=cp))
