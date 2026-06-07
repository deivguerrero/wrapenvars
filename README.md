# wrapenvars

Encode and decode base64 strings — a tiny, zero-dependency Python utility for
obfuscating configuration values, environment variables, or any string data.

[![PyPI](https://img.shields.io/pypi/v/wrapenvars)](https://pypi.org/project/wrapenvars/)
[![Python](https://img.shields.io/pypi/pyversions/wrapenvars)](https://pypi.org/project/wrapenvars/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Installation

```bash
pip install wrapenvars
```

Requires Python **3.12.13+** (< 3.14).

## Usage

```python
from wrapenvars import get_dict, get_str, set_dict, set_str

# ── Strings ─────────────────────────────────────
encoded = set_str("hello world")
# → "aGVsbG8gd29ybGQ="

decoded = get_str(encoded)
# → "hello world"

# ── Dictionaries ────────────────────────────────
token = set_dict({"api_key": "sk-abc123", "region": "us-east-1"})
# → "eyJhcGlfa2V5IjogInNr..."

config = get_dict(token)
# → {"api_key": "sk-abc123", "region": "us-east-1"}
```

### API

| Function | Input | Output | On failure |
|----------|-------|--------|------------|
| `set_str(stream: str)` | Plain string | Base64-encoded string | `""` |
| `get_str(stream: str)` | Base64 string | Decoded string | `""` |
| `set_dict(stream: dict)` | Dictionary | Base64-encoded JSON | `""` |
| `get_dict(stream: str)` | Base64 string | Decoded dictionary | `{}` |

All functions handle invalid input gracefully — they return a safe default
instead of raising exceptions.

## Development

```bash
git clone https://github.com/deivguerrero/wrapenvars.git
cd wrapenvars

# Create venv and install dev dependencies
uv sync

# Run tests
uv run pytest

# Lint + type-check
uv run ruff check --fix
uv run mypy --strict wrapenvars tests

# Format
uv run ruff format
```

### Pre-commit hooks

```bash
pre-commit install
```

Runs `ruff` (lint + format), `mypy`, and basic file checks on every commit.

## License

MIT — see [LICENSE](LICENSE).
