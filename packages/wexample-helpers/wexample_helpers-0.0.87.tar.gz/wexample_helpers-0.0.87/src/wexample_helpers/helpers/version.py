from __future__ import annotations

import re
from typing import TYPE_CHECKING

from wexample_helpers.const.types import (
    UPGRADE_TYPE_MINOR,
)

if TYPE_CHECKING:
    from wexample_helpers.const.types import StringsList, VersionDescriptor


def is_greater_than(
    first: VersionDescriptor, second: VersionDescriptor, true_if_equal: bool = False
) -> bool:
    keys_to_check: StringsList = [
        "major",
        "intermediate",
        "minor",
        "pre_build_type",
        "pre_build_number",
    ]

    for key in keys_to_check:
        first_value = first.get(key, None)
        second_value = second.get(key, None)

        if first_value is not None and second_value is None:
            return False
        elif first_value is None and second_value is not None:
            return True

        if first_value is not None and second_value is not None:
            assert isinstance(first_value, int)
            assert isinstance(second_value, int)
            if first_value < second_value:
                return False
            elif first_value > second_value:
                return True

    return true_if_equal


def version_increment(
    version: str,
    type: str = UPGRADE_TYPE_MINOR,
    increment: int = 1,
    build: bool | str = False,
) -> str:
    from wexample_helpers.const.types import (
        UPGRADE_TYPE_ALPHA,
        UPGRADE_TYPE_BETA,
        UPGRADE_TYPE_DEV,
        UPGRADE_TYPE_INTERMEDIATE,
        UPGRADE_TYPE_MAJOR,
        UPGRADE_TYPE_NIGHTLY,
        UPGRADE_TYPE_RC,
        UPGRADE_TYPE_SNAPSHOT,
    )

    version_dict = version_parse(version)
    if not version_dict:
        raise ValueError(f"Invalid version format: {version}")

    # Increment according to type
    if type == UPGRADE_TYPE_MAJOR:
        version_dict["major"] = int(version_dict["major"]) + increment
        version_dict["intermediate"] = 0
        version_dict["minor"] = 0
    elif type == UPGRADE_TYPE_INTERMEDIATE:
        version_dict["intermediate"] = int(version_dict["intermediate"]) + increment
        version_dict["minor"] = 0
    elif type == UPGRADE_TYPE_MINOR:
        version_dict["minor"] = int(version_dict["minor"]) + increment
    # Any of pre-build version
    elif type in [
        UPGRADE_TYPE_ALPHA,
        UPGRADE_TYPE_BETA,
        UPGRADE_TYPE_DEV,
        UPGRADE_TYPE_RC,
        UPGRADE_TYPE_NIGHTLY,
        UPGRADE_TYPE_SNAPSHOT,
    ]:
        version_dict["pre_build_type"] = type
        version_dict["pre_build_number"] = increment

    return version_join(version_dict, build)


def version_join(version: VersionDescriptor, add_build: bool | str = False) -> str:
    output = f"{version['major']}.{version['intermediate']}.{version['minor']}"

    # Build version string
    if version["pre_build_type"]:
        output += f'-{version["pre_build_type"]}.{version["pre_build_number"]}'

    if add_build:
        if isinstance(add_build, str):
            output += f"+build.{add_build}"
        else:
            import datetime

            output += f"+build." + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    return output


def version_parse(version: str) -> VersionDescriptor | None:
    pre_build_number: int | None = None
    pre_build_type: str | None = None

    try:
        # Handle 1.0.0-beta.1+build.1234
        if "-" in version:
            base_version, pre_build = version.split("-")

            if "." in pre_build:
                pre_build_parts = pre_build.split(".")
                pre_build_type = pre_build_parts[0]

                # pre_build_number can be : 1+build.1234
                if "+" in pre_build_parts[1]:
                    pre_build_number_str, build_metadata = pre_build_parts[1].split("+")
                    pre_build_number = (
                        int(pre_build_number_str) if pre_build_number_str else None
                    )
                else:
                    pre_build_number = (
                        int(pre_build_parts[1]) if pre_build_parts[1] else None
                    )

        base_parts = version.split("-")[0].split(".")
        for part in base_parts:
            if part and not part.isdigit():
                return None

        match = re.match(r"(\d+)?\.?(\d+)?\.?(\d+)?([-.+].*)?", version)
        if not match:
            return None

        major, intermediate, minor, _ = match.groups()

        if not (major or intermediate or minor):
            return None

        # Create a dictionary to store the elements
        version_dict: VersionDescriptor = {
            "major": int(major) if major else None,
            "intermediate": int(intermediate) if intermediate else None,
            "minor": int(minor) if minor else None,
            "pre_build_type": pre_build_type,
            "pre_build_number": pre_build_number,
        }
    except Exception:
        return None

    return version_dict
