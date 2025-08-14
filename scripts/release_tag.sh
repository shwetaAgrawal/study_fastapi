#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/release_tag.sh v0.1.0
# Tags current commit with the provided version and pushes the tag.

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-tag> (e.g., v0.1.0)" >&2
  exit 1
fi

tag="$1"

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Please commit or stash changes before tagging." >&2
  exit 1
fi

git tag -a "$tag" -m "Release $tag"
git push origin "$tag"

echo "Tagged and pushed $tag"
