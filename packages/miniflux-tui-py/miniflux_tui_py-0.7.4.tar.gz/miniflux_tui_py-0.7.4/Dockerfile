# syntax=docker/dockerfile:1.19
ARG PYTHON_IMAGE=python:3.13.9-slim@sha256:0222b795db95bf7412cede36ab46a266cfb31f632e64051aac9806dabf840a61

# hadolint ignore=DL3006
FROM ${PYTHON_IMAGE} AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENV=/opt/app/.venv

WORKDIR /src

RUN python -m venv "${UV_PROJECT_ENV}"

ENV PATH=${UV_PROJECT_ENV}/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:ba4857bf2a068e9bc0e64eed8563b065908a4cd6bfb66b531a9c424c8e25e142 /uv /bin/
COPY --from=ghcr.io/astral-sh/uv:latest@sha256:ba4857bf2a068e9bc0e64eed8563b065908a4cd6bfb66b531a9c424c8e25e142 /uvx /bin/

COPY pyproject.toml uv.lock README.md LICENSE /src/
COPY miniflux_tui /src/miniflux_tui

RUN uv export \
        --format requirements-txt \
        --frozen \
        --no-dev \
        --no-editable \
        --no-emit-project \
        --output-file requirements.txt \
    && uv build --wheel --out-dir dist \
    && pip install --no-cache-dir --require-hashes -r requirements.txt \
    && pip install --no-cache-dir --no-deps dist/*.whl \
    && rm -rf requirements.txt dist \
    && find "${UV_PROJECT_ENV}" -type d -name "__pycache__" -prune -exec rm -rf {} +

# hadolint ignore=DL3006
FROM ${PYTHON_IMAGE} AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_PROJECT_ENV=/opt/app/.venv \
    PATH=/opt/app/.venv/bin:$PATH \
    HOME=/home/miniflux

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install --no-install-recommends --yes ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --home-dir "${HOME}" --shell /usr/sbin/nologin --system miniflux

COPY --from=builder /opt/app/.venv /opt/app/.venv
COPY --chown=miniflux:miniflux config.toml.example /opt/app/config.toml.example

WORKDIR "${HOME}"

LABEL org.opencontainers.image.title="miniflux-tui-py" \
    org.opencontainers.image.description="Terminal UI client for Miniflux packaged as a container" \
    org.opencontainers.image.url="https://github.com/reuteras/miniflux-tui-py" \
    org.opencontainers.image.source="https://github.com/reuteras/miniflux-tui-py" \
    org.opencontainers.image.licenses="MIT"

USER miniflux

HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 CMD ["miniflux-tui", "--version"]

ENTRYPOINT ["miniflux-tui"]
