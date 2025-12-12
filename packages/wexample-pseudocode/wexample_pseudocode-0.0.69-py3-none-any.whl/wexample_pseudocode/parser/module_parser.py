from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


def parse_module_constants(source_code: str) -> Iterable[ConstantItem]:
    """Extract top-level assignments with ALL_CAPS names as constants.

    Description is taken from an inline comment on the same line when possible.
    Example handled:
        MAX_RETRIES = 3  # Maximum number of retries for API calls
    """
    tree = ast.parse(source_code)

    # Build a map of line_no -> comment text by scanning original lines.
    # Python's ast doesn't keep comments; we do a light heuristic by reading the source.
    line_map = {}
    for i, line in enumerate(source_code.splitlines(), start=1):
        if "#" in line:
            # take text after the first #, strip spaces
            comment = line.split("#", 1)[1].strip()
            if comment:
                line_map[i] = comment

    for node in tree.body:
        # Assign targets like NAME = value
        if isinstance(node, ast.Assign):
            if len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            name = target.id
            # consider ALL_CAPS only for this minimal scope
            if not name.isupper():
                continue

            value = _literal_eval_safe(node.value)
            description = line_map.get(node.lineno)
            yield ConstantItem(name=name, value=value, description=description)


def _literal_eval_safe(node: ast.AST):
    try:
        return ast.literal_eval(node)
    except Exception:
        # Fallback to a simple repr if non-literal
        try:
            return ast.unparse(node)  # type: ignore[attr-defined]
        except Exception:
            return None


@dataclass
class ConstantItem:
    name: str
    value: object

    description: str | None = None
