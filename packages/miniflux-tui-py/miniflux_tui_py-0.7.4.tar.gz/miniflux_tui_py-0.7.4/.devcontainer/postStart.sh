#!/usr/bin/env bash
set -euo pipefail

echo "🔄 Running post-start setup..."

# Ensure virtual environment exists and is up to date
if [ ! -d ".venv" ]; then
    echo "📦 Virtual environment not found, creating..."
    uv sync --locked --all-groups
else
    echo "✓ Virtual environment exists"
fi

# Ensure venv activation is in bashrc
WORKSPACE_DIR="$(pwd)"
BASHRC="${HOME}/.bashrc"

if [ -f "$BASHRC" ] && ! grep -q "Auto-activate Python virtual environment" "$BASHRC"; then
    echo "🔧 Adding venv activation to .bashrc..."
    cat >>"$BASHRC" <<EOF

# Auto-activate Python virtual environment for miniflux-tui-py
if [ -f "${WORKSPACE_DIR}/.venv/bin/activate" ]; then
    source "${WORKSPACE_DIR}/.venv/bin/activate"
fi
EOF
fi

echo "✅ Post-start setup complete!"
