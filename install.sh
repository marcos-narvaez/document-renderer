#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
VENV="$ROOT/.venv"
BIN_DIR="$HOME/.local/bin"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: Python 3 is required." >&2
  echo "Check with: python3 --version" >&2
  echo "Install on macOS with Homebrew: brew install python" >&2
  exit 1
fi

if ! command -v latexmk >/dev/null 2>&1; then
  echo "error: latexmk is required." >&2
  echo "Check with: latexmk --version" >&2
  echo "Install on macOS with Homebrew: brew install --cask mactex-no-gui" >&2
  exit 1
fi

python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install --editable "$ROOT"

mkdir -p "$BIN_DIR"
ln -sfn "$VENV/bin/document-renderer" "$BIN_DIR/document-renderer"

echo "Installed document-renderer."
echo "Command: $BIN_DIR/document-renderer"
if ! printf '%s' ":$PATH:" | grep -q ":$BIN_DIR:"; then
  echo "Add this line to your shell profile, then restart the terminal:"
  echo "export PATH=\"$BIN_DIR:\$PATH\""
fi
echo "Claude instructions: $ROOT/CLAUDE_TOOLS.md"
