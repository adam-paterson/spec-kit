# Implementation Plan: TerminalBench Benchmark Suite Integration

**Branch**: `[001-add-terminalbench-benchmark]` | **Date**: 2025-09-15 | **Spec**: `/root/projects/personal/spec-kit/specs/001-add-terminalbench-benchmark/spec.md`
**Input**: Feature specification from `/specs/001-add-terminalbench-benchmark/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → Completed (spec located at /root/projects/personal/spec-kit/specs/001-add-terminalbench-benchmark/spec.md)
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → No outstanding NEEDS CLARIFICATION markers after spec update
3. Evaluate Constitution Check section below
   → Constitution file is templated; no explicit constraints identified, proceed with documented guardrails
   → Progress Tracking updated: Initial Constitution Check
4. Execute Phase 0 → research.md
   → Research summary authored, capturing harness usage, dataset governance, and baseline policy
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent context stub
   → Artifacts generated under specs/001-add-terminalbench-benchmark/
6. Re-evaluate Constitution Check section
   → Design remains within documented scope; guardrails reaffirmed
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
   → Approach documented in Phase 2 section below
8. STOP - Ready for /tasks command
```

## Summary
The TerminalBench benchmark suite will formalize performance validation for Spec Kit’s CLI workflows (`/specify`, `/plan`, `/tasks`) while keeping benchmarking capabilities in standalone tooling under `tools/benchmarks`. A custom orchestrator agent will enforce that workflow for every `terminal-bench-core` task before delegating to Claude Code, Codex, or other agents. We will author benchmark scenarios, enforce environment parity through TerminalBench harness integrations, preserve baselines, and ensure regression signals propagate to maintainers before releases without altering the end-user CLI.

## Technical Context
**Language/Version**: Python 3.11 (existing Spec Kit CLI baseline)  
**Primary Dependencies**: Typer (for tools CLI), Rich, TerminalBench CLI (for harness orchestration), Docker, uv, LiteLLM (agent mediation)  
**Storage**: Local filesystem for artifacts and baselines (Git-tracked metadata + TerminalBench registry)  
**Testing**: pytest contract/integration suites + TerminalBench regression runs  
**Target Platform**: Linux containers (TerminalBench runner image) and maintainers’ macOS/Linux dev environments  
**Project Type**: single-project CLI toolkit with separate tools module  
**Performance Goals**: Scenario runtime ≤ baseline +15%; peak memory ≤ baseline +20%; alerts within 1 business day; all 100 `terminal-bench-core` tasks initiate the Spec Kit workflow in under 5 seconds setup time  
**Constraints**: Runs only on approved Docker image + dataset version; triage gating before release acceptance  
**Scale/Scope**: Initial coverage: 3 high-frequency CLI commands; expandable to additional templates/scripts as features grow

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 1 (existing CLI + tests)
- Using framework directly? yes (Typer CLI, no additional wrappers)
- Single data model? yes (benchmark metadata layer only)
- Avoiding patterns? yes (no new abstraction layers introduced)

**Architecture**:
- EVERY feature as library? Spec Kit CLI remains primary library for end users; benchmarking orchestration and the orchestrator agent will live under `src/tools/benchmarks` as standalone tooling separated from the user-facing CLI
- Libraries listed: `specify_cli` (CLI + orchestration), prospective `benchmarking` helper module for TerminalBench integration
- CLI per library: new module `tools.benchmarks` executed via `python -m tools.benchmarks` by maintainers and automation, plus orchestrator agent exported for the TerminalBench harness
- Library docs: quickstart + contracts planned in Phase 1 outputs

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN cycle plan: contract tests for CLI interface fail first, then harness integration tests, followed by regression validation via TerminalBench
- Commit sequencing: tests before implementation (enforced in tasks.md later)
- Order: Contract → Integration → Bench regression (documented in Phase 2 strategy)
- Real dependencies: yes (TerminalBench CLI + Docker) in integration stage
- Integration tests scope: new CLI entry points, orchestrator agent behavior across sample `terminal-bench-core` tasks, baseline management workflows
- FORBIDDEN actions acknowledged: no implementation before tests, no mock-only flows

**Observability**:
- Structured logging plan: reuse Rich logging with JSON export for machine-readable artifacts, exposed only through tools module/orchestrator and automation
- Error context: TerminalBench artifacts (run metadata, logs) linked in run summaries

**Versioning**:
- Benchmark artifacts versioned via baseline records (semantic date-based ID + dataset version)
- BUILD increments tracked through release process; regression failure blocks release until resolved
- Breaking changes: update contracts + quickstart; require new baseline approval before merge; regenerate orchestrator golden transcripts when dataset updates

## Project Structure

