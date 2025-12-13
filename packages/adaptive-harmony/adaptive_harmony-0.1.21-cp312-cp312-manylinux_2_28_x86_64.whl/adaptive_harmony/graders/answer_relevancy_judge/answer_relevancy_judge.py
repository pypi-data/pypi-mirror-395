from __future__ import annotations

from typing import Literal

import numpy as np
import pysbd
from pydantic import BaseModel, Field

from adaptive_harmony.adaptive_harmony import Grade, HarmonyClient, InferenceModel, StringThread
from adaptive_harmony.core.utils import stringify_thread
from adaptive_harmony.graders.answer_relevancy_judge.prompts import DEFAULT_SHOTS, SYSTEM, USER
from adaptive_harmony.graders.base_grader import Grader
from adaptive_harmony.graders.faithfulness_judge.faithfulness_judge import SupportedLanguages
from adaptive_harmony.graders.utils import sample_score_distribution, separate_context_from_last_user_turn
from adaptive_harmony.logging_table import Table


class StatementRelevancy(BaseModel):
    reason: str = Field(description="The justification for the score given to a statement. Keep it short and concise.")
    score: Literal[0, 1] = Field(
        description="The score for the statement. A score of 1 if the statement is relevant to addressing the original input, and 0 if the statement is irrelevant to addressing the input"
    )


class AnswerRelevancyResults(BaseModel):
    results: list[StatementRelevancy] = Field(description="A list of relevancy results for the statements")


class AnswerRelevancyGrader(Grader):
    def __init__(
        self,
        model_key: str,
        client: HarmonyClient,
        tp: int | None = None,
        kv_cache_len: int | None = None,
        max_gen_length: int | None = None,
        language: SupportedLanguages = "en",
        grader_key: str = "answer_relevancy_judge",
        grader_id: str | None = None,
    ):
        super().__init__(grader_key)
        self.model_key = model_key
        self.client = client
        self.tp = tp
        self.kv_cache_len = kv_cache_len
        self.language = language
        self.max_gen_length = max_gen_length
        self.grader_id_or_key = grader_id or grader_key
        self.judge_is_spawned = False
        self.sentence_splitter = pysbd.Segmenter(language=language)
        self.shots = DEFAULT_SHOTS
        self.model: InferenceModel

    async def grade(self, thread: StringThread) -> Grade:
        if not self.judge_is_spawned:
            raise RuntimeError("Model not initialized, run grader.setup() before grading")

        _, user_question = separate_context_from_last_user_turn(thread)

        completion = thread.last_content()
        split_sentences = self.sentence_splitter.segment(completion)
        sentences = [sentence.strip() for sentence in split_sentences if sentence.strip()]
        sentences_judge_str = "\n".join(f"{i}: {sentence}" for i, sentence in enumerate(sentences))

        thread = (
            StringThread()
            .system(SYSTEM.format(json_schema=self.model.render_schema(AnswerRelevancyResults), shots=self.shots))
            .user(USER.format(user_question=user_question, statements=sentences_judge_str))
        )

        try:
            _, response = await self.model.temperature(0.0).generate_and_validate(thread, AnswerRelevancyResults)
            results = response.results
        except Exception as e:
            self.add_log({"prompt": stringify_thread(thread, sep=f"\n\n{'-' * 10}\n\n"), "error": str(e)})
            raise

        reason = ""
        for i, (result, statement) in enumerate(zip(results, sentences)):
            emoji = "✅" if result.score == 1 else "❌"
            result = "PASS" if result.score == 1 else "FAIL"
            statement_display = statement[:150] + ("..." if len(statement) > 150 else "")
            reason += f"{emoji} Statement {i}: {result}\n Excerpt: {statement_display}:\nReason: {result}\n\n"

        score = np.mean([float(result.score) for result in results]) if results else 0.0
        self.add_log(
            {"score": score, "prompt": stringify_thread(thread, sep=f"\n\n{'-' * 10}\n\n"), "reasoning": reason}
        )
        return Grade(value=float(score), grader_key=self.grader_id_or_key, reasoning=reason)

    def get_logs(self, clear: bool = False, log_all_samples: bool = False) -> dict[str, float | Table]:
        # Only clear logs at the end if clear is True
        logs = super().get_logs(clear=False)

        successfully_scored_samples = [log for log in self._logs if "score" in log]

        # stratified sample range of scores to see high and low
        if not log_all_samples:
            subset_successfully_scored_samples = sample_score_distribution(successfully_scored_samples, 15)
        else:
            # if we have fewer than 15 samples or we want to log all samples, take them all
            subset_successfully_scored_samples = successfully_scored_samples

        failed_scored_samples = [log for log in self._logs if "error" in log]

        sample_logs = self.get_sample_tables(subset_successfully_scored_samples, failed_scored_samples)

        logs.update(sample_logs)

        if clear:
            self.clear_logs()

        return logs

    async def setup(self) -> None:
        gen_params = {
            k: v
            for k, v in {
                "kv_cache_len": self.kv_cache_len,
                "tokens_to_generate": self.max_gen_length,
            }.items()
            if v is not None
        }
        model = self.client.model(self.model_key, **gen_params)
        if self.tp is not None:
            model = model.tp(self.tp)
        self.model = await model.spawn_inference(self.grader_key)
        self.judge_is_spawned = True

    async def teardown(self) -> None:
        if self.judge_is_spawned:
            await self.model.dealloc()
        self.judge_is_spawned = False
