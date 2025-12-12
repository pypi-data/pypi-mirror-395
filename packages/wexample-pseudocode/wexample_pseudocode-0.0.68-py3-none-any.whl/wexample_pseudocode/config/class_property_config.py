from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return repr(value)


@dataclass
class ClassPropertyConfig:
    name: str

    default: Any = None
    description: str | None = None
    type: str | None = None

    def to_code(self) -> str:
        left = f"{self.name}: {self.type}" if self.type is not None else self.name
        code = left
        if self.default is not None:
            code += f" = {_format_value(self.default)}"
        if self.description:
            code += f"  # {self.description}"
        return code
