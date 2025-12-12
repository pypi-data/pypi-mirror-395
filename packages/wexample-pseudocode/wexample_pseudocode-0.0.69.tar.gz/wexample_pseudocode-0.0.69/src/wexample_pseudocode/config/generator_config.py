from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GeneratorConfig:
    """Global generator config (minimal placeholder).

    For now we don't use any global options for the constant case, but we keep the
    structure to mirror the PHP API and allow future extension.
    """

    @classmethod
    def from_config(cls, data: dict[str, Any]) -> GeneratorConfig:
        return cls()
