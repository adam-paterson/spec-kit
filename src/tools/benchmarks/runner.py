"""Benchmark runner integration points."""

from typing import Optional


def run_benchmarks(
    scenarios: str,
    dataset: str,
    agent: str,
    model: Optional[str] = None,
) -> None:  # pragma: no cover - placeholder
    """Invoke TerminalBench for the requested scenarios (placeholder)."""
    raise NotImplementedError("Benchmark runner integration not implemented yet")
