from __future__ import annotations

import subprocess
from typing import Any, Optional

import pytest

from gemini_cli_sdk import GeminiCLI, OutputFormat, RunOptions


class _FakeCompleted:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_client_run_builds_argv(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_run(argv: list[str], **kwargs: Any) -> _FakeCompleted:
        captured["argv"] = argv
        return _FakeCompleted(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    cli = GeminiCLI(executable="gemini")
    cli.run(["--version"], options=RunOptions(debug=True), check=True)
    argv = captured["argv"]
    assert argv[0] == "gemini"
    assert "--debug" in argv
    assert "--version" in argv


def test_client_prompt_json_parses(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(argv: list[str], **kwargs: Any) -> _FakeCompleted:
        # Minimal JSON matching HeadlessResponse
        return _FakeCompleted(
            returncode=0,
            stdout='{"response":"hi","stats":{"models":{}}}',
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    cli = GeminiCLI(executable="gemini")
    resp = cli.prompt_json("hello")
    assert resp.response == "hi"
