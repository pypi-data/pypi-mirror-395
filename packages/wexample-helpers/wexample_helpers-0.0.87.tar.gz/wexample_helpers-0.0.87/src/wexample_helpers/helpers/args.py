from __future__ import annotations

import ast
import inspect
import re
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from wexample_helpers.const.types import (
        AnyCallable,
        BasicValue,
        StringKeysDict,
        StringsList,
    )


def args_convert_dict_to_snake_dict(input_dict: dict[str, Any]) -> dict[str, Any]:
    from wexample_helpers.helpers.string import string_to_snake_case

    return {string_to_snake_case(key): value for key, value in input_dict.items()}


def args_in_function(function: AnyCallable, arg_name: str) -> bool:
    return arg_name in inspect.signature(function).parameters


def args_is_basic_value(value: Any) -> bool:
    """
    Check if the value is compatible with basic YAML types
    """
    from wexample_helpers.const.types import Scalar

    if isinstance(value, Scalar):
        return True

    elif isinstance(value, list):
        return all(args_is_basic_value(item) for item in value)

    elif isinstance(value, dict):
        return all(
            isinstance(key, str) and args_is_basic_value(val)
            for key, val in value.items()
        )

    else:
        return False


def args_parse_dict(arg: str) -> StringKeysDict:
    arg_dict = args_parse_one(arg, {})

    if not isinstance(arg_dict, dict):
        return {}

    return arg_dict


def args_parse_list(arg: str) -> StringsList:
    from wexample_helpers.const.types import StringsList

    arg_list = args_parse_one(arg, [])

    if not isinstance(arg_list, list):
        return []

    assert isinstance(arg_list, list)

    return cast(StringsList, arg_list)


def args_parse_list_or_strings_list(arg: str) -> StringsList:
    if arg.startswith("[") and arg.endswith("]"):
        return args_parse_list(arg)

    return arg.split()


def args_parse_one(argument: str, default: Any | None = None) -> BasicValue:
    from wexample_helpers.const.types import BasicValue

    if argument is None or argument == "":
        return default

    try:
        parsed = ast.literal_eval(argument)
        if args_is_basic_value(parsed):
            return cast(BasicValue, parsed)
        return default
    except (ValueError, SyntaxError):
        return argument


def args_push_one(arg_list: list[str], arg_name: str, value: Any | None = None) -> None:
    arg_list.append(f"--{arg_name}")

    if value is not None:
        arg_list.append(str(value))


def args_replace_one(
    arg_list: list[str],
    arg_name: str,
    value: Any | None = None,
    is_flag: bool = False,
) -> str | bool | None:
    previous = args_shift_one(arg_list=arg_list, arg_name=arg_name, is_flag=is_flag)

    args_push_one(arg_list=arg_list, arg_name=arg_name, value=value)

    return previous


def args_shift_one(
    arg_list: list[str], arg_name: str, is_flag: bool = False
) -> str | bool | None:
    """
    Alter arg list by removing arg names and returning arg value.
    Take arg name without dash, and remove args with any count of prefixed dashes.
    """
    arg_pattern = re.compile(r"(-+)" + re.escape(arg_name) + r"$")

    for i, arg in enumerate(arg_list):
        if isinstance(arg, str) and arg_pattern.match(arg):
            del arg_list[i]

            if is_flag:
                return True
            else:
                try:
                    next_value = arg_list.pop(i)
                    return next_value
                except IndexError:
                    return None
    return None


def args_split_arg_array(arg: str | Iterable[str], separator: str = ",") -> StringsList:
    from collections.abc import Iterable

    if not arg:
        return []

    if isinstance(arg, str):
        arg = re.sub(r'[\[\]"\']', "", arg)

        # The array was empty.
        if not arg:
            return []

        return [item.strip() for item in arg.split(separator)]
    elif isinstance(arg, Iterable):
        return [item.strip() for item in arg]
