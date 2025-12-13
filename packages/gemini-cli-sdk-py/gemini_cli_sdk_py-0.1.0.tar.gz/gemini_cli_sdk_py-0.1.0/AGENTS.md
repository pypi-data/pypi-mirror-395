# AGENTS.md

This file provides practical integration guidance for AI agents that want to drive Gemini CLI programmatically via this Python SDK.

## Mental model

- `gemini-cli-sdk` is a subprocess wrapper.
- Any capability supported by the installed `gemini` binary can be invoked.
- Prefer `--output-format json` for deterministic automation.
- Prefer `--output-format stream-json` for long-running workflows where you need live tool-call visibility.

Relevant upstream docs:
- Headless mode: https://geminicli.com/docs/cli/headless/
- Configuration: https://geminicli.com/docs/get-started/configuration/
- Sessions (`--resume`): https://geminicli.com/docs/cli/session-management/
- MCP servers: https://geminicli.com/docs/tools/mcp-server/

## Recommended patterns

### 1) Robust automation (non-streaming)

Use JSON output and validate via Pydantic.

```python
from gemini_cli_sdk import GeminiCLI

cli = GeminiCLI()
resp = cli.prompt_json("Generate a changelog entry for these commits: ...")
assert resp.response
```

### 2) Event-driven automation (streaming)

Stream JSONL and react to tool calls and tool results.

```python
from gemini_cli_sdk import GeminiCLI

cli = GeminiCLI()
for ev in cli.prompt_stream_json("Run tests, fix failures, and summarize."):
    if ev.type == "tool_use":
        # observe tool args
        ...
    elif ev.type == "tool_result":
        # observe success/failure
        ...
    elif ev.type == "error":
        # non-fatal warnings
        ...
    elif ev.type == "result":
        # final status/stats
        ...
```

### 3) Escape hatch for new CLI features

When upstream adds a new flag/subcommand, use `run()` immediately:

```python
from gemini_cli_sdk import GeminiCLI

cli = GeminiCLI()
res = cli.run(["--some-new-flag", "value", "mcp", "list"])
print(res.stdout)
```

## Notes on sessions

- Gemini CLI automatically saves sessions to a user directory; session continuation is enabled via `--resume`. See upstream session docs for details and paths.

## Notes on MCP

- Use `gemini mcp add|list|remove` via `GeminiCLI.mcp_*`.
- Configure server definitions in `.gemini/settings.json` under `mcpServers` as needed.
