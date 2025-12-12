#!/usr/bin/env sh
set -eu

log() { echo "[$(date -Is)] $*" >&2; }

CMD="${1:-mcp}"

# LightRAG API runtime configuration
LIGHTRAG_HOST="${LIGHTRAG_HOST:-0.0.0.0}"
LIGHTRAG_PORT="${LIGHTRAG_PORT:-9621}"
LIGHTRAG_WORKDIR="${LIGHTRAG_WORKDIR:-/data/rag_storage}"
LIGHTRAG_INPUTDIR="${LIGHTRAG_INPUTDIR:-/data/input}"
LLM_BINDING="${LLM_BINDING:-}"
EMBEDDING_BINDING="${EMBEDDING_BINDING:-}"
LIGHTRAG_EXTRA_ARGS="${LIGHTRAG_EXTRA_ARGS:-}"

# MCP server API key (optional) for talking to LightRAG API
MCP_API_KEY="${MCP_API_KEY:-}" # alias: LIGHTRAG_API_KEY also supported via args passed to mcp

start_lightrag_api() {
  if [ -f "/opt/LightRAG/lightrag/api/lightrag_server.py" ]; then
    log "Starting LightRAG API on ${LIGHTRAG_HOST}:${LIGHTRAG_PORT}"
    mkdir -p "$LIGHTRAG_WORKDIR" "$LIGHTRAG_INPUTDIR"

    API_FLAGS="--host ${LIGHTRAG_HOST} --port ${LIGHTRAG_PORT} --working-dir ${LIGHTRAG_WORKDIR} --input-dir ${LIGHTRAG_INPUTDIR}"
    if [ -n "$LLM_BINDING" ]; then API_FLAGS="$API_FLAGS --llm-binding ${LLM_BINDING}"; fi
    if [ -n "$EMBEDDING_BINDING" ]; then API_FLAGS="$API_FLAGS --embedding-binding ${EMBEDDING_BINDING}"; fi

    # Start API in background; route stdout to stderr to avoid polluting MCP stdio
    python /opt/LightRAG/lightrag/api/lightrag_server.py $API_FLAGS $LIGHTRAG_EXTRA_ARGS 1>&2 &
    API_PID=$!
  else
    log "LightRAG API not found at /opt/LightRAG; skipping API start"
    API_PID=""
  fi
}

wait_for_api() {
  if [ -n "${API_PID:-}" ]; then
    for i in $(seq 1 60); do
      if curl -sf "http://127.0.0.1:${LIGHTRAG_PORT}/health" >/dev/null 2>&1; then
        log "LightRAG API is up"
        return 0
      fi
      sleep 0.5
    done
    log "LightRAG API did not become healthy in time; continuing anyway"
  fi
}

cleanup() {
  if [ -n "${API_PID:-}" ] && kill -0 "$API_PID" 2>/dev/null; then
    kill "$API_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

start_lightrag_api
wait_for_api

if [ "$CMD" = "mcp" ]; then
  shift || true
  MCP_ARGS="--host localhost --port ${LIGHTRAG_PORT}"
  if [ -n "$MCP_API_KEY" ]; then MCP_ARGS="$MCP_ARGS --api-key ${MCP_API_KEY}"; fi
  exec rag-agent $MCP_ARGS "$@"
else
  exec "$@"
fi

