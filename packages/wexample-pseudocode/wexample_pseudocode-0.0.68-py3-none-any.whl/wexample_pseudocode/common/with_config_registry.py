from __future__ import annotations


class WithConfigRegistry:
    """Minimal registry to map pseudocode items to config loader classes.

    Mirrors the PHP trait `WithConfigRegistry` for our limited scope (constants only).
    """

    _registry: dict[str, type]

    def __init__(self) -> None:
        from wexample_pseudocode.config.class_config import ClassConfig
        from wexample_pseudocode.config.constant_config import ConstantConfig
        from wexample_pseudocode.config.function_config import FunctionConfig

        self._registry = {
            "constant": ConstantConfig,
            "class": ClassConfig,
            "function": FunctionConfig,
        }

    def find_matching_config_loader(self, data: dict) -> type | None:
        item_type = data.get("type")
        if not item_type:
            return None
        return self._registry.get(item_type)

    def get_config_registry(self) -> WithConfigRegistry:
        return self
