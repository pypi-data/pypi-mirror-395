from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Mapping, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from .enums import OutputFormat


class GeneralCheckpointing(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: Optional[bool] = None


class GeneralSessionRetention(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: Optional[bool] = None
    maxAge: Optional[str] = None
    maxCount: Optional[int] = None
    minRetention: Optional[str] = None


class GeneralSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    previewFeatures: Optional[bool] = None
    preferredEditor: Optional[str] = None
    vimMode: Optional[bool] = None
    disableAutoUpdate: Optional[bool] = None
    disableUpdateNag: Optional[bool] = None
    checkpointing: Optional[GeneralCheckpointing] = None
    enablePromptCompletion: Optional[bool] = None
    retryFetchErrors: Optional[bool] = None
    debugKeystrokeLogging: Optional[bool] = None
    sessionRetention: Optional[GeneralSessionRetention] = None


class OutputSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    # `output.format` values: "text", "json". citeturn22view0
    format: Optional[Literal["text", "json"]] = None


class UiFooterSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    hideCWD: Optional[bool] = None
    hideSandboxStatus: Optional[bool] = None


class UiSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    theme: Optional[str] = None
    customThemes: Optional[Dict[str, Any]] = None
    hideWindowTitle: Optional[bool] = None
    showStatusInTitle: Optional[bool] = None
    hideTips: Optional[bool] = None
    hideBanner: Optional[bool] = None
    hideContextSummary: Optional[bool] = None
    footer: Optional[UiFooterSettings] = None


class PrivacySettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    usageStatisticsEnabled: Optional[bool] = None


class ToolsSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    # Many tool-related settings exist; keep as structured+forward-compatible.
    sandbox: Optional[Union[bool, str]] = None
    allowed: Optional[List[str]] = None
    exclude: Optional[List[str]] = None

    # Custom tool wiring. (Docs describe discovery/call commands but not the schema here.)
    discoveryCommand: Optional[str] = None
    callCommand: Optional[str] = None


class McpSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    # Global MCP behavior knobs; see CLI docs for details.
    enabled: Optional[bool] = None
    allowedServers: Optional[List[str]] = None
    blockedServers: Optional[List[str]] = None


class SecurityFolderTrustSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: Optional[bool] = None


class SecurityAuthSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    selectedType: Optional[str] = None
    enforcedType: Optional[str] = None


class SecuritySettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    disableYoloMode: Optional[bool] = None
    blockGitExtensions: Optional[bool] = None
    folderTrust: Optional[SecurityFolderTrustSettings] = None
    auth: Optional[SecurityAuthSettings] = None


class AdvancedSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    bugCommand: Optional[str] = None


class McpServerConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    # Stdio servers commonly use command+args. citeturn24view7
    command: Optional[str] = None
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    cwd: Optional[str] = None

    # HTTP/SSE servers may use URL-style config; allow.
    url: Optional[str] = None
    headers: Optional[List[str]] = None


class GeminiSettings(BaseModel):
    """Pydantic model for `.gemini/settings.json` (v2 format).

    The config docs state settings are organized into top-level category objects. citeturn22view0
    """

    model_config = ConfigDict(extra="allow")

    general: Optional[GeneralSettings] = None
    output: Optional[OutputSettings] = None
    ui: Optional[UiSettings] = None
    privacy: Optional[PrivacySettings] = None
    tools: Optional[ToolsSettings] = None
    mcp: Optional[McpSettings] = None
    security: Optional[SecuritySettings] = None
    advanced: Optional[AdvancedSettings] = None

    # Top-level `mcpServers` mapping. citeturn23view10turn24view7
    mcpServers: Optional[Dict[str, McpServerConfig]] = Field(default=None)

    @classmethod
    def load(cls, path: Path) -> "GeminiSettings":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.model_validate(data)

    def dump(self, path: Path, *, indent: int = 2) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.model_dump_json(indent=indent, exclude_none=True), encoding="utf-8")
