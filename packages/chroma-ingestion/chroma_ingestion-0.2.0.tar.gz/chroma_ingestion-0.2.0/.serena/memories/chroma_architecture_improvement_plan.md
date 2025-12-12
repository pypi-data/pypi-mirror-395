# Chroma Architecture Improvement Plan (summary)

Created: 2025-12-03
Source: `/home/ob/Development/Tools/chroma/docs/ARCHITECTURE_IMPROVEMENT_PLAN.md`

Summary:
- Purpose: Modernize the Chroma code ingestion project into a maintainable, testable Python package aligned with modern best practices (johnthagen/python-blueprint + chroma-core patterns).
- Key goals: Standardize project structure, add testing/type-checking/linting automation, enable packaging + CLI, archive legacy scripts, add CI.

Critical changes proposed:
- Adopt `src/chroma_ingestion/` package (avoid name collisions with chromadb).
- Add `pyproject.toml` metadata, dev dependencies (`nox`, `pytest`, `mypy`, `ruff`, `mkdocs`).
- Add `noxfile.py`, `.pre-commit-config.yaml`, and GitHub Actions CI.
- Create `tests/` with `unit` and `integration` partitions and `conftest.py` fixtures.
- Move examples to `examples/` and archive one-off scripts to `archive/` or `docs/archive/`.
- Provide CLI via `click` and `project.scripts` entrypoint (`chroma-ingest`).

Migration phases & success criteria:
- Phase 1: Foundation (pyproject, nox, pre-commit)
- Phase 2: Package restructure (rename, move modules, update imports)
- Phase 3: Test organization (move tests, add unit tests)
- Phase 4: Cleanup & archive
- Phase 5: CI/CD setup

Success criteria:
- All code under `src/chroma_ingestion/`.
- `uv run nox -s test` passes; `uv run nox -s type_check` passes; `uv run nox -s lint` passes.
- CLI `chroma-ingest` available and docs build with MkDocs.

Next recommended actions:
1. Run a lightweight migration: add `pyproject.toml` entries and `noxfile.py` (Phase 1).
2. Create package skeleton `src/chroma_ingestion/` and move core modules (Phase 2).
3. Run local `nox` sessions and update imports incrementally.

Context tags: chroma, ingestion, architecture, python-blueprint, migration-plan

Notes:
- Memory stores a brief summary and pointers; full plan is in `docs/ARCHITECTURE_IMPROVEMENT_PLAN.md`.
- Use memory key `chroma_architecture_improvement_plan` to recall plan in future sessions.
