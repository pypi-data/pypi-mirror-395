from __future__ import annotations

import functools


def abstract_method(func):
    func.__isabstract__ = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> None:
        cls = args[0].__class__.__name__
        raise NotImplementedError(f"{cls}.{func.__name__}() must be implemented")

    return wrapper
