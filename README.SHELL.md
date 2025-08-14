Template-local Zsh setup

This template ships small, non-invasive zsh snippets you can opt into. They only load when your shell is started from this template (or when our loader is sourced explicitly).

Files:
- .template.zsh: loader that sources all ./shell/zsh/*.zsh
- shell/zsh/10-env.zsh: environment tweaks (PATH for .venv, uv completions)
- shell/zsh/20-aliases.zsh: handy aliases (python, pytest, git helpers)
- shell/zsh/30-python.zsh: Python niceties (optional .venv auto-activate)
- .zshrc.example: sample Oh My Zsh config you can copy/adapt
- .envrc: direnv configuration for automatic env on cd

How to enable (Option A: ~/.zshrc loader, recommended):
1) Open your ~/.zshrc and ensure Oh My Zsh loads first:
   source $ZSH/oh-my-zsh.sh

2) Add this block AFTER that line:

   # --- Begin template loader ---
   _try_source_template() {
     # Find git root; fallback to $PWD
     local root
     if command -v git >/dev/null 2>&1; then
       root="$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null)" || root="$PWD"
     else
       root="$PWD"
     fi
     local candidate="$root/.template.zsh"
     [[ -r "$candidate" ]] && source "$candidate"
   }
   _try_source_template
   # --- End template loader ---

3) Optional toggles in ~/.zshrc:
   export TEMPLATE_AUTO_VENV=1   # auto-activate .venv when present

Option B: Direnv auto-load (no ~/.zshrc edits)
- Requirements: direnv installed and hooked into your shell.

Steps:
1) Install direnv (macOS):
   brew install direnv

2) Hook direnv into zsh (one-time, in ~/.zshrc):
   eval "$(direnv hook zsh)"

3) In the project root, allow the .envrc:
   direnv allow

What .envrc does here:
- Exposes PROJECT_DIR to the shell.
- Adds .venv/bin to PATH if present.
- Sets PYTHONPATH=src so `python -m ...` finds your package.
- Exports TEMPLATE_ENV=1 as a convenient marker.
- Optionally enforces PIP_REQUIRE_VIRTUALENV (commented; enable if desired).

Coexistence and precedence:
- You can use both Option A and direnv. They are complementary.
- If both are active, PATH/PYTHONPATH changes are additive. The loader provides aliases and optional features; .envrc focuses on env wiring.

Uninstall:
- Option A: remove the loader block from ~/.zshrc.
- Direnv: remove/rename .envrc and run `direnv deny` (or remove the hook from ~/.zshrc).
