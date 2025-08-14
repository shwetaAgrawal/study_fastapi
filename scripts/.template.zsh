# Project-local zsh loader (Option A)
# Sources all zsh snippets in ./shell/zsh when the shell starts from this project.
# Safe: does nothing if directory not present.

# Resolve the absolute directory of this loader file, even when sourced
PROJECT_FILE="${(%):-%N}"
PROJECT_DIR="${PROJECT_FILE:A:h}"
SNIPPETS_DIR="$PROJECT_DIR/shell/zsh"

if [[ -d "$SNIPPETS_DIR" ]]; then
  for f in "$SNIPPETS_DIR"/*.zsh(.N); do
    source "$f"
  done
fi
