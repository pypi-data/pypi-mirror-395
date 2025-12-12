from __future__ import annotations

import re

PARAM_RE = re.compile(
    r"^\s*:param\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?P<desc>.+)\s*$"
)
RETURN_RE = re.compile(r"^\s*:return[s]?\s*:\s*(?P<desc>.+)\s*$")


def parse_docstring(doc: str | None) -> dict[str, dict[str, str]]:
    """Extract simple parameter and return descriptions from a docstring.

    Supported styles (single-line only):
    - reST/Sphinx: ":param name: desc" and ":return: desc"
    - Google/NumPy minimal: "Args:"/"Parameters:" block with lines "name: desc"
    """
    result: dict[str, dict[str, str]] = {"params": {}, "return": {}}
    if not doc:
        return result

    lines = [l.rstrip() for l in doc.splitlines()]

    # Pass 1: reST style
    for line in lines:
        m = PARAM_RE.match(line)
        if m:
            result["params"][m.group("name")] = m.group("desc").strip()
            continue
        m = RETURN_RE.match(line)
        if m:
            result["return"]["description"] = m.group("desc").strip()

    # Pass 2: Google/NumPy minimal blocks
    def parse_block(header: str) -> None:
        try:
            idx = next(
                i for i, l in enumerate(lines) if l.strip().lower().startswith(header)
            )
        except StopIteration:
            return
        i = idx + 1
        while i < len(lines):
            s = lines[i].strip()
            if not s:
                i += 1
                continue
            # stop at next section header (simple heuristic: ends with ':')
            if s.endswith(":"):
                break
            if ":" in s:
                name, desc = s.split(":", 1)
                name = name.strip()
                desc = desc.strip()
                if header.startswith("args") or header.startswith("parameters"):
                    if name:
                        result["params"][name] = desc
                elif header.startswith("returns"):
                    if desc and "description" not in result["return"]:
                        result["return"]["description"] = (
                            f"{name}: {desc}" if name else desc
                        )
            i += 1

    parse_block("args:")
    parse_block("parameters:")
    parse_block("returns:")

    return result
