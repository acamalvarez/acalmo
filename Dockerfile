# --- Build Stage ---
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies into a virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the project and install it
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# --- Runtime Stage ---
FROM python:3.13-slim-bookworm

WORKDIR /app

# Set production environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --shell /bin/bash --create-home nonroot

# Copy only the necessary files from the builder
COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
COPY --from=builder --chown=nonroot:nonroot /app /app

# Use the non-root user
USER nonroot

# Run the django application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "acalmo.wsgi:application"]
