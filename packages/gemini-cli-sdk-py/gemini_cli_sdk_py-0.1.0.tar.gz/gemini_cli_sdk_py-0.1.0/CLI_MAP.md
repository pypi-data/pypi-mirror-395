# CLI_MAP.md

This document summarizes *documented* Gemini CLI entrypoints that this SDK wraps directly, and how to discover the full set of commands/options from the installed CLI.

## Discover everything from your installed CLI

Because Gemini CLI changes quickly, the SDK includes a `--help` parser:

```python
from gemini_cli_sdk import GeminiCLI

spec = GeminiCLI().help_spec()
print(spec.commands)
print(spec.options)
```

This gives you a structured list of commands + options for the *exact* CLI version on your machine.

## Headless (non-interactive) mode

Docs: https://geminicli.com/docs/cli/headless/

- Prompt:
  - `gemini -p "..."` / `gemini --prompt "..."` (direct prompt)
  - `echo "..." | gemini` (stdin as prompt)
  - `cat file | gemini --prompt "..."` (combine stdin + prompt)

- Output:
  - `--output-format text` (default)
  - `--output-format json` (single JSON)
  - `--output-format stream-json` (newline-delimited JSONL events)

### JSON schema (high-level)

The JSON format includes:
- `response` (string)
- `stats.models[model-name].api` and `.tokens`
- optional `stats.tools[...]` and `stats.files[...]`

### Streaming JSONL event types

Docs list 6 event types:
- `init`
- `message`
- `tool_use`
- `tool_result`
- `error`
- `result`

## Session management

Docs: https://geminicli.com/docs/cli/session-management/

- `--resume` / `-r`:
  - `gemini --resume` (resume latest)
  - `gemini --resume 1` (resume by index)
  - `gemini --resume <uuid>` (resume by session id)

## MCP servers

Docs: https://geminicli.com/docs/tools/mcp-server/

- Add:
  - `gemini mcp add --transport sse <name> <url>`
- List:
  - `gemini mcp list`
- Remove:
  - `gemini mcp remove <name> [-s|--scope user|project]`

## Extensions

Docs: https://geminicli.com/docs/extensions/getting-started-extensions/

- Development link:
  - `gemini extensions link .`
