from __future__ import annotations

from typing import Any


def copy_shallow(x: Any) -> Any:
    if isinstance(x, list):
        return list(x)
    if isinstance(x, dict):
        return dict(x)
    if isinstance(x, set):
        return set(x)
    if isinstance(x, tuple):
        return tuple(x)
    return x  # immutables
