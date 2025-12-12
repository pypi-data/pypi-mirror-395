from __future__ import annotations

from enum import Enum


class ErrorTruncateRule:
    def __init__(
        self,
        truncate_after_module: str | None = None,
        truncate_after_file: str | None = None,
        truncate_stack_count: int | None = None,
    ) -> None:
        self.truncate_after_module = truncate_after_module
        self.truncate_after_file = truncate_after_file
        self.truncate_stack_count = truncate_stack_count


class ErrorTruncateRules(Enum):
    PYDANTIC = ("pydantic.", ErrorTruncateRule(truncate_after_module="pydantic"))

    def __init__(self, module_prefix: str, rule: ErrorTruncateRule) -> None:
        self.module_prefix = module_prefix
        self.rule = rule
