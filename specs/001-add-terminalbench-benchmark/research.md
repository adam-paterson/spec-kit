# Phase 0 Research: TerminalBench Benchmark Suite

## Decision Log

### TerminalBench Harness Integration
- **Decision**: Use the official TerminalBench CLI inside the published runner Docker image to ensure parity with registry scenarios.
- **Rationale**: Harness enforces artifact schema (`run_metadata.json`, `agent.cast`, `post-test.txt`) and environment controls, aligning with spec requirements for parity and reproducibility.
- **Alternatives Considered**: Running benchmarks via ad-hoc pytest timers (rejected: lacks artifact parity, harder to compare baselines) and custom shell scripts (rejected: duplicates TerminalBench functionality, higher maintenance).

### Scenario Mapping to Spec Kit Commands
- **Decision**: Model three primary scenarios—`/specify`, `/plan`, `/tasks`—with explicit capture of generated markdown artifacts and branch state while routing execution through `tools/benchmarks` standalone tooling.
- **Rationale**: These workflows mirror how users create specs, plans, and tasks; TerminalBench scenarios must validate the CLI guarantees referenced in the feature spec.
- **Alternatives Considered**: Aggregated “end-to-end” mega-scenario (rejected: harder to attribute regressions) and minimal smoke tests (rejected: would not satisfy regression detection requirement).

### Baseline Promotion Policy
- **Decision**: Require three consecutive passing runs on the approved image/dataset before publishing or updating a baseline record.
- **Rationale**: Matches TerminalBench registry guidance for promoting provisional scenarios and reduces noise from transient variation.
- **Alternatives Considered**: Single-run baseline approval (rejected: fragile) and time-based approval (rejected: ignores run quality).

### Alerting and Governance
- **Decision**: Route regression notifications to the Benchmark Maintainers guild via the incident channel with 1 business day SLA, plus create automated triage tickets for functional failures; all automation is triggered via the `python -m tools.benchmarks` entry point, which wraps a custom orchestrator agent for `terminal-bench-core`.
- **Rationale**: Aligns with spec requirement for prompt responses and ensures functional issues are separated from performance regressions.
- **Alternatives Considered**: Manual email notifications (rejected: low reliability) and ad-hoc messaging (rejected: hard to audit).

### Artifact Storage Strategy
- **Decision**: Store baseline records and run summaries in Git-tracked YAML/JSON under `specs/benchmarks/` plus attach raw TerminalBench artifacts in artifact storage (e.g., release assets), with the tooling commands and orchestrator agent under `tools/benchmarks` handling synchronization.
- **Rationale**: Keeps baselines reviewable and versioned while avoiding repository bloat from large binary artifacts.
- **Alternatives Considered**: Commit full artifacts to repo (rejected: size/performance) and rely solely on TerminalBench cloud storage (rejected: reduces local auditability).

## Outstanding Questions
- None. All NEEDS CLARIFICATION items from the spec have been resolved in decisions above.

## References Consulted
- TerminalBench Harness Guide (CLI usage, artifact contract)
- TerminalBench Dataset Registry Notes (baseline promotion, release cadence)
- Spec Kit README (CLI workflow guarantees)


### Orchestrator Agent
- **Decision**: Build a `SpecKitBenchAgent` (subclasses TerminalBench `BaseAgent`) that runs `/specify`, `/plan`, `/tasks`, then executes the generated tasks before delegating to Claude Code, Codex, etc.
- **Rationale**: Guarantees every `terminal-bench-core` task evaluates the Spec Kit workflow uniformly across agents.
- **Alternatives Considered**: Prompt-only guidance via Terminus (rejected: inconsistent compliance), dataset fork (rejected: would no longer represent the core benchmark).
