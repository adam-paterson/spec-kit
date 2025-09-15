# Contract: Spec Kit Tools: Benchmarks CLI

## Command: `python -m tools.benchmarks run`
- **Purpose**: Execute the TerminalBench suite for selected scenarios.
- **Inputs**:
  - `--scenarios` (comma-separated identifiers; REQUIRED)
  - `--dataset` (string; REQUIRED, matches TerminalBench registry version; default `terminal-bench-core`)
  - `--output` (path; optional; default: `.terminalbench/latest`)
  - `--format` (enum: `table`, `json`; optional; default: `table`)
  - `--agent` (string; optional; default: `spec-kit-orchestrator`, wraps downstream agent)
  - `--model` (string; optional when `--agent` handles provider configuration)
  - `--no-incident` (flag to suppress automated incident creation; restricted to maintainers during dry runs)
- **Preconditions**:
  - Docker daemon reachable
  - TerminalBench runner image and dataset installed
  - Repository clean or explicitly acknowledged via `--allow-dirty`
- **Outputs**:
  - Exit code `0` on success, `1` on regression detected, `2` on blocked/parity failure
  - stdout: human-readable summary or JSON (if `--format json`)
  - stderr: structured error messages for parity failures or harness errors
  - Artifacts saved to output directory (`run_metadata.json`, `agent.cast`, `post-test.txt`, `summary.json`)

## Command: `python -m tools.benchmarks report`
- **Purpose**: Summarize latest or specified benchmark run(s).
- **Inputs**:
  - `--run` (string; optional; defaults to latest)
  - `--dataset` (string; optional; default `terminal-bench-core`)
  - `--format` (`table`, `json`; default `table`)
  - `--deltas` (flag; include baseline comparison detail)
- **Outputs**:
  - Exit code `0` when report generated, `3` when run not found
  - stdout: summary (table or JSON) including scenario metrics, baseline deltas, status
  - stderr: validation errors (missing artifacts, corrupted JSON)

## Command: `python -m tools.benchmarks baseline approve`
- **Purpose**: Promote a provisional run to active baseline.
- **Inputs**:
  - `--scenario` (string; REQUIRED)
  - `--run` (string; REQUIRED)
  - `--notes` (string; optional, appended to baseline record)
  - `--dataset` (string; optional; default `terminal-bench-core`)
- **Preconditions**:
  - Selected run status is `provisional` or `pass`
  - Three consecutive passing runs recorded for scenario in same environment
  - User belongs to Benchmark Maintainers guild (enforced by config)
- **Outputs**:
  - Exit code `0` on success, `4` on validation failure (insufficient runs, mismatched environment)
  - Updates baseline record file and writes audit entry including approver and timestamp
  - stdout: confirmation with updated baseline ID

## Failure Modes
- **Environment Drift**: `python -m tools.benchmarks run` exits with code `2`, reports mismatched Docker digest/dataset version, and writes diff summary to stderr + artifact bundle.
- **Functional Failure**: Run exits with code `1`, triggers triage ticket creation with logs attached.
- **Artifact Corruption**: `report` command exits `3`, instructs user to regenerate run.
- **Authorization Failure**: `baseline approve` exits `4`, indicates missing maintainer role or insufficient passing runs.

## JSON Schema (Report Output)
```json
{
  "run_id": "uuid",
  "generated_at": "ISO-8601",
  "scenarios": [
    {
      "scenario_id": "specify",
      "status": "pass|regression|blocked|provisional",
      "runtime_ms": 12345,
      "runtime_delta_percent": 5.4,
      "peak_memory_mb": 512,
      "memory_delta_percent": -2.1,
      "baseline_id": "specify-2025-09-01",
      "artifacts": {
        "run_metadata": "path",
        "agent_cast": "path",
        "post_test": "path"
      },
      "notes": "string"
    }
  ],
  "summary": {
    "regressions": 0,
    "blocked": 0,
    "provisional": 1
  }
}
```


## Agent Integration
- Default agent `spec-kit-orchestrator` subclasses TerminalBench `BaseAgent` and enforces `/specify → /plan → /tasks → execute tasks` before invoking downstream models.
- `--agent` may point to alternative orchestrators; when omitted, the default agent wraps LiteLLM model names supplied via `--model`.
