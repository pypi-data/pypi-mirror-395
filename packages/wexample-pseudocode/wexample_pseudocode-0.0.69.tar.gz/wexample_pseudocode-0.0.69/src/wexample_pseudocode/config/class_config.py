from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from wexample_pseudocode.config.generator_config import GeneratorConfig

if TYPE_CHECKING:
    from wexample_pseudocode.config.class_method_config import ClassMethodConfig
    from wexample_pseudocode.config.class_property_config import ClassPropertyConfig
    from wexample_pseudocode.config.generator_config import GeneratorConfig


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return repr(value)


@dataclass
class ClassConfig:
    name: str

    description: str | None = None
    methods: list[ClassMethodConfig] = field(default_factory=list)
    properties: list[ClassPropertyConfig] = field(default_factory=list)

    @classmethod
    def from_config(
        cls,
        data: dict[str, Any],
        global_config: GeneratorConfig | None = None,
    ) -> ClassConfig:
        from wexample_pseudocode.config.class_method_config import ClassMethodConfig
        from wexample_pseudocode.config.class_property_config import ClassPropertyConfig

        props = [
            ClassPropertyConfig(
                name=p.get("name"),
                type=p.get("type"),
                description=p.get("description"),
                default=p.get("default"),
            )
            for p in (data.get("properties") or [])
        ]
        methods = [
            ClassMethodConfig.from_config(m) for m in (data.get("methods") or [])
        ]
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            properties=props,
            methods=methods,
        )

    def to_code(self) -> str:
        lines: list[str] = [f"class {self.name}:"]
        if self.description:
            lines.append(f'    """{self.description}"""')
            lines.append("")
        for p in self.properties:
            lines.append("    " + p.to_code())
        if self.properties and self.methods:
            lines.append("")
        for m in self.methods:
            lines.append(m.to_code(indent="    "))
        if not self.properties and not self.methods and not self.description:
            lines.append("    pass")
        return "\n".join(lines)
