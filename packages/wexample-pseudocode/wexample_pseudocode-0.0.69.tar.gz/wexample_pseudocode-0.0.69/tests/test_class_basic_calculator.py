from __future__ import annotations

import yaml


def test_class_basic_calculator() -> None:
    from pathlib import Path

    from wexample_pseudocode.generator.pseudocode_generator import PseudocodeGenerator

    resources_dir = Path(__file__).parent / "resources" / "item" / "class"
    source_path = resources_dir / "basic_calculator.py"
    expected_yaml_path = resources_dir / "basic_calculator.yml"

    source = source_path.read_text(encoding="utf-8")
    expected = yaml.safe_load(expected_yaml_path.read_text(encoding="utf-8"))

    gen = PseudocodeGenerator()
    actual = gen.generate_config_data(source)

    # Debug outputs
    tmp_dir = Path.cwd() / "tmp" / "pseudocode_tests"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    (tmp_dir / "basic_calculator_expected.yml").write_text(
        yaml.safe_dump(expected, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (tmp_dir / "basic_calculator_actual.yml").write_text(
        yaml.safe_dump(actual, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    assert actual == expected
