# Git Hygiene for Flow Coding

Purpose: Keep your iteration “vibes” high while producing reviewable, traceable history.

## Contract (quick)
- Inputs: Local repo with active feature work.
- Outputs: Small, meaningful commits with clear messages; PR structured for easy review.
- Success: Reviewers can follow intent; CI is green; merges produce clean history.

## Core Principles
1) Small scopes
- Change one thing per commit (tests first, then minimal code, then refactor).
- Avoid mixing formatting/lint-only changes with logic; commit them separately.

2) Conventional commits (lightweight)
- Format: `<type>(optional-scope): <summary>`
- Common types: feat, fix, docs, style, refactor, test, chore, perf, build, ci.
- Keep summary under ~72 chars; add body when explaining “why”.

3) Red/Green/Refactor sets
- Red: failing tests that capture intended behavior.
- Green: minimal code to pass those tests.
- Refactor: improve structure without changing behavior.
- Prefer 2–3 commits per micro-feature following this sequence.

4) PR etiquette
- One topic per PR; draft early; push often.
- Keep PRs < ~300 lines if possible; attach screenshots or logs.
- Use checklists; call out risky bits and test coverage.

## Day-to-day Loop
1. Start a feature branch
```bash
git checkout -b feat/<short-topic>
```
2. Red commit (tests only)
```bash
git add -p
git commit -m "test(<scope>): specify behavior for <thing>"
```
3. Green commit (minimal implementation)
```bash
git add -p
git commit -m "feat(<scope>): implement minimal logic for <thing>"
```
4. Refactor commit (no behavior change)
```bash
git add -p
git commit -m "refactor(<scope>): simplify <area> without changing behavior"
```
5. Sync & push
```bash
git rebase main
git push -u origin HEAD
```

Tip: Use `git add -p` to stage intentionally and keep commits tight.

## Squash vs Merge
- Squash merge:
  - Pros: compact history on main; great for PRs with many micro-commits.
  - Cons: loses individual Red/Green/Refactor steps on main.
  - Use when: the PR has many tiny commits or noisy interim work.
- Merge commit (no squash):
  - Pros: preserves the commit series (useful for archaeology, bisect).
  - Cons: can clutter main if commits are too granular.
  - Use when: commit series tells a clear story (clean Red/Green/Refactor).

Practical rule: Prefer squash for feature branches with noisy commit history; keep full merges for polished sequences.

## Commit Message Patterns (examples)
- feat(math): add add(a,b) overflow handling
- fix(logger): avoid duplicate handlers in get_logger
- test(math): cover negative inputs for add
- refactor(logging): extract formatter builder
- docs(readme): link Testing & TDD guides
- chore(ci): cache uv between jobs

Body examples:
```
Motivation: clarify failure mode when inputs overflow platform ints.
Notes: kept branch coverage; added parametrized tests for boundaries.
``` 

## Safety Nets
- Run the "verify" task locally before pushing (ruff, mypy, tests).
- Use pre-commit hooks to catch style issues early.
- Rebase frequently to keep diffs small and resolve conflicts early.

## Optional: Lightweight Rebase & Cleanup
- Combine noisy fixups locally before opening PR:
```bash
git rebase -i origin/main
# mark small fixes as "fixup" or squash into their parent commit
```
- Keep only meaningful commits; avoid "wip" on shared branches.

## Try it (suggested flow)
```bash
git checkout -b feat/logging-json-levels
# Red
#  - write failing tests in tests/example_pkg/test_logging_utils.py
uv run pytest -q
git add -p
git commit -m "test(logging): specify JSON debug output format"
# Green
#  - implement minimal change in src/example_pkg/logging_utils.py
uv run pytest -q
git add -p
git commit -m "feat(logging): support JSON debug log formatting"
# Refactor
uv run ruff check --fix . && uv run ruff format .
uv run mypy -p example_pkg
git add -p
git commit -m "refactor(logging): tidy formatter creation"
# Push
git rebase main
git push -u origin HEAD
```

## Notes
- Favor clarity over strict adherence to any one convention.
- If CI is red, fix forward quickly or revert the faulty commit.
- Communicate intent in PR descriptions; link issues and designs when relevant.
