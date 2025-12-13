"""
Tiny, stable, dependency-free: canonical JSON/path aliases and a micro-protocol
shared across Money Ex Machina packages.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from os import PathLike
from typing import Any, Protocol, TypedDict, runtime_checkable
from typing import Literal  # stricter options for CLIFormatOptions.format

# JSON types ---------------------------------------------------------------------------

# Scalars exactly representable in JSON (+ None)
type JSONScalar = str | int | float | bool | None

# Strict JSON: only list/dict at inner nodes. Best for real JSON round-trips.
type JSONValue = JSONScalar | list[JSONValue] | dict[str, JSONValue]

# Permissive JSON-like: accept any Sequence/Mapping at inner nodes (for inputs).
type JSONLike = JSONScalar | Sequence[JSONLike] | Mapping[str, JSONLike]

# Top-level mapping conveniences
type JSONObj = Mapping[str, JSONValue]  # preferred for params (read-only interface)
type JSONMap = dict[str, JSONValue]  # preferred for concrete, mutable results

type HeadersLike = Mapping[str, str | Sequence[str]]

# Path-like ----------------------------------------------------------------------------

type StrPath = str | PathLike[str]

# Minimal shared protocol(s) -----------------------------------------------------------


@runtime_checkable
class KVReadable(Protocol):
    """Any mapping-like with a `get` method (without requiring full Mapping)."""

    def get(self, key: str, default: Any = ...) -> Any: ...


class CLIFormatOptions(TypedDict, total=False):
    """Optional CLI format hints used across MXM command outputs."""

    format: Literal["plain", "rich", "json"]


__all__ = [
    "CLIFormatOptions",
    "HeadersLike",
    "JSONLike",
    "JSONMap",
    "JSONObj",
    "JSONScalar",
    "JSONValue",
    "KVReadable",
    "StrPath",
]
