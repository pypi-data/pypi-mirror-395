from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

if TYPE_CHECKING:
    from types import UnionType


def type_generic_value_is_valid(value: Any, allowed_type: type | UnionType) -> bool:
    """Helper to recursively validate parameter types for generics like Dict, List, Set, Tuple, and Union."""
    from types import UnionType

    from wexample_helpers.exception.not_allowed_variable_type_exception import (
        NotAllowedVariableTypeException,
    )

    origin = get_origin(allowed_type) or allowed_type
    args = get_args(allowed_type)

    # Validate Union (supports typing.Union and PEP 604 | operator which yields types.UnionType)
    if origin is Union or origin is UnionType:
        typed_dict_errors = []
        for arg in args:
            # Check TypedDict in Union
            if _is_typed_dict(arg) and isinstance(value, dict):
                try:
                    _validate_typed_dict(value, arg)
                    return True
                except NotAllowedVariableTypeException as e:
                    # Collect TypedDict specific errors
                    error_msg = getattr(e, "variable_type", str(e))
                    typed_dict_errors.append(f"{arg.__name__}: {error_msg}")
                    continue
                except Exception:
                    continue
            # Regular type validation
            if type_generic_value_is_valid(value, arg):
                return True

        # If we had TypedDict errors and value is dict, raise specific error
        if typed_dict_errors and isinstance(value, dict):
            from wexample_helpers.exception.not_allowed_variable_type_exception import (
                NotAllowedVariableTypeException,
            )

            raise NotAllowedVariableTypeException(
                variable_type=f"dict validation failed: {'; '.join(typed_dict_errors)}",
                variable_value=value,
                allowed_types=[allowed_type],
            )

        return False

    # Handle Type[T] annotations: we expect "value" to be a class, and it must be a subclass of T
    if origin is type:
        # If no parameter provided, accept any class
        if not args:
            return isinstance(value, type)

        param = args[0]

        # value must be a class object to satisfy Type[...]
        if not isinstance(value, type):
            return False

        # Type[Any] accepts any class
        if param is Any:
            return True

        # If param itself is a Union of classes, accept if value is subclass of any
        param_origin = get_origin(param) or param
        if param_origin is Union or param_origin is UnionType:
            res = any(_safe_issubclass(value, p) for p in get_args(param))
            return res

        # Normal Type[SomeClass]
        res = _safe_issubclass(value, param_origin)
        return res

    # Validate dictionary type with possible nested generics
    if origin is dict:
        if not isinstance(value, dict):
            return False
        # Accept empty dict
        if not value:
            return True
        # Validate key and value types recursively
        key_type, value_type = args if len(args) == 2 else (Any, Any)
        return all(
            type_generic_value_is_valid(k, key_type)
            and type_generic_value_is_valid(v, value_type)
            for k, v in value.items()
        )

    # Validate list type with possible nested generics
    elif origin is list:
        if not isinstance(value, list):
            return False
        # Accept empty list
        if not value:
            return True
        # Validate item type recursively
        item_type = args[0] if args else Any
        return all(type_generic_value_is_valid(item, item_type) for item in value)

    # Validate set type with possible nested generics
    elif origin is set:
        if not isinstance(value, set):
            return False
        # Accept empty set
        if not value:
            return True
        # Validate item type recursively
        item_type = args[0] if args else Any
        return all(type_generic_value_is_valid(item, item_type) for item in value)

    # Validate tuple type with possible nested generics
    elif origin is tuple:
        if not isinstance(value, tuple) or (args and len(value) != len(args)):
            return False
        # Validate each item in the tuple recursively
        return all(
            type_generic_value_is_valid(item, arg)
            for item, arg in zip(value, args)
            if args
        )

    elif origin is Any:
        return True

    # For any other types, fallback to isinstance check
    return type_is_isinstance(value, origin)


