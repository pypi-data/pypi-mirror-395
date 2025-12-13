from gemini_cli_sdk import parse_help_text


SAMPLE_HELP = """Usage: gemini [options] [command]

Gemini CLI - An interactive CLI for Gemini.

Commands:
  gemini [promptWords...]  Launch Gemini CLI [default]
  gemini mcp               Manage MCP servers
  gemini extensions        Manage Gemini CLI extensions.

Options:
  -m, --model              Model [string]
  -p, --prompt             Prompt. Appended to input on stdin (if any).
                           [deprecated: use positional prompt argument] [string]
  --output-format <format> Output format (text, json, stream-json). [string]
  -r, --resume             Resume latest session or by index/id. [string]
  -h, --help               Show help [boolean]
"""


def test_parse_help_text() -> None:
    spec = parse_help_text(SAMPLE_HELP)
    assert spec.usage and spec.usage.startswith("Usage:")
    assert any(c.name.startswith("gemini mcp") for c in spec.commands)
    opt = next(o for o in spec.options if "--prompt" in o.flags)
    assert opt.deprecated is True
