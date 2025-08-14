# Environment tweaks specific to this project
# Guard with TEMPLATE_ZSH_ENABLE=1 in your env to activate optional bits

# Minimal prompt project marker (non-invasive)
export TEMPLATE_PROJECT=1

# Example: prefer local bin/.venv paths when present
if [[ -n "$PROJECT_DIR" && -d "$PROJECT_DIR/.venv" ]]; then
  export PATH="$PROJECT_DIR/.venv/bin:$PATH"
fi

# Example: uv completions if available (no-op if uv missing)
if command -v uv >/dev/null 2>&1; then
  eval "$(uv generate-shell-completion zsh)"
fi
