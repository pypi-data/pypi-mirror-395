from __future__ import annotations

import asyncio
from typing import Literal

import numpy as np
import pysbd
from pydantic import BaseModel, Field

from adaptive_harmony.adaptive_harmony import Grade, HarmonyClient, InferenceModel, StringThread
from adaptive_harmony.core.utils import stringify_thread
from adaptive_harmony.graders.base_grader import Grader
from adaptive_harmony.graders.context_relevancy_judge.prompts import DEFAULT_SHOTS, SYSTEM, USER
from adaptive_harmony.graders.faithfulness_judge.faithfulness_judge import SupportedLanguages
from adaptive_harmony.graders.utils import sample_score_distribution
from adaptive_harmony.logging_table import Table


class DocumentRelevancyResult(BaseModel):
    reason: str = Field(description="The justification for the score given to a document. Keep it short and concise.")
    score: Literal[0, 1] = Field(
        description="The score for the document. A score of 1 if the document contains information relevant to answering the user input, and 0 if the document does not contain information relevant to answering the user input"
    )


class ContextRelevancyGrader(Grader):
    def __init__(
        self,
        model_key: str,
        client: HarmonyClient,
        tp: int | None = None,
        kv_cache_len: int | None = None,
        max_gen_length: int | None = None,
        language: SupportedLanguages = "en",
        grader_key: str = "context_relevancy_judge",
        grader_id: str | None = None,
    ):
        super().__init__(grader_key)
        self.model_key = model_key
        self.client = client
        self.tp = tp
        self.kv_cache_len = kv_cache_len
        self.max_gen_length = max_gen_length
        self.language = language
        self.grader_id_or_key = grader_id or grader_key
        self.judge_is_spawned = False
        self.sentence_splitter = pysbd.Segmenter(language=language)
        self.shots = DEFAULT_SHOTS
        self.model: InferenceModel

    async def grade(self, thread: StringThread) -> Grade:
        if not self.judge_is_spawned:
            raise RuntimeError("Model not initialized, run grader.setup() before grading")

        documents = thread.metadata.get("documents", []) if thread.metadata else []
        if not documents:
            self.add_log(
                {
                    "prompt": stringify_thread(thread, sep=f"\n\n{'-' * 10}\n\n"),
                    "error": "No document turns found in thread",
                }
            )
            raise ValueError("No document turns found in thread")

        user_question = next((turn[1] for turn in reversed(thread.get_turns()) if turn[0] == "user"), None)
        if not user_question:
            self.add_log(
                {"prompt": stringify_thread(thread, sep=f"\n\n{'-' * 10}\n\n"), "error": "No user turn found in thread"}
            )
            raise ValueError("No user turn found in thread")

        judging_threads = [
            (
                StringThread()
                .system(SYSTEM.format(json_schema=self.model.render_schema(DocumentRelevancyResult), shots=self.shots))
                .user(USER.format(user_question=user_question, document=document))
            )
            for document in documents
        ]

        try:
            judge_tasks = [
                self.model.temperature(0.0).generate_and_validate(thread, DocumentRelevancyResult)
                for thread in judging_threads
            ]
            results = await asyncio.gather(*judge_tasks)
        except Exception as e:
            self.add_log(
                {
                    "error": str(e),
                    "number_of_documents": len(documents),
                    "documents": documents,
                    "prompt": stringify_thread(judging_threads[0]),
                }
            )
            raise

        doc_relevancy_results = [result[1] for result in results]

        reason = ""
        for i, (document, doc_result) in enumerate(zip(documents, doc_relevancy_results)):
            emoji = "✅" if doc_result.score == 1 else "❌"
            result = "PASS" if doc_result.score == 1 else "FAIL"
            doc_display = document[:150] + ("..." if len(document) > 150 else "")
            reason += f"{emoji} Document {i}: {result}\n Content: {doc_display}:\nReason: {doc_result.reason}\n\n"

        score = np.mean([float(verdict.score) for verdict in doc_relevancy_results]) if doc_relevancy_results else 0.0
        self.add_log(
            {
                "score": score,
                "reasoning": reason,
                "number_of_documents": len(documents),
                "documents": documents,
                "prompt": stringify_thread(judging_threads[0]),
            }
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
