from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T", bound=type)


def polyfill_import(classes: Any, *args, **kwargs) -> None:
    """
    Fix this error, by importing classes for in a dummy method. These classes are actually not used anywhere :
    pydantic.errors.PydanticUserError: `ClassName` is not fully defined; you should define `Kernel`,
    then call `CountAdminCommand.model_rebuild()`.
    Using this method allow to add missing imports in file, event not used in page, and prevent auto formatters
    to consider import as useless.
    """


def polyfill_not_implemented_error() -> None:
    import inspect

    function_name = inspect.currentframe().f_back.f_code.co_name
    raise NotImplementedError(f"{function_name} must be implemented by subclass")


def polyfill_register_global(
    classes: T | list[T] | tuple[T, ...], context: dict | None = None
) -> None:
    """
    Registers classes in the global namespace to fix Pydantic type resolution issues.
    This is particularly useful when Pydantic needs to resolve forward references or
    when type hints reference classes that might not be in the current scope.

    Args:
        classes: A class, or list/tuple of classes to register in the global namespace

    Usage:
        polyfill_register_global(AbstractKernel)
        polyfill_register_global([AbstractKernel, Kernel])
        polyfill_register_global((AbstractKernel, Kernel))
    """
    import inspect

    # Convert single class to list
    if not isinstance(classes, (list, tuple)):
        classes = [classes]

    if context is None:
        caller_frame = inspect.currentframe().f_back
        if caller_frame is None:
            raise RuntimeError("Unable to find calling frame")
        context = caller_frame.f_globals

    for cls in classes:
        if not isinstance(cls, type):
            raise TypeError(f"Expected a class, got {type(cls)}")
        cls_name = cls.__name__
        context[cls_name] = cls
