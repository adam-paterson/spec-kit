"""Scenario metadata helpers for Spec Kit benchmarking."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Scenario:
    """Describes a benchmark scenario executed by TerminalBench."""

    scenario_id: str
    display_name: str
    command_path: str
    prerequisites: List[str]
    success_artifacts: List[str]


def default_scenarios() -> Dict[str, Scenario]:  # pragma: no cover - placeholder
    """Return the default scenarios tracked by the benchmarking toolkit."""
    return {
        "specify": Scenario(
            scenario_id="specify",
            display_name="Generate specification",
            command_path="/specify",
            prerequisites=[],
            success_artifacts=["spec.md"],
        ),
        "plan": Scenario(
            scenario_id="plan",
            display_name="Create implementation plan",
            command_path="/plan",
            prerequisites=["spec.md"],
            success_artifacts=["plan.md"],
        ),
        "tasks": Scenario(
            scenario_id="tasks",
            display_name="Create task list",
            command_path="/tasks",
            prerequisites=["plan.md"],
            success_artifacts=["tasks.md"],
        ),
    }
