from __future__ import annotations

from typing import List, Mapping, Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import ApprovalMode, OutputFormat, TelemetryOtlpProtocol, TelemetryTarget


ResumeSpec = Union[bool, int, str]


class RunOptions(BaseModel):
    """Typed representation of commonly used Gemini CLI flags.

    Notes:
      * The CLI evolves quickly; any unsupported flag will be rejected by the installed
        `gemini` binary at runtime. Use `extra_args` as an escape hatch.
      * `--output-format` supports `text`, `json`, and `stream-json`. citeturn23view2turn25view1
      * Session resumption uses `--resume` / `-r`. citeturn25view3
    """

    model_config = ConfigDict(extra="forbid")

    model: Optional[str] = None

    # Non-interactive prompt. If you provide `stdin`, CLI appends this prompt to stdin.
    prompt: Optional[str] = None

    # Starts interactive session with initial prompt.
    prompt_interactive: Optional[str] = None

    # Output format for non-interactive mode.
    output_format: Optional[OutputFormat] = None

    # Tool approval.
    yolo: Optional[bool] = None
    approval_mode: Optional[ApprovalMode] = None

    # Sandbox.
    sandbox: Optional[bool] = None
    sandbox_image: Optional[str] = None

    # Misc.
    debug: Optional[bool] = None
    all_files: Optional[bool] = None
    show_memory_usage: Optional[bool] = None
    screen_reader: Optional[bool] = None

    # Session management.
    resume: Optional[ResumeSpec] = None

    # Telemetry.
    telemetry: Optional[bool] = None
    telemetry_target: Optional[TelemetryTarget] = None
    telemetry_otlp_endpoint: Optional[str] = None
    telemetry_otlp_protocol: Optional[TelemetryOtlpProtocol] = None
    telemetry_log_prompts: Optional[bool] = None
    telemetry_outfile: Optional[str] = None

    # Extensions.
    extensions: Optional[List[str]] = None
    list_extensions: Optional[bool] = None

    # MCP/tool allowlists (CLI-help documented). citeturn17view0
    allowed_mcp_server_names: Optional[List[str]] = None
    allowed_tools: Optional[List[str]] = None

    # Workspace.
    include_directories: Optional[List[str]] = None
    proxy: Optional[str] = None

    # Escape hatch for new/unmodeled flags.
    extra_args: List[str] = Field(default_factory=list)

    @field_validator("resume")
    @classmethod
    def _validate_resume(cls, v: Optional[ResumeSpec]) -> Optional[ResumeSpec]:
        if v is None:
            return None
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            if v < 0:
                raise ValueError("resume index must be >= 0")
            return v
        if isinstance(v, str):
            if not v.strip():
                raise ValueError("resume id must be non-empty")
            return v
        raise TypeError("invalid resume type")

    def to_argv(self) -> List[str]:
        argv: List[str] = []

        def add_flag(flag: str, enabled: Optional[bool]) -> None:
            if enabled is True:
                argv.append(flag)
            elif enabled is False:
                # CLI typically doesn't support explicit false flags; omit.
                return

        def add_kv(flag: str, value: Optional[str]) -> None:
            if value is None:
                return
            argv.extend([flag, value])

        def add_multi(flag: str, values: Optional[Sequence[str]]) -> None:
            if not values:
                return
            for item in values:
                argv.extend([flag, item])

        add_kv("--model", self.model)

        if self.prompt is not None:
            argv.extend(["--prompt", self.prompt])

        if self.prompt_interactive is not None:
            argv.extend(["--prompt-interactive", self.prompt_interactive])

        if self.output_format is not None:
            argv.extend(["--output-format", self.output_format.value])

        add_flag("--yolo", self.yolo)
        add_kv("--approval-mode", self.approval_mode.value if self.approval_mode else None)

        add_flag("--sandbox", self.sandbox)
        add_kv("--sandbox-image", self.sandbox_image)

        add_flag("--debug", self.debug)
        add_flag("--all-files", self.all_files)
        add_flag("--show-memory-usage", self.show_memory_usage)
        add_flag("--screen-reader", self.screen_reader)

        if self.resume is not None:
            if self.resume is True:
                argv.append("--resume")
            elif self.resume is False:
                # Not supported: ignore
                pass
            else:
                argv.extend(["--resume", str(self.resume)])

        add_flag("--telemetry", self.telemetry)
        add_kv("--telemetry-target", self.telemetry_target.value if self.telemetry_target else None)
        add_kv("--telemetry-otlp-endpoint", self.telemetry_otlp_endpoint)
        add_kv("--telemetry-otlp-protocol", self.telemetry_otlp_protocol.value if self.telemetry_otlp_protocol else None)
        add_flag("--telemetry-log-prompts", self.telemetry_log_prompts)
        add_kv("--telemetry-outfile", self.telemetry_outfile)

        add_multi("--extensions", self.extensions)
        add_flag("--list-extensions", self.list_extensions)

        add_multi("--allowed-mcp-server-names", self.allowed_mcp_server_names)
        add_multi("--allowed-tools", self.allowed_tools)

        add_multi("--include-directories", self.include_directories)
        add_kv("--proxy", self.proxy)

        argv.extend(self.extra_args)
        return argv

    def merged(self, other: Optional["RunOptions"]) -> "RunOptions":
        """Return a new instance with values from `other` overriding this instance."""
        if other is None:
            return self
        data = self.model_dump()
        for k, v in other.model_dump(exclude_unset=True).items():
            data[k] = v
        return RunOptions.model_validate(data)
