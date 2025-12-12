from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from wexample_pseudocode.config.generator_config import GeneratorConfig

if TYPE_CHECKING:
    from wexample_pseudocode.config.generator_config import GeneratorConfig


@dataclass
class ConstantConfig:
    name: str
    value: Any

    description: str | None = None

    @classmethod
    def from_config(
        cls, data: dict[str, Any], global_config: GeneratorConfig | None = None
    ) -> ConstantConfig:
        return cls(
            name=data.get("name"),
            value=data.get("value"),
            description=data.get("description"),
        )

    def to_code(self) -> str:
        # For the Python side, produce Python assignment code with inline comment if present.
        # This mirrors the PHP to-code idea but targets Python syntax.
        if isinstance(self.value, str):
            # Emit double-quoted string with escaped quotes to match fixtures
            escaped = self.value.replace('"', '\\"')
            value_repr = f'"{escaped}"'
        else:
            value_repr = repr(self.value)
        code = f"{self.name} = {value_repr}"
        if self.description:
            code += f"  # {self.description}"
        return code
