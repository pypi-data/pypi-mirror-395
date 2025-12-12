from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from wexample_helpers.const.types import (
        StringKeysDict,
        StringKeysMapping,
        StringsList,
    )

DICT_PATH_SEPARATOR_DEFAULT = "."
DICT_ITEM_EXISTS_ACTION_ABORT = "abort"
DICT_ITEM_EXISTS_ACTION_MERGE = "merge"
DICT_ITEM_EXISTS_ACTION_REPLACE = "replace"


def dict_get_first_missing_key(
    dictionary: StringKeysMapping, required_keys: StringsList
) -> str | None:
    for key in required_keys:
        if key not in dictionary:
            return key
    return None


def dict_get_item_by_path(
    data: Any,
    key: str,
    default: Any | None = None,
    separator: str = DICT_PATH_SEPARATOR_DEFAULT,
) -> Any:
    from collections.abc import Mapping, Sequence

    for k in key.split(separator):
        if isinstance(data, Mapping) and k in data:
            data = data[k]

        elif isinstance(data, Sequence) and k.isdigit():
            idx = int(k)
            if -len(data) <= idx < len(data):
                data = data[idx]
            else:
                return default

        else:
            return default

    return data


def dict_has_item_by_path(
    data: StringKeysMapping, key: str, separator: str = DICT_PATH_SEPARATOR_DEFAULT
) -> bool:
    # Split the key into its individual parts
    keys = key.split(separator)

    # Traverse the data dictionary using the key parts
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return False

    return True


def dict_interpolate(value: Any, variables: StringKeysDict) -> Any:
    import re

    VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")

    if isinstance(value, dict):
        return {k: dict_interpolate(v, variables) for k, v in value.items()}

    if isinstance(value, list):
        return [dict_interpolate(v, variables) for v in value]

    if isinstance(value, str):

        def repl(match):
            var = match.group(1)
            return variables.get(
                var, f"${{{var}}}"
            )  # si non trouvé → on laisse tel quel

        return VAR_PATTERN.sub(repl, value)

    return value


def dict_merge(*dicts: StringKeysMapping) -> StringKeysDict:
    """
    Recursively merge multiple dictionaries.
    If a key exists in multiple dictionaries, the values are merged recursively.
    The function can take any number of dictionary arguments.

    Note: Only keys of type str are supported; values are Any.
    """
    from wexample_helpers.const.types import StringKeysMapping

    result: StringKeysDict = {}
    for dictionary in dicts:
        for key, value in dictionary.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = dict_merge(
                    cast(StringKeysMapping, result[key]),
                    cast(StringKeysMapping, value),
                )
            else:
                result[key] = copy.deepcopy(value)
    return result


def dict_remove_item_by_path(data: dict[str, Any], key: str) -> None:
    keys = key.split(".")
    for k in keys[:-1]:
        if k not in data or not isinstance(data[k], dict):
            return
        data = data[k]

    data.pop(keys[-1], None)


def dict_set_item_by_path(
    data: dict[str, Any],
    key: str | StringsList,
    value: Any,
    when_exist: str = DICT_ITEM_EXISTS_ACTION_REPLACE,
) -> None:
    from wexample_helpers.const.types import StringsList

    # Allow pre-split to escape non-separator dots, like in file names.
    if isinstance(key, list):
        keys = cast(StringsList, key)
    else:
        keys = key.split(".")

    for k in keys[:-1]:
        data = data.setdefault(k, {})

    final_key = keys[-1]
    if final_key in data and when_exist != DICT_ITEM_EXISTS_ACTION_REPLACE:
        if when_exist == DICT_ITEM_EXISTS_ACTION_ABORT:
            return
        elif (
            when_exist == DICT_ITEM_EXISTS_ACTION_MERGE
            and isinstance(data[final_key], dict)
            and isinstance(value, dict)
        ):
            data[final_key] = dict_merge(data[final_key], value)
    else:
        data[final_key] = value


def dict_sort_values(
    dictionary: StringKeysMapping, key: Any | None = None
) -> StringKeysDict:
    return {
        k: v for k, v in sorted(dictionary.items(), key=key or (lambda item: item[1]))
    }
