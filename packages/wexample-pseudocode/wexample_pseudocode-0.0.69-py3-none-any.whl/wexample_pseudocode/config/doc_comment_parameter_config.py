from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DocCommentParameterConfig:
    name: str

    description: str | None = None
    type: str | None = None
