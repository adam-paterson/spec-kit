"""Expose the source package when running from a checkout.

This module makes ``import specify_cli`` succeed for tools like Terminal-Bench
without requiring an editable install. When the real package from
``src/specify_cli`` is available we load and return that module object so the
rest of the codebase observes the canonical implementation.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_SRC_PACKAGE = Path(__file__).resolve().parent.parent / "src" / "specify_cli"

if _SRC_PACKAGE.is_dir():
    spec = importlib.util.spec_from_file_location(__name__, _SRC_PACKAGE / "__init__.py")
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[__name__] = module
        spec.loader.exec_module(module)
    else:  # pragma: no cover - defensive guard, extremely unlikely
        raise ImportError(f"Unable to load specify_cli package from {_SRC_PACKAGE!s}")
else:  # pragma: no cover - occurs only if layout changes unexpectedly
    raise ImportError(
        "specify_cli source package not found. Did the repository layout change?"
    )
