# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-06-07

### Changed
- **Build system**: Migrated from Poetry to uv with PEP 621 (`hatchling` builder).
- **Python**: Bumped minimum version from `^3.8` to `>=3.12.13, <3.14`.
- **Dev tooling**: Replaced `black` and `flake8` with `ruff` (lint + format) and `mypy` (strict type checking).
- **Code modernization**: Refactored `wrapenvars/__init__.py` with Python 3.12 idioms — direct imports, `cast()` for `json.loads` return type, explicit exception types (`UnicodeError`, `TypeError`, `AttributeError`, `binascii.Error`, `json.JSONDecodeError`, `ValueError`), and google-style docstrings.

### Added
- **Test suite**: 24 pytest tests covering all four public functions, edge cases (None, bytes, unicode, large strings/dicts), and graceful failure paths.
- **Root `.gitignore`**: Excludes bytecode, caches, virtual environments, IDE files, and `.atl/` (contains machine-local paths).

### Removed
- `poetry.lock` — replaced by `uv.lock`.

### Security
- `.atl/skill-registry.md` excluded from git tracking (contained absolute home paths).

## [0.1.0] — 2021

### Added
- Initial release published to PyPI.
- `set_str`, `get_str`, `set_dict`, `get_dict` functions for base64 encoding/decoding.
