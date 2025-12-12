# Project Overview
- **Purpose**: Expose Model Context Protocol (MCP) tools for interacting with self-hosted Supabase instances, including optional integration with a rag-agent service for retrieval-augmented generation workflows.
- **Key Components**:
  - Node.js/TypeScript MCP server (`src/`, built into `dist/`).
  - Optional rag-agent integration driven via `uvx rag-agent` bridge (`src/integrations/rag-agent-client.ts`).
  - Python-based rag-agent helper package vendor copy under `src/rag_agent/`.
- **Deployment**: Built with `npm run build` into `dist` and executed via `node dist/index.js` (Dockerfile sets same entrypoint).