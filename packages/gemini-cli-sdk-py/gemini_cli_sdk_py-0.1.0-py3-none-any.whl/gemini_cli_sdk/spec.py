from __future__ import annotations

import re
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CommandSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str
    description: str


class OptionSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    flags: List[str] = Field(default_factory=list)
    param: Optional[str] = None
    description: str
    raw: str
    deprecated: bool = False


class GeminiHelpSpec(BaseModel):
    """Parsed representation of `gemini --help` output."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    usage: Optional[str] = None
    commands: List[CommandSpec] = Field(default_factory=list)
    options: List[OptionSpec] = Field(default_factory=list)


_SECTION_RE = re.compile(r"^\s*(Commands|Options):\s*$")


def parse_help_text(text: str) -> GeminiHelpSpec:
    lines = [ln.rstrip() for ln in text.splitlines()]

    usage: Optional[str] = None
    commands: List[CommandSpec] = []
    options: List[OptionSpec] = []

    section: Optional[str] = None
    pending_opt: Optional[OptionSpec] = None

    def flush_pending() -> None:
        nonlocal pending_opt
        if pending_opt is not None:
            options.append(pending_opt)
            pending_opt = None

    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip("\n")
        if not line.strip():
            i += 1
            continue

        if line.lstrip().startswith("Usage:"):
            usage = line.lstrip()
            i += 1
            continue

        m = _SECTION_RE.match(line)
        if m:
            flush_pending()
            section = m.group(1)
            i += 1
            continue

        if section == "Commands":
            flush_pending()
            # Commands are typically indented. Split on 2+ spaces to separate name/desc.
            raw = raw_line.rstrip()
            m2 = re.match(r"^\s*(\S+(?:\s+\S+)*)\s{2,}(.*)$", raw)
            if m2:
                name = m2.group(1).strip()
                desc = m2.group(2).strip()
                if name:
                    commands.append(CommandSpec(name=name, description=desc))
            i += 1
            continue

        if section == "Options":
            raw = raw_line.rstrip()
            stripped = raw.lstrip()

            # Continuation line: doesn't start with a flag but we have a pending option.
            if pending_opt is not None and (not stripped.startswith("-")):
                dep = pending_opt.deprecated or ("[deprecated:" in stripped)
                pending_opt = pending_opt.model_copy(
                    update={
                        "description": f"{pending_opt.description} {stripped}".strip(),
                        "deprecated": dep,
                        "raw": f"{pending_opt.raw}\n{raw}",
                    }
                )
                i += 1
                continue

            if not stripped.startswith("-"):
                i += 1
                continue

            flush_pending()

            tokens = stripped.split()
            flag_tokens: List[str] = []
            j = 0
            while j < len(tokens):
                t = tokens[j]
                t_clean = t.rstrip(",")
                if t_clean.startswith("-"):
                    flag_tokens.append(t_clean)
                    j += 1
                    continue
                break

            if not flag_tokens:
                i += 1
                continue

            param: Optional[str] = None
            if j < len(tokens) and re.match(r"^<[^>]+>$", tokens[j]):
                param = tokens[j]
                j += 1

            desc = " ".join(tokens[j:]).strip()
            deprecated = "[deprecated:" in stripped

            pending_opt = OptionSpec(
                flags=flag_tokens,
                param=param,
                description=desc,
                raw=raw,
                deprecated=deprecated,
            )
            i += 1
            continue

        i += 1

    flush_pending()
    return GeminiHelpSpec(usage=usage, commands=commands, options=options)
