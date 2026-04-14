FROM python:3.13-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# ── Layer 1: install Python dependencies (cached when only pyproject.toml/uv.lock change)
# Build context is ./backend, so COPY here is relative to ./backend/
COPY pyproject.toml uv.lock ./backend/
# Export pinned deps from uv.lock → requirements.txt, then install (no project source needed)
RUN cd /app/backend && \
    uv export --no-hashes --no-dev -o /tmp/requirements.txt && \
    uv pip install --system -r /tmp/requirements.txt

# ── Layer 2: copy full source (always fresh — busts cache on any source change)
# package-dir {"" = ".."} in pyproject.toml means setuptools looks in /app/
# (the parent) and finds the `backend` package at /app/backend/
COPY . ./backend/

# Install the local backend package only (deps already installed above)
RUN cd /app/backend && uv pip install --system --no-deps .

# Persistent data directory (override DATABASE_URL and AUDIO_STORAGE_PATH via env)
RUN mkdir -p /data/audio_uploads
# Copy entrypoint script and make it executable
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8001"]
