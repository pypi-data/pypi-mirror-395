"""
Main module for RAG Agent MCP server.

Supports three authentication modes:
1. API Key mode (legacy): Uses api_key for authentication
2. Kong Basic Auth mode: Uses HTTP Basic Authentication for Kong gateway
3. Supabase Auth mode: Uses JWT token for user-level authentication and permission control
"""

import asyncio
import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union, cast

from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

from rag_agent import config
from rag_agent.basic_auth import BasicAuthClient
from rag_agent.rag_agent_client import LightRAGClient
from rag_agent.supabase_auth import SupabaseAuthClient

logger = logging.getLogger(__name__)

mcp = FastMCP("RAG Agent MCP Server")


def format_response(result: Any, is_error: bool = False) -> str:
    """
    Formats response in standard format with proper Unicode handling.

    Returns a JSON string with ensure_ascii=False to preserve Unicode characters
    (e.g., Chinese, Japanese, etc.) in their original form instead of Unicode escapes.

    Args:
        result: Operation result
        is_error: Error flag

    Returns:
        str: JSON string with standardized response
    """
    response_dict = None

    if is_error:
        if isinstance(result, str):
            response_dict = {"status": "error", "error": result}
        else:
            response_dict = {"status": "error", "error": str(result)}
    elif result is None:
        # Handle None result as an error
        response_dict = {
            "status": "error",
            "error": "API call returned None. This usually indicates a connection error or API failure. Check server logs for details."
        }
    elif isinstance(result, dict):
        # If result is already a dictionary, return it wrapped
        response_dict = {"status": "success", "response": result}
    elif hasattr(result, "dict") and callable(getattr(result, "dict")):
        # If result has dict() method, use it
        response_dict = {"status": "success", "response": result.dict()}
    elif hasattr(result, "__dict__"):
        # If result has __dict__, use it
        response_dict = {"status": "success", "response": result.__dict__}
    elif hasattr(result, "to_dict") and callable(getattr(result, "to_dict")):
        # If result has to_dict() method, use it
        response_dict = {"status": "success", "response": result.to_dict()}
    else:
        # In other cases, convert to string
        response_dict = {"status": "success", "response": str(result)}

    # Serialize to JSON with ensure_ascii=False to preserve Unicode characters
    return json.dumps(response_dict, ensure_ascii=False, indent=2)


@dataclass
class AppContext:
    """Application context with typed resources."""

    lightrag_client: LightRAGClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """
    Manages application lifecycle with typed context.
    Initializes RAG Agent API client at startup and closes it at shutdown.
    
    Supports three modes based on config.AUTH_MODE:
    1. "none": API Key mode (legacy) - when only --api-key is provided
    2. "basic": Kong Basic Auth mode - when --user is not an email
    3. "supabase": Supabase Auth mode - when --user is an email
    """
    auth_client: Optional[SupabaseAuthClient] = None
    basic_auth_client: Optional[BasicAuthClient] = None
    
    # Initialize authentication based on AUTH_MODE
    if config.AUTH_MODE == "supabase":
        logger.info("Supabase Auth mode enabled - initializing auth client")
        auth_client = SupabaseAuthClient(
            auth_url=config.SUPABASE_AUTH_URL,
            anon_key=config.LIGHTRAG_API_KEY,
            user=config.AUTH_USER,
            password=config.AUTH_USER_PASSWORD,
        )
        
        # Perform initial login
        try:
            await auth_client.login()
            logger.info("Supabase Auth login successful")
            
            # Start auto-refresh background task
            await auth_client.start_auto_refresh()
        except Exception as e:
            logger.error(f"Supabase Auth login failed: {e}")
            raise RuntimeError(f"Failed to authenticate with Supabase: {e}")
    
    elif config.AUTH_MODE == "basic":
        logger.info("Kong Basic Auth mode enabled - initializing basic auth client")
        basic_auth_client = BasicAuthClient(
            user=config.AUTH_USER,
            password=config.AUTH_USER_PASSWORD,
        )
        logger.info("Kong Basic Auth initialized successfully")
    
    else:
        logger.info("API Key mode enabled (no user authentication)")
    
    # Initialize RAG Agent client
    lightrag_client = LightRAGClient(
        base_url=config.LIGHTRAG_API_BASE_URL,
        api_key=config.LIGHTRAG_API_KEY,
        auth_client=auth_client,
        basic_auth_client=basic_auth_client,
    )

    try:
        yield AppContext(lightrag_client=lightrag_client)
    finally:
        await lightrag_client.close()
        logger.info("RAG Agent MCP Server stopped")


