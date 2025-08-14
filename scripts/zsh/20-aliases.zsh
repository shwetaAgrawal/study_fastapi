# Lightweight, project-scoped aliases

alias p='python3'
alias pt='pytest -q'
alias ruff='ruff --quiet'

# git helpers (only if inside this repo)
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  alias gs='git status -sb'
  alias gp='git pull --rebase --autostash'
  alias gco='git checkout'
fi
