from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return repr(value)


@dataclass
class FunctionParameterConfig:
    name: str

    default: Any = None
    description: str | None = None
    has_default: bool = False
    type: str | None = None

    @classmethod
    def from_config(cls, data: dict[str, Any]) -> FunctionParameterConfig:
        return cls(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            default=data.get("default"),
            has_default=("default" in data),
        )

    def to_code(self) -> str:
        from wexample_pseudocode.common.type_normalizer import to_python_type

        py_type = to_python_type(self.type)
        annotated = self.name
        if py_type is not None:
            # If default is None (optional), wrap type with typing.Optional[]
            if (
                self.has_default
                and self.default is None
                and not py_type.startswith("typing.Optional[")
            ):
                annotated = f"{self.name}: typing.Optional[{py_type}]"
            else:
                annotated = f"{self.name}: {py_type}"

        left = annotated
        if self.has_default:
            if self.default is None:
                return f"{left} = None"
            return f"{left} = {_format_value(self.default)}"
        return left
