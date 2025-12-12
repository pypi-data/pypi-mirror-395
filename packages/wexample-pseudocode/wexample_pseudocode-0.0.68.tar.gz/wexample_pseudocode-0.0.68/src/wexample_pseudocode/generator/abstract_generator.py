from __future__ import annotations

from typing import Any

import yaml
from wexample_helpers.classes.abstract_method import abstract_method


class AbstractGenerator:
    """Base class mirroring the PHP AbstractGenerator responsibilities.

    Provides a common YAML dump helper and enforces the public API
    expected from concrete generators.
    """

    @staticmethod
    def dump_pseudocode(data: dict[str, Any]) -> str:
        """Serialize pseudocode structure to YAML string.

        Kept as a static method to mimic the PHP usage ergonomics.
        """
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)

    @abstract_method
    def generate_config_data(self, source_code: str) -> dict[str, Any]:
        """Generate the pseudocode config data from the given source code."""
        raise NotImplementedError