### Documentation (this feature)
```
specs/001-add-terminalbench-benchmark/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── tools-benchmarks-cli.md
└── tasks.md          # RESERVED for /tasks command
```

### Source Code (repository root)
```
src/
├── specify_cli/
│   └── __init__.py
├── tools/
│   ├── __init__.py
│   └── benchmarks/
│       ├── __init__.py
│       ├── __main__.py             # Enables `python -m tools.benchmarks`
│       ├── cli.py                  # Typer app exposing benchmarking commands
│       ├── orchestrator_agent.py   # Custom agent enforcing Spec Kit workflow
│       ├── scenarios.py
│       ├── baselines.py
│       ├── runner.py
│       └── reporting.py
├── tools_cli.py                    # Optional dispatcher for future tools
└── tests/
    ├── contract/
    │   ├── test_tools_benchmarks_run.py
    │   ├── test_tools_benchmarks_report.py
    │   └── test_tools_benchmarks_baseline.py
    ├── integration/
    │   └── test_terminalbench_runs.py
    ├── integration_agents/
    │   └── test_orchestrator_agent.py
    └── regression/
        └── fixtures/               # captures baseline metadata + sample artifacts
```

**Structure Decision**: Option 1 (single project) retained. No web/mobile split required.

## Phase 0: Outline & Research
1. Unknowns addressed:
   - TerminalBench harness invocation and required tooling
   - Dataset registry workflow and baseline promotion policy
   - Mapping Spec Kit CLI workflows to TerminalBench scenarios
   - Governance cadence for maintainers & alert routing
2. Research tasks executed:
   - "Research TerminalBench CLI usage and artifact schema for Spec Kit benchmarks"
   - "Document baseline promotion requirements for new scenarios"
   - "Map Spec Kit command flows to measurable benchmarks"
   - "Define incident workflow for regressions in Spec Kit"
3. Findings recorded in `research.md` (decisions, rationales, alternatives)

**Output**: `research.md` populated; no remaining unknowns.

## Phase 1: Design & Contracts
1. Entities extracted → `data-model.md`: Benchmark Scenario, Benchmark Run, Baseline Record with fields, relationships, state transitions.
2. Contracts generated under `contracts/tools-benchmarks-cli.md`: defines CLI command surface (`python -m tools.benchmarks run`, `python -m tools.benchmarks baseline approve`, `python -m tools.benchmarks report`) with inputs/outputs and failure modes exposed only to maintainers, plus agent contract notes for orchestrator integration.
3. Contract tests planned: `tests/contract/test_tools_benchmarks_run.py`, `tests/contract/test_tools_benchmarks_report.py`, and `tests/contract/test_tools_benchmarks_baseline.py` to assert CLI parameters/JSON output, plus `tests/integration_agents/test_orchestrator_agent.py` to verify every task injects the Spec Kit workflow before calling downstream agents (tests to be authored during implementation).
4. Integration test scenarios captured in quickstart + plan (e.g., full benchmark run, regression detection, baseline promotion).
5. Agent context updates deferred until implementation; plan notes new technologies (TerminalBench CLI) for future injection.

**Output**: `data-model.md`, `contracts/tools-benchmarks-cli.md`, `quickstart.md` drafted.

## Phase 2: Task Planning Approach
**Task Generation Strategy**:
- Use `/templates/tasks-template.md` to produce ~25 tasks when /tasks runs.
- Derive tasks from contracts (CLI commands), data model elements (scenario/baseline persistence), and quickstart flows (happy path, regression handling).
- Ensure each contract gains a failing test task before implementation tasks, that the tools module remains inaccessible from the end-user command set, and that the orchestrator agent shims are exercised before implementation.

**Ordering Strategy**:
1. Author contract tests for tooling CLI commands (`test_tools_benchmarks_run.py`, `test_tools_benchmarks_report.py`, `test_tools_benchmarks_baseline.py`).
2. Implement CLI stubs returning TODO responses and orchestrator agent skeleton enforcing the workflow.
3. Create data model persistence helpers (baseline records, run registry).
4. Wire TerminalBench runner integration with Docker + CLI invocation, registering the orchestrator agent for `terminal-bench-core` runs.
5. Add integration tests executing dry-run with fixture artifacts.
6. Document quickstart validation and update incident channel hooks.

**Estimated Output**: 24-30 tasks, flagged `[P]` where parallelizable (e.g., scenario docs vs. alert wiring).

## Phase 3+: Future Implementation
- Phase 3: /tasks command will generate tasks.md using strategy above.
- Phase 4: Execute tasks, ensuring RED-GREEN discipline and capturing baselines.
- Phase 5: Validate via pytest suite + TerminalBench run + quickstart walkthrough.

## Complexity Tracking
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *(none)* | | |

## Progress Tracking

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none required)

---
*Based on Constitution template (constraints pending formalization)*
