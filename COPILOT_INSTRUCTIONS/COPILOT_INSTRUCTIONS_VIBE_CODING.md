# Vibe Coding (LLM/Agent‑Driven Spike + TDD Flow)

Purpose: Move fast in exploratory spikes with an LLM or agent, while staying one command away from a clean, reviewable change set.

## Contract (quick)
- Inputs: A fuzzy goal or a concrete micro-feature.
- Outputs: Either a discarded spike or a tidy PR built from Red/Green/Refactor steps.
- Success: Instant feedback (watchers green), tiny commits, easy to squash-or-merge.

## Tooling you already have
- Watchers: "watch:all" for tests, Ruff, mypy on save; or run "verify" between commits.
- Guides: Tests.md (placement, factories), TDD.md (R/G/R loop, quality gates), Git Hygiene.md (tiny commits, conventional commits, squash vs merge).
 - Starter: 1.STARTER_PROMPT.md (paste at session start to pin repo guardrails).

## LLM/Agent rules of engagement
- Always follow the four guides: Tests, TDD, Git Hygiene, Vibe (this file).
- Start each session by pasting the Starter Prompt; keep these constraints active:
  - Tests‑first unless explicitly in a short spike; convert spikes to tests quickly.
  - Minimal diffs only; respect file placement rules and the Proposed Test Cases comment.
  - After each step: list files changed, summarize deltas, propose a conventional commit message, and list the next micro‑steps.
- Editing scope:
  - Red: modify tests only; update Proposed Test Cases.
  - Green: minimal src edits to pass; no refactors or bonus features.
  - Refactor: behavior‑preserving cleanups only.
- Verification: ensure tests/types/lint pass (or watchers are green) before suggesting commit text.
- Transparency: before applying changes, enumerate planned edits; after applying, summarize what changed and why.

## Autonomy levels (pick one per session)
- Low: Propose changes and diffs; wait for approval before edits.
- Medium (default): Apply tests and minimal src changes directly; refactors only after confirmation.
- High: Proceed through Red/Green/Refactor autonomously; pause on API changes or broad refactors.

## Two modes

### Mode A: Spike-first (pure vibe)
1) Proof-of-life: implement the thinnest path to see it working (can be a script or minimal function).
2) Convert to tests quickly:
   - Update the "### Proposed Test Cases" comment with planned coverage.
   - Add failing tests only (Red).
3) Minimal src to pass (Green).
4) Refactor safely (Refactor).
5) Decide: squash the spike noise or preserve a clean commit series.

### Mode B: TDD-first (structured vibe)
1) Red: add failing tests for one small behavior.
2) Green: implement the minimum to pass.
3) Refactor: no behavior changes.
4) Repeat in tiny increments.

## Quality gates (green-before-done)
- Tests: `uv run pytest -q`
- Types: `uv run mypy -p example_pkg`
- Lint/format: `uv run ruff check --fix .` and `uv run ruff format .`

## Prompt snippets (LLM‑oriented)
- Red (tests only)
  - "We are in Red. Plan and list the edits. Update the '### Proposed Test Cases' comment and add failing tests for: <behaviors>. Follow Tests.md (placement, factories, parametrization ids). Do not modify src yet. After editing, summarize file deltas and propose a commit message."
- Green (minimal implementation)
  - "We are in Green. Implement only the minimal src changes to pass these tests. No refactors or extras. Keep diffs small and note assumptions. Then run the quality gates (or assume 'verify') and propose a commit message."
- Refactor (safe)
  - "We are in Refactor. Improve names/structure without behavior changes. Confirm ruff/mypy/tests remain green. Summarize changes and propose a commit message."
- Commit helper
  - "Propose a conventional commit message (type(scope): summary <=72 chars) with a one-line why."
- Spike → tests
  - "Convert this working spike into tests per Tests.md. Update/mark Proposed Test Cases and add failing tests first, then guide minimal src changes to pass."

## Safety rails for LLM sessions
- Don’t introduce speculative features; keep scope to the stated goal.
- Avoid reordering unrelated code; preserve style and public APIs unless required.
- Do not add new dependencies without calling it out explicitly.
- Be explicit about assumptions and call out ambiguities before proceeding.
- If a gate fails, attempt up to two targeted fixes; then summarize root cause and options.

## Commit hygiene
- Use tiny conventional commits: test → feat → refactor.
- On spike branches, freely commit WIP, then squash before merge.
- Prefer one topic per PR; use draft PRs early.

## Definition of Done
- Proposed Test Cases updated; new items marked [IMPLEMENTED].
- Watchers or verify flow green (tests, types, lint/format).
- LLM provided: change summary, conventional commit(s), and next micro‑steps.
- Squash vs merge decision recorded (spike branches are usually squashed).

## Try it
```bash
# Start a short-lived spike branch
git checkout -b spike/math-overflow

# Run watchers for instant feedback
# (or use one-shot: uv run pytest -q, uv run mypy -p example_pkg, ruff checks)

# 1) Spike a minimal behavior in src/example_pkg/math_utils.py
# 2) Convert to tests in tests/example_pkg/test_math_utils.py
# 3) Red → Green → Refactor with tiny commits

# When satisfied
git rebase -i origin/main  # clean up noisy commits if needed
git push -u origin HEAD
```

## Notes
- Keep scope very small—5–15 minutes per loop if possible.
- Prefer factories for test data to keep spikes easy to translate into tests.
- If a spike dead-ends, delete the branch; if it’s promising, distill and keep.
