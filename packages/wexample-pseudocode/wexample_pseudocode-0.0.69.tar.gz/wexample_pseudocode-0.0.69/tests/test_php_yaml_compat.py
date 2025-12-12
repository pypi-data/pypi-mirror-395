from __future__ import annotations

from pathlib import Path

PHP_RES = Path(
    "/home/weeger/Desktop/WIP/WEB/WEXAMPLE/COMPOSER/packages/wexample/php-pseudocode/tests/resources/item"
)
PY_RES = Path(
    "/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PIP/pip/pseudocode/tests/resources/item"
)


def test_php_class_basic_yaml_generates_code_contains_class_name() -> None:
    from wexample_pseudocode.generator.code_generator import CodeGenerator

    yml_path = PHP_RES / "class" / "basic_calculator.yml"
    yml = yml_path.read_text(encoding="utf-8")
    code = CodeGenerator().generate(yml)
    assert "class Calculator" in code


def test_php_function_complex_yaml_to_py_matches_python_fixture() -> None:
    from wexample_pseudocode.generator.code_generator import CodeGenerator

    yml_path = PHP_RES / "function" / "complex_function.yml"
    py_expected = (
        (PY_RES / "function" / "complex_function.py")
        .read_text(encoding="utf-8")
        .strip()
    )
    yml = yml_path.read_text(encoding="utf-8")
    code = CodeGenerator().generate(yml).strip()
    assert code == py_expected
