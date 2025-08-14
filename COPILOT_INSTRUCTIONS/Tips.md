Follow:
COPILOT_INSTRUCTIONS_TESTS.md (placement rules, Proposed Test Cases, factories)
COPILOT_INSTRUCTIONS_TDD.md (Red/Green/Refactor loop, quality gates)
COPILOT_INSTRUCTIONS_GIT_HYGIENE.md (tiny commits, conventional commits, squash vs merge)
Constraints:
Start tests-first unless this is a spike; for spikes, convert to tests ASAP
Keep changes minimal; no speculative features; respect file placement rules
After each step, suggest a conventional commit message and list next micro-steps

----------------------------------------------------------------------
Tip: Keep those three files open side-by-side as your “rules of engagement.”

vibe coding loop
Setup once per spike

Branch: spike/<topic> (or feat/<topic> if you already know the shape)
Start watchers: “watch:all” (fast feedback) or run “verify” between commits
Mode A: Spike-first (pure vibe)

Proof-of-life (minimal script or function) to validate the idea
Convert immediately to tests:
Update “### Proposed Test Cases” comment with planned coverage
Add failing tests only (Red)
Minimal src to pass (Green)
Refactor safely (Refactor)
Commits: test → feat → refactor (see Git Hygiene)
If spike got noisy, squash before PR
Mode B: TDD-first (structured vibe)

Red: add failing tests (use factories, parametrization ids)
Green: minimal code to pass tests
Refactor: no behavior change
Repeat with tiny scope


Red (tests only)

“Update the ‘### Proposed Test Cases’ comment and add failing tests for: <behaviors>. Follow COPILOT_INSTRUCTIONS_TESTS.md (placement, factories, parametrization with ids). Don’t modify src yet.”
Green (minimal implementation)

“Implement only the minimal src changes to pass the new tests. No refactors or bonus features. Keep diffs small and call out any assumptions.”
Refactor (no behavior change)

“Refactor for clarity/DRY only. Ensure ruff/mypy/tests still pass per the TDD quality gates.”
Commit helper

“Propose a conventional commit message for this change (type(scope): summary, <=72 chars) with a one-line ‘why’ body.”
Spike → tests conversion

“Convert this working spike into tests per COPILOT_INSTRUCTIONS_TESTS.md. Add/mark items in the Proposed Test Cases, then guide a minimal src change to pass.”

Using the guides at each step
Tests guide (Tests.md)

Use it when writing/placing tests, drafting Proposed Test Cases, and choosing factory fixtures vs local fixtures.
TDD guide (TDD.md)

Use it to keep you in Red/Green/Refactor and to enforce quality gates:
uv run pytest -q
uv run mypy -p example_pkg
uv run ruff check --fix . && uv run ruff format .
Git Hygiene (GIT_HYGIENE.md)

Use it to keep commits tiny, messages conventional, and choose squash vs merge:
Squash noisy spike branches
Preserve a clean Red/Green/Refactor series when it tells a good story

Definition of done (quick gate)
Proposed Test Cases updated; new items tagged [IMPLEMENTED]
Watchers or “verify” all green (tests, types, lint/format)
Conventional commit message prepared
If it started as a spike: either squash to a tidy PR or discard the branch cleanly
