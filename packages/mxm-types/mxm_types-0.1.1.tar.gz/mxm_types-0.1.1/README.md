# `mxm-types`

![Version](https://img.shields.io/github/v/release/moneyexmachina/mxm-types)
![License](https://img.shields.io/github/license/moneyexmachina/mxm-types)
![Python](https://img.shields.io/badge/python-3.13+-blue)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)

Shared typing primitives for the Money Ex Machina ecosystem.

`mxm-types` provides a canonical, dependency-free set of JSON/path aliases and micro-protocols used across MXM packages.  
It is intentionally small, stable, and domain-agnostic. All domain models live in their respective packages.

## Install

```bash
pip install mxm-types
```

## Overview

`mxm-types` defines:

- **Strict JSON tree types** for use across configuration, metadata, requests, and portable data structures.
- **Lightweight aliases** for common patterns (e.g., path-like values).
- **Micro-protocols** for cross-cutting interfaces (e.g., objects with a `get` method).
- **PEP 561 typing support** (`py.typed` included in the wheel).

The package has **no runtime dependencies**.

## Public API

The following names form the stable public API of `mxm-types`.  
All other names are private and may change across releases.

### JSON Types

| Name          | Description |
|---------------|-------------|
| `JSONScalar`  | `str \| int \| float \| bool \| None` |
| `JSONValue`   | Strict recursive JSON tree: scalars, `list[JSONValue]`, `dict[str, JSONValue]` |
| `JSONLike`    | Permissive tree for accepting general `Sequence`/`Mapping` inputs |
| `JSONObj`     | `Mapping[str, JSONValue]` — preferred for function parameters |
| `JSONMap`     | `dict[str, JSONValue]` — preferred for concrete, mutable results |
| `HeadersLike` | Canonical alias for HTTP Header Mappping. |

### Paths

| Name       | Description |
|------------|-------------|
| `StrPath`  | `str \| PathLike[str]` |

### Protocols and TypedDicts

| Name               | Description |
|--------------------|-------------|
| `KVReadable`       | Minimal protocol: objects exposing a `get(key, default)` method |
| `CLIFormatOptions` | Optional formatting hints for CLI output (`"plain" \| "rich" \| "json"`) |

---

## Usage

```python
from mxm.types import (
    JSONValue,
    JSONObj,
    JSONMap,
    StrPath,
    KVReadable,
    CLIFormatOptions,
)

def load_metadata(path: StrPath) -> JSONObj:
    ...
```

For permissive JSON acceptance (e.g., reading config from arbitrary Python structures):

```python
from mxm.types import JSONLike

def normalise(data: JSONLike) -> JSONValue:
    ...
```

## Design Principles

- **Minimal surface**: only house-style primitives, no domain models.  
- **Dependency-free**: safe to import everywhere, including low-level layers.  
- **PEP 695 `type` aliases**: modern, expressive, static-typing-friendly.  
- **Strict JSON encouraged**: permissive types optional and explicit.  

## Development

```bash
poetry install
poetry run ruff check .
poetry run pyright
poetry run pytest -q
poetry build
```

## License

MIT License. See [LICENSE](LICENSE).
