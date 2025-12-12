from __future__ import annotations

from typing import Any

import pytest


class AbstractTestHelpers:
    def _test_type_validate_or_fail(
        self,
        success_cases: list[tuple[Any, Any]] = None,
        failure_cases: list[tuple[Any, Any]] = None,
    ) -> None:
        from wexample_helpers.exception.not_allowed_variable_type_exception import (
            NotAllowedVariableTypeException,
        )
        from wexample_helpers.helpers.type import type_validate_or_fail

        # Success cases: should not raise exceptions
        for value, expected_type in success_cases or []:
            type_validate_or_fail(
                value=value,
                allowed_type=expected_type,
            )

        # Failure cases: should raise a validation exception
        for value, expected_type in failure_cases or []:
            with pytest.raises(NotAllowedVariableTypeException):
                type_validate_or_fail(
                    value=value,
                    allowed_type=expected_type,
                )