def type_is_compatible(actual_type: type, allowed_type: type) -> bool:
    """Check if actual_type is compatible with allowed_type for generics like Dict, List, Tuple, and Union."""
    from collections.abc import Callable

    origin = get_origin(allowed_type) or allowed_type
    actual_origin = get_origin(actual_type) or actual_type
    allowed_args = get_args(allowed_type)
    actual_args = get_args(actual_type)

    # If allowed_type is Any, it is compatible with any actual_type
    if origin is Any:
        return True

    # Handle Union type for allowed_type
    if origin is Union:
        return any(type_is_compatible(actual_type, arg) for arg in allowed_args)

    # Handle Callable type with possible nested generics
    if _safe_issubclass(origin, Callable):
        # Check if actual_type is also a Callable
        if not _safe_issubclass(actual_origin, Callable):
            return False
        # If allowed_type is just Callable without specific args, consider it compatible with any Callable
        if not allowed_args:
            return True
        # If allowed_type has specific args, compare return types (last element in allowed_args)
        if len(allowed_args) == len(actual_args):
            return type_is_compatible(actual_args[-1], allowed_args[-1])
        return False

    # Handle dictionary type with possible nested generics
    if origin is dict:
        if actual_origin is not dict:
            return False
        # Check compatibility for key and value types recursively
        key_type, value_type = allowed_args if len(allowed_args) == 2 else (Any, Any)
        actual_key_type, actual_value_type = (
            actual_args if len(actual_args) == 2 else (Any, Any)
        )
        return type_is_compatible(actual_key_type, key_type) and type_is_compatible(
            actual_value_type, value_type
        )

    # Handle list type with possible nested generics
    elif origin is list:
        if actual_origin is not list:
            return False
        # Validate item type recursively
        item_type = allowed_args[0] if allowed_args else Any
        actual_item_type = actual_args[0] if actual_args else Any
        return type_is_compatible(actual_item_type, item_type)

    # Handle tuple type with possible nested generics
    elif origin is tuple:
        if actual_origin is not tuple or len(actual_args) != len(allowed_args):
            return False
        # Validate each item type in the tuple recursively
        return all(
            type_is_compatible(act, exp) for act, exp in zip(actual_args, allowed_args)
        )

    # For other types, fall back to direct comparison
    return actual_type == allowed_type


def type_is_generic(type_value: Any) -> bool:
    """Detects if a given type is a generic type like List, Dict, Union"""
    # Set of known generic types for quick membership testing
    generic_types = {list, dict, tuple, Union}

    # Extract the base type of type_value using get_origin, or use type_value itself if get_origin is None
    type_value = get_origin(type_value) or type_value

    # Check if type_value is a known generic type
    return type_value in generic_types


def type_is_isinstance(value: Any, allowed_type: Any) -> bool:
    """Like isinstance but never raises TypeError; returns False instead."""
    try:
        return isinstance(value, allowed_type)
    except TypeError:
        return False


def type_to_name(t: Any) -> str:
    from types import UnionType

    # Accept python types, strings, and mypy UnionType
    if isinstance(t, str):
        return t
    if isinstance(t, type):
        return t.__name__
    if isinstance(t, UnionType):
        # Convert "A | B" style if possible
        try:
            return " | ".join(type_to_name(it) for it in t.items)
        except Exception:
            return str(t)
    return str(t)


def type_validate_or_fail(value: Any, allowed_type: type | UnionType) -> None:
    from collections.abc import Callable

    from wexample_helpers.exception.not_allowed_variable_type_exception import (
        NotAllowedVariableTypeException,
    )

    if allowed_type is Any:
        return

    # Check for TypedDict validation
    if _is_typed_dict(allowed_type) and isinstance(value, dict):
        _validate_typed_dict(value, allowed_type)
        return

    if allowed_type is Callable:
        if callable(value):
            return
        # Not a callable where one was expected
        raise NotAllowedVariableTypeException(
            variable_type=type(value).__name__,
            variable_value=value,
            allowed_types=["callable"],
        )

    # Check if the raw value matches any allowed base type
    if not type_is_generic(allowed_type):
        if type_is_isinstance(allowed_type, Callable):
            if isinstance(value, Callable):
                # Type is probably not a meta type, i.e:
                #   - allowed_type=Type[MyClass] will match value MyClass
                #   - allowed_type=MyClass will not match value MyClass
                if isinstance(allowed_type, type):
                    raise NotAllowedVariableTypeException(
                        variable_type=type(value).__name__,
                        variable_value=value,
                        allowed_types=[allowed_type],
                    )

                args = get_args(allowed_type)
                if args:
                    return_type = args[-1]

                    try:
                        type_hints = get_type_hints(value, localns=locals())
                        actual_return_type_hint = type_hints.get("return", None)
                    except NameError:
                        actual_return_type_hint = None

                    if actual_return_type_hint is None:
                        return

                    # Handle generic types
                    if type_is_compatible(
                        actual_type=cast(type, actual_return_type_hint),
                        allowed_type=return_type,
                    ):
                        return

                    raise NotAllowedVariableTypeException(
                        variable_type=str(actual_return_type_hint),
                        variable_value=value,
                        allowed_types=[return_type],
                    )

                return
        # Explicit check for simple types without get_origin
        elif type_is_isinstance(value, allowed_type):
            return

    # Handle generic types (includes Union/| and Type[...])
    if type_generic_value_is_valid(value, allowed_type):
        return

    # If none of the checks passed, raise an exception
    raise NotAllowedVariableTypeException(
        variable_type=type(value).__name__,
        variable_value=value,
        allowed_types=[allowed_type],
    )


