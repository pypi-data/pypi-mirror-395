from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Union

from .enums import OutputFormat, McpTransport
from .errors import GeminiCLIError
from .mcp import McpAddRequest, McpListEntry, McpScope, parse_mcp_list
from .models import CommandResult, HeadlessResponse, StreamEvent, parse_stream_event_json
from .options import RunOptions
from .spec import GeminiHelpSpec, parse_help_text


PathLike = Union[str, os.PathLike[str]]


class GeminiCLI:
    """Python wrapper around the `gemini` CLI binary.

    This SDK executes the installed CLI as a subprocess, so you get feature parity with
    whatever version of Gemini CLI is present on the machine.

    Official docs (headless mode, output formats, sessions, MCP): citeturn22view1turn25view1turn25view3turn25view4
    """

    def __init__(
        self,
        *,
        executable: str = "gemini",
        cwd: Optional[PathLike] = None,
        env: Optional[Mapping[str, str]] = None,
        default_options: Optional[RunOptions] = None,
        timeout_s: Optional[float] = None,
    ) -> None:
        self._exe = executable
        self._cwd = str(cwd) if cwd is not None else None
        self._env = dict(env) if env is not None else {}
        self._default_options = default_options or RunOptions()
        self._timeout_s = timeout_s

    @property
    def executable(self) -> str:
        return self._exe

    def with_options(self, options: RunOptions) -> "GeminiCLI":
        return GeminiCLI(
            executable=self._exe,
            cwd=self._cwd,
            env=self._env,
            default_options=self._default_options.merged(options),
            timeout_s=self._timeout_s,
        )

    def _build_env(self, extra_env: Optional[Mapping[str, str]]) -> Dict[str, str]:
        merged = dict(os.environ)
        merged.update(self._env)
        if extra_env:
            merged.update({k: str(v) for k, v in extra_env.items()})
        return merged

    def _run_process(
        self,
        argv: Sequence[str],
        *,
        stdin: Optional[Union[str, bytes]] = None,
        cwd: Optional[PathLike] = None,
        env: Optional[Mapping[str, str]] = None,
        timeout_s: Optional[float] = None,
        check: bool = True,
    ) -> CommandResult:
        proc = subprocess.run(
            list(argv),
            input=stdin,
            capture_output=True,
            text=isinstance(stdin, str) or stdin is None,
            encoding="utf-8",
            errors="replace",
            cwd=str(cwd) if cwd is not None else self._cwd,
            env=self._build_env(env),
            timeout=timeout_s if timeout_s is not None else self._timeout_s,
        )
        result = CommandResult(
            argv=list(argv),
            exit_code=int(proc.returncode),
            stdout=proc.stdout or "",
            stderr=proc.stderr or "",
        )
        if check and result.exit_code != 0:
            raise GeminiCLIError(
                message="Gemini CLI exited non-zero",
                argv=result.argv,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
            )
        return result

    def run(
        self,
        args: Sequence[str],
        *,
        options: Optional[RunOptions] = None,
        stdin: Optional[Union[str, bytes]] = None,
        cwd: Optional[PathLike] = None,
        env: Optional[Mapping[str, str]] = None,
        timeout_s: Optional[float] = None,
        check: bool = True,
    ) -> CommandResult:
        """Run `gemini` with explicit args (escape hatch)."""
        merged = self._default_options.merged(options)
        argv = [self._exe, *merged.to_argv(), *args]
        return self._run_process(
            argv,
            stdin=stdin,
            cwd=cwd,
            env=env,
            timeout_s=timeout_s,
            check=check,
        )

    #
    # Headless prompts
    #
    def prompt_text(
        self,
        prompt: Optional[str] = None,
        *,
        stdin: Optional[Union[str, bytes]] = None,
        options: Optional[RunOptions] = None,
        cwd: Optional[PathLike] = None,
        env: Optional[Mapping[str, str]] = None,
        timeout_s: Optional[float] = None,
        check: bool = True,
    ) -> str:
        """Execute a non-interactive prompt and return stdout as text."""
        opts = (options or RunOptions()).model_copy()
        if prompt is not None:
            # Prefer positional prompt for modern CLI, but `--prompt` is well documented
            # and supports appending to stdin. citeturn24view2
            opts.prompt = prompt
        opts.output_format = OutputFormat.TEXT
        res = self.run([], options=opts, stdin=stdin, cwd=cwd, env=env, timeout_s=timeout_s, check=check)
        return res.stdout

    def prompt_json(
        self,
        prompt: Optional[str] = None,
        *,
        stdin: Optional[Union[str, bytes]] = None,
        options: Optional[RunOptions] = None,
        cwd: Optional[PathLike] = None,
        env: Optional[Mapping[str, str]] = None,
        timeout_s: Optional[float] = None,
        check: bool = True,
    ) -> HeadlessResponse:
        """Execute a non-interactive prompt and parse `--output-format json`."""
        opts = (options or RunOptions()).model_copy()
        if prompt is not None:
            opts.prompt = prompt
        opts.output_format = OutputFormat.JSON
        res = self.run([], options=opts, stdin=stdin, cwd=cwd, env=env, timeout_s=timeout_s, check=check)
        try:
            payload = json.loads(res.stdout)
        except json.JSONDecodeError as e:
            raise GeminiCLIError(
                message=f"Failed to parse JSON output: {e}",
                argv=res.argv,
                exit_code=res.exit_code,
                stdout=res.stdout,
                stderr=res.stderr,
            ) from e
        try:
            return HeadlessResponse.model_validate(payload)
        except Exception as e:  # pydantic validation error
            raise GeminiCLIError(
                message=f"JSON output did not match expected schema: {e}",
                argv=res.argv,
                exit_code=res.exit_code,
                stdout=res.stdout,
                stderr=res.stderr,
            ) from e

    def prompt_stream_json(
        self,
        prompt: Optional[str] = None,
        *,
        stdin: Optional[Union[str, bytes]] = None,
        options: Optional[RunOptions] = None,
        cwd: Optional[PathLike] = None,
        env: Optional[Mapping[str, str]] = None,
        check: bool = True,
    ) -> Iterator[StreamEvent]:
        """Execute `--output-format stream-json` and yield JSONL events.

        Event types are documented as: init, message, tool_use, tool_result, error, result. citeturn25view1
        """
        opts = (options or RunOptions()).model_copy()
        if prompt is not None:
            opts.prompt = prompt
        opts.output_format = OutputFormat.STREAM_JSON

        argv = [self._exe, *self._default_options.merged(opts).to_argv()]
        p = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE if stdin is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(cwd) if cwd is not None else self._cwd,
            env=self._build_env(env),
            text=True if isinstance(stdin, str) or stdin is None else False,
            encoding="utf-8",
            errors="replace",
            bufsize=1,  # line buffered
        )
        try:
            if stdin is not None and p.stdin is not None:
                if isinstance(stdin, bytes):
                    # If binary stdin is provided, feed via .buffer if available.
                    try:
                        p.stdin.buffer.write(stdin)
                        p.stdin.buffer.flush()
                        p.stdin.close()
                    except Exception:
                        # Fallback: decode best-effort
                        p.stdin.write(stdin.decode("utf-8", errors="replace"))
                        p.stdin.close()
                else:
                    p.stdin.write(stdin)
                    p.stdin.close()

            assert p.stdout is not None
            for raw in p.stdout:
                line = raw.strip()
                if not line:
                    continue
                try:
                    yield parse_stream_event_json(line)
                except Exception as e:
                    raise GeminiCLIError(
                        message=f"Failed to parse stream-json event: {e}",
                        argv=argv,
                        exit_code=-1,
                        stdout=line,
                        stderr=None,
                    ) from e

            exit_code = p.wait()
            if check and exit_code != 0:
                stderr = p.stderr.read() if p.stderr else ""
                raise GeminiCLIError(
                    message="Gemini CLI exited non-zero during stream-json",
                    argv=argv,
                    exit_code=int(exit_code),
                    stdout="",
                    stderr=stderr,
                )
        finally:
            try:
                if p.stdout:
                    p.stdout.close()
            except Exception:
                pass
            try:
                if p.stderr:
                    p.stderr.close()
            except Exception:
                pass
            try:
                if p.stdin:
                    p.stdin.close()
            except Exception:
                pass

    #
    # CLI help/spec discovery
    #
    def help_spec(self) -> GeminiHelpSpec:
        """Parse `gemini --help` output into a structured spec."""
        res = self._run_process([self._exe, "--help"], check=True)
        return parse_help_text(res.stdout)

    #
    # MCP management
    #
    def mcp_list(self, *, check: bool = True) -> List[McpListEntry]:
        """List configured MCP servers (`gemini mcp list`). citeturn23view9turn25view4"""
        res = self.run(["mcp", "list"], check=check)
        return parse_mcp_list(res.stdout)

    def mcp_add(self, req: McpAddRequest, *, check: bool = True) -> CommandResult:
        """Add an MCP server (`gemini mcp add ...`)."""
        args: List[str] = ["mcp", "add", "--transport", req.transport.value]
        if req.scope is not None:
            args.extend(["--scope", req.scope.value])

        if req.headers:
            for h in req.headers:
                args.extend(["--header", h])

        args.append(req.name)

        if req.transport in (McpTransport.HTTP, McpTransport.SSE):
            if not req.url:
                raise ValueError("url is required for HTTP/SSE transports")
            args.append(req.url)
        else:
            if not req.command:
                raise ValueError("command is required for stdio transport")
            args.append(req.command)
            if req.args:
                args.extend(req.args)

        return self.run(args, check=check)

    def mcp_remove(self, name: str, *, scope: Optional[McpScope] = None, check: bool = True) -> CommandResult:
        """Remove an MCP server (`gemini mcp remove <name>`). citeturn25view5"""
        args: List[str] = ["mcp", "remove", name]
        if scope is not None:
            args.extend(["--scope", scope.value])
        return self.run(args, check=check)

    #
    # Extensions
    #
    def extensions_link(self, path: PathLike = ".", *, check: bool = True) -> CommandResult:
        """Link a local extension directory (`gemini extensions link .`). citeturn23view11"""
        return self.run(["extensions", "link", str(path)], check=check)

    def extensions(self, args: Sequence[str], *, check: bool = True) -> CommandResult:
        """Escape hatch for `gemini extensions ...` subcommands."""
        return self.run(["extensions", *args], check=check)
