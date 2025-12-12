from __future__ import annotations

from wexample_helpers.const.types import PathOrString


def classes_get_definition_path(instance: object) -> PathOrString:
    import inspect

    return inspect.getfile(instance.__class__)
