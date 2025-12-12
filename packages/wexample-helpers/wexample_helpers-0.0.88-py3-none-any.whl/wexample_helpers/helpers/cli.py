from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wexample_helpers.const.types import PathOrString


def cli_argument_convert_value(value: str, target_type: type) -> Any:
    """
    Convert an argument value to the target type.
    """
    if target_type == bool:
        return value.lower() in ("true", "yes", "y", "1")
    elif target_type == int:
        return int(value)
    elif target_type == float:
        return float(value)
    elif target_type == str:
        return value
    elif target_type == list:
        # Assume comma-separated values
        return [item.strip() for item in value.split(",")]
    else:
        # For custom types, try to use the constructor
        return target_type(value)


def cli_make_clickable_path(
    path: PathOrString, short_title: bool | PathOrString = False
) -> str:
    from pathlib import Path

    if short_title is True:
        display_text = Path(path).name
    elif short_title is False:
        display_text = path
    else:
        display_text = str(short_title)

    # \033]8;;file://{path}\033\\  : Link start
    # \033]8;;\033\\              : Link end
    return f"\033]8;;file://{path}\033\\{display_text}\033]8;;\033\\"
