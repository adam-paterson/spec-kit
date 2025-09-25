# Benchmarking with Terminal-Bench

Run the full Spec Kit specification → implementation workflow inside the
[Terminal-Bench](https://www.tbench.ai/docs) harness using the `SpecKitOpenCodeAgent`. This
agent packages the Spec Kit prompts, installs the Specify CLI with `uv`, and orchestrates the
entire `/constitution → /specify → /plan → /tasks → /implement` sequence through the
`opencode` CLI so you can measure end-to-end performance on the benchmark task suite.

## Prerequisites

Before launching a run ensure that:

- [Terminal-Bench](https://www.tbench.ai/docs/installation) is installed (`uv tool install terminal-bench`).
- Docker is running (Terminal-Bench executes tasks inside a container sandbox).
- You have credentials for the `opencode/grok-code` model – export `XAI_API_KEY`,
  `OPENCODE_API_KEY`, or any other token your workspace requires.
- Optional: provide additional environment variables if your `opencode` workspace mandates
  them (for example, `GROK_API_KEY`).

## Quick start

Execute a single task with the Spec Kit agent:

```bash
uv tool install terminal-bench

export XAI_API_KEY=sk-...

# Run a single Terminal-Bench task
uv run tb run \
  --agent-import-path specify_cli.terminal_bench:SpecKitOpenCodeAgent \
  --dataset terminal-bench-core==0.1.1 \
  --task-id hello-world
```

> [!TIP]
> The repository's `pyproject.toml` declares the project as a local source for `uv`, so
> `uv run` automatically exposes `specify_cli` on `sys.path`. You don't need manual shims or
> editable installs when launching Terminal-Bench from a checkout.

The harness mounts the Spec Kit repository into the benchmark container, installs the
Specify CLI, provisions the `.specify` and `.opencode` directories, then runs the standard
prompt sequence with the benchmark instruction as input. Each stage feeds the instruction back
into the correct Spec Kit command so you receive the specification, plan, task list, and
implementation artifacts without manual intervention.

## What happens during a run

1. **Environment bootstrap** – installs Node, the `opencode` CLI, `uv`, and the Specify CLI
   using the templated setup script shipped with Spec Kit.
2. **Project provisioning** – executes `specify init --here` with non-interactive flags to
   merge the Spec Kit templates into the benchmark workspace only if they are missing.
3. **Workflow execution** – invokes `opencode -p <prompt> --model opencode/grok-code run "…"`
   so each request loads the matching Spec Kit prompt from `.opencode/commands` before
   sending the benchmark instruction:
   - `constitution` – seeds high-level engineering principles tailored for benchmark runs.
   - `specify` – captures the benchmark instruction as a formal specification.
   - `plan` – creates a detailed implementation plan (explicitly allowed to proceed even
     when no clarifications are recorded yet).
   - `tasks` – breaks the plan into an ordered task list.
   - `implement` – performs the implementation, referencing the generated artifacts.
4. **Optional extras** – you can append more prompt invocations (for example `analyze`) using
   the agent kwargs described below.

## Customising the workflow

The agent accepts additional keyword arguments via the standard Terminal-Bench
`--agent-kwarg` flag. Values are parsed with `ast.literal_eval`, letting you provide Python
literals for advanced settings.

| Kwarg | Description |
|-------|-------------|
| `model_name` | Override the default `opencode/grok-code` model. |
| `constitution_template` | Custom text appended to `/constitution`. `{instruction}` expands to the benchmark instruction. |
| `specify_template` | Controls the argument passed to `/specify`. |
| `plan_template` | Adjusts the `/plan` instructions. Include `{instruction}` to reference the task. |
| `tasks_template` | Customises the `/tasks` prompt. |
| `implement_template` | Customises the `/implement` instructions. |
| `extra_prompts` | A list of `(prompt_name, template)` tuples for additional prompt files (e.g. `[('analyze', '{instruction}')]`). |
| `specify_init_command` | Replace the default non-interactive `specify init` invocation. |
| `skip_specify_if_present` | Set to `False` to force re-running `specify init` on every task. |
| `path_prefixes` | Extend the PATH export applied before running commands. |
| `provider_env_overrides` | Map provider names to extra environment variable names, e.g. `{"opencode": ("OPENCODE_WORKSPACE",)}`. |

### Examples

Pass a custom plan emphasis:

```bash
uv run tb run \
  --agent-import-path specify_cli.terminal_bench:SpecKitOpenCodeAgent \
  --task-id hello-world \
  --agent-kwarg plan_template="Highlight performance optimisations for {instruction}"
```

Add the `/analyze` command before implementation:

```bash
uv run tb run \
  --agent-import-path specify_cli.terminal_bench:SpecKitOpenCodeAgent \
  --task-id hello-world \
  --agent-kwarg extra_prompts="[('analyze', '{instruction}')]"
```

Provide additional credentials for a custom opencode workspace:

```bash
uv run tb run \
  --agent-import-path specify_cli.terminal_bench:SpecKitOpenCodeAgent \
  --task-id hello-world \
  --agent-kwarg provider_env_overrides="{'opencode': ('OPENCODE_API_KEY', 'MY_WORKSPACE_TOKEN')}"
```

## Roadmap

The OpenCode override is the first in a series of Spec Kit benchmarking agents. The same
workflow scaffold can be extended to support Claude Code, Codex, and other CLIs by building on
`specify_cli.terminal_bench.agents`. Contributions and feedback are welcome!
