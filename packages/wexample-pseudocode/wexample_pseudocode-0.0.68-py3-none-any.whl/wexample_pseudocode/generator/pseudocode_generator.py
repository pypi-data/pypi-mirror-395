from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from wexample_pseudocode.generator.abstract_generator import AbstractGenerator


def _literal_eval_safe(node):
    try:
        import ast as _ast

        if node is None:
            return None
        return _ast.literal_eval(node)
    except Exception:
        try:
            import ast as _ast

            return _ast.unparse(node)  # type: ignore[attr-defined]
        except Exception:
            return None


@dataclass
class PseudocodeGenerator(AbstractGenerator):
    """Minimal generator focusing on Python module-level constants -> YAML pseudocode.

    Public API kept close to the PHP lib naming:
    - generate_config_data(source_code: str) -> dict
    - dump_pseudocode(data: dict) -> str
    """

    def generate_config_data(self, source_code: str) -> dict[str, Any]:
        from wexample_pseudocode.common.type_normalizer import normalize_type
        from wexample_pseudocode.parser.class_parser import parse_module_classes
        from wexample_pseudocode.parser.function_parser import parse_module_functions
        from wexample_pseudocode.parser.module_parser import parse_module_constants

        items: list[dict[str, Any]] = []

        for const in parse_module_constants(source_code):
            items.append(
                {
                    "type": "constant",
                    "name": const.name,
                    "value": const.value,
                    **({"description": const.description} if const.description else {}),
                }
            )

        for cls in parse_module_classes(source_code):
            item: dict[str, Any] = {
                "type": "class",
                "name": cls.name,
            }
            if cls.description:
                item["description"] = cls.description

            if cls.properties:
                props: list[dict[str, Any]] = []
                for p in cls.properties:
                    pd: dict[str, Any] = {"name": p.name}
                    if p.type is not None:
                        pd["type"] = normalize_type(p.type)
                    if p.description:
                        pd["description"] = p.description
                    if p.default is not None:
                        pd["default"] = p.default
                    props.append(pd)
                item["properties"] = props

            if cls.methods:
                methods: list[dict[str, Any]] = []
                for m in cls.methods:
                    md: dict[str, Any] = {"type": "method", "name": m.name}
                    if m.description:
                        md["description"] = m.description
                    if m.parameters:
                        params: list[dict[str, Any]] = []
                        for a in m.parameters:
                            ad: dict[str, Any] = {"name": a.name}
                            if a.type is not None:
                                ad["type"] = normalize_type(a.type)
                            if a.description:
                                ad["description"] = a.description
                            params.append(ad)
                        md["parameters"] = params
                    if m.return_type is not None or m.return_description is not None:
                        rd: dict[str, Any] = {}
                        if m.return_type is not None:
                            rd["type"] = normalize_type(m.return_type)
                        if m.return_description:
                            rd["description"] = m.return_description
                        md["return"] = rd
                    methods.append(md)
                item["methods"] = methods

            items.append(item)

        for fn in parse_module_functions(source_code):
            item: dict[str, Any] = {
                "type": "function",
                "name": fn.name,
            }
            if fn.description:
                item["description"] = fn.description
            if fn.parameters:
                params: list[dict[str, Any]] = []
                for p in fn.parameters:
                    pd: dict[str, Any] = {"name": p.name}
                    if p.type is not None:
                        pd["type"] = normalize_type(p.type)
                    if getattr(p, "description", None):
                        pd["description"] = p.description
                    if getattr(p, "has_default", False):
                        default_val = _literal_eval_safe(p.default)
                        # explicit None default (null)
                        if (
                            isinstance(getattr(p, "default", None), type(None))
                            or default_val is None
                        ):
                            pd["optional"] = True
                            pd["default"] = None
                        else:
                            pd["default"] = default_val
                    params.append(pd)
                item["parameters"] = params
            if (
                fn.return_type is not None
                or getattr(fn, "return_description", None) is not None
            ):
                rd: dict[str, Any] = {}
                if fn.return_type is not None:
                    rd["type"] = normalize_type(fn.return_type)
                if getattr(fn, "return_description", None):
                    rd["description"] = fn.return_description
                item["return"] = rd
            items.append(item)

        return {"items": items}
