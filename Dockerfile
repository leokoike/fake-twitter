# Stage 1: Builder - Build dependencies
FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install only production dependencies (no dev dependencies)
RUN uv sync --frozen --no-dev

# Stage 2: Runtime - Minimal production image
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/src" \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv in runtime stage
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy virtual environment and dependencies from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/pyproject.toml /app/uv.lock ./

# Copy application code
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY gunicorn.conf.py ./

# Expose port
EXPOSE 8000

# Run the application with uv
CMD ["uv", "run", "gunicorn", "fake_twitter.main:app", "-c", "gunicorn.conf.py"]
