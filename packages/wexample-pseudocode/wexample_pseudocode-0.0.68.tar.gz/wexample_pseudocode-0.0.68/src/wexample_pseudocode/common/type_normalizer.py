from __future__ import annotations


def normalize_type(type_str: str | None) -> str | None:
    if type_str is None:
        return None
    t = type_str.strip()

    # Strip leading 'typing.' for readability
    if t.startswith("typing."):
        t = t[len("typing.") :]

    # Optional[...] -> inner + marker handled by caller
    if t.startswith("Optional[") and t.endswith("]"):
        inner = t[len("Optional[") : -1].strip()
        return normalize_type(inner)

    # Common aliases across languages
    # Python -> schema (PHP uses 'array')
    if t in {"list", "List", "Sequence", "MutableSequence", "dict", "Dict", "Mapping"}:
        return "array"

    if t in {"Callable"}:
        return "callable"

    # Primitives stay as-is
    if t in {"int", "float", "str", "bool", "mixed", "void", "None"}:
        return t if t != "None" else None

    return t


def to_python_type(type_str: str | None) -> str | None:
    if type_str is None:
        return None
    t = type_str.strip()
    if t == "array":
        return "list"
    if t == "callable":
        return "typing.Callable"
    if t in {"mixed"}:
        return "typing.Any"
    if t in {"void"}:
        return None
    return t
