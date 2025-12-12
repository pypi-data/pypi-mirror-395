from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_pseudocode.generator.pseudocode_generator import PseudocodeGenerator


@pytest.fixture()
def generator() -> PseudocodeGenerator:
    from wexample_pseudocode.generator.pseudocode_generator import PseudocodeGenerator

    return PseudocodeGenerator()


@pytest.fixture()
def resources_dir() -> Path:
    from pathlib import Path

    # Mirror PHP test resources structure under python package tests
    return Path(__file__).parent / "resources" / "item" / "constant"
