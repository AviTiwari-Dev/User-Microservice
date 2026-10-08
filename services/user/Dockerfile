# ==========================================
# Builder Stage
# ==========================================

FROM python:3.14.7-slim-bookworm AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Build tools are required only while installing packages
# that contain native extensions.
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create isolated Python virtual environment
RUN python -m venv "${VIRTUAL_ENV}"

# Copy dependency definitions separately so Docker can cache
# the dependency installation layer when application code changes.
COPY services/user/requirements ./requirements

# Install production dependencies into the virtual environment.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        -r requirements/base.txt \
        -r requirements/prod.txt


# ==========================================
# Base Runtime Stage
# ==========================================

FROM python:3.14.7-slim-bookworm AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Copy only the virtual environment from the builder.
# Build tools and package caches are not included.
COPY --from=builder /opt/venv /opt/venv

COPY services/user/src ./src
COPY shared ./shared


# ==========================================
# Test Stage
# ==========================================

FROM base AS test

COPY services/user/requirements/test.txt ./requirements/test.txt

RUN pip install --no-cache-dir \
    -r requirements/test.txt

COPY services/user/tests ./tests


# ==========================================
# Migration Stage
# ==========================================

FROM base AS migration

COPY services/user/requirements/migration.txt ./requirements/migration.txt

RUN pip install --no-cache-dir \
    -r requirements/migration.txt

COPY services/user/alembic ./alembic
COPY services/user/alembic.ini ./alembic.ini

ENTRYPOINT ["alembic"]
CMD ["upgrade", "head"]


# ==========================================
# Production Stage
# ==========================================

FROM base AS prod

# Create a non-root user for running the application.
RUN useradd \
    --create-home \
    --system \
    appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

# Health check
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c \
    "import urllib.request, sys; \
    sys.exit(0 if urllib.request.urlopen( \
    'http://localhost:8080/health', timeout=3 \
    ).status == 200 else 1)"

CMD ["python", "-m", "uvicorn", "src.main:user_api", "--host", "0.0.0.0", "--port", "8080"]
