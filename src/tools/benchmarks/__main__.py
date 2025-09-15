"""Entry point enabling `python -m tools.benchmarks`."""

from .cli import app


def main() -> None:
    """Dispatch to the Typer application."""
    app()


if __name__ == "__main__":
    main()
