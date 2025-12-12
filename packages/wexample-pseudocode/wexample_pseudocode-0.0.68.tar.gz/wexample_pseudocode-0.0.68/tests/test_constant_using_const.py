from __future__ import annotations

from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from pathlib import Path


def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_constant_using_const(resources_dir) -> None:
    from pathlib import Path

    from wexample_pseudocode.generator.pseudocode_generator import PseudocodeGenerator

    source_path = resources_dir / "constant_using_const.py"
    expected_yaml_path = resources_dir / "constant_using_const.yml"

    source = load_file(source_path)
    expected = yaml.safe_load(load_file(expected_yaml_path))

    gen = PseudocodeGenerator()
    actual = gen.generate_config_data(source)

    # Dump debug files (like PHP trait does), into a tmp folder
    tmp_dir = Path.cwd() / "tmp" / "pseudocode_tests"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    (tmp_dir / "constant_using_const_expected.yml").write_text(
        yaml.safe_dump(expected, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (tmp_dir / "constant_using_const_actual.yml").write_text(
        yaml.safe_dump(actual, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    assert actual == expected
