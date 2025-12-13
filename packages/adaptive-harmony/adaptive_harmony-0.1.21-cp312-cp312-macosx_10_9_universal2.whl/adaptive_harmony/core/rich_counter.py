#!/usr/bin/env python

"""
Progress tracking and coroutine observability for async operations.

Provides real-time visualization of async task execution with a progress bar
and hierarchical coroutine call tree display.
"""

import asyncio
import os
import weakref

from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text


def _is_stdlib(filename: str) -> bool:
    """Check if a filename is from Python's standard library."""
    if not filename:
        return False

    # Check for common stdlib patterns
    stdlib_indicators = [
        "asyncio",
        "threading",
    ]

    return any(indicator in filename for indicator in stdlib_indicators)


def describe_coroutine(coro):
    """
    Extracts and returns all user code locations in the await chain as a list
    (excluding stdlib). Each entry is formatted as "filename:lineno code..."
    """
    user_code_locations = []

    # Follow the cr_await chain to collect all user coroutines
    while coro is not None:
        frame = getattr(coro, "cr_frame", None)
        if frame is None:
            break

        filename = frame.f_code.co_filename
        lineno = frame.f_lineno

        # Don't descend into stdlib code
        if _is_stdlib(filename):
            user_code_locations.append("Internals:...")
            break

        # Collect this user code location (no indentation - tree will handle that)
        # Truncate long file paths to just the filename
        short_filename = filename.split("/")[-1]
        # Get function name from frame
        func_name = frame.f_code.co_name
        # Keep it very short to fit in panel
        user_code_locations.append(f"{short_filename}:{lineno} {func_name}()")

        # Check if this coroutine is awaiting another coroutine
        awaited = getattr(coro, "cr_await", None)
        if awaited is None or not hasattr(awaited, "cr_frame"):
            # This is the innermost coroutine
            break

        # Descend into the awaited coroutine
        coro = awaited

    return user_code_locations


class ProgressCounterRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._main_counter_instance: ProgressCounter | None = None
        self._wrappers: dict[str, ProgressCounterWrapper] = {}
        self._initialized = True

    def get_main_counter(self) -> "ProgressCounter | None":
        return self._main_counter_instance

    def set_main_counter(self, counter: "ProgressCounter | None"):
        self._main_counter_instance = counter

    def get_wrapper(self, key: str) -> "ProgressCounterWrapper | None":
        return self._wrappers.get(key)

    def set_wrapper(self, key: str, wrapper: "ProgressCounterWrapper"):
        self._wrappers[key] = wrapper

    def reset(self):
        self._main_counter_instance = None
        self._wrappers.clear()


class CoroutineTree:
    """Manages building and formatting a tree structure from coroutine call chains."""

    def __init__(self):
        self.max_height = 1

    def build_from_chains(self, chains: list[list[str]]) -> dict:
        """Build a tree structure from coroutine call chains."""
        tree = {}

        for chain in chains:
            current = tree
            for desc in chain:
                if desc not in current:
                    current[desc] = {"count": 0, "children": {}}
                current[desc]["count"] += 1
                current = current[desc]["children"]

        return tree

    def format_as_text(self, tree: dict, prefix: str = "") -> Text:
        """Format tree structure as Rich Text with counts."""
        text = Text()
        items = list(tree.items())

        for i, (desc, node) in enumerate(items):
            is_last_item = i == len(items) - 1

            # Tree branch characters
            if prefix == "":
                branch = ""
            else:
                branch = "└── " if is_last_item else "├── "

            # Format line with count
            count_str = f"[{node['count']}] "
            text.append(prefix + branch, style="dim")
            text.append(count_str, style="bold magenta")
            text.append(desc + "\n")

            # Recurse into children
            if node["children"]:
                # Add indentation for children
                new_prefix = prefix + ("    " if is_last_item else "│   ")
                text.append(self.format_as_text(node["children"], new_prefix))

        return text

    def create_padded_display(self, chains: list[list[str]], active_count: int) -> Text:
        """Create a formatted and padded display text for the tree."""
        if not chains:
            return Text("No chains available", style="dim")

        # Build and format tree
        tree = self.build_from_chains(chains)
        header = Text(f"{active_count} tasks active\n\n", style="bold cyan")
        tree_content = self.format_as_text(tree)

        # Count lines to track height
        current_height = len(header.plain.split("\n")) + len(tree_content.plain.split("\n"))
        if current_height > self.max_height:
            self.max_height = current_height

        # Combine and add padding
        display = Text()
        display.append(header)
        display.append(tree_content)

        # Add padding to maintain consistent height
        padding_lines = max(0, self.max_height - current_height)
        for _ in range(padding_lines):
            display.append("\n")

        return display

    def create_empty_display(self) -> Text:
        """Create a display for when there are no active tasks."""
        display = Text("No active tasks but updated", style="dim")

        # Pad to maintain consistent height
        current_height = 1
        padding_lines = max(0, self.max_height - current_height)
        for _ in range(padding_lines):
            display.append("\n")

        return display


