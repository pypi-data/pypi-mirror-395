from __future__ import annotations


def test_property_class() -> None:
    from wexample_helpers.common.debug.debug_dump import DebugDump
    from wexample_helpers.testing.classes.property_class import PropertyClass

    # Create instance
    instance = PropertyClass()

    # Set value through property
    instance.value = "test"

    # Dump the instance
    dump = DebugDump(instance)
    dump.execute()
