from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable


def parse_module_classes(source_code: str) -> Iterable[ClassItem]:
    from wexample_pseudocode.common.docstring import parse_docstring

    tree = ast.parse(source_code)
    # map line -> end-of-line comment
    line_map: dict[int, str] = {}
    for i, line in enumerate(source_code.splitlines(), start=1):
        if "#" in line:
            comment = line.split("#", 1)[1].strip()
            if comment:
                line_map[i] = comment

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            cls = ClassItem(
                name=node.name,
                description=_first_line(ast.get_docstring(node)),
            )
            # properties
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(
                    stmt.target, ast.Name
                ):
                    name = stmt.target.id
                    ann = _annotation_to_str(stmt.annotation)
                    default = _literal_eval_safe(stmt.value)
                    desc = line_map.get(stmt.lineno)
                    cls.properties.append(
                        ClassProperty(
                            name=name, type=ann, description=desc, default=default
                        )
                    )
                elif (
                    isinstance(stmt, ast.Assign)
                    and len(stmt.targets) == 1
                    and isinstance(stmt.targets[0], ast.Name)
                ):
                    name = stmt.targets[0].id
                    default = _literal_eval_safe(stmt.value)
                    desc = line_map.get(stmt.lineno)
                    cls.properties.append(
                        ClassProperty(
                            name=name, type=None, description=desc, default=default
                        )
                    )
                elif isinstance(stmt, ast.FunctionDef):
                    if stmt.name.startswith("__") and stmt.name.endswith("__"):
                        continue
                    raw_doc = ast.get_docstring(stmt)
                    parsed = parse_docstring(raw_doc)
                    m = ClassMethod(
                        name=stmt.name,
                        description=_first_line(raw_doc),
                        return_type=_annotation_to_str(stmt.returns),
                        return_description=parsed.get("return", {}).get("description"),
                    )
                    for arg in stmt.args.args:
                        if arg.arg == "self":
                            continue
                        m.parameters.append(
                            MethodParameter(
                                name=arg.arg,
                                type=_annotation_to_str(arg.annotation),
                                description=parsed.get("params", {}).get(arg.arg),
                            )
                        )
                    cls.methods.append(m)
            yield cls


def _annotation_to_str(ann: ast.AST | None) -> str | None:
    if ann is None:
        return None
    try:
        return ast.unparse(ann)  # type: ignore[attr-defined]
    except Exception:
        if isinstance(ann, ast.Name):
            return ann.id
        return None


def _first_line(doc: str | None) -> str | None:
    if not doc:
        return None
    return doc.strip().splitlines()[0].strip()


def _literal_eval_safe(node: ast.AST | None):
    if node is None:
        return None
    try:
        return ast.literal_eval(node)
    except Exception:
        try:
            return ast.unparse(node)  # type: ignore[attr-defined]
        except Exception:
            return None


@dataclass
class ClassProperty:
    name: str

    default: Any = None
    description: str | None = None
    type: str | None = None


@dataclass
class MethodParameter:
    name: str

    description: str | None = None
    type: str | None = None


@dataclass
class ClassMethod:
    name: str

    description: str | None = None
    parameters: list[MethodParameter] = field(default_factory=list)
    return_description: str | None = None
    return_type: str | None = None


@dataclass
class ClassItem:
    name: str

    description: str | None = None
    methods: list[ClassMethod] = field(default_factory=list)
    properties: list[ClassProperty] = field(default_factory=list)