class ProgressCounter:
    def __init__(self, main_job_name: str, total_tasks: int):
        registry = ProgressCounterRegistry()
        assert registry.get_main_counter() is None, "Only one main counter instance is allowed"
        self.total_tasks = total_tasks

        # construct the left panel that will give the state of the batch at a glance
        self.overall_progress = Progress(
            "{task.description}",
            BarColumn(),
            TextColumn("[magenta]{task.completed:n} steps"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        )
        self.overall_task = self.overall_progress.add_task(main_job_name, total=self.total_tasks)
        self.overall_panel = Panel(
            self.overall_progress, title="Overall Progress", border_style="green", padding=(1, 1, 0, 1)
        )

        # construct the right panel for the coroutine tree
        self.coroutine_tree = CoroutineTree()
        self.tree_text = Text("Waiting for tasks...", style="dim")
        self.tree_panel = Panel(self.tree_text, title="[b]Coroutine Tree", border_style="blue", padding=(1, 2))

        self._monitored_tasks: weakref.WeakSet[asyncio.Task] = weakref.WeakSet()
        self._monitor_task: asyncio.Task | None = None
        self.interval = 0.5

        # Construct the general table with two columns
        self.progress_table = Table.grid()
        self.progress_table.add_row(self.overall_panel, self.tree_panel)

        # Disable the display if DISABLE_RICH_PROGRESS is set
        # TODO: make this less dirty
        self.enable_display = not os.getenv("DISABLE_RICH_PROGRESS", "0") == "1"

    def register_task(self, task: asyncio.Task):
        self._monitored_tasks.add(task)

    def increment_total_counter(self):
        self.overall_progress.advance(TaskID(0))

    def is_done(self):
        return self.overall_progress.finished

    async def _monitor_loop(self):
        try:
            while True:
                await asyncio.sleep(self.interval)

                # Filter out done tasks (just in case gc hasn't run yet)
                active = [t for t in self._monitored_tasks if not t.done()]

                # Collect all call chains
                chains = []
                for task in active:
                    coro = task.get_coro()
                    descriptions = describe_coroutine(coro)
                    if descriptions:
                        chains.append(descriptions)

                # Create tree display
                if not active or not chains:
                    self.tree_text = self.coroutine_tree.create_empty_display()
                else:
                    self.tree_text = self.coroutine_tree.create_padded_display(chains, len(active))

                # Update tree panel
                self.tree_panel = Panel(self.tree_text, title="[b]Coroutine Tree", border_style="blue", padding=(1, 2))

                # Update overall panel with matching height
                overall_with_padding = Group(
                    self.overall_progress,
                    Text("\n" * max(0, self.coroutine_tree.max_height - 2)),  # Account for progress bar base height
                )
                self.overall_panel = Panel(
                    overall_with_padding, title="Overall Progress", border_style="green", padding=(1, 1, 0, 1)
                )

                # Recreate the progress table with updated panels
                self.progress_table = Table.grid()
                self.progress_table.add_row(self.overall_panel, self.tree_panel)
                if self.enable_display:
                    self.live.update(self.progress_table)

        except asyncio.CancelledError:
            pass

    async def __aenter__(self):
        if self.enable_display:
            self.live = Live(self.progress_table, refresh_per_second=4).__enter__()
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        # Cancel the monitor task
        if self._monitor_task and not self._monitor_task.done():
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

        if self.enable_display:
            self.live.__exit__(exc_type, exc_value, exc_traceback)
        registry = ProgressCounterRegistry()
        assert registry.get_main_counter() is not None, "Weird state"
        # we clear both the main counter and any wrapper that would point to the old counter
        registry.reset()


class ProgressCounterWrapper(ProgressCounter):
    """Used to wrap a preexisting counter, needed to have simple logic in case an async_map is used inside an async_map_batch"""

    def __init__(self, inner: ProgressCounter, main_function_name: str):
        self.inner = inner
        self.main_function_name = main_function_name

    def register_task(self, task: asyncio.Task):
        return self.inner.register_task(task)

    def increment_total_counter(self):
        # For now we do nothing
        ...

    async def __aenter__(self):
        # do nothing, the inner progress counter has already been initialized
        return self

    async def __aexit__(self, _exc_type, _exc_value, _exc_traceback):
        # do nothing, the inner progress counter will be exited later
        ...


def get_progress_counter_or_wrapper(main_job_name: str, total_samples: int):
    registry = ProgressCounterRegistry()
    main_counter = registry.get_main_counter()

    if main_counter is None:
        main_counter = ProgressCounter(main_job_name, total_samples)
        registry.set_main_counter(main_counter)
        return main_counter
    else:
        wrapper = registry.get_wrapper(main_job_name)
        if wrapper is None:
            wrapper = ProgressCounterWrapper(main_counter, main_job_name)
            registry.set_wrapper(main_job_name, wrapper)
        return wrapper
