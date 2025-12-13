from __future__ import annotations

from enum import Enum


class OutputFormat(str, Enum):
    """Gemini CLI output formats for non-interactive mode.

    Docs: `--output-format` supports `text`, `json`, and `stream-json`. The streaming
    variant emits JSONL events (one JSON object per line).  citeturn23view2turn25view1
    """

    TEXT = "text"
    JSON = "json"
    STREAM_JSON = "stream-json"


class ApprovalMode(str, Enum):
    """Approval mode for tool execution.

    CLI help shows: default, auto_edit, yolo. citeturn17view0
    """

    DEFAULT = "default"
    AUTO_EDIT = "auto_edit"
    YOLO = "yolo"


class TelemetryTarget(str, Enum):
    LOCAL = "local"
    GCP = "gcp"


class TelemetryOtlpProtocol(str, Enum):
    GRPC = "grpc"
    HTTP = "http"


class McpTransport(str, Enum):
    """Transport types used by `gemini mcp add --transport ...`."""

    STDIO = "stdio"
    HTTP = "http"
    SSE = "sse"
