from __future__ import annotations


def test_attrs_class() -> None:
    from datetime import datetime

    from wexample_helpers.common.debug.debug_dump import DebugDump
    from wexample_helpers.testing.classes.attrs_class import AttrsClass

    # Create instance with some data
    instance = AttrsClass(
        name="test_item",
        count=42,
        description="A test item",
        tags=["test", "debug"],
        created_at=datetime(2025, 3, 5, 15, 46),
    )

    # Dump the instance
    dump = DebugDump(instance)
    dump.execute()
