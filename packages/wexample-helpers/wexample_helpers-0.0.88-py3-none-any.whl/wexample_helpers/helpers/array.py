from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


def array_dict_get_by(key: str, value: Any, list_of_dicts: list[dict]) -> dict | None:
    """
    Retrieve a dictionary from a list of dictionaries based on a specific key-value pair.

    :param key: The key to search for in the dictionaries.
    :param value: The value to match for the specified key.
    :param list_of_dicts: The list of dictionaries to search.
    :return: The first dictionary that matches the key-value pair, or None if not found.
    """
    return next((d for d in list_of_dicts if d.get(key) == value), None)


def array_replace_value(
    array: Sequence[Any], search: Any, replacement: Any
) -> list[Any]:
    return [replacement if value == search else value for value in array]


def array_sort_in_place(array: Iterable) -> None:
    try:
        # tomlkit array supports list protocol; rebuild sorted content
        items = [str(x) for x in list(array)]
        items.sort()
        # Clear and re-append to preserve tomlkit node type
        while len(array):
            array.pop()  # type: ignore[attr-defined]
        for it in items:
            array.append(it)  # type: ignore[attr-defined]
    except Exception:
        # Be forgiving; leave as-is on any unexpected structure
        pass


def array_swap(two_items_array: list[Any], do_swap: bool) -> list[Any]:
    if do_swap:
        two_items_array.reverse()

        return two_items_array

    return two_items_array


def array_unique(array: Sequence[Any]) -> list[Any]:
    return list(set(array))
