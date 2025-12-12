from __future__ import annotations


def test_attrs_advanced() -> None:
    from datetime import datetime

    from wexample_helpers.common.debug.debug_dump import DebugDump
    from wexample_helpers.testing.classes.attrs_advanced import (
        AttrsAdvanced,
        Status,
    )

    # Create an instance with various data types
    instance = AttrsAdvanced(
        id="test123",
        status=Status.ACTIVE,
        score=99.999,  # Will be rounded to 100.00
        metadata={"version": "1.0", "enabled": True, "priority": 1},
    )

    # Add some notes
    instance.notes = ["Note 1  ", "  Note 2  "]  # Will be stripped

    # Force creation time for consistent test
    instance._created_at = datetime(2025, 3, 5, 15, 30)

    # Dump the instance
    dump = DebugDump(instance)
    dump.execute()
