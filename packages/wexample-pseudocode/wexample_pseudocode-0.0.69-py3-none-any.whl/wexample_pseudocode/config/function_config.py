from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from wexample_pseudocode.config.generator_config import GeneratorConfig

if TYPE_CHECKING:
    from wexample_pseudocode.config.function_parameter_config import (
        FunctionParameterConfig,
    )
    from wexample_pseudocode.config.generator_config import GeneratorConfig


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return repr(value)


@dataclass
class FunctionConfig:
    name: str

    description: str | None = None
    parameters: list[FunctionParameterConfig] = field(default_factory=list)
    return_description: str | None = None
    return_type: str | None = None

    @classmethod
    def from_config(
        cls,
        data: dict[str, Any],
        global_config: GeneratorConfig | None = None,
    ) -> FunctionConfig:
        from wexample_pseudocode.config.function_parameter_config import (
            FunctionParameterConfig,
        )

        params = [
            FunctionParameterConfig.from_config(p)
            for p in (data.get("parameters") or [])
        ]
        ret_type = None
        if "return" in data:
            ret_type = (
                (data["return"] or {}).get("type")
                if isinstance(data["return"], dict)
                else data["return"]
            )
        ret_desc = None
        if isinstance(data.get("return"), dict):
            ret_desc = data["return"].get("description")
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            parameters=params,
            return_type=ret_type,
            return_description=ret_desc,
        )

    def to_code(self) -> str:
        from wexample_pseudocode.common.type_normalizer import to_python_type

        params_src = ", ".join(p.to_code() for p in self.parameters)
        py_ret = to_python_type(self.return_type)
        ret = f" -> {py_ret}" if py_ret else ""
        header = f"def {self.name}({params_src}){ret}:"
        body_lines: list[str] = []
        # Build docstring including description, parameter descriptions and return description
        doc_lines: list[str] = []
        if self.description:
            doc_lines.append(self.description)
        # parameters
        for p in self.parameters:
            if p.description:
                if not doc_lines:
                    doc_lines.append("")
                doc_lines.append(f":param {p.name}: {p.description}")
        # return description
        if self.return_description:
            if not doc_lines:
                doc_lines.append("")
            doc_lines.append(f":return: {self.return_description}")
        if doc_lines:
            first = doc_lines[0]
            rest = doc_lines[1:]
            inner_block: list[str] = [first]
            if rest:
                inner_block.append("")
                inner_block.extend(["    " + line for line in rest])
            doc = '"""' + "\n".join(inner_block) + "\n    " + '"""'
            body_lines.append(doc)
        body_lines.append("pass")
        body = "\n".join("    " + line for line in body_lines)
        return f"{header}\n{body}"
