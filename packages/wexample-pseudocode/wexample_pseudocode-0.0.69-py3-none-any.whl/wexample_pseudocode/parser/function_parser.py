from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


def parse_module_functions(source_code: str) -> Iterable[FunctionItem]:
    from class_parser import _annotation_to_str

    from wexample_pseudocode.common.docstring import parse_docstring

    tree = ast.parse(source_code)

    def _literal(node: ast.AST | None):
        if node is None:
            return None
        try:
            return ast.literal_eval(node)
        except Exception:
            try:
                return ast.unparse(node)  # type: ignore[attr-defined]
            except Exception:
                return None

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            raw_doc = ast.get_docstring(node)
            parsed = parse_docstring(raw_doc)
            item = FunctionItem(
                name=node.name,
                description=_first_line(raw_doc),
                parameters=[],
                return_type=_annotation_to_str(node.returns),
                return_description=parsed.get("return", {}).get("description"),
            )
            total_args = [a for a in node.args.args]
            num_defaults = len(node.args.defaults)
            split_index = len(total_args) - num_defaults
            for i, arg in enumerate(total_args):
                if arg.arg == "self":
                    continue
                has_default = i >= split_index and num_defaults > 0
                default = None
                if has_default:
                    default = node.args.defaults[i - split_index]
                item.parameters.append(
                    FunctionParameter(
                        name=arg.arg,
                        type=_annotation_to_str(arg.annotation),
                        description=parsed["params"].get(arg.arg),
                        default=default,
                        has_default=has_default,
                    )
                )
            yield item


def _first_line(doc: str | None) -> str | None:
    if not doc:
        return None
    return doc.strip().splitlines()[0].strip()


@dataclass
class FunctionParameter:
    name: str

    default: ast.AST | None = None
    description: str | None = None
    has_default: bool = False
    type: str | None = None


@dataclass
class FunctionItem:
    name: str

    description: str | None = None
    parameters: list[FunctionParameter] = None
    return_description: str | None = None
    return_type: str | None = None
