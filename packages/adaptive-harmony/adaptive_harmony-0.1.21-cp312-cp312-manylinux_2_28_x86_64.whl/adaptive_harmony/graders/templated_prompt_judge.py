import html
from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pybars import Compiler
from pydantic import BaseModel, Field

from adaptive_harmony import Grade, InferenceModel, StringThread, StringTurn
from adaptive_harmony.adaptive_harmony import HarmonyClient
from adaptive_harmony.core.structured_output import JsonParseError, render_schema
from adaptive_harmony.core.utils import stringify_thread
from adaptive_harmony.graders import Grader
from adaptive_harmony.graders.utils import (
    FailedJudgeLog,
    SuccessJudgeLog,
    separate_context_from_last_user_turn,
    validate_thread_last_assistant,
)

OPENAI_MODEL_FAMILIES_TEMPERATURE_1_ONLY = ["gpt-5", "o1", "o3", "o4"]


def _turns_to_dicts(turns: list[StringTurn]) -> list[dict[str, str]]:
    return [{"role": turn.role, "content": turn.content} for turn in turns]


class BaseTemplatedPromptJudgeOutput(ABC, BaseModel):
    @abstractmethod
    def get_score(self) -> float:
        pass

    def get_reasoning(self) -> str | None:
        return None


class SimpleReasonedFloatOutput(BaseTemplatedPromptJudgeOutput):
    """Sample default output format for simple float scores."""

    score: float = Field(description="The numerical score for the sample")
    reasoning: str = Field(description="Reasoning behind the score")

    def get_score(self) -> float:
        return self.score

    def get_reasoning(self) -> str:
        """Extract the reasoning from this output."""
        return self.reasoning


class BinaryJudgeOutput(BaseTemplatedPromptJudgeOutput):
    """Output format for binary PASS/FAIL/NA judges."""

    reasoning: str = Field(description="Reasoning string to support the rationale behind the score")
    score: str = Field(description="The literal score for the sample", pattern="^(PASS|FAIL|NA)$")

    SCORES_MAP: ClassVar[dict[str, float]] = {"PASS": 1.0, "FAIL": 0.0}

    def get_score(self) -> float:
        """Convert PASS/FAIL/NA to float. NA raises an exception."""
        if self.score not in self.SCORES_MAP:
            from adaptive_harmony.graders.exceptions import IgnoreScoreException

            raise IgnoreScoreException(f"Non applicable score: {self.reasoning}")
        return self.SCORES_MAP[self.score]

    def get_reasoning(self) -> str:
        return self.reasoning


