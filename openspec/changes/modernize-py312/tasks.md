# Tasks: Modernize to Python 3.12 & uv

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~130 reviewable + lock files (~420 auto-generated) |
| 400-line budget risk | Medium |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 → PR 2 |
| Delivery strategy | force-chained |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: stacked-to-main
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Build system: Poetry → uv, PEP 621, Python >=3.12.13, correct dev-deps | PR 1 | ~102 review lines + lock file churn |
| 2 | Code modernization + pre-commit mypy hook | PR 2 | ~20 review lines; base = main after PR 1 merges |

## Phase 1: Build System Migration (PR 1)

- [x] 1.1 Rewrite `pyproject.toml`: replace `[tool.poetry]` with `[project]` (PEP 621, hatchling builder, Python `>=3.12.13,<3.14`), move dev-deps to `[dependency-groups]`, remove `black` and `flake8`, keep `ruff`/`mypy`/`pre-commit`, retain `[tool.ruff]` and `[tool.mypy]` blocks
- [x] 1.2 Run `uv lock` to generate `uv.lock` — verify zero runtime dependencies
- [x] 1.3 Delete `poetry.lock` from working tree
- [x] 1.4 Verify `uv build` produces valid `.whl` and `.tar.gz` in `dist/`

## Phase 2: Code Modernization (PR 2)

- [x] 2.1 Modernize `wrapenvars/__init__.py`: replace aliased imports with `import json` and `import base64`, tighten type hints (`dict[str, Any]` on `set_dict`), replace bare `except Exception: pass` with explicit exception types, drop explicit `"utf8"` encoding args
- [x] 2.2 Run `ruff check --fix && ruff format` — zero changes expected after modernization
- [x] 2.3 Run `mypy --strict wrapenvars` — zero errors
- [x] 2.4 Add `mypy` hook to `.pre-commit-config.yaml` under `ruff` hooks (repo: `https://github.com/pre-commit/mirrors-mypy`, rev: `v2.1.0`)
- [x] 2.5 Run `pre-commit run --all-files` — all hooks pass clean
- [x] 2.6 Run `uv publish --dry-run` — verifies publish readiness
