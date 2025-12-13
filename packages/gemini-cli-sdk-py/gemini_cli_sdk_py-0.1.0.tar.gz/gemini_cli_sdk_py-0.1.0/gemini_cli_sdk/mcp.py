from __future__ import annotations

import re
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .enums import McpTransport


class McpScope(str, Enum):
    PROJECT = "project"
    USER = "user"


class McpListEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str
    transport: Optional[str] = None
    detail: str
    connected: Optional[bool] = None


_MCP_LIST_RE = re.compile(
    r"^(?P<mark>[✓✗])\s+(?P<name>[^:]+):\s+(?P<detail>.*?)(?:\s+\((?P<transport>[^)]+)\))?\s+-\s+(?P<status>Connected|Disconnected)\s*$"
)


def parse_mcp_list(text: str) -> List[McpListEntry]:
    entries: List[McpListEntry] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = _MCP_LIST_RE.match(line)
        if not m:
            # Keep raw line for troubleshooting; ignore unparseable lines.
            continue
        connected = True if m.group("status") == "Connected" else False
        entries.append(
            McpListEntry(
                name=m.group("name").strip(),
                transport=m.group("transport"),
                detail=m.group("detail").strip(),
                connected=connected,
            )
        )
    return entries


class McpAddRequest(BaseModel):
    """Parameters for `gemini mcp add`.

    Docs show at least SSE transport syntax: `gemini mcp add --transport sse <name> <url>`. citeturn23view9turn25view4
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    transport: McpTransport
    name: str

    # For HTTP/SSE transports.
    url: Optional[str] = None
    headers: Optional[List[str]] = None

    # For stdio transport.
    command: Optional[str] = None
    args: Optional[List[str]] = None

    scope: Optional[McpScope] = None
