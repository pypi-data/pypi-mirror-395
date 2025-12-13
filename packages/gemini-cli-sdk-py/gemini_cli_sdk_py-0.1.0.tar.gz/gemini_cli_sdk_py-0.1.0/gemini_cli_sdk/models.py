from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Mapping, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class CommandResult(BaseModel):
    """Raw process output."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    argv: List[str]
    exit_code: int
    stdout: str
    stderr: str


class ApiStats(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    totalRequests: Optional[int] = None
    totalErrors: Optional[int] = None
    totalLatencyMs: Optional[int] = None


class TokenStats(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    prompt: Optional[int] = None
    candidates: Optional[int] = None
    total: Optional[int] = None
    cached: Optional[int] = None
    thoughts: Optional[int] = None
    tool: Optional[int] = None


class ModelStats(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    api: Optional[ApiStats] = None
    tokens: Optional[TokenStats] = None


class ToolDecisionStats(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    accept: Optional[int] = None
    reject: Optional[int] = None
    modify: Optional[int] = None
    auto_accept: Optional[int] = Field(default=None, alias="auto_accept")


class ToolStats(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    count: Optional[int] = None
    success: Optional[int] = None
    fail: Optional[int] = None
    durationMs: Optional[int] = None
    decisions: Optional[ToolDecisionStats] = None


class FilesStats(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    totalLinesAdded: Optional[int] = None
    totalLinesRemoved: Optional[int] = None


class HeadlessStats(BaseModel):
    """`stats` object returned in JSON output format."""

    model_config = ConfigDict(extra="allow", frozen=True)

    models: Dict[str, ModelStats] = Field(default_factory=dict)
    tools: Optional[Dict[str, ToolStats]] = None
    files: Optional[FilesStats] = None


class HeadlessResponse(BaseModel):
    """Structured JSON output for `--output-format json`. citeturn23view4turn24view3turn24view4"""

    model_config = ConfigDict(extra="allow", frozen=True)

    response: str
    stats: HeadlessStats


#
# Streaming JSON (JSONL) events: `--output-format stream-json`
# citeturn25view1turn25view2
#
class StreamInitEvent(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    type: Literal["init"]
    session_id: Optional[str] = None
    model: Optional[str] = None
    timestamp: Optional[datetime] = None


class StreamMessageEvent(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    type: Literal["message"]
    role: Optional[Literal["user", "assistant", "system"]] = None
    content: Optional[str] = None
    delta: Optional[bool] = None
    timestamp: Optional[datetime] = None


class StreamToolUseEvent(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    type: Literal["tool_use"]
    tool_id: Optional[str] = None
    name: Optional[str] = None
    parameters: Optional[Mapping[str, Any]] = None
    timestamp: Optional[datetime] = None


class StreamToolResultEvent(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    type: Literal["tool_result"]
    tool_id: Optional[str] = None
    status: Optional[str] = None
    output: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: Optional[datetime] = None


class StreamErrorEvent(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    type: Literal["error"]
    message: Optional[str] = None
    code: Optional[str] = None
    timestamp: Optional[datetime] = None


class StreamResultStats(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    total_tokens: Optional[int] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    duration_ms: Optional[int] = None
    tool_calls: Optional[int] = None


class StreamResultEvent(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    type: Literal["result"]
    status: Optional[str] = None
    stats: Optional[StreamResultStats] = None
    timestamp: Optional[datetime] = None


StreamEvent = Union[
    StreamInitEvent,
    StreamMessageEvent,
    StreamToolUseEvent,
    StreamToolResultEvent,
    StreamErrorEvent,
    StreamResultEvent,
]

_stream_event_adapter: TypeAdapter[StreamEvent] = TypeAdapter(StreamEvent)


def parse_stream_event(obj: Mapping[str, Any]) -> StreamEvent:
    return _stream_event_adapter.validate_python(obj)


def parse_stream_event_json(line: str) -> StreamEvent:
    import json

    return parse_stream_event(json.loads(line))
