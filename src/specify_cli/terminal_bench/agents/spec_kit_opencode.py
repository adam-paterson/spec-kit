"""Custom Terminal-Bench agent that executes the Spec Kit workflow with OpenCode."""

from __future__ import annotations

import os
import shlex
from collections.abc import Mapping, Sequence
from typing import Final

from terminal_bench.agents.installed_agents.opencode.opencode_agent import (
    OpenCodeAgent,
)
from terminal_bench.terminal.models import TerminalCommand


class SpecKitOpenCodeAgent(OpenCodeAgent):
    """Run the Spec Kit prompt workflow inside Terminal-Bench using OpenCode."""

    DEFAULT_MODEL_NAME: Final[str] = "opencode/grok-code"
    DEFAULT_PATH_PREFIXES: Final[tuple[str, ...]] = (
        "$HOME/.local/bin",
        "$HOME/.local/share/uv/tools/bin",
    )
    DEFAULT_SPECIFY_INIT_COMMAND: Final[str] = (
        "specify init --here --ai opencode --script sh "
        "--ignore-agent-tools --no-git --force"
    )
    DEFAULT_CONSTITUTION_TEMPLATE: Final[str] = (
        "Establish a concise engineering constitution for this benchmark environment. "
        "Emphasize maintainability, incremental delivery, automated testing, "
        "and respecting the Terminal-Bench workspace."
    )
    DEFAULT_SPECIFY_TEMPLATE: Final[str] = "{instruction}"
    DEFAULT_PLAN_TEMPLATE: Final[str] = (
        "You have explicit approval to proceed even if clarifications are missing. "
        "Create a pragmatic implementation plan that references the generated "
        "specification and constitution. Focus on satisfying this benchmark task:\n\n"
        "{instruction}"
    )
    DEFAULT_TASKS_TEMPLATE: Final[str] = (
        "Translate the implementation plan into concrete, sequential tasks with "
        "clear acceptance criteria. Maintain alignment with the specification for:\n\n"
        "{instruction}"
    )
    DEFAULT_IMPLEMENT_TEMPLATE: Final[str] = (
        "Execute every task and update the repository to fulfil the specification "
        "derived from:\n\n{instruction}\n\nRun available tests or linters before "
        "finishing and summarise the outcome."
    )
    DEFAULT_PROVIDER_ENV: Final[dict[str, tuple[str, ...]]] = {
        "opencode": ("OPENCODE_API_KEY", "XAI_API_KEY", "GROK_API_KEY"),
    }

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        *,
        constitution_template: str | None = None,
        specify_template: str | None = None,
        plan_template: str | None = None,
        tasks_template: str | None = None,
        implement_template: str | None = None,
        extra_prompts: Sequence[tuple[str, str]] | None = None,
        specify_init_command: str | None = None,
        skip_specify_if_present: bool = True,
        path_prefixes: Sequence[str] | None = None,
        provider_env_overrides: Mapping[str, Sequence[str]] | None = None,
        **kwargs,
    ) -> None:
        self._constitution_template = (
            constitution_template
            if constitution_template is not None
            else self.DEFAULT_CONSTITUTION_TEMPLATE
        )
        self._specify_template = (
            specify_template if specify_template is not None else self.DEFAULT_SPECIFY_TEMPLATE
        )
        self._plan_template = (
            plan_template if plan_template is not None else self.DEFAULT_PLAN_TEMPLATE
        )
        self._tasks_template = (
            tasks_template if tasks_template is not None else self.DEFAULT_TASKS_TEMPLATE
        )
        self._implement_template = (
            implement_template
            if implement_template is not None
            else self.DEFAULT_IMPLEMENT_TEMPLATE
        )
        self._extra_prompts = list(extra_prompts or [])
        self._specify_init_command = (
            specify_init_command
            if specify_init_command is not None
            else self.DEFAULT_SPECIFY_INIT_COMMAND
        )
        self._skip_specify_if_present = skip_specify_if_present
        self._path_prefixes = tuple(path_prefixes or self.DEFAULT_PATH_PREFIXES)
        self._provider_env_overrides = {
            **self.DEFAULT_PROVIDER_ENV,
            **{k: tuple(v) for k, v in (provider_env_overrides or {}).items()},
        }

        workflow_steps: list[tuple[str, str | None]] = [
            ("constitution", self._constitution_template),
            ("specify", self._specify_template),
            ("plan", self._plan_template),
            ("tasks", self._tasks_template),
            ("implement", self._implement_template),
        ]
        workflow_steps.extend(self._extra_prompts)
        self._workflow_steps = workflow_steps

        super().__init__(model_name=model_name, **kwargs)

    @staticmethod
    def name() -> str:
        return "spec-kit-opencode"

    @property
    def _env(self) -> dict[str, str]:  # type: ignore[override]
        if self._provider == "opencode":
            env: dict[str, str] = {}
            for key in self._provider_env_overrides.get("opencode", ()):  # pragma: no branch
                if key in os.environ:
                    env[key] = os.environ[key]
            if not env:
                self._logger.warning(
                    "No credentials detected for provider 'opencode'. "
                    "Ensure the opencode CLI is authenticated before running tasks."
                )
            return env
        return super()._env

    @property
    def _install_agent_script_path(self):  # type: ignore[override]
        return self._get_templated_script_path("spec-kit-opencode-setup.sh.j2")

    def _run_agent_commands(self, instruction: str) -> list[TerminalCommand]:  # type: ignore[override]
        sanitized_instruction = instruction.strip()
        instruction_for_format = self._escape_for_format(sanitized_instruction)

        commands: list[TerminalCommand] = []

        if self._path_prefixes:
            export_command = self._render_path_export()
            commands.append(self._shell_command(export_command))

        init_command = self._render_specify_init_command()
        if init_command:
            commands.append(self._shell_command(init_command))

        for prompt_name, template in self._workflow_steps:
            if template is None:
                continue
            prompt_body = template.format(
                instruction=instruction_for_format
            ).strip()
            if not prompt_body:
                continue
            commands.append(
                self._opencode_command(
                    prompt_body,
                    prompt_name=prompt_name,
                )
            )

        return commands

    def _render_path_export(self) -> str:
        joined_paths = ":".join(self._path_prefixes) + ":$PATH"
        return f"export PATH=\"{joined_paths}\""

    def _render_specify_init_command(self) -> str | None:
        if not self._specify_init_command:
            return None
        if self._skip_specify_if_present:
            return (
                "if [ ! -d .specify ] || [ ! -d .opencode ]; then "
                f"{self._specify_init_command}; fi"
            )
        return self._specify_init_command

    def _opencode_command(
        self,
        prompt: str,
        *,
        prompt_name: str | None = None,
    ) -> TerminalCommand:
        quoted_prompt = shlex.quote(prompt)
        prompt_flag = ""
        if prompt_name:
            prompt_flag = f"-p {shlex.quote(prompt_name)} "
        return TerminalCommand(
            command=(
                f"opencode {prompt_flag}--model {self._model_name} run {quoted_prompt}"
            ),
            min_timeout_sec=0.0,
            max_timeout_sec=float("inf"),
            block=True,
            append_enter=True,
        )

    def _shell_command(self, command: str) -> TerminalCommand:
        return TerminalCommand(
            command=command,
            min_timeout_sec=0.0,
            max_timeout_sec=float("inf"),
            block=True,
            append_enter=True,
        )

    @staticmethod
    def _escape_for_format(value: str) -> str:
        return value.replace("{", "{{").replace("}", "}}")