def _is_typed_dict(type_hint: Any) -> bool:
    """Check if a type hint is a TypedDict."""

    # Check module and class name for TypedDict
    if hasattr(type_hint, "__module__") and hasattr(type_hint, "__name__"):
        # Direct check for typing module TypedDict classes
        if hasattr(type_hint, "__annotations__") and hasattr(type_hint, "__total__"):
            return True

    # Check for typing_extensions.TypedDict or typing.TypedDict metaclass
    try:
        from typing_extensions import _TypedDictMeta

        if isinstance(type_hint, _TypedDictMeta):
            return True
    except ImportError:
        pass

    try:
        import typing

        if hasattr(typing, "_TypedDictMeta") and isinstance(
            type_hint, typing._TypedDictMeta
        ):
            return True
    except (ImportError, AttributeError):
        pass

    # Fallback check for standard attributes
    result = (
        hasattr(type_hint, "__annotations__")
        and hasattr(type_hint, "__total__")
        and hasattr(type_hint, "__required_keys__")
        and hasattr(type_hint, "__optional_keys__")
    )
    return result


def _safe_issubclass(a: Any, b: Any) -> bool:
    """Like issubclass but never raises TypeError; returns False instead."""
    try:
        return issubclass(a, b)
    except TypeError:
        return False


def _validate_typed_dict(value: dict, typed_dict_type: Any) -> None:
    """Validate a dict against a TypedDict type."""
    from wexample_helpers.exception.not_allowed_variable_type_exception import (
        NotAllowedVariableTypeException,
    )

    annotations = getattr(typed_dict_type, "__annotations__", {})
    required_keys = getattr(typed_dict_type, "__required_keys__", set())
    optional_keys = getattr(typed_dict_type, "__optional_keys__", set())

    # Check for missing required keys
    missing_keys = required_keys - set(value.keys())
    if missing_keys:
        raise NotAllowedVariableTypeException(
            variable_type=f"dict missing keys: {missing_keys}",
            variable_value=value,
            allowed_types=[typed_dict_type],
        )

    # Check for unexpected keys
    allowed_keys = required_keys | optional_keys
    unexpected_keys = set(value.keys()) - allowed_keys
    if unexpected_keys:
        raise NotAllowedVariableTypeException(
            variable_type=f"dict with unexpected keys: {unexpected_keys}",
            variable_value=value,
            allowed_types=[typed_dict_type],
        )

    # Validate types of present keys
    for key, expected_type in annotations.items():
        if key in value:
            # Unwrap Required/NotRequired wrappers
            actual_type = expected_type
            if hasattr(expected_type, "__origin__"):
                origin = get_origin(expected_type)
                if (
                    origin
                    and hasattr(origin, "__name__")
                    and origin.__name__ in ("Required", "NotRequired")
                ):
                    args = get_args(expected_type)
                    if args:
                        actual_type = args[0]

            try:
                type_validate_or_fail(value[key], actual_type)
            except Exception as e:
                # Handle both NotAllowedVariableTypeException and other exceptions
                error_msg = getattr(e, "variable_type", str(e))
                raise NotAllowedVariableTypeException(
                    variable_type=f"dict key '{key}' has invalid type: {error_msg}",
                    variable_value=value,
                    allowed_types=[typed_dict_type],
                )
