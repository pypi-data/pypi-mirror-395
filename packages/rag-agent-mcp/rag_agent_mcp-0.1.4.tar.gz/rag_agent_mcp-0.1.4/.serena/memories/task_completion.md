# Task Completion Checklist
- Run `npm run build` to ensure the TypeScript sources compile into `dist/`.
- If rag-agent integration changes are involved, invoke `uvx rag-agent --host <host> --port <port> --api-key <key> --operation status` (or similar) to confirm connectivity.
- Smoke test MCP server via `node dist/index.js --help` or by connecting from an MCP client (Cursor/Claude) to confirm tool registration.