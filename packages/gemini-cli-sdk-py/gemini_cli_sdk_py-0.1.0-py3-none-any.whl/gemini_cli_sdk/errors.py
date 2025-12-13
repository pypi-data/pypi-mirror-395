from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True, slots=True)
class GeminiCLIError(RuntimeError):
    """Raised when the Gemini CLI exits non-zero."""

    message: str
    argv: Sequence[str]
    exit_code: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None

    def __str__(self) -> str:
        base = f"{self.message} (exit_code={self.exit_code})"
        cmd = " ".join(self.argv)
        if self.stderr:
            return f"{base}\nCommand: {cmd}\n--- stderr ---\n{self.stderr}"
        if self.stdout:
            return f"{base}\nCommand: {cmd}\n--- stdout ---\n{self.stdout}"
        return f"{base}\nCommand: {cmd}"
