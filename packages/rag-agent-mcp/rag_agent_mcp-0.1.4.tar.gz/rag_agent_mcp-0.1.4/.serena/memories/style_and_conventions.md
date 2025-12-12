# Code Style & Conventions
- TypeScript sources use modern ES module imports, async/await, and explicit interfaces; prefer concise logging via `console.error` for operational traces.
- Naming follows camelCase for methods/properties and PascalCase for classes.
- Docblocks (JSDoc style) document classes/methods; keep helper functions focused on a single responsibility (SRP).
- Python helper code under `src/rag_agent/` mirrors rag-agent package layout; follow standard PEP 8 naming when editing.
- Keep configuration values injected via constructor/config interfaces rather than hardcoding within logic (supports DI and SOLID principles).