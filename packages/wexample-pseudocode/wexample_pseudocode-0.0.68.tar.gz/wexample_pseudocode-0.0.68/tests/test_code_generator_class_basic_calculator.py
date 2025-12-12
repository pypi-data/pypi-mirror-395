from __future__ import annotations


def test_code_generator_class_basic_calculator() -> None:
    from pathlib import Path

    from wexample_pseudocode.generator.code_generator import CodeGenerator

    resources_dir = Path(__file__).parent / "resources" / "item" / "class"
    yml_path = resources_dir / "basic_calculator.yml"
    expected_code_path = resources_dir / "basic_calculator.py"

    gen = CodeGenerator()
    output = gen.generate(yml_path.read_text(encoding="utf-8"))

    assert output.strip() == expected_code_path.read_text(encoding="utf-8").strip()
