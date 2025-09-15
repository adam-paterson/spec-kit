"""Configuration helpers for the benchmarking toolkit."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv

# Load environment variables from a `.env` file if present so maintainers can
# configure credentials without exporting them in every shell.
load_dotenv()

DEFAULT_DATASET = "terminal-bench-core"
DEFAULT_SCENARIOS = ["specify", "plan", "tasks"]
DEFAULT_AGENT = "spec-kit-orchestrator"


@dataclass
class BenchmarkConfig:
    """Serializable configuration describing how benchmarks should run."""

    dataset: str = DEFAULT_DATASET
    default_scenarios: List[str] = field(default_factory=lambda: DEFAULT_SCENARIOS.copy())
    default_agent: str = DEFAULT_AGENT
    default_model: Optional[str] = None
    artifacts_dir: Path = Path(".terminalbench")
    baselines_dir: Path = Path("specs/benchmarks")
    incident_channel: Optional[str] = None


def load_config() -> BenchmarkConfig:
    """Load configuration using environment overrides where available."""

    dataset = os.getenv("SPEC_BENCH_DATASET", DEFAULT_DATASET)
    scenarios_env = os.getenv("SPEC_BENCH_SCENARIOS")
    if scenarios_env:
        scenarios = [entry.strip() for entry in scenarios_env.split(",") if entry.strip()]
    else:
        scenarios = DEFAULT_SCENARIOS.copy()

    agent = os.getenv("SPEC_BENCH_AGENT", DEFAULT_AGENT)
    model = os.getenv("SPEC_BENCH_MODEL")
    artifacts_dir = Path(os.getenv("SPEC_BENCH_ARTIFACTS", ".terminalbench"))
    baselines_dir = Path(os.getenv("SPEC_BENCH_BASELINES", "specs/benchmarks"))
    incident_channel = os.getenv("SPEC_BENCH_INCIDENT_CHANNEL") or None

    return BenchmarkConfig(
        dataset=dataset,
        default_scenarios=scenarios,
        default_agent=agent,
        default_model=model,
        artifacts_dir=artifacts_dir,
        baselines_dir=baselines_dir,
        incident_channel=incident_channel,
    )


__all__ = [
    "BenchmarkConfig",
    "load_config",
    "DEFAULT_DATASET",
    "DEFAULT_SCENARIOS",
    "DEFAULT_AGENT",
]
