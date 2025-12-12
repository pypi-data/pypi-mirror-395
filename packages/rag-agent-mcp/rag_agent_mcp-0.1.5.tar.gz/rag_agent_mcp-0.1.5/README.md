[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/shemhamforash23-lightrag-mcp-badge.png)](https://mseep.ai/app/shemhamforash23-lightrag-mcp)

# RAG Agent

RAG Agent is a CLI-enabled MCP server for integrating LightRAG Dataset functionality with AI tools. Provides a unified interface for managing datasets, querying data, and accessing knowledge graphs through the MCP protocol. Can be run directly via `uvx rag-agent`.

## Description

RAG Agent is a specialized bridge between LightRAG's Dataset API and MCP-compatible clients. It enables dataset-isolated RAG operations, allowing you to create, manage, and query multiple independent datasets with their own knowledge graphs and document collections.

### Key Features

- **Health Check**: Verify LightRAG API server status and configuration before operations
- **Guided Workflow**: Built-in prompt to guide users through RAG operations step-by-step
- **Dataset Management**: Create, update, delete, and list datasets with full configuration control
- **Dataset Queries**: Execute queries on single or multiple datasets with cross-dataset reranking
- **Document Management**: Upload, list, and delete documents within specific datasets
- **Knowledge Graph Access**: Retrieve graph data and labels for dataset-specific knowledge graphs
- **Dataset Isolation**: Each dataset maintains its own PostgreSQL schema for complete data separation

## Installation

### Quick Start with uvx (Recommended)

```bash
# Run directly without installation
uvx rag-agent --host localhost --port 9621
```

### Development Installation

```bash
# Create a virtual environment
uv venv --python 3.11

# Install the package in development mode
uv pip install -e .
```

## Requirements

- Python 3.11+
- Running LightRAG API server

## Usage

**Important**: RAG Agent should be run as an MCP server through an MCP client configuration file (mcp-config.json), or directly via `uvx rag-agent`.

### Command Line Options

The following arguments are available when configuring the server in mcp-config.json:

- `--host`: Supabase URL or LightRAG API host (default: localhost). Supports full URLs like `https://xxx.supabase.co`
- `--port`: API port (default: 9621). Ignored for standard ports (80/443) when using full URLs
- `--api-key`: Supabase anon key or LightRAG API key (required for authentication)
- `--user`: Authentication user (email for Supabase Auth, username for Kong Basic Auth)
- `--user-password`: User password for authentication

### Authentication Modes

RAG Agent supports three authentication modes, automatically determined by the `--user` parameter format:

| Mode | Trigger Condition | Description |
|------|-------------------|-------------|
| **API Key** | Only `--api-key` provided | Legacy mode, uses API key header |
| **Kong Basic Auth** | `--user` is NOT an email | HTTP Basic Authentication for Kong gateway |
| **Supabase Auth** | `--user` IS an email (contains `@`) | JWT token authentication with auto-refresh |

### Integration with LightRAG API

The MCP server requires a running LightRAG API server. Start it as follows:

```bash
# Create virtual environment
uv venv --python 3.11

# Install dependencies
uv pip install -r LightRAG/lightrag/api/requirements.txt

# Start LightRAG API
uv run LightRAG/lightrag/api/lightrag_server.py --host localhost --port 9621 --working-dir ./rag_storage --input-dir ./input --llm-binding openai --embedding-binding openai --log-level DEBUG
```

### Setting up as MCP server

To set up RAG Agent as an MCP server, add the following configuration to your MCP client configuration file (e.g., `mcp-config.json`):

#### Using uvx (Recommended):

**API Key Mode (Legacy):**
```json
{
  "mcpServers": {
    "rag-agent": {
      "command": "uvx",
      "args": [
        "rag-agent",
        "--host", "localhost",
        "--port", "9621",
        "--api-key", "your_api_key"
      ]
    }
  }
}
```

**Supabase Auth Mode (JWT):**
```json
{
  "mcpServers": {
    "rag-agent": {
      "command": "uvx",
      "args": [
        "rag-agent",
        "--host", "https://your-project.supabase.co",
        "--api-key", "your_supabase_anon_key",
        "--user", "user@example.com",
        "--user-password", "your_password"
      ]
    }
  }
}
```

**Kong Basic Auth Mode:**
```json
{
  "mcpServers": {
    "rag-agent": {
      "command": "uvx",
      "args": [
        "rag-agent",
        "--host", "https://api-gateway.example.com",
        "--api-key", "your_api_key",
        "--user", "service_account",
        "--user-password", "your_password"
      ]
    }
  }
}
```

#### Development

```json
{
  "mcpServers": {
    "rag-agent": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/rag-agent",
        "run", "src/rag_agent/main.py",
        "--host", "localhost",
        "--port", "9621",
        "--api-key", "your_api_key",
        "--user", "user@example.com",
        "--user-password", "your_password"
      ]
    }
  }
}
```

Replace `/path/to/rag-agent` with the actual path to your rag-agent directory.

## Container Image (LightRAG API + RAG Agent)

Build a single image that starts LightRAG API and RAG Agent together.

### Build

Option A — clone LightRAG during build:

```bash
docker build \
  --build-arg LIGHTRAG_REPO_URL="<git url to LightRAG repo>" \
  --build-arg LIGHTRAG_REF=main \
  -t rag-agent:local .
```

Option B — mount LightRAG at runtime: build without args, and mount the repo to `/opt/LightRAG` when running.

### Run (local test)

```bash
docker run --rm -it \
  -e LLM_BINDING=openai \
  -e EMBEDDING_BINDING=openai \
  -e OPENAI_API_KEY=sk-... \
  -p 9621:9621 \
  -v "$(pwd)/data:/data" \
  rag-agent:local bash
```

Inside the container the entrypoint starts LightRAG API (0.0.0.0:9621) and then execs RAG Agent when invoked with `mcp` (see below for MCP client integration). Logs are written to stderr to avoid interfering with MCP stdio.

### Use with MCP client (docker-run)

Most MCP clients spawn servers via stdio. Configure your MCP client to run this container with `-i` (interactive, no TTY) so stdio is attached to the MCP server process:

```json
{
  "mcpServers": {
    "rag-agent": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "LLM_BINDING=openai",
        "-e", "EMBEDDING_BINDING=openai",
        "-e", "OPENAI_API_KEY=sk-...",
        "-e", "MCP_API_KEY=", // optional, only if LightRAG API requires it
        "-v", "/absolute/path/to/data:/data",
        "rag-agent:local",
        "mcp"
      ],
      "alwaysAllow": [
        "create_dataset", "get_dataset", "list_datasets", "update_dataset", "delete_dataset",
        "get_dataset_statistics", "query_dataset", "query_multiple_datasets",
        "upload_document_to_dataset", "get_dataset_documents", "delete_dataset_document",
        "scan_dataset_documents", "get_dataset_graph", "get_dataset_graph_labels"
      ]
    }
  }
}
```

Notes:
- The container runs LightRAG API inside and binds it to `localhost:9621` for the MCP server; you do not need to expose it unless you want external access.
- If your LightRAG build needs different bindings, set `LLM_BINDING`, `EMBEDDING_BINDING` and their provider keys (e.g., `OPENAI_API_KEY`).
- To customize LightRAG paths, use `LIGHTRAG_WORKDIR`, `LIGHTRAG_INPUTDIR`, and `LIGHTRAG_EXTRA_ARGS`.

## Available MCP Tools

### Health Check
- `check_health`: Check LightRAG API server health status, configuration, and version information

### Prompts
- `start_rag_workflow`: Initial workflow prompt that guides users through the recommended steps:
  1. Check API server health
  2. List available datasets
  3. Choose appropriate operations based on available datasets

### Dataset Management
- `create_dataset`: Create a new dataset with full configuration (name, description, RAG type, storage type, etc.)
- `get_dataset`: Get detailed information about a specific dataset by ID
- `list_datasets`: List all datasets with pagination and filtering by status/visibility
- `update_dataset`: Update dataset configuration and metadata
- `delete_dataset`: Delete a dataset and all its associated data
- `get_dataset_statistics`: Get comprehensive statistics for a dataset (document count, graph metrics, etc.)

### Dataset Queries
- `query_dataset`: Execute a query on a specific dataset with full RAG capabilities
  - Supports multiple search modes (global, hybrid, local, mix, naive)
  - Configurable token limits and response types
  - High-level and low-level keyword prioritization
- `query_multiple_datasets`: Execute cross-dataset queries with automatic result merging
  - Query multiple datasets simultaneously
  - Optional cross-dataset reranking
  - Per-dataset document filtering

### Dataset Document Management
- `upload_document_to_dataset`: Upload a document file to a specific dataset
- `get_dataset_documents`: List documents in a dataset with pagination and status filtering
- `delete_dataset_document`: Delete a specific document from a dataset
- `scan_dataset_documents`: Scan dataset's input directory for new documents

### Dataset Knowledge Graph
- `get_dataset_graph`: Retrieve knowledge graph data for a dataset
  - Optional node label filtering
  - Configurable depth and node limits
- `get_dataset_graph_labels`: Get all graph labels (node and relationship types) for a dataset

## Usage Examples

### Recommended Workflow

```python
# Step 1: Check API server health
check_health()
# Returns: Server status, configuration, version info

# Step 2: List available datasets
list_datasets()
# Returns: All datasets with pagination

# Step 3: Choose your operation based on available datasets
```

### Creating and Querying a Dataset

```python
# Create a new dataset
create_dataset(
    name="research_papers",
    description="Academic research papers collection",
    rag_type="rag",
    visibility="private"
)

# Upload documents to the dataset
upload_document_to_dataset(
    dataset_id="<dataset-uuid>",
    file_path="/path/to/paper.pdf"
)

# Query the dataset
query_dataset(
    dataset_id="<dataset-uuid>",
    query_text="What are the main findings?",
    mode="mix",
    top_k=10
)
```

### Cross-Dataset Query

```python
# Query multiple datasets simultaneously
query_multiple_datasets(
    dataset_ids=["<dataset-1-uuid>", "<dataset-2-uuid>"],
    query_text="Compare approaches to machine learning",
    enable_rerank=True,
    top_k=5
)
```

### Managing Dataset Knowledge Graph

```python
# Get graph labels
get_dataset_graph_labels(dataset_id="<dataset-uuid>")

# Retrieve graph data
get_dataset_graph(
    dataset_id="<dataset-uuid>",
    node_label="CONCEPT",
    max_depth=3,
    max_nodes=100
)
```

## Development

### Installing development dependencies

```bash
uv pip install -e ".[dev]"
```

### Running linters

```bash
ruff check src/
mypy src/
```

## License

MIT