mcp = FastMCP("RAG Agent MCP Server", lifespan=app_lifespan)


async def execute_lightrag_operation(
    operation_name: str, operation_func: Callable, ctx: Context
) -> str:
    """
    Universal wrapper function for executing operations with RAG Agent API.

    Automatically handles:
    - Getting client from context
    - Type casting
    - Exception handling
    - Response formatting with proper Unicode handling

    Args:
        operation_name: Operation name for logging
        operation_func: Function to execute that takes client as first argument

    Returns:
        str: JSON string with formatted response (ensure_ascii=False for Unicode)
    """
    try:
        if not ctx or not ctx.request_context or not ctx.request_context.lifespan_context:
            return format_response(
                f"Error: Request context is not available for {operation_name}", is_error=True
            )

        app_ctx = cast(AppContext, ctx.request_context.lifespan_context)
        client = app_ctx.lightrag_client

        logger.info(f"Executing operation: {operation_name}")
        result = await operation_func(client)

        return format_response(result)
    except Exception as e:
        logger.exception(f"Error during {operation_name}: {str(e)}")
        return format_response(str(e), is_error=True)


# === Prompts ===


@mcp.prompt(
    name="start_rag_workflow",
    description="Initial workflow prompt to guide users through RAG operations"
)
async def start_rag_workflow(ctx: Context) -> str:
    """
    Provides initial guidance for using RAG Agent tools.
    This prompt should be called at the start of any RAG-related conversation.
    """
    return """Welcome to RAG Agent! Before we begin, let's verify the connection and see available datasets.

Please follow these steps:

1. **Check Health**: First, call the `check_health` tool to verify the RAG Agent API server is running and healthy.

2. **List Datasets**: Then, call the `list_datasets` tool to see all available datasets.

3. **Choose Operation**: Based on the available datasets, you can:
   - Query an existing dataset using `query_dataset`
   - Create a new dataset using `create_dataset`
   - Upload documents to a dataset using `upload_document_to_dataset`
   - Perform cross-dataset queries using `query_multiple_datasets`

Let's start by checking the health status!"""


# === Health Check Tool ===


@mcp.tool(name="check_health", description="Check RAG Agent API server health status and configuration")
async def check_health(ctx: Context) -> str:
    """
    Check the health status of RAG Agent API server.
    Returns server status, configuration, and version information.
    This should be called first to verify the connection before using other tools.
    """
    async def _operation(client: LightRAGClient) -> Any:
        return await client.get_health()

    return await execute_lightrag_operation(
        operation_name="checking health",
        operation_func=_operation,
        ctx=ctx,
    )


# === Dataset MCP Tools ===


