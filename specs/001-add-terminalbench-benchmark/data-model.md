# Data Model: TerminalBench Benchmark Suite

## Entities

### BenchmarkScenario
- **Description**: Represents a single CLI workflow benchmarked by TerminalBench.
- **Key Fields**:
  - `scenario_id` (string, e.g., `specify-generate-spec`)
  - `display_name` (string)
  - `command_path` (string, `/specify`, `/plan`, `/tasks` subcommands)
  - `prerequisites` (list of strings, e.g., fixtures, repo state)
  - `success_artifacts` (list, e.g., `spec.md`, `plan.md`, `tasks.md`)
  - `metrics_tracked` (list of metric identifiers: runtime, peak_memory, exit_status)
  - `owner_rotation` (string, guild rotation identifier)
  - `registry_version` (string, TerminalBench dataset reference)
- **Relationships**:
  - Has many `BenchmarkRun`
  - Has one active `BaselineRecord`

### BenchmarkRun
- **Description**: Captures a single execution of a TerminalBench scenario suite.
- **Key Fields**:
  - `run_id` (UUID)
  - `scenario_id` (foreign key → BenchmarkScenario)
  - `executed_at` (timestamp)
  - `runner_image` (string, Docker image digest)
  - `dataset_version` (string)
  - `metrics` (map: `runtime_ms`, `peak_memory_mb`, `success` boolean)
  - `artifacts_path` (URI to stored artifacts, includes `run_metadata.json`, `agent.cast`, `post-test.txt`)
  - `comparison` (struct capturing delta vs baseline: runtime_percent, memory_percent)
  - `status` (enum: `pass`, `regression`, `blocked`, `provisional`)
  - `notes` (text for triage context)
- **Relationships**:
  - Belongs to `BenchmarkScenario`
  - References `BaselineRecord` used for comparison

### BaselineRecord
- **Description**: Stores approved baseline metrics and metadata for a scenario.
- **Key Fields**:
  - `baseline_id` (string combining scenario + version)
  - `scenario_id` (foreign key)
  - `approved_on` (date)
  - `approved_by` (string, maintainer rotation)
  - `runner_image` (string)
  - `dataset_version` (string)
  - `metrics` (map: `runtime_ms`, `peak_memory_mb`, `exit_status`)
  - `artifact_snapshot` (URI to baseline artifact bundle)
  - `status` (enum: `active`, `retired`, `provisional`)
  - `supersedes_baseline_id` (optional string)
- **Relationships**:
  - Belongs to `BenchmarkScenario`
  - Linked from multiple `BenchmarkRun` entries for comparison

## State Transitions

### BenchmarkRun.status
- `provisional` → `pass`: Achieved when run meets thresholds and baseline exists.
- `provisional` → `blocked`: Triggered when environment parity check fails.
- `pass` → `regression`: Triggered when runtime >15% or memory >20% above baseline.
- `regression` → `pass`: After acknowledgement and new baseline approval or fix deployed.

### BaselineRecord.status
- `provisional` → `active`: After three consecutive passing runs on approved environment.
- `active` → `retired`: When superseded by new baseline or scenario decommissioned.
- `retired` → *(no further transitions)*

## Derived Views
- **RunSummaryReport**: Aggregates latest run per scenario, including deltas, status, and alert routing info for stakeholder dashboards.
- **BaselineAuditTrail**: Sequence of baseline records showing changes in metrics, dataset versions, and approvers.

