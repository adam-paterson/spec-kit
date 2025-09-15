"""Baseline persistence helpers for benchmarks."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


@dataclass
class BaselineRecord:
    """Represents an approved baseline for a benchmark scenario."""

    scenario_id: str
    metrics: Dict[str, float]
    dataset_version: str
    runner_image: str
    notes: Optional[str] = None


def load_baselines(root: Path) -> Dict[str, BaselineRecord]:  # pragma: no cover - placeholder
    """Load baseline records from storage.

    Actual persistence will be implemented in a subsequent task.
    """

    return {}


def save_baseline(root: Path, record: BaselineRecord) -> None:  # pragma: no cover - placeholder
    """Persist a baseline record to storage (not yet implemented)."""
    raise NotImplementedError("Baseline persistence is not implemented yet")
