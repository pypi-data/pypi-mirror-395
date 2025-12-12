from __future__ import annotations

import re


def python_get_return_type_from_annotations(func) -> str | None:
    if not hasattr(func, "__annotations__") or "return" not in func.__annotations__:
        return None

    return_annotation = func.__annotations__["return"]

    if hasattr(return_annotation, "__name__"):
        return return_annotation.__name__
    return str(return_annotation).replace("typing.", "")


def python_get_return_type_from_docstring(docstring: str | None) -> str | None:
    if not docstring:
        return None

    arrow_pattern = r"->\s*['\"]?([\w\d_]+)['\"]?"
    returns_pattern = r"Returns\s+['\"]?([\w\d_]+)['\"]?"

    arrow_match = re.search(arrow_pattern, docstring)
    returns_match = re.search(returns_pattern, docstring)

    if arrow_match:
        return arrow_match.group(1)
    elif returns_match:
        return returns_match.group(1)

    return None
