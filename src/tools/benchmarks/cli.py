"""Typer CLI entry points for TerminalBench benchmarking workflows."""

from typing import Optional

import typer

from .config import load_config

app = typer.Typer(help="Run Spec Kit benchmarking workflows backed by TerminalBench.")


@app.command()
def run(
    scenarios: Optional[str] = typer.Option(
        None,
        "--scenarios",
        help="Comma-separated scenario identifiers to execute.",
    ),
    dataset: Optional[str] = typer.Option(
        None,
        "--dataset",
        help="TerminalBench dataset name to execute.",
    ),
    agent: Optional[str] = typer.Option(
        None,
        "--agent",
        help="TerminalBench agent identifier to load.",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        help="Optional downstream model identifier to forward to the orchestrator.",
    ),
) -> None:
    """Execute the requested benchmarking scenarios."""
    cfg = load_config()
    selected_dataset = dataset or cfg.dataset
    selected_agent = agent or cfg.default_agent
    selected_model = model or cfg.default_model
    if scenarios:
        scenario_list = [item.strip() for item in scenarios.split(",") if item.strip()]
    else:
        scenario_list = cfg.default_scenarios

    typer.echo(
        "Spec Kit benchmarking run tooling is not yet implemented. "
        "Scenarios=%s, dataset=%s, agent=%s, model=%s"
        % ("/".join(scenario_list), selected_dataset, selected_agent, selected_model)
    )
    raise typer.Exit(code=1)


@app.command()
def report(
    run_id: Optional[str] = typer.Option(
        None,
        "--run",
        help="Specific benchmark run identifier to summarize.",
    ),
    dataset: Optional[str] = typer.Option(
        None,
        "--dataset",
        help="Dataset name for report scope.",
    ),
    output_format: str = typer.Option(
        "table",
        "--format",
        help="Output format for the summary (table or json).",
    ),
) -> None:
    """Summarize the most recent benchmarking results."""
    cfg = load_config()
    selected_dataset = dataset or cfg.dataset

    typer.echo(
        "Benchmark reporting is not yet implemented. "
        "run=%s, dataset=%s, format=%s"
        % (run_id or "latest", selected_dataset, output_format)
    )
    raise typer.Exit(code=1)


@app.command("baseline-approve")
def baseline_approve(
    scenario: str = typer.Option(..., "--scenario", help="Scenario identifier to promote."),
    run_id: str = typer.Option(..., "--run", help="Benchmark run to use for promotion."),
    dataset: Optional[str] = typer.Option(
        None,
        "--dataset",
        help="Dataset name for baseline record.",
    ),
    notes: Optional[str] = typer.Option(
        None,
        "--notes",
        help="Optional notes to record alongside the baseline promotion.",
    ),
) -> None:
    """Promote a provisional result to become the active baseline."""
    cfg = load_config()
    selected_dataset = dataset or cfg.dataset

    typer.echo(
        "Baseline promotion tooling is not yet implemented. "
        "scenario=%s, run=%s, dataset=%s"
        % (scenario, run_id, selected_dataset)
    )
    if notes:
        typer.echo(f"Notes: {notes}")
    raise typer.Exit(code=1)


@app.callback()
def main(_: Optional[bool] = typer.Option(None, hidden=True)) -> None:
    """Entrypoint for the spec-tools benchmarking CLI."""
    # Callback exists to provide a top-level help description.
    return None
