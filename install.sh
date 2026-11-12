#!/bin/sh
# Install the secure-coding-skills pack into your agent's skills directory.
#
# Usage:
#   ./install.sh                install into ~/.claude/skills
#   SKILLS_DIR=/path ./install.sh   install somewhere else
#
# The script copies each skill folder under skills/ into the target
# directory. Re-running it updates the installed copies.

set -eu

SRC_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET_DIR=${SKILLS_DIR:-"$HOME/.claude/skills"}

mkdir -p "$TARGET_DIR"

for skill in "$SRC_DIR"/skills/*/; do
  name=$(basename "$skill")
  rm -rf "$TARGET_DIR/$name"
  cp -R "$skill" "$TARGET_DIR/$name"
  echo "installed: $name -> $TARGET_DIR/$name"
done

echo "Done. Two skills installed: diff-security-audit, adversarial-disproof."
echo "Ask your agent to run diff-security-audit on a change before the PR,"
echo "then adversarial-disproof on the findings before reporting them."