@mcp.tool(name="create_dataset", description="Create a new dataset in RAG Agent")
async def create_dataset(
    ctx: Context,
    name: str = Field(description="Dataset name"),
    description: str | None = Field(description="Dataset description", default=None),
    rag_type: str = Field(description="RAG type (rag, graphrag)", default="rag"),
    workspace: str | None = Field(description="Workspace path", default=None),
    namespace_prefix: str | None = Field(description="Namespace prefix", default=None),
    storage_type: str = Field(description="Storage type (local, s3)", default="local"),
    chunk_engine: str = Field(description="Chunk engine", default="default"),
    schedule: str | None = Field(description="Schedule configuration", default=None),
    args: Dict[str, Any] | None = Field(description="Additional arguments", default=None),
    created_by: str | None = Field(description="Creator name", default=None),
    owner_id: str | None = Field(description="Owner ID", default=None),
    visibility: str = Field(description="Visibility (private, public)", default="private"),
    default_permission: str = Field(description="Default permission", default="none"),
    user_id: str | None = Field(description="User ID", default=None),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.create_dataset(
            name=name,
            description=description,
            rag_type=rag_type,
            workspace=workspace,
            namespace_prefix=namespace_prefix,
            storage_type=storage_type,
            chunk_engine=chunk_engine,
            schedule=schedule,
            args=args,
            created_by=created_by,
            owner_id=owner_id,
            visibility=visibility,
            default_permission=default_permission,
            user_id=user_id,
        )

    return await execute_lightrag_operation(
        operation_name=f"creating dataset: {name}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="get_dataset", description="Get dataset information by ID")
async def get_dataset(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.get_dataset(dataset_id=dataset_id)

    return await execute_lightrag_operation(
        operation_name=f"getting dataset: {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="list_datasets", description="List all datasets with pagination")
async def list_datasets(
    ctx: Context,
    page: int = Field(description="Page number", default=1),
    page_size: int = Field(description="Items per page", default=20),
    status: Optional[str] = Field(description="Filter by status", default=None),
    visibility: Optional[str] = Field(description="Filter by visibility", default=None),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.list_datasets(
            page=page,
            page_size=page_size,
            status=status,
            visibility=visibility,
        )

    return await execute_lightrag_operation(
        operation_name="listing datasets",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="update_dataset", description="Update dataset information")
async def update_dataset(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
    updates: Dict[str, Any] = Field(description="Dictionary of fields to update"),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.update_dataset(dataset_id=dataset_id, updates=updates)

    return await execute_lightrag_operation(
        operation_name=f"updating dataset: {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="delete_dataset", description="Delete a dataset")
async def delete_dataset(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.delete_dataset(dataset_id=dataset_id)

    return await execute_lightrag_operation(
        operation_name=f"deleting dataset: {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="get_dataset_statistics", description="Get comprehensive statistics for a dataset")
async def get_dataset_statistics(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.get_dataset_statistics(dataset_id=dataset_id)

    return await execute_lightrag_operation(
        operation_name=f"getting statistics for dataset: {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="query_dataset", description="Query a specific dataset")
async def query_dataset(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
    query_text: str = Field(description="Query text"),
    mode: str = Field(description="Search mode (global, hybrid, local, mix, naive)", default="mix"),
    top_k: int = Field(description="Number of results", default=5),
    chunk_top_k: int = Field(description="Number of chunks to retrieve", default=20),
    only_need_context: bool = Field(description="Return only context without LLM response", default=False),
    only_need_prompt: bool = Field(description="Return only generated prompt", default=False),
    enable_rerank: bool = Field(description="Enable reranking of results", default=True),
    response_type: str = Field(description="Response format", default="Multiple Paragraphs"),
    max_token_for_text_unit: int = Field(description="Maximum tokens for each text fragment", default=1000),
    max_token_for_global_context: int = Field(description="Maximum tokens for global context", default=1000),
    max_token_for_local_context: int = Field(description="Maximum tokens for local context", default=1000),
    max_entity_tokens: int = Field(description="Maximum tokens for entity context", default=10000),
    max_relation_tokens: int = Field(description="Maximum tokens for relation context", default=10000),
    max_total_tokens: int = Field(description="Maximum total tokens for response", default=32000),
    hl_keywords: List[str] = Field(description="High-level keywords for prioritization", default=[]),
    ll_keywords: List[str] = Field(description="Low-level keywords for search refinement", default=[]),
    history_turns: int = Field(description="Number of conversation turns in response context", default=0),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.query_dataset(
            dataset_id=dataset_id,
            query_text=query_text,
            mode=mode,
            top_k=top_k,
            chunk_top_k=chunk_top_k,
            only_need_context=only_need_context,
            only_need_prompt=only_need_prompt,
            enable_rerank=enable_rerank,
            response_type=response_type,
            max_token_for_text_unit=max_token_for_text_unit,
            max_token_for_global_context=max_token_for_global_context,
            max_token_for_local_context=max_token_for_local_context,
            max_entity_tokens=max_entity_tokens,
            max_relation_tokens=max_relation_tokens,
            max_total_tokens=max_total_tokens,
            hl_keywords=hl_keywords,
            ll_keywords=ll_keywords,
            history_turns=history_turns,
        )

    return await execute_lightrag_operation(
        operation_name=f"querying dataset {dataset_id}: {query_text[:50]}...",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="query_multiple_datasets", description="Query multiple datasets simultaneously (cross-dataset query)")
async def query_multiple_datasets(
    ctx: Context,
    dataset_ids: List[str] = Field(description="List of dataset UUIDs to query"),
    query_text: str = Field(description="Query text"),
    mode: str = Field(description="Search mode (global, hybrid, local, mix, naive)", default="mix"),
    top_k: int = Field(description="Number of results per dataset", default=10),
    only_need_context: bool = Field(description="Return only context without LLM response", default=False),
    enable_rerank: bool = Field(description="Enable cross-dataset reranking", default=True),
    document_filters: Dict[str, List[str]] = Field(
        description="Optional document filters per dataset (dataset_id -> [doc_ids])",
        default_factory=dict,
    ),
    response_type: str = Field(description="Response format", default="Multiple Paragraphs"),
    max_token_for_text_unit: int = Field(description="Maximum tokens for each text fragment", default=1000),
    max_token_for_global_context: int = Field(description="Maximum tokens for global context", default=1000),
    max_token_for_local_context: int = Field(description="Maximum tokens for local context", default=1000),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.query_multiple_datasets(
            dataset_ids=dataset_ids,
            query_text=query_text,
            mode=mode,
            top_k=top_k,
            only_need_context=only_need_context,
            enable_rerank=enable_rerank,
            document_filters=document_filters,
            response_type=response_type,
            max_token_for_text_unit=max_token_for_text_unit,
            max_token_for_global_context=max_token_for_global_context,
            max_token_for_local_context=max_token_for_local_context,
        )

    return await execute_lightrag_operation(
        operation_name=f"querying {len(dataset_ids)} datasets: {query_text[:50]}...",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="upload_document_to_dataset", description="Upload document to a specific dataset")
async def upload_document_to_dataset(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
    file_path: str = Field(description="Path to file to upload"),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.upload_document_to_dataset(dataset_id=dataset_id, file_path=file_path)

    return await execute_lightrag_operation(
        operation_name=f"uploading document to dataset {dataset_id}: {file_path}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="get_dataset_documents", description="Get list of documents in a dataset")
async def get_dataset_documents(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
    page: int = Field(description="Page number", default=1),
    page_size: int = Field(description="Items per page", default=20),
    status: Optional[str] = Field(description="Filter by document status", default=None),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.get_dataset_documents(
            dataset_id=dataset_id,
            page=page,
            page_size=page_size,
            status=status,
        )

    return await execute_lightrag_operation(
        operation_name=f"getting documents for dataset {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="delete_dataset_document", description="Delete a document from a dataset")
async def delete_dataset_document(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
    doc_id: str = Field(description="Document ID to delete"),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.delete_dataset_document(dataset_id=dataset_id, doc_id=doc_id)

    return await execute_lightrag_operation(
        operation_name=f"deleting document {doc_id} from dataset {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="scan_dataset_documents", description="Scan dataset's input directory for new documents")
async def scan_dataset_documents(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.scan_dataset_documents(dataset_id=dataset_id)

    return await execute_lightrag_operation(
        operation_name=f"scanning documents for dataset {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="get_dataset_graph", description="Get knowledge graph data for a dataset")
async def get_dataset_graph(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
    node_label: Optional[str] = Field(description="Optional node label to filter", default=None),
    max_depth: int = Field(description="Maximum graph depth", default=3),
    max_nodes: int = Field(description="Maximum number of nodes", default=100),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.get_dataset_graph(
            dataset_id=dataset_id,
            node_label=node_label,
            max_depth=max_depth,
            max_nodes=max_nodes,
        )

    return await execute_lightrag_operation(
        operation_name=f"getting graph for dataset {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )


@mcp.tool(name="get_dataset_graph_labels", description="Get graph labels for a dataset")
async def get_dataset_graph_labels(
    ctx: Context,
    dataset_id: str = Field(description="Dataset UUID"),
) -> str:
    async def _operation(client: LightRAGClient) -> Any:
        return await client.get_dataset_graph_labels(dataset_id=dataset_id)

    return await execute_lightrag_operation(
        operation_name=f"getting graph labels for dataset {dataset_id}",
        operation_func=_operation,
        ctx=ctx,
    )
