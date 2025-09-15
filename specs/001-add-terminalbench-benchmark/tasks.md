# Tasks: TerminalBench Benchmark Suite Integration

**Input**: Design documents from `/specs/001-add-terminalbench-benchmark/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/, quickstart.md

## Phase 3.1: Setup
- [ ] T001 Establish `src/tools/benchmarks/` package scaffolding (`__init__.py`, `__main__.py`, `cli.py`, `orchestrator_agent.py`, `scenarios.py`, `baselines.py`, `runner.py`, `reporting.py`) and ensure `python -m tools.benchmarks` boots a Typer app skeleton.
- [ ] T002 Update `pyproject.toml` to declare runtime dependencies (Typer extras, LiteLLM, TerminalBench CLI invocation helper, rich logging) and add an entry point script if packaging as `spec-tools`.
- [ ] T003 [P] Add configuration stubs under `src/tools/benchmarks/config.py` (or equivalent) capturing dataset defaults (`terminal-bench-core`), incident channel settings, and file locations for baselines/run artifacts.

## Phase 3.2: Tests First (TDD)
- [ ] T004 [P] Author contract tests for `python -m tools.benchmarks run` in `tests/contract/test_tools_benchmarks_run.py`, asserting options (`--scenarios`, `--dataset`, `--agent`, `--model`) and error handling match `contracts/tools-benchmarks-cli.md`.
- [ ] T005 [P] Author contract tests for `python -m tools.benchmarks report` in `tests/contract/test_tools_benchmarks_report.py`, validating table/JSON output schema and dataset scoping.
- [ ] T006 [P] Author contract tests for `python -m tools.benchmarks baseline approve` in `tests/contract/test_tools_benchmarks_baseline.py`, covering validation failures and audit logging.
- [ ] T007 [P] Write integration-agent test skeleton in `tests/integration_agents/test_orchestrator_agent.py` that simulates a `terminal-bench-core` task and verifies the orchestrator issues `/specify`, `/plan`, `/tasks`, then executes generated task commands before delegating.
- [ ] T008 [P] Add integration test in `tests/integration/test_terminalbench_runs.py` that fakes TerminalBench harness calls to ensure run metadata, artifact paths, and regression thresholds flow through reporting.
- [ ] T009 [P] Capture fixture data in `tests/regression/fixtures/terminalbench_core/` (sample `run_metadata.json`, `agent.cast`, `post-test.txt`) for use across tests.

## Phase 3.3: Core Implementation (only after tests fail)
- [ ] T010 Implement CLI command surfaces in `src/tools/benchmarks/cli.py` (Typer app) wiring `run`, `report`, and `baseline approve`, returning structured summaries and respecting config defaults.
- [ ] T011 Implement orchestrator agent in `src/tools/benchmarks/orchestrator_agent.py` (subclass TerminalBench `BaseAgent`) that enforces the Spec Kit workflow, integrates with LiteLLM-backed agents, and exposes a registration hook for the harness.
- [ ] T012 Build scenario catalog helpers in `src/tools/benchmarks/scenarios.py` to map `/specify`, `/plan`, `/tasks` workflows to benchmark scenarios with metadata from `data-model.md`.
- [ ] T013 Implement baseline persistence layer in `src/tools/benchmarks/baselines.py`, handling read/write of `BaselineRecord` data, provisional promotion logic, and storage under `specs/benchmarks/`.
- [ ] T014 Implement run execution pipeline in `src/tools/benchmarks/runner.py` that shells out to `tb run` (with Docker/env checks), injects the orchestrator agent parameters, captures artifacts, and enforces regression thresholds.
- [ ] T015 Implement reporting module in `src/tools/benchmarks/reporting.py` aggregating latest `BenchmarkRun` data, computing deltas, and formatting table/JSON output per contract.
- [ ] T016 Extend `tools_cli.py` (or add new dispatcher) so maintainers can list available tools and invoke benchmarks via a single entry point when installed as `spec-tools`.

## Phase 3.4: Integration & Harness Wiring
- [ ] T017 Integrate LiteLLM provider selection and credential loading (env vars, config files) within orchestrator/runner modules so downstream agents (Claude Code, Codex, Copilot) can be swapped via `--model`.
- [ ] T018 Add dataset/image parity checks in `runner.py`, comparing Docker digest, dataset version, and resource limits against baseline records; block runs on mismatch and emit structured diffs.
- [ ] T019 Implement incident escalation hooks that create triage tickets (with artifact bundle references) when regressions or functional failures occur, adhering to FR-005.
- [ ] T020 Wire baseline approval flow: ensure `baseline approve` updates Git-tracked YAML/JSON, records approver metadata, and regenerates audit logs.
- [ ] T021 Create TerminalBench harness configuration assets (e.g., agent import path, environment overlays) under `tools/benchmarks/harness/` so `tb run` can load the orchestrator inside CI/local runs.

## Phase 3.5: Polish & Documentation
- [ ] T022 [P] Author quickstart validation script referenced in `quickstart.md` (ensuring docs command works end-to-end) and document troubleshooting steps.
- [ ] T023 [P] Update repository docs (`README.md` benchmarking section and `/docs/`) to introduce the benchmarking toolkit, orchestrator behavior, and how to compare agents.
- [ ] T024 [P] Add structured logging configuration (JSON logs + metrics) and ensure logs surface in reports and incident payloads.
- [ ] T025 Final regression run: execute `uv run -m tools.benchmarks run --dataset terminal-bench-core --agent spec-kit-orchestrator` against a dry-run model, refresh baselines as needed, and capture outputs for release notes.

## Dependencies
- Setup tasks T001-T003 must complete before any tests.
- Contract and integration tests (T004-T009) must exist and fail before implementing CLI/orchestrator features (T010-T021).
- Orchestrator and runner implementation (T011, T014) depend on scenario/baseline modules (T012-T013).
- Incident and baseline workflows (T019-T020) depend on runner/baselines implementations.
- Polish tasks (T022-T025) require all core and integration work complete.

## Parallel Execution Example
```
# Example: Run independent contract and integration-agent tests in parallel
/spec-tools task run T004
/spec-tools task run T005
/spec-tools task run T006
/spec-tools task run T007
/spec-tools task run T008
/spec-tools task run T009
```

