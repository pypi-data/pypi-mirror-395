from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from numbers import Number
from typing import Any, Callable

import numpy as np

from adaptive_harmony import StringThread
from adaptive_harmony.logging_table import Table


@dataclass
class TurnScore:
    score: float
    num_assistant_turns: int


@dataclass
class TrajectoryScore:
    scores: list[TurnScore]

    def to_turn_scores(self) -> list[float]:
        return [turn_score.score for turn_score in self.scores for _ in range(turn_score.num_assistant_turns)]

    @property
    def cumulative_score(self) -> float:
        return sum([turn_score.score for turn_score in self.scores])


class Environment(ABC):
    """
    Environment to inherit from when building an environment.
    """

    def __init__(self, logging_function: Callable):
        self.logging_function = logging_function

    @abstractmethod
    async def react_to(self, thread: StringThread) -> list[tuple[str, str]] | TrajectoryScore:
        """Returns either [("tool", tool response), ...] or [("user", user question)] or TrajectoryScore when DONE."""
        pass

    async def bootstrap_prompt(self, thread: StringThread) -> StringThread:
        return thread

    async def generate_trajectory_and_grade(
        self, model, initial_thread: StringThread
    ) -> tuple[StringThread, TrajectoryScore]:
        """Generate a full trajectory by interacting with the model until termination."""
        thread = await self.bootstrap_prompt(initial_thread)

        while True:
            # Generate model response
            thread = await model.generate(thread)

            # Get environment reaction
            env_response = await self.react_to(thread)

            # If we got a score, we're done
            if isinstance(env_response, TrajectoryScore):
                return thread, env_response

            # Otherwise, add the environment responses to the thread
            for role, content in env_response:
                if role == "tool":
                    thread = thread.tool(content)
                elif role == "user":
                    thread = thread.user(content)
                else:
                    raise ValueError(f"Unknown role: {role}")


class EnvironmentFactory(ABC):
    """
    Abstract class to build environments. It is necessary because each trajectory must have its own unique Environment
    """

    def __init__(self, logging_name: str | None = None):
        self._logs: dict[str, list] = defaultdict(list)
        self.logging_name = logging_name

    def add_log(self, key, new_value) -> None:
        """Add a log entry to the scorer's log collection."""
        self._logs[key].append(new_value)

    def get_logs(self, clear: bool = False) -> dict[str, float | Table]:
        """
        Get aggregated logs from all score calls.
        Base implementation computes statistics for "score" keys in individual logs.
        If there are none, returns empty dict.
        """
        if not self._logs:
            return {}

        logs = {}
        for k, v in self._logs.items():
            if isinstance(v[0], Number):
                logs[k] = np.asarray(v).mean()
            elif isinstance(v[0], Table):
                headers = v[0].headers
                assert all(table.headers == headers for table in v)
                overall_table = Table(headers)
                for table in v:
                    overall_table.add_rows(table.rows)
                logs[k] = overall_table
            else:
                raise ValueError(f"Unknown type: {type(v[0])}")

        if clear:
            self.clear_logs()
        return logs

    def clear_logs(self) -> None:
        """
        Clear all accumulated logs.
        """
        self._logs.clear()

    @abstractmethod
    def create_environment(self, metadata: Any) -> Environment: ...
