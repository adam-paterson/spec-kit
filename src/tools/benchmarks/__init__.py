"""TerminalBench benchmarking toolkit for Spec Kit."""

from .cli import app  # re-export for convenience
from .config import BenchmarkConfig, load_config

__all__ = ["app", "BenchmarkConfig", "load_config"]
