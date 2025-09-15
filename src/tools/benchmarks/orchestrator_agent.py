"""Placeholder orchestrator agent enforcing the Spec Kit workflow."""

from typing import Any


class SpecKitBenchAgent:
    """Stub agent that will orchestrate Spec Kit benchmarking runs.

    This placeholder supplies the public surface expected by TerminalBench. The
    full implementation will subclass the proper TerminalBench agent base class
    and ensure each task executes the `/specify`, `/plan`, `/tasks` workflow
    before delegating to a downstream model driver.
    """

    def perform_task(self, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover - placeholder
        raise NotImplementedError("SpecKitBenchAgent.perform_task is not implemented yet")
