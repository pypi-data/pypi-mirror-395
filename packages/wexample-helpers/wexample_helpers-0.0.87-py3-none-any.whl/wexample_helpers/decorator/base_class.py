from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import attrs

if TYPE_CHECKING:
    from collections.abc import Callable


def base_class(_cls: type | None = None, *, slots: bool = False) -> Callable:
    def wrap(cls: type) -> type:
        return attrs.define(kw_only=True, slots=slots)(cls)

    if _cls is None:
        # usage: @base_class(slots=True)
        return wrap
    else:
        # usage: @base_class
        return wrap(_cls)
