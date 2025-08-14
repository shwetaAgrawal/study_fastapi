# Python conveniences for this repo

# Optional auto-activate .venv for this project
# Turn on by setting: export TEMPLATE_AUTO_VENV=1
if [[ -n "$TEMPLATE_AUTO_VENV" && -n "$PROJECT_DIR" && -z "$VIRTUAL_ENV" ]]; then
  if [[ -f "$PROJECT_DIR/.venv/bin/activate" ]]; then
    source "$PROJECT_DIR/.venv/bin/activate"
  fi
fi

# Add src to PYTHONPATH if present
if [[ -n "$PROJECT_DIR" && -d "$PROJECT_DIR/src" ]]; then
  export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"
fi
