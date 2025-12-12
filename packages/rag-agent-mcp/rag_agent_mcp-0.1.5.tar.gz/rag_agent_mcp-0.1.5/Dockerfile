# syntax=docker/dockerfile:1

FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy MCP server code
COPY pyproject.toml README.md uv.lock /app/
COPY src /app/src

RUN pip install --upgrade pip setuptools wheel \
 && pip install .

# Optionally clone LightRAG API at build time
ARG LIGHTRAG_REPO_URL=""
ARG LIGHTRAG_REF="main"
RUN if [ -n "$LIGHTRAG_REPO_URL" ]; then \
      echo "Cloning LightRAG from $LIGHTRAG_REPO_URL (ref=$LIGHTRAG_REF)"; \
      git clone --depth 1 -b "$LIGHTRAG_REF" "$LIGHTRAG_REPO_URL" /opt/LightRAG && \
      pip install -r /opt/LightRAG/lightrag/api/requirements.txt; \
    else \
      echo "LIGHTRAG_REPO_URL not provided. You can mount LightRAG at /opt/LightRAG or set it at build."; \
    fi

# Runtime dirs for LightRAG data
RUN mkdir -p /data/input /data/rag_storage
VOLUME ["/data"]

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 9621

# NOTE: MCP servers speak over stdio; we keep stderr for logs and preserve stdout for MCP protocol.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["mcp"]

