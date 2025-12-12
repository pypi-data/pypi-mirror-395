from __future__ import annotations

import json
import os
from typing import Any

from wexample_helpers.const.types import PathOrString


def json_load(path: PathOrString) -> list[Any] | dict[Any, Any]:
    with open(path) as f:
        return json.load(f)


def json_load_if_valid(path: PathOrString) -> Any | bool:
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return False
    return False


def json_parse_if_valid(json_data: PathOrString, default: any = False) -> Any:
    try:
        return json.loads(json_data)
    except:
        return default
