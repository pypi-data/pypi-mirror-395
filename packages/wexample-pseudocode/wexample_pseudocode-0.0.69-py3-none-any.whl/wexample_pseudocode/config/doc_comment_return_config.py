from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DocCommentReturnConfig:
    description: str | None = None
    type: str | None = None
