# Use Alpine with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS uv

# Upgrade OpenSSL to patched version immediately
RUN apk add --no-cache --upgrade openssl=3.5.4-r0

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.13-alpine

# Upgrade OpenSSL to patched version FIRST THING
RUN apk add --no-cache --upgrade openssl=3.5.4-r0

# Upgrade pip to fix CVE-2025-8869
RUN pip install --no-cache-dir --upgrade pip==25.3

# Add MCP registry label for package validation
LABEL io.modelcontextprotocol.server.name="io.github.neverinfamous/sqlite-mcp-server"

# Create app user
RUN addgroup -g 1000 app && adduser -u 1000 -G app -s /bin/sh -D app

WORKDIR /app

# Copy the virtual environment from the uv stage
COPY --from=uv /app/.venv /app/.venv

# Copy the source code (needed for non-editable installs)
COPY --from=uv /app/src /app/src

# Fix broken Python symlinks from uv stage - point to system Python
RUN rm -f /app/.venv/bin/python* && \
    ln -s /usr/local/bin/python3 /app/.venv/bin/python && \
    ln -s /usr/local/bin/python3 /app/.venv/bin/python3 && \
    ln -s /usr/local/bin/python3 /app/.venv/bin/python3.13 && \
    chown -R app:app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER app

# when running the container, add --db-path and a bind mount to the host's db file
ENTRYPOINT ["mcp-server-sqlite"]
