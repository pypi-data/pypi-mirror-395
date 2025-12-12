from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import yaml

from wexample_pseudocode.common.with_config_registry import WithConfigRegistry
from wexample_pseudocode.generator.abstract_generator import AbstractGenerator


@dataclass
class CodeGenerator(AbstractGenerator, WithConfigRegistry):
    """Generate Python code from pseudocode YAML.

    Mirrors the PHP CodeGenerator class but targets Python as the output language.
    Minimal scope: only constant items.
    """

    def __post_init__(self) -> None:  # dataclass hook; ensure registry init
        WithConfigRegistry.__init__(self)

    def generate(self, input_text: str) -> str:
        configs = self._generate_config(input_text)
        output = ""
        for cfg in configs:
            output += cfg.to_code() + "\n"
        return output

    # Implement abstract method (not used directly in CodeGenerator flow)
    def generate_config_data(self, source_code: str) -> dict[str, Any]:
        raise NotImplementedError(
            "CodeGenerator does not parse source; it generates code from YAML"
        )

    def get_source_file_extension(self) -> str:
        return "yml"

    def get_target_file_extension(self) -> str:
        return "py"

    def _generate_config(self, input_text: str):
        from wexample_pseudocode.config.generator_config import GeneratorConfig

        data = yaml.safe_load(input_text) or {}
        registry = self.get_config_registry()
        instances = []

        global_generator_config = None
        if "generator" in data:
            global_generator_config = GeneratorConfig.from_config(
                data["generator"]
            )  # kept for parity

        for item in data.get("items", []) or []:
            config_cls: type | None = registry.find_matching_config_loader(item)  # type: ignore[attr-defined]
            if config_cls is not None:
                instances.append(config_cls.from_config(item, global_generator_config))
        return instances