class TemplatedPromptJudgeGrader[T: BaseTemplatedPromptJudgeOutput](Grader[SuccessJudgeLog | FailedJudgeLog]):
    r"""
    A flexible grader that uses Handlebars templates for system and user prompts.
    Generic over T, which must inherit from BaseTemplatedPromptJudgeOutput.
    This enforces that all output models implement get_score() and get_reasoning() methods.
    Templates have access to comprehensive context extracted from the StringThread:
    - output_schema: Expected output structure schema as a string
    - turns: List of all turns as dicts with "role" and "content" keys
    - metadata: Thread metadata dict
    - context_turns: All turns without the assistant's completion (includes system prompt)
    - context_str: Context formatted as string ('turn.role:\nturn.content\n' for every turn)
    - context_turns_without_last_user: Same as context_turns, but without the last user turn
    - context_str_without_last_user: Same as context_str, but without the last user turn
    - last_user_turn_content: Content of the last user turn
    - completion: Assistant's completion
    Example Handlebars templates:
    System: "You are a judge. Evaluate responses based on: {{criteria}}.
             Always output the following JSON schema, with no preamble or postamble: {{output_schema}}"
    User: "Conversation context:\n {{context_str_without_last_user}}
           Question:\n {{last_user_turn_content}}
           Response:\n {{completion}}"
    Advanced examples:
    - Conditionals: "{{#if metadata.domain}}Domain: {{metadata.domain}}{{/if}}"
    - Loops with element index: "{{#each user_turns}}Turn {{@index}}: {{content}}{{/each}}"
    - Built-in vars: "{{@index}}, {{@key}}, {{@first}}, {{@last}}"
    """

    def __init__(
        self,
        grader_key: str,
        model_key: str,
        client: HarmonyClient,
        system_template: str,
        user_template: str,
        output_model: type[T],
        template_variables: dict[str, Any] | None = None,
        tp: int | None = None,
        kv_cache_len: int | None = None,
        max_gen_length: int | None = None,
        temperature: float = 0.0,
        grader_id: str | None = None,
    ):
        """
        Initialize the templated prompt judge.
        Args:
            grader_key: Unique identifier for this grader
            model_key: Model to use for judgment
            client: HarmonyClient instance
            system_template: Handlebars template string for system prompt
            user_template: Handlebars template string for user prompt
            output_model: Pydantic model class that inherits from BaseOutput
                         (must implement get_score() and get_reasoning() methods)
            template_variables: Additional variables to make available in templates
            tp: Tensor parallel degree for judge model
            kv_cache_len: KV cache length for judge model
            max_gen_length: Maximum generation length for judge model
            grader_id: Optional grader ID (defaults to grader_key)
        """
        super().__init__(grader_key)
        self._logs: list[SuccessJudgeLog | FailedJudgeLog] = []  # type: ignore[assignment]

        self.model_key = model_key
        self.client = client
        self.tp = tp
        self.kv_cache_len = kv_cache_len
        self.max_gen_length = max_gen_length
        self.temperature = temperature
        # Set temperature to 1.0 if model_key is an OpenAI model in the temperature-1-only list
        if self.model_key.startswith("openai://"):
            model_name = self.model_key.removeprefix("openai://").split("?")[0]
            if any(model_name.startswith(model) for model in OPENAI_MODEL_FAMILIES_TEMPERATURE_1_ONLY):
                self.temperature = 1.0
        self.grader_id_or_key = grader_id or grader_key

        # Template setup
        self.compiler = Compiler()
        self.system_template = self.compiler.compile(system_template)
        self.user_template = self.compiler.compile(user_template)
        self.template_variables = template_variables or {}

        # Output configuration
        self.output_model = output_model

        self.model: InferenceModel
        self.judge_is_spawned = False

    @classmethod
    def render_template(cls, template: str, thread: StringThread, output_model: type[BaseModel]):
        compiler = Compiler()
        compiled_template = compiler.compile(template)
        context = cls._extract_template_context(thread, output_model)
        return html.unescape(compiled_template(context))

    @classmethod
    def _extract_template_context(
        cls,
        thread: StringThread,
        output_model: type[BaseModel],
        template_variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Extract context from StringThread for template rendering"""
        validate_thread_last_assistant(thread)

        turns = thread.get_turns()
        context_without_last_user, last_user_turn = separate_context_from_last_user_turn(
            thread, include_system_prompt=True
        )
        context = [turn for turn in turns[:-1]]

        # Build comprehensive context
        context = {
            # Core thread data
            "metadata": thread.metadata,
            "turns": _turns_to_dicts(turns),
            # Context and key turns
            "context_turns": _turns_to_dicts(context),
            "context_str": stringify_thread(StringThread(context)),
            "context_turns_without_last_user": _turns_to_dicts(context_without_last_user),
            "context_str_without_last_user": stringify_thread(StringThread(context_without_last_user)),
            "last_user_turn_content": last_user_turn,
            "completion": thread.last_content(),
            "output_schema": render_schema(output_model),
            # Additional template variables
            **(template_variables or {}),
        }

        return context

    def _build_judge_prompt(self, thread: StringThread) -> StringThread:
        """Build the judging prompt using Handlebars templates"""
        context = self._extract_template_context(thread, self.output_model, self.template_variables)

        # Render templates using pybars with helpers
        system_content = html.unescape(self.system_template(context))
        user_content = html.unescape(self.user_template(context))

        # Build prompt thread
        judge_thread = StringThread().system(system_content).user(user_content)
        return judge_thread

    async def setup(self) -> None:
        """Initialize the model for inference"""
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
        self.model = self.model.temperature(self.temperature)
        self.judge_is_spawned = True

    async def teardown(self) -> None:
        """Clean up the model."""
        if self.judge_is_spawned:
            await self.model.dealloc()
        self.judge_is_spawned = False

    async def grade(self, sample: StringThread) -> Grade:
        """Grade a sample using the templated prompt"""
        if not self.judge_is_spawned:
            raise RuntimeError("Model not initialized, run grader.setup() before grading")

        judging_prompt = self._build_judge_prompt(sample)
        str_prompt = stringify_thread(judging_prompt, sep=f"\n\n{'-' * 10}\n\n")

        try:
            judgement_str, parsed_output = await self.model.generate_and_validate(judging_prompt, self.output_model)
        except JsonParseError as e:
            self.add_log({"prompt": str_prompt, "error": f"{str(e)}\n\nCOMPLETION:\n{e.completion}"})
            raise
        except Exception as e:
            self.add_log({"prompt": str_prompt, "error": str(e)})
            raise

        # Extract score and reasoning using the abstract methods
        score = parsed_output.get_score()
        reasoning = parsed_output.get_reasoning() or ""

        grade = Grade(value=score, grader_key=self.grader_id_or_key, reasoning=reasoning)
        self.add_log({"score": score, "prompt": str_prompt, "reasoning": reasoning})

        return grade

    def get_logs(self, clear: bool = False, log_all_samples: bool = False) -> dict[str, float | Any]:
        """Get aggregated logs from all grading calls"""
        # Get base statistics
        logs = super().get_logs(clear=False)

        # Get sample logs
        successfully_scored_samples = [log for log in self._logs if "score" in log]
        failed_scored_samples = [log for log in self._logs if "error" in log]

        if not log_all_samples and successfully_scored_samples:
            # Limit samples for display
            successfully_scored_samples = successfully_scored_samples[:10]

        sample_logs = self.get_sample_tables(successfully_scored_samples, failed_scored_samples)
        logs.update(sample_logs)

        if clear:
            self.clear_logs()

        return logs
