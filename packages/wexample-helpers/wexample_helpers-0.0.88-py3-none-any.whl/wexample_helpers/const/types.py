from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from re import Match
from typing import (
    Any,
    Optional,
    TypeAlias,
    TypedDict,
    Union,
)

AnyList = list[Any]
StringKeysDict = dict[str, Any]
StringKeysMapping = Mapping[str, Any]
StringsDict = dict[str, str]
StringsList = list[str]
SetList = set[str]
StringsMatch = Match[str]
Scalar = str | int | float | bool | None
BasicValue = Scalar | AnyList | StringKeysDict
StructuredData: TypeAlias = (
    Scalar | Sequence["StructuredData"] | Mapping[str, "StructuredData"]
)
JsonContent: StructuredData
PathOrString = Union[Path, str]

AnyCallable = Callable[..., Any]
Args = Any
DecoratedCallable = Callable[..., AnyCallable]
Kwargs = Any
ResponsePrintType = Optional[Scalar | StringKeysDict | AnyList]
StringMessageParameters = StringKeysDict

FileStringOrPath = Union[str, Path]

# Version types
# filestate: python-constant-sort
UPGRADE_TYPE_ALPHA: str = "alpha"
UPGRADE_TYPE_BETA: str = "beta"
UPGRADE_TYPE_DEV: str = "dev"
UPGRADE_TYPE_INTERMEDIATE: str = "intermediate"
UPGRADE_TYPE_MAJOR: str = "major"
UPGRADE_TYPE_MINOR: str = "minor"
UPGRADE_TYPE_NIGHTLY: str = "nightly"
UPGRADE_TYPE_RC: str = "rc"
UPGRADE_TYPE_SNAPSHOT: str = "snapshot"

VERSION_PRE_BUILD_NUMBER: int = 0


class VersionDescriptor(TypedDict):
    intermediate: int | None
    major: int | None
    minor: int | None
    pre_build_number: int | None
    pre_build_type: str | None
