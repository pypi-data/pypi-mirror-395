#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
    UV_VERSION="0.9.6"
    ARCH="$(uname -m)"
    case "${ARCH}" in
    x86_64)
        UV_ARCHIVE="uv-x86_64-unknown-linux-gnu"
        ;;
    aarch64)
        UV_ARCHIVE="uv-aarch64-unknown-linux-gnu"
        ;;
    *)
        echo "Unsupported architecture for uv installer: ${ARCH}" >&2
        exit 1
        ;;
    esac

    UV_BASE_URL="https://github.com/astral-sh/uv/releases/download/${UV_VERSION}"
    TMP_DIR="$(mktemp -d)"
    trap 'rm -rf "${TMP_DIR}"' EXIT

    ARCHIVE_PATH="${TMP_DIR}/${UV_ARCHIVE}.tar.gz"
    SHA_PATH="${ARCHIVE_PATH}.sha256"

    curl -LsSf "${UV_BASE_URL}/${UV_ARCHIVE}.tar.gz" -o "${ARCHIVE_PATH}"
    curl -LsSf "${UV_BASE_URL}/${UV_ARCHIVE}.tar.gz.sha256" -o "${SHA_PATH}"

    (cd "${TMP_DIR}" && sha256sum --check --status "${UV_ARCHIVE}.tar.gz.sha256")

    tar -xzf "${ARCHIVE_PATH}" -C "${TMP_DIR}"
    install -d "${HOME}/.local/bin"
    install -m 755 "${TMP_DIR}/${UV_ARCHIVE}/uv" "${HOME}/.local/bin/uv"
    install -m 755 "${TMP_DIR}/${UV_ARCHIVE}/uvx" "${HOME}/.local/bin/uvx"
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "📦 Installing Python dependencies..."
# Install dev and docs groups, but skip fuzz (requires clang/libFuzzer)
# and binary (requires heavy PyInstaller) for faster setup
uv sync --locked --group dev --group docs

# Activate virtual environment in shell sessions
echo "Setting up automatic virtual environment activation..."
WORKSPACE_DIR="$(pwd)"
BASHRC="${HOME}/.bashrc"

# Add venv activation to .bashrc if not already present
if [ -f "$BASHRC" ] && ! grep -q "Auto-activate Python virtual environment" "$BASHRC"; then
    cat >>"$BASHRC" <<EOF

# Auto-activate Python virtual environment for miniflux-tui-py
if [ -f "${WORKSPACE_DIR}/.venv/bin/activate" ]; then
    source "${WORKSPACE_DIR}/.venv/bin/activate"
fi
EOF
fi

# Set up shell completions
echo "Setting up shell completions..."

# Create completions directory
mkdir -p "${HOME}/.local/share/bash-completion/completions"

# Generate and install completions for uv
if command -v uv >/dev/null 2>&1; then
    uv generate-shell-completion bash >"${HOME}/.local/share/bash-completion/completions/uv"
fi

# Generate completions for pytest, ruff, and other Python tools
for tool in pytest ruff pyright; do
    if uv run which "$tool" >/dev/null 2>&1; then
        case "$tool" in
        pytest)
            # pytest doesn't have built-in completion, but we can use argcomplete if available
            if uv run python -c "import argcomplete" 2>/dev/null; then
                eval "$(uv run register-python-argcomplete pytest)" >"${HOME}/.local/share/bash-completion/completions/pytest" 2>/dev/null || true
            fi
            ;;
        ruff)
            uv run ruff generate-shell-completion bash >"${HOME}/.local/share/bash-completion/completions/ruff" 2>/dev/null || true
            ;;
        esac
    fi
done

# Add completion loading to bashrc if not already present
BASHRC="${HOME}/.bashrc"
if [ -f "$BASHRC" ] && ! grep -q "bash-completion/completions" "$BASHRC"; then
    cat >>"$BASHRC" <<'EOF'

# Load custom completions
if [ -d "${HOME}/.local/share/bash-completion/completions" ]; then
    for completion in "${HOME}/.local/share/bash-completion/completions"/*; do
        [ -f "$completion" ] && source "$completion"
    done
fi
EOF
fi

# Install pre-commit hooks for development
echo "Installing pre-commit hooks..."
uv run pre-commit install

echo "✅ Codespace setup complete!"
echo ""
echo "Quick start:"
echo "  • Run tests:     uv run pytest tests"
echo "  • Lint code:     uv run ruff check miniflux_tui tests"
echo "  • Format code:   uv run ruff format miniflux_tui tests"
echo "  • Type check:    uv run pyright miniflux_tui tests"
echo "  • Run app:       uv run miniflux-tui --init"
echo "  • View docs:     uv run mkdocs serve"
echo ""
echo "Or use VS Code tasks (Ctrl+Shift+B for test/build)!"
