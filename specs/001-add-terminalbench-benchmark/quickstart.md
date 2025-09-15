# Quickstart: Running TerminalBench for Spec Kit

## Prerequisites
- Docker installed with access to the TerminalBench runner image (`ghcr.io/terminal-bench/runner:<tag>`)
- TerminalBench CLI (`tbench`) installed and authenticated if registry access requires credentials
- `uv` and Python 3.11 available (matches Spec Kit CLI runtime)
- Standalone tooling available via `python -m tools.benchmarks` (optionally installed as `spec-tools` via `uv tool`)
- Configure LiteLLM or provider credentials for downstream agents (e.g., Claude Code, Codex).
- Spec Kit repository checked out on branch `001-add-terminalbench-benchmark`

## 1. Prepare Environment
```bash
# Ensure dependencies
uv sync
# Verify TerminalBench CLI
tbench --version
# Pull approved runner image
docker pull ghcr.io/terminal-bench/runner:<approved-tag>
```

## 2. Run Benchmarks
```bash
# Execute TerminalBench suite for Spec Kit
uv run -m tools.benchmarks run --scenarios specify,plan,tasks --dataset terminal-bench-core --agent spec-kit-orchestrator --model <provider/model-id>
```
- Command performs environment parity checks (runner image digest, dataset version, CPU/RAM).
- On success, outputs run summary and paths to generated artifacts (`run_metadata.json`, `agent.cast`, `post-test.txt`).

## 3. Review Results
```bash
# Summarize run delta vs baseline
uv run -m tools.benchmarks report --format table --dataset terminal-bench-core
# View JSON for automation
uv run -m tools.benchmarks report --format json --dataset terminal-bench-core > reports/latest.json
```
- `report` highlights regressions (>15% runtime or >20% memory) and blocked runs.
- If regression detected, an incident ticket is created automatically referencing artifact bundle.

## 4. Promote Baseline (if applicable)
```bash
# After three passing runs on approved environment
tbench baseline approve --scenario specify --run <run-id>
uv run -m tools.benchmarks baseline approve --scenario specify --run <run-id> --dataset terminal-bench-core
```
- Updates baseline record in Git (`specs/benchmarks/<scenario>/baseline.yaml`).
- Requires maintainer rotation sign-off recorded in commit message.

## 5. Clean Up / Next Steps
- Attach artifact bundle to release or CI artifact store.
- Update `specs/benchmarks/` with new baseline metadata and open PR.
- Proceed to `/tasks` workflow to generate implementation tasks if changes are pending.

