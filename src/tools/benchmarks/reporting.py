"""Benchmark reporting helpers."""

from typing import Any, Dict, List


def summarize_latest_run(dataset: str) -> Dict[str, Any]:  # pragma: no cover - placeholder
    """Return a structured summary of the most recent benchmark run."""
    raise NotImplementedError("Reporting has not been implemented yet")


def format_table(summary: Dict[str, Any]) -> str:  # pragma: no cover - placeholder
    """Render a human-readable table for the benchmark summary."""
    return "Benchmark reporting is not yet implemented"


def format_json(summary: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover - placeholder
    """Return a JSON-serialisable payload for the summary."""
    return summary
