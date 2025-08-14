# LLM-Oriented Test-Driven Development (TDD)

These steps guide an AI assistant (or a developer) to write tests first and then implement just enough code to pass them, while preserving repo conventions and minimizing churn.

## TDD Loop (for LLMs)
1) Red: Add or update tests to define behavior
    - Create/extend tests under `tests/` first.
    - Use the “### Proposed Test Cases” section to list planned cases and mark `[IMPLEMENTED]` as you go.
    - Prefer factory fixtures for test data; avoid copy-paste.

2) Run watchers for fast feedback
    - Use the task "watch:all" to run tests, lint, and mypy continuously.
    - For one-shot checks, run "verify".

3) Green: Implement minimal code to pass
    - Add/change code in `src/` only to satisfy failing tests.
    - Keep changes as small as possible; avoid speculative features.

4) Refactor: Improve design safely
    - Clean up duplication; improve names and structure.
    - Keep tests passing; update tests when intent changes (not for implementation details).

## Editing Scope Exceptions (for TDD)
- The default rule is to modify only `tests/`. In TDD, you are allowed to modify `src/` to implement the minimal code required for the tests to pass.
- Do not break public APIs without updating tests and documenting the change in the PR description.
- Keep each change atomic: tests first, then minimal src changes.

## Practical Tips for LLM-Driven TDD
- Start with the simplest, most observable behavior; avoid complex integration first.
- Use factory fixtures to build inputs; prefer parametrization with `ids=` for readability.
- Patch environment/time/IO using `monkeypatch`, `tmp_path`, `caplog`, `capsys`.
- Keep unit tests hermetic: no network, no real FS unless explicitly marked `@pytest.mark.integration`.
- Treat style/type errors as first-class: run Ruff and mypy (watchers or verify task) until green.

## Quality Gates (Green-before-Done)
- Tests: `uv run pytest -q` (or "watch:pytest")
- Types: `uv run mypy -p example_pkg` (or "watch:mypy")
- Lint/format: `uv run ruff check --fix .` and `uv run ruff format .` (or watchers)
- Optional: Coverage `uv run pytest -q --cov --cov-report=term-missing`

## Structure and Commit Hygiene
- Keep the "### Proposed Test Cases" section updated in each test file; mark implemented items.
- Commit series:
  - commit 1: tests (failing) – Red
  - commit 2: minimal src code – Green
  - commit 3: refactor (no behavior change) – Refactor
- Avoid mixing unrelated changes; small, focused commits help reviewers and tools.

## Example Minimal TDD Flow
1. Add tests for `add(a, b)` overflow or type validation to `tests/example_pkg/test_math_utils.py`.
2. Run watchers; observe failures.
3. Implement/adjust code in `src/example_pkg/math_utils.py` to satisfy tests.
4. Re-run verify; ensure Ruff/mypy/tests pass.
5. Refactor for clarity; keep tests green.
