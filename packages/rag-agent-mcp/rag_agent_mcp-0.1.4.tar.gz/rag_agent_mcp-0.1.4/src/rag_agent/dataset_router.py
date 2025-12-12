"""
This module contains all dataset-related routes for the LightRAG API.

Provides endpoints for dataset management including CRUD operations for datasets
and dataset-aware document and query operations.
"""

import json
import logging
import traceback
import re
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path as FilePath

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, Query, Path, UploadFile, File, BackgroundTasks, Body, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator

from ..utils_api import get_combined_auth_dependency, create_base_rag_config
from ...dataset import DatasetManager, DatasetAdapter
from ..routers.document_routes import DocumentsRequest, PaginatedDocsResponse, DocStatusResponse, PaginationInfo, DeleteDocRequest, DeleteDocByIdResponse, DocumentManager, ScanResponse
from ..routers.multimodal_models import MultimodalUploadRequest, pipeline_multimodal_index_file, process_remote_file
from ... import LightRAG
import asyncio
from ...dataset.exceptions import (
    DatasetNotFoundError,
    DatasetAlreadyExistsError,
    DatasetConfigurationError,
    SchemaCreationError,
)
from ...kg.dataset_pipeline_manager import DatasetPipelineManager
from ...utils import generate_track_id
from ..services.rag_manager import rag_manager
from ..models.dataset_models import Dataset
from lightrag.timing_monitor import timing_start, timing_end

# Try to import AutoEmbeddingService if available
try:
    from ..services.auto_embedding_service import AutoEmbeddingService
    auto_embedding_available = True
except ImportError:
    auto_embedding_available = False
    AutoEmbeddingService = None

# Try to import Dataset model if available
try:
    from ..models.dataset_models import Dataset as DatasetModel, RemoteFileUploadRequest
except ImportError:
    DatasetModel = None
    RemoteFileUploadRequest = None

router = APIRouter(tags=["dataset"])

logger = logging.getLogger(__name__)

# Global adapter cache for performance optimization
_adapter_cache: Dict[str, DatasetAdapter] = {}

async def _get_cached_adapter(dataset_id: str, db_config: Dict[str, Any]) -> DatasetAdapter:
    """Get cached DatasetAdapter instance for performance optimization.

    Args:
        dataset_id: Dataset UUID
        db_config: Database configuration

    Returns:
        Cached or new DatasetAdapter instance
    """
    if dataset_id not in _adapter_cache:
        _adapter_cache[dataset_id] = DatasetAdapter(dataset_id, db_config)
        await _adapter_cache[dataset_id].initialize_schemas()
        logger.debug(f"Created new DatasetAdapter for {dataset_id}")
    else:
        logger.debug(f"Using cached DatasetAdapter for {dataset_id}")

    return _adapter_cache[dataset_id]


def _dataset_info_to_model(dataset_info: dict) -> Dataset:
    """Convert dataset info dictionary to Dataset model object.

    Args:
        dataset_info: Dataset information dictionary from DatasetManager

    Returns:
        Dataset model object for use with RAGManager
    """
    return Dataset(
        dataset_uuid=dataset_info.get('dataset_uuid'),
        name=dataset_info.get('name'),
        description=dataset_info.get('description'),
        rag_type=dataset_info.get('rag_type', 'rag'),
        workspace=dataset_info.get('workspace'),
        namespace_prefix=dataset_info.get('namespace_prefix'),
        created_at=dataset_info.get('created_at'),
        updated_at=dataset_info.get('updated_at'),
        status=dataset_info.get('status', 'active'),
        storage_type=dataset_info.get('storage_type', 'local'),
        chunk_engine=dataset_info.get('chunk_engine', 'default'),
        schedule=dataset_info.get('schedule'),
        args=dataset_info.get('args', {}),
        created_by=dataset_info.get('created_by'),
        owner_id=dataset_info.get('owner_id'),
        visibility=dataset_info.get('visibility', 'private'),
        default_permission=dataset_info.get('default_permission', 'none'),
        user_id=dataset_info.get('user_id'),
    )


def _parse_dataset_context_response(response: str, dataset_id: str, query_mode: str):
    """Parse context response string into structured data for dataset queries."""
    entities = []
    relationships = []
    chunks = []
    timing_start("Parse dataset context response")

    try:
        # Extract entities
        entities_match = re.search(r'-----Entities\(KG\)-----\s*```json\s*(.*?)\s*```', response, re.DOTALL)
        if entities_match:
            entities_json = entities_match.group(1).strip()
            if entities_json:
                entities = json.loads(entities_json)

        # Extract relationships
        relationships_match = re.search(r'-----Relationships\(KG\)-----\s*```json\s*(.*?)\s*```', response, re.DOTALL)
        if relationships_match:
            relationships_json = relationships_match.group(1).strip()
            if relationships_json:
                relationships = json.loads(relationships_json)

        # Extract chunks
        chunks_match = re.search(r'-----Document Chunks\(DC\)-----\s*```json\s*(.*?)\s*```', response, re.DOTALL)
        if chunks_match:
            chunks_json = chunks_match.group(1).strip()
            if chunks_json:
                chunks = json.loads(chunks_json)
        elif re.search(r'---Document Chunks\(DC\)---\s*```json\s*(.*?)\s*```', response, re.DOTALL):
            # Handle naive mode format
            chunks_match = re.search(r'---Document Chunks\(DC\)---\s*```json\s*(.*?)\s*```', response, re.DOTALL)
            if chunks_match:
                chunks_json = chunks_match.group(1).strip()
                if chunks_json:
                    chunks = json.loads(chunks_json)

    except json.JSONDecodeError as e:
        logging.warning(f"Failed to parse dataset context response JSON: {e}")

    timing_end("Parse dataset context response")

    return DatasetQueryResponse(
        response="",
        dataset_id=dataset_id,
        query_mode=query_mode,
        entities=entities if entities else None,
        relationships=relationships if relationships else None,
        chunks=chunks if chunks else None
    )


# Dataset query models
class DatasetQueryRequest(BaseModel):
    query: str = Field(min_length=1, description="The query text")
    mode: str = Field(default="mix", description="Query mode: local, global, hybrid, naive, mix, bypass")
    only_need_context: Optional[bool] = Field(default=None, description="Only return context without response")
    only_need_prompt: Optional[bool] = Field(default=None, description="Only return prompt without response")
    response_type: Optional[str] = Field(default=None, description="Response format type")
    top_k: Optional[int] = Field(default=None, ge=1, le=100, description="Number of top results")
    chunk_top_k: Optional[int] = Field(default=None, ge=1, le=100, description="Number of top chunks")
    max_entity_tokens: Optional[int] = Field(default=None, ge=1, description="Max tokens for entity context")
    max_relation_tokens: Optional[int] = Field(default=None, ge=1, description="Max tokens for relation context")
    max_total_tokens: Optional[int] = Field(default=None, ge=1, description="Max total tokens budget")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default=None, description="Conversation history")
    history_turns: Optional[int] = Field(default=None, ge=0, description="Number of conversation turns")
    ids: Optional[List[str]] = Field(default=None, description="List of doc ids to filter")
    user_prompt: Optional[str] = Field(default=None, description="Custom user prompt")
    enable_rerank: Optional[bool] = Field(default=None, description="Enable reranking")

class DatasetQueryResponse(BaseModel):
    response: str = Field(description="Query response")
    dataset_id: str = Field(description="Dataset ID")
    query_mode: str = Field(description="Query mode used")
    entities: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Structured entities data when only_need_context=True",
    )
    relationships: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Structured relationships data when only_need_context=True",
    )
    chunks: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Structured document chunks data when only_need_context=True",
    )

class DatasetQueryContextResponse(BaseModel):
    context_stats: Dict[str, Any] = Field(description="Query context statistics")
    dataset_id: str = Field(description="Dataset ID")


# Cross-dataset query models
class CrossDatasetQueryRequest(BaseModel):
    """Request model for cross-dataset query operations."""

    query: str = Field(min_length=1, description="The query text")
    dataset_ids: List[str] = Field(
        min_items=1,
        max_items=10,
        description="List of dataset IDs to query (1-10 datasets)"
    )
    document_filters: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="Optional document ID filters per dataset. Format: {dataset_id: [doc_id1, doc_id2, ...]}"
    )
    mode: str = Field(
        default="mix",
        description="Query mode: local, global, hybrid, naive, mix, bypass"
    )
    only_need_context: Optional[bool] = Field(
        default=None,
        description="Only return context without response"
    )
    only_need_prompt: Optional[bool] = Field(
        default=None,
        description="Only return prompt without response"
    )
    response_type: Optional[str] = Field(
        default=None,
        description="Response format type"
    )
    top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
        description="Number of top results per dataset"
    )
    chunk_top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
        description="Number of top chunks in final merged results"
    )
    max_entity_tokens: Optional[int] = Field(
        default=None,
        ge=1,
        description="Max tokens for entity context"
    )
    max_relation_tokens: Optional[int] = Field(
        default=None,
        ge=1,
        description="Max tokens for relation context"
    )
    max_total_tokens: Optional[int] = Field(
        default=None,
        ge=1,
        description="Max total tokens budget"
    )
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Conversation history"
    )
    history_turns: Optional[int] = Field(
        default=None,
        ge=0,
        description="Number of conversation turns"
    )
    user_prompt: Optional[str] = Field(
        default=None,
        description="Custom user prompt"
    )
    enable_rerank: Optional[bool] = Field(
        default=True,
        description="Enable cross-dataset reranking"
    )
    max_results_per_dataset: Optional[int] = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum results to retrieve per dataset before merging"
    )

    @field_validator("dataset_ids")
    @classmethod
    def validate_dataset_ids(cls, v):
        """Validate dataset IDs are not empty and contain valid UUIDs."""
        if not v:
            raise ValueError("At least one dataset ID is required")

        # Basic UUID format validation
        import uuid
        for dataset_id in v:
            try:
                uuid.UUID(dataset_id, version=4)
            except ValueError:
                raise ValueError(f"Invalid dataset ID format: {dataset_id}")

        return v

    @field_validator("document_filters")
    @classmethod
    def validate_document_filters(cls, v, info):
        """Validate document filters format and consistency with dataset_ids."""
        if v is None:
            return v

        # Check if all keys in document_filters are valid dataset IDs
        dataset_ids = info.data.get("dataset_ids", [])
        for dataset_id in v.keys():
            if dataset_id not in dataset_ids:
                raise ValueError(
                    f"Document filter dataset_id '{dataset_id}' not found in dataset_ids list"
                )

        # Validate document ID lists are not empty
        for dataset_id, doc_ids in v.items():
            if not doc_ids or not isinstance(doc_ids, list):
                raise ValueError(
                    f"Document IDs list for dataset '{dataset_id}' must be a non-empty list"
                )

        return v


class CrossDatasetQueryResponse(BaseModel):
    """Response model for cross-dataset query operations."""

    response: str = Field(description="Generated query response")
    query: str = Field(description="Original query text")
    dataset_count: int = Field(description="Number of datasets successfully queried")
    total_chunks: int = Field(description="Total number of chunks in merged results")
    query_mode: str = Field(description="Query mode used")
    dataset_results: Dict[str, Any] = Field(
        description="Individual dataset query results and metadata"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Merged context information from all datasets"
    )
    performance_stats: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Query performance statistics"
    )


class CrossDatasetQueryContextResponse(BaseModel):
    """Response model for cross-dataset context-only queries."""

    query: str = Field(description="Original query text")
    dataset_count: int = Field(description="Number of datasets successfully queried")
    total_chunks: int = Field(description="Total number of chunks in merged results")
    context: Dict[str, Any] = Field(description="Merged context information from all datasets")
    dataset_results: Dict[str, Any] = Field(
        description="Individual dataset context results and metadata"
    )
    performance_stats: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Query performance statistics"
    )


class DatasetSearchRequest(BaseModel):
    query: str = Field(min_length=1, description="Search query")
    search_type: str = Field(default="all", description="Search type: entities, relations, chunks, all")
    top_k: int = Field(default=10, ge=1, le=100, description="Number of top results")

class DatasetSearchResponse(BaseModel):
    results: Dict[str, List[Dict[str, Any]]] = Field(description="Search results by type")
    dataset_id: str = Field(description="Dataset ID")
    query: str = Field(description="Original query")


# Request Models
class CreateDatasetRequest(BaseModel):
    """Request model for creating a new dataset."""
    
    name: str = Field(
        min_length=1,
        max_length=255,
        description="Dataset name (must be unique)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional dataset description",
    )
    rag_type: str = Field(
        default="rag",
        description="RAG type (default: 'rag')",
    )
    workspace: Optional[str] = Field(
        default=None,
        description="Optional workspace identifier",
    )
    namespace_prefix: Optional[str] = Field(
        default=None,
        description="Optional namespace prefix",
    )
    storage_type: str = Field(
        default="local",
        description="Storage type: 'local', 'aliyun-oss', 'supabase', 's3' (default: 'local')",
    )
    chunk_engine: str = Field(
        default="default",
        description="Chunk engine type (default: 'default')",
    )
    schedule: Optional[str] = Field(
        default=None,
        description="Optional schedule configuration",
    )
    args: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional arguments as JSON",
    )
    created_by: Optional[str] = Field(
        default=None,
        description="Creator identifier",
    )
    owner_id: Optional[str] = Field(
        default=None,
        description="Owner identifier",
    )
    visibility: str = Field(
        default="private",
        description="Dataset visibility ('private', 'public')",
    )
    default_permission: str = Field(
        default="none",
        description="Default permission level",
    )

    @field_validator('storage_type')
    @classmethod
    def validate_storage_type(cls, v):
        """Validate storage type is one of the allowed values."""
        allowed_types = ['local', 'aliyun-oss', 'supabase', 's3']
        if v not in allowed_types:
            raise ValueError(f"storage_type must be one of {allowed_types}, got '{v}'")
        return v

    @field_validator("name", mode="after")
    @classmethod
    def name_strip_after(cls, name: str) -> str:
        return name.strip()


class UpdateDatasetRequest(BaseModel):
    """Request model for updating a dataset."""
    
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Dataset description",
    )
    rag_type: Optional[str] = Field(
        default=None,
        description="RAG type",
    )
    workspace: Optional[str] = Field(
        default=None,
        description="Workspace identifier",
    )
    namespace_prefix: Optional[str] = Field(
        default=None,
        description="Namespace prefix",
    )
    status: Optional[str] = Field(
        default=None,
        description="Dataset status",
    )
    storage_type: Optional[str] = Field(
        default=None,
        description="Storage type",
    )
    chunk_engine: Optional[str] = Field(
        default=None,
        description="Chunk engine type",
    )
    schedule: Optional[str] = Field(
        default=None,
        description="Schedule configuration",
    )
    args: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional arguments as JSON",
    )
    owner_id: Optional[str] = Field(
        default=None,
        description="Owner identifier",
    )
    visibility: Optional[str] = Field(
        default=None,
        description="Dataset visibility",
    )
    default_permission: Optional[str] = Field(
        default=None,
        description="Default permission level",
    )


# Response Models
class DatasetInfo(BaseModel):
    """Dataset information model."""

    dataset_uuid: str = Field(description="Dataset UUID (Primary Key)")
    name: str = Field(description="Dataset name")
    description: Optional[str] = Field(description="Dataset description")
    rag_type: str = Field(description="RAG type")
    workspace: Optional[str] = Field(description="Workspace")
    namespace_prefix: Optional[str] = Field(description="Namespace prefix")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Update timestamp")
    status: str = Field(description="Dataset status")
    storage_type: str = Field(description="Storage type")
    chunk_engine: str = Field(description="Chunk engine")
    schedule: Optional[str] = Field(description="Schedule")
    args: Dict[str, Any] = Field(description="Additional arguments")
    created_by: Optional[str] = Field(description="Creator")
    owner_id: Optional[str] = Field(description="Owner ID")
    visibility: str = Field(description="Visibility")
    default_permission: str = Field(description="Default permission")


class DatasetListResponse(BaseModel):
    """Response model for dataset list."""
    
    datasets: List[DatasetInfo] = Field(description="List of datasets")
    total: int = Field(description="Total number of datasets")
    page: int = Field(description="Current page")
    page_size: int = Field(description="Page size")


class DatasetResponse(BaseModel):
    """Response model for single dataset."""
    
    dataset: DatasetInfo = Field(description="Dataset information")


class DeleteDatasetResponse(BaseModel):
    """Response model for dataset deletion."""
    
    dataset_id: str = Field(description="Deleted dataset ID")
    name: str = Field(description="Deleted dataset name")
    status: str = Field(description="Deletion status")
    message: str = Field(description="Deletion message")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    dataset_id: Optional[str] = Field(default=None, description="Related dataset ID")


def create_dataset_routes(rag, api_key: Optional[str] = None):
    """Create dataset management routes.
    
    Args:
        rag: LightRAG instance
        api_key: Optional API key for authentication
    """
    combined_auth = get_combined_auth_dependency(api_key)
    
    # Initialize dataset manager
    # Get database configuration from environment
    import os
    db_config = {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", 5432)),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "database": os.getenv("POSTGRES_DATABASE"),
        "workspace": os.getenv("POSTGRES_WORKSPACE", "default"),
        "max_connections": int(os.getenv("POSTGRES_MAX_CONNECTIONS", 20)),
    }
    
    dataset_manager = DatasetManager(db_config)

    @router.post(
        "/datasets",
        response_model=DatasetResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            400: {"model": ErrorResponse, "description": "Dataset already exists or invalid configuration"},
            500: {"model": ErrorResponse, "description": "Internal server error"},
        }
    )
    async def create_dataset(
        request: CreateDatasetRequest,
        background_tasks: BackgroundTasks
    ):
        """
        Create a new dataset.
        
        Creates a new dataset with the specified configuration and initializes
        the corresponding PostgreSQL schemas for data isolation.
        """
        try:
            timing_start(f"Creating dataset: {request.name}")
            dataset_info = await dataset_manager.create_dataset(
                name=request.name,
                description=request.description,
                rag_type=request.rag_type,
                workspace=request.workspace,
                namespace_prefix=request.namespace_prefix,
                storage_type=request.storage_type,
                chunk_engine=request.chunk_engine,
                schedule=request.schedule,
                args=request.args,
                created_by=request.created_by,
                owner_id=request.owner_id,
                visibility=request.visibility,
                default_permission=request.default_permission,
            )
            timing_end(f"Creating dataset: {request.name}")

            # Initialize auto-embedding task if storage type is not local
            if auto_embedding_available and request.storage_type != 'local':
                try:
                    # Create a temporary Dataset model for AutoEmbeddingService
                    if DatasetModel:
                        temp_dataset = DatasetModel(
                            dataset_uuid=dataset_info['dataset_uuid'],
                            name=dataset_info['name'],
                            description=dataset_info.get('description'),
                            rag_type=dataset_info.get('rag_type', 'rag'),
                            workspace=dataset_info.get('workspace'),
                            namespace_prefix=dataset_info.get('namespace_prefix'),
                            storage_type=request.storage_type,
                            chunk_engine=dataset_info.get('chunk_engine', 'default'),
                            schedule=dataset_info.get('schedule'),
                            args=dataset_info.get('args', {}),
                            created_by=dataset_info.get('created_by'),
                            owner_id=dataset_info.get('owner_id'),
                            visibility=dataset_info.get('visibility', 'private'),
                            default_permission=dataset_info.get('default_permission', 'none'),
                            status=dataset_info.get('status', 'active'),
                            created_at=dataset_info.get('created_at'),
                            updated_at=dataset_info.get('updated_at')
                        )
                        auto_service = AutoEmbeddingService()
                        await auto_service.init_auto_embedding_task(
                            temp_dataset,
                            background_tasks=background_tasks
                        )
                        logger.info(f"Auto-embedding task initialized for dataset: {request.name}")
                except Exception as e:
                    # Don't fail dataset creation if auto-embedding initialization fails
                    logger.warning(f"Failed to initialize auto-embedding for dataset {request.name}: {e}")

            return DatasetResponse(dataset=DatasetInfo(**dataset_info))
            
        except DatasetAlreadyExistsError as e:
            raise HTTPException(
                status_code=400,
                detail={"error": "DatasetAlreadyExists", "message": str(e), "dataset_id": e.dataset_id}
            )
        except DatasetConfigurationError as e:
            raise HTTPException(
                status_code=400,
                detail={"error": "DatasetConfiguration", "message": str(e), "dataset_id": e.dataset_id}
            )
        except Exception as e:
            logger.error(f"Failed to create dataset: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets",
        response_model=DatasetListResponse,
        dependencies=[Depends(combined_auth)],
    )
    async def list_datasets(
        owner_id: Optional[str] = Query(None, description="Filter by owner ID"),
        status: Optional[str] = Query(None, description="Filter by status"),
        visibility: Optional[str] = Query(None, description="Filter by visibility"),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Page size"),
    ):
        """
        List datasets with optional filtering and pagination.
        """
        try:
            offset = (page - 1) * page_size
            datasets = await dataset_manager.list_datasets(
                owner_id=owner_id,
                status=status,
                visibility=visibility,
                limit=page_size,
                offset=offset,
            )
            
            # For now, return count as length since we don't have a separate count query
            # In production, you'd want to implement a proper count query
            total = len(datasets) + offset  # This is an approximation
            
            dataset_list = [DatasetInfo(**dataset) for dataset in datasets]
            
            return DatasetListResponse(
                datasets=dataset_list,
                total=total,
                page=page,
                page_size=page_size,
            )
            
        except Exception as e:
            logger.error(f"Failed to list datasets: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets/{dataset_id}",
        response_model=DatasetResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def get_dataset(
        dataset_id: str = Path(..., description="Dataset UUID"),
    ):
        """
        Get dataset by ID.
        """
        try:
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )
            
            return DatasetResponse(dataset=DatasetInfo(**dataset_info))
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.put(
        "/datasets/{dataset_id}",
        response_model=DatasetResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
            400: {"model": ErrorResponse, "description": "Invalid configuration"},
        }
    )
    async def update_dataset(
        dataset_id: str = Path(..., description="Dataset UUID"),
        request: UpdateDatasetRequest = None,
    ):
        """
        Update dataset information.
        """
        try:
            # Convert request to dict and filter out None values
            updates = request.model_dump(exclude_none=True) if request else {}
            
            if not updates:
                # If no updates provided, just return current dataset
                dataset_info = await dataset_manager.get_dataset(dataset_id)
                if not dataset_info:
                    raise HTTPException(
                        status_code=404,
                        detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                    )
                return DatasetResponse(dataset=DatasetInfo(**dataset_info))
            
            dataset_info = await dataset_manager.update_dataset(dataset_id, **updates)
            
            return DatasetResponse(dataset=DatasetInfo(**dataset_info))
            
        except DatasetNotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail={"error": "DatasetNotFound", "message": str(e), "dataset_id": e.dataset_id}
            )
        except DatasetConfigurationError as e:
            raise HTTPException(
                status_code=400,
                detail={"error": "DatasetConfiguration", "message": str(e), "dataset_id": e.dataset_id}
            )
        except Exception as e:
            logger.error(f"Failed to update dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.delete(
        "/datasets/{dataset_id}",
        response_model=DeleteDatasetResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def delete_dataset(
        dataset_id: str = Path(..., description="Dataset UUID"),
    ):
        """
        Delete dataset and all its data.
        
        This operation is irreversible and will remove all data associated with the dataset,
        including all documents, entities, relations, and schemas.
        """
        try:
            result = await dataset_manager.delete_dataset(dataset_id)
            
            return DeleteDatasetResponse(**result)
            
        except DatasetNotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail={"error": "DatasetNotFound", "message": str(e), "dataset_id": e.dataset_id}
            )
        except SchemaCreationError as e:
            raise HTTPException(
                status_code=500,
                detail={"error": "SchemaError", "message": str(e), "dataset_id": e.dataset_id}
            )
        except Exception as e:
            logger.error(f"Failed to delete dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    # Dataset-aware document API endpoints

    class DatasetDocumentUploadResponse(BaseModel):
        status: str = Field(default="success", description="Upload status")
        message: str = Field(description="Status message")
        track_id: str = Field(description="Tracking ID for monitoring processing")
        dataset_id: Optional[str] = Field(default=None, description="Dataset ID")
        doc_id: Optional[str] = Field(default=None, description="Document ID (available immediately)")
        file_url: Optional[str] = Field(default=None, description="Remote file URL (for remote uploads)")
        storage_type: Optional[str] = Field(default=None, description="Storage type (for remote uploads)")
        original_filename: Optional[str] = Field(default=None, description="Original filename")

    class DatasetDocumentTextRequest(BaseModel):
        text: str = Field(min_length=1, description="Text content to insert")
        file_source: Optional[str] = Field(default="text_input", description="Source identifier for the text")

    class DatasetDocumentTextsRequest(BaseModel):
        texts: List[str] = Field(min_items=1, description="List of text contents to insert")
        file_sources: Optional[List[str]] = Field(default=None, description="List of source identifiers for each text")

    class DatasetDocumentListResponse(BaseModel):
        documents: List[Dict[str, Any]] = Field(description="List of documents")
        total_count: int = Field(description="Total number of documents")
        dataset_id: str = Field(description="Dataset ID")

    class DatasetDocumentStatsResponse(BaseModel):
        statistics: Dict[str, Any] = Field(description="Document statistics")
        dataset_id: str = Field(description="Dataset ID")

    # Helper functions for unified upload endpoint

    def _parse_multimodal_config(multimodal_config: Optional[str]) -> Optional[MultimodalUploadRequest]:
        """Parse and validate multimodal configuration."""
        if not multimodal_config:
            return None

        try:
            import json
            multimodal_data = json.loads(multimodal_config)

            # Merge environment variables with request data
            from lightrag.api.config import parse_args
            args = parse_args()

            # Create merged configuration with environment variables as defaults
            merged_config = {
                # MinerU API configuration
                "mineru_api_token": args.mineru_api_token,
                "mineru_api_base_url": args.mineru_api_base_url,
                "mineru_enable_ocr": args.mineru_enable_ocr,
                "mineru_enable_formula": args.mineru_enable_formula,
                "mineru_enable_table": args.mineru_enable_table,
                "mineru_language": args.mineru_language,
                "mineru_max_file_size": args.mineru_max_file_size,
                "mineru_timeout": args.mineru_timeout,
                "mineru_max_retries": args.mineru_max_retries,
                "mineru_retry_delay": args.mineru_retry_delay,
                "mineru_debug_save_files": args.mineru_debug_save_files,
                "mineru_max_images": args.mineru_max_images,
                "mineru_max_concurrent": args.mineru_max_concurrent,

                # OSS configuration
                "oss_endpoint": getattr(args, 'oss_endpoint', None),
                "oss_access_key_id": getattr(args, 'oss_access_key_id', None),
                "oss_access_key_secret": getattr(args, 'oss_access_key_secret', None),
                "oss_bucket_name": getattr(args, 'oss_bucket_name', None),

                # Vision model configuration
                "mineru_vision_model_enabled": args.mineru_vision_model_enabled,
                "mineru_vision_model_name": args.mineru_vision_model_name,
                "mineru_vision_model_api_key": args.mineru_vision_model_api_key,
                "mineru_vision_model_base_url": args.mineru_vision_model_base_url,

                # Performance configuration
                "mineru_max_concurrent": getattr(args, 'mineru_max_concurrent', 5),

                # file_parse compatibility defaults
                "mineru_return_md": getattr(args, 'mineru_return_md', True),
                "mineru_return_middle_json": getattr(args, 'mineru_return_middle_json', True),
                "mineru_return_images": getattr(args, 'mineru_return_images', True),
                "mineru_start_page_id": getattr(args, 'mineru_start_page_id', 0),
                "mineru_end_page_id": getattr(args, 'mineru_end_page_id', 100),
                "mineru_backend": getattr(args, 'mineru_backend', None),
                "mineru_parse_method": getattr(args, 'mineru_parse_method', None),
                "mineru_server_url": getattr(args, 'mineru_server_url', None),

                # Default values for other fields
                "enable_multimodal_parsing": False,
                "file_upload_method": "oss",
            }

            # Override with request data (request data has higher priority)
            merged_config.update(multimodal_data)

            return MultimodalUploadRequest(**merged_config)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=400,
                detail={"error": "InvalidConfig", "message": f"Invalid multimodal configuration: {e}"}
            )

    async def _handle_local_upload(
        background_tasks: BackgroundTasks,
        dataset_rag: LightRAG,
        dataset_id: str,
        track_id: str,
        file: UploadFile,
        original_filename: Optional[str],
        multimodal_config: Optional[str]
    ) -> DatasetDocumentUploadResponse:
        """Handle local file upload processing."""
        import tempfile
        import os
        from pathlib import Path

        # Use provided filename or fall back to uploaded filename
        filename_to_use = original_filename or file.filename

        # Create temporary file with original filename suffix for better identification
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename_to_use}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = FilePath(temp_file.name)

        try:
            # Generate doc_id immediately from file content
            from ...utils import compute_mdhash_id, clean_text

            # Decode content and clean it for doc_id generation
            try:
                # Try to decode as text for doc_id generation
                if isinstance(content, bytes):
                    text_content = content.decode('utf-8', errors='ignore')
                else:
                    text_content = str(content)

                # Clean the text content
                cleaned_content = clean_text(text_content)

                # Generate doc_id using the same logic as in apipeline_enqueue_documents
                doc_id = compute_mdhash_id(cleaned_content, prefix="doc-")
                logger.info(f"Generated doc_id immediately: {doc_id} for file: {filename_to_use}")

            except Exception as doc_id_error:
                logger.warning(f"Failed to generate doc_id immediately for {filename_to_use}: {doc_id_error}")
                doc_id = None

            # Parse multimodal configuration
            multimodal_request = _parse_multimodal_config(multimodal_config)

            # Create wrapper function for background processing with cleanup
            async def process_with_cleanup():
                try:
                    if multimodal_request and multimodal_request.enable_multimodal_parsing:
                        # Use multimodal processing pipeline
                        await pipeline_multimodal_index_file(
                            dataset_rag,
                            temp_file_path,
                            track_id,
                            multimodal_request,
                            original_filename=filename_to_use,
                            doc_id=doc_id
                        )
                    else:
                        # Use standard processing pipeline
                        from ..routers.document_routes import pipeline_index_file
                        await pipeline_index_file(
                            dataset_rag,
                            temp_file_path,
                            track_id,
                            original_filename=filename_to_use
                        )
                finally:
                    # Clean up temp file after processing
                    try:
                        if temp_file_path.exists():
                            os.unlink(temp_file_path)
                            logger.info(f"Cleaned up temporary file: {temp_file_path}")
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to clean up temp file {temp_file_path}: {cleanup_error}")

            # Choose processing pipeline based on multimodal configuration
            if multimodal_request and multimodal_request.enable_multimodal_parsing:
                message = f"File '{filename_to_use}' accepted for multimodal processing in dataset {dataset_id}"
            else:
                message = f"File '{filename_to_use}' accepted for processing in dataset {dataset_id}"

            # Add processing task with cleanup to background tasks
            background_tasks.add_task(process_with_cleanup)

            return DatasetDocumentUploadResponse(
                status="accepted",
                message=message,
                track_id=track_id,
                dataset_id=dataset_id,
                doc_id=doc_id,
                original_filename=filename_to_use
            )
        except Exception as e:
            # Clean up temp file on error
            if temp_file_path.exists():
                os.unlink(temp_file_path)
            raise e

    async def _handle_remote_upload(
        background_tasks: BackgroundTasks,
        dataset_rag: LightRAG,
        dataset_id: str,
        track_id: str,
        remote_file_path: str,
        remote_storage_type: str,
        remote_storage_config: Optional[str],
        original_filename: Optional[str],
        multimodal_config: Optional[str],
        dataset_info: Optional[Dict[str, Any]] = None
    ) -> DatasetDocumentUploadResponse:
        """Handle remote file upload processing."""

        # Parse storage configuration
        storage_config = {}
        if remote_storage_config:
            try:
                import json
                storage_config = json.loads(remote_storage_config)
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400,
                    detail={"error": "InvalidConfig", "message": f"Invalid remote_storage_config JSON: {e}"}
                )

        # Parse multimodal configuration
        multimodal_request = _parse_multimodal_config(multimodal_config)

        # Validate storage configuration completeness
        # Note: We don't inherit from dataset config because the user might want to download
        # from a different storage source than where the dataset stores its data
        if not storage_config:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "InvalidConfig",
                    "message": "remote_storage_config is required for remote file upload"
                }
            )

        # Create wrapper function for background processing
        async def process_remote_file_with_cleanup():
            try:
                await process_remote_file(
                    rag=dataset_rag,
                    file_url=remote_file_path,
                    storage_type=remote_storage_type,
                    storage_config=storage_config,
                    track_id=track_id,
                    original_filename=original_filename,
                    multimodal_request=multimodal_request,
                    dataset_config=None,  # Don't pass dataset config to avoid confusion
                    doc_id=doc_id
                )
                logger.info(f"Successfully processed remote file: {remote_file_path} for dataset {dataset_id}")
            except Exception as e:
                logger.error(f"Failed to process remote file {remote_file_path} for dataset {dataset_id}: {e}")
                raise

        # Add background task
        background_tasks.add_task(process_remote_file_with_cleanup)

        # Determine filename for response
        filename_for_response = original_filename
        if not filename_for_response:
            # Try to infer filename from path
            from lightrag.api.utils.storage_manager import infer_filename_from_url
            filename_for_response = infer_filename_from_url(remote_file_path)

        # Try to generate doc_id immediately by downloading and processing the file content
        doc_id = None
        try:
            # Import necessary modules
            from lightrag.api.utils.storage_manager import StorageConfigManager, RemoteFileDownloader
            from lightrag.utils import clean_text, compute_mdhash_id
            import tempfile
            import os
            from pathlib import Path

            # Create storage client
            storage_client = StorageConfigManager.create_storage_client(
                storage_type=remote_storage_type,
                config=storage_config
            )

            # Download file to memory for doc_id generation (with size limit)
            try:
                content = await RemoteFileDownloader.download_to_memory(
                    storage_client=storage_client,
                    remote_path=remote_file_path,
                    storage_type=remote_storage_type,
                    max_size_mb=50,  # Limit to 50MB for immediate processing
                    timeout_seconds=15  # Quick timeout for immediate response
                )

                # Try to decode as text for doc_id generation
                if isinstance(content, bytes):
                    text_content = content.decode('utf-8', errors='ignore')
                else:
                    text_content = str(content)

                # Clean the text content
                cleaned_content = clean_text(text_content)

                # Generate doc_id using the same logic as local uploads
                doc_id = compute_mdhash_id(cleaned_content, prefix="doc-")
                logger.info(f"Generated doc_id immediately for remote file: {doc_id} for file: {filename_for_response}")

            except Exception as download_error:
                logger.warning(f"Failed to download file for immediate doc_id generation: {download_error}")
                logger.info(f"doc_id will be generated during background processing for: {filename_for_response}")

        except Exception as doc_id_error:
            logger.warning(f"Failed to generate doc_id immediately for remote file {filename_for_response}: {doc_id_error}")

        # Choose message based on multimodal configuration
        if multimodal_request and multimodal_request.enable_multimodal_parsing:
            message = f"Remote file '{filename_for_response}' accepted for multimodal processing in dataset {dataset_id}"
        else:
            message = f"Remote file '{filename_for_response}' accepted for processing in dataset {dataset_id}"

        return DatasetDocumentUploadResponse(
            status="accepted",
            message=message,
            track_id=track_id,
            dataset_id=dataset_id,
            doc_id=doc_id,  # Now includes immediately generated doc_id when possible
            file_url=remote_file_path,
            storage_type=remote_storage_type,
            original_filename=filename_for_response
        )

    @router.post(
        "/datasets/{dataset_id}/documents/upload",
        response_model=DatasetDocumentUploadResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
            400: {"model": ErrorResponse, "description": "Invalid file type, upload error, or invalid remote file configuration"},
            500: {"model": ErrorResponse, "description": "Internal server error"},
        }
    )
    async def upload_document_to_dataset(
        background_tasks: BackgroundTasks,
        dataset_id: str = Path(..., description="Dataset UUID"),
        # Local file upload (optional)
        file: Optional[UploadFile] = File(None, description="File to upload"),
        # Remote file upload (optional)
        remote_file_path: Optional[str] = Form(None, description="Remote file path (relative path in storage bucket)"),
        remote_storage_type: Optional[str] = Form(None, description="Remote storage type (aliyun-oss, supabase, s3)"),
        remote_storage_config: Optional[str] = Form(None, description="JSON string of remote storage configuration"),
        # Common parameters
        original_filename: Optional[str] = Form(None, description="Original filename (for remote files or to override local filename)"),
        multimodal_config: Optional[str] = Form(None, description="JSON string of multimodal configuration")
    ):
        """
        Upload a document to a specific dataset.

        This unified endpoint supports both local file uploads and remote file processing.
        Files are processed in the background and indexed for querying within the
        dataset's isolated environment.

        **Upload Methods:**
        1. **Local File Upload**: Provide 'file' parameter with multipart/form-data
        2. **Remote File Upload**: Provide 'remote_file_path', 'remote_storage_type', and 'remote_storage_config'

        **Supported Remote Storage:**
        - Alibaba Cloud OSS (aliyun-oss)
        - Supabase Storage (supabase)
        - Amazon S3 (s3)

        **Storage Configuration Parameters:**

        For **Supabase** (supports both formats for compatibility):
        - Standardized format (recommended): `SUPABASE_URL`, `SUPABASE_API_KEY`, `SUPABASE_BUCKET_NAME`
        - Legacy format: `url`, `api_key`, `bucket_name`
        - **Note**: Must provide complete configuration for the storage source you want to download from

        For **Alibaba Cloud OSS** (supports both formats for compatibility):
        - Standardized format (recommended): `ALIYUN_OSS_ACCESS_KEY`, `ALIYUN_OSS_SECRET_KEY`, `ALIYUN_OSS_ENDPOINT`, `ALIYUN_OSS_BUCKET_NAME`
        - Legacy format: `access_key_id`, `access_key_secret`, `endpoint`, `bucket_name`
        - **Note**: Must provide complete configuration for the storage source you want to download from

        **Processing Options:**
        - Standard document processing (default)
        - Multimodal processing with MinerU (when multimodal_config is provided)

        **Examples:**

        Local file upload:
        ```
        curl -X POST "/datasets/{id}/documents/upload" \\
          -F "file=@document.pdf" \\
          -F "multimodal_config={...}"
        ```

        Remote file upload examples:

        **Supabase (standardized format - recommended):**
        ```
        curl -X POST "/datasets/{id}/documents/upload" \\
          -F "remote_file_path=documents/file.pdf" \\
          -F "remote_storage_type=supabase" \\
          -F "remote_storage_config={\"SUPABASE_URL\":\"http://8.152.126.86\",\"SUPABASE_API_KEY\":\"your_key\",\"SUPABASE_BUCKET_NAME\":\"rag\"}" \\
          -F "original_filename=document.pdf"
        ```

        **Alibaba Cloud OSS (standardized format - recommended):**
        ```
        curl -X POST "/datasets/{id}/documents/upload" \\
          -F "remote_file_path=documents/file.pdf" \\
          -F "remote_storage_type=aliyun-oss" \\
          -F "remote_storage_config={\"ALIYUN_OSS_ACCESS_KEY\":\"your_key\",\"ALIYUN_OSS_SECRET_KEY\":\"your_secret\",\"ALIYUN_OSS_ENDPOINT\":\"oss-cn-hangzhou.aliyuncs.com\",\"ALIYUN_OSS_BUCKET_NAME\":\"your_bucket\"}" \\
          -F "original_filename=document.pdf"
        ```
        """
        try:
            # Parameter validation
            if file is None and remote_file_path is None:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "InvalidParameters",
                        "message": "Either 'file' (for local upload) or 'remote_file_path' (for remote upload) must be provided"
                    }
                )

            if file is not None and remote_file_path is not None:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "InvalidParameters",
                        "message": "Cannot provide both 'file' and 'remote_file_path'. Choose either local or remote upload"
                    }
                )

            # Validate remote upload parameters
            if remote_file_path is not None:
                if not remote_storage_type:
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "error": "InvalidParameters",
                            "message": "remote_storage_type is required when using remote_file_path"
                        }
                    )

                # Validate storage type
                valid_storage_types = ["aliyun-oss", "supabase", "s3"]
                if remote_storage_type not in valid_storage_types:
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "error": "InvalidParameters",
                            "message": f"Invalid remote_storage_type. Must be one of: {valid_storage_types}"
                        }
                    )

            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter
            adapter = DatasetAdapter(dataset_id, db_config)

            # Determine upload type and generate appropriate track_id
            is_remote_upload = remote_file_path is not None
            upload_type = "remote" if is_remote_upload else "local"

            track_id_prefix = f"dataset_{upload_type}_upload"
            if multimodal_config:
                track_id_prefix = f"dataset_{upload_type}_multimodal_upload"
            track_id = generate_track_id(track_id_prefix)

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            dataset_rag = await rag_manager.get_instance(dataset_model)

            # Route to appropriate processing method
            if is_remote_upload:
                # Handle remote file upload
                return await _handle_remote_upload(
                    background_tasks=background_tasks,
                    dataset_rag=dataset_rag,
                    dataset_id=dataset_id,
                    track_id=track_id,
                    remote_file_path=remote_file_path,
                    remote_storage_type=remote_storage_type,
                    remote_storage_config=remote_storage_config,
                    original_filename=original_filename,
                    multimodal_config=multimodal_config,
                    dataset_info=dataset_info
                )
            else:
                # Handle local file upload
                return await _handle_local_upload(
                    background_tasks=background_tasks,
                    dataset_rag=dataset_rag,
                    dataset_id=dataset_id,
                    track_id=track_id,
                    file=file,
                    original_filename=original_filename,
                    multimodal_config=multimodal_config
                )



        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to upload document to dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )



    @router.post(
        "/datasets/{dataset_id}/documents/text",
        response_model=DatasetDocumentUploadResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def insert_text_to_dataset(
        background_tasks: BackgroundTasks,
        dataset_id: str,
        request: DatasetDocumentTextRequest
    ):
        """
        Insert text content into a specific dataset.

        This endpoint accepts text content and processes it within the
        specified dataset's isolated environment.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Generate track_id
            track_id = generate_track_id("dataset_text")

            # Generate doc_id immediately from text content
            from ...utils import compute_mdhash_id, clean_text
            try:
                # Clean the text content
                cleaned_content = clean_text(request.text)

                # Generate doc_id using the same logic as in apipeline_enqueue_documents
                doc_id = compute_mdhash_id(cleaned_content, prefix="doc-")
                logger.info(f"Generated doc_id immediately for text: {doc_id}")

            except Exception as doc_id_error:
                logger.warning(f"Failed to generate doc_id immediately for text: {doc_id_error}")
                doc_id = None

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            dataset_rag = await rag_manager.get_instance(dataset_model)

            # Process text through dataset-aware pipeline
            async def process_text_async():
                try:
                    await dataset_rag.apipeline_enqueue_documents(
                        request.text,
                        file_paths=request.file_source or "text_input",
                        track_id=track_id
                    )
                    await dataset_rag.apipeline_process_enqueue_documents()
                except Exception as e:
                    logger.error(f"Error processing text in dataset {dataset_id}: {e}")

            # Add to background tasks
            background_tasks.add_task(process_text_async)

            return DatasetDocumentUploadResponse(
                status="accepted",
                message=f"Text content accepted for processing in dataset {dataset_id}",
                track_id=track_id,
                dataset_id=dataset_id,
                doc_id=doc_id
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to insert text to dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets/{dataset_id}/track_status/{track_id}",
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found or track ID not found"},
        }
    )
    async def get_dataset_track_status(
        dataset_id: str = Path(..., description="Dataset UUID"),
        track_id: str = Path(..., description="Track ID to query")
    ):
        """
        Get the processing status of documents by tracking ID within a specific dataset.

        This endpoint retrieves all documents associated with a specific tracking ID
        within the dataset's isolated environment.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            dataset_rag = await rag_manager.get_instance(dataset_model)

            # Get documents by track_id from dataset-specific storage
            docs_by_track_id = await dataset_rag.aget_docs_by_track_id(track_id)

            if not docs_by_track_id:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "TrackIdNotFound", "message": f"No documents found for track_id: {track_id}", "track_id": track_id}
                )

            # Format response similar to the global track_status endpoint
            from ..routers.document_routes import DocStatusResponse, TrackStatusResponse, format_datetime

            documents = []
            status_summary = {}

            for doc_id, doc_status in docs_by_track_id.items():
                documents.append(
                    DocStatusResponse(
                        id=doc_id,
                        content_summary=doc_status.content_summary,
                        content_length=doc_status.content_length,
                        status=doc_status.status,
                        created_at=format_datetime(doc_status.created_at),
                        updated_at=format_datetime(doc_status.updated_at),
                        track_id=doc_status.track_id,
                        chunks_count=doc_status.chunks_count,
                        error_msg=doc_status.error_msg,
                        metadata=doc_status.metadata,
                        file_path=doc_status.file_path,
                    )
                )

                # Build status summary
                status_key = str(doc_status.status)
                status_summary[status_key] = status_summary.get(status_key, 0) + 1

            return TrackStatusResponse(
                track_id=track_id,
                documents=documents,
                total_count=len(documents),
                status_summary=status_summary,
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get track status for dataset {dataset_id}, track_id {track_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets/{dataset_id}/documents",
        response_model=DatasetDocumentListResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def list_dataset_documents(
        dataset_id: str = Path(..., description="Dataset UUID"),
        limit: int = Query(100, ge=1, le=1000, description="Maximum number of documents to return"),
        offset: int = Query(0, ge=0, description="Number of documents to skip")
    ):
        """
        List documents in a specific dataset.

        Returns a paginated list of documents stored in the specified dataset.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter and get documents
            adapter = DatasetAdapter(dataset_id, db_config)
            documents = await adapter.get_document_list(limit=limit, offset=offset)
            total_count = await adapter.get_document_count()

            return DatasetDocumentListResponse(
                documents=documents,
                total_count=total_count,
                dataset_id=dataset_id
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to list documents for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.post(
        "/datasets/{dataset_id}/query/stream",
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def query_dataset_stream(
        dataset_id: str = Path(..., description="Dataset UUID"),
        request: DatasetQueryRequest = Body(..., description="Query request parameters")
    ):
        """
        Stream query results for a specific dataset.

        This endpoint provides streaming query responses for the specified dataset,
        allowing real-time processing of query results with dataset-specific data isolation.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            dataset_rag = await rag_manager.get_instance(dataset_model)

            # Convert request to QueryParam
            from ..routers.query_routes import QueryParam
            param = QueryParam(
                mode=request.mode,
                only_need_context=request.only_need_context or False,
                only_need_prompt=request.only_need_prompt or False,
                response_type=request.response_type or "Multiple Paragraphs",
                stream=True,  # Enable streaming for this endpoint
                top_k=request.top_k or 60,
                chunk_top_k=request.chunk_top_k or 60,
                max_entity_tokens=request.max_entity_tokens or 4000,
                max_relation_tokens=request.max_relation_tokens or 4000,
                max_total_tokens=request.max_total_tokens or 8000,
                conversation_history=request.conversation_history or [],
                history_turns=request.history_turns,
                ids=request.ids,
                user_prompt=request.user_prompt,
                enable_rerank=request.enable_rerank or True
            )

            # Import streaming response utilities
            import json
            import asyncio

            async def generate_stream():
                """Generate streaming response chunks"""
                try:
                    logger.info(f"Starting dataset query with stream=True for query: {request.query[:50]}...")

                    # Execute streaming query using dataset-aware RAG
                    response = await dataset_rag.aquery(request.query, param=param)

                    logger.info(f"Dataset query completed, response type: {type(response)}")

                    if isinstance(response, str):
                        # If it's a string, send it all at once
                        logger.info(f"Sending string response: {len(response)} characters")
                        yield f"{json.dumps({'chunk': response})}\n"
                    elif response is None:
                        # Handle None response
                        logger.warning("Dataset query returned None response")
                        yield f"{json.dumps({'chunk': 'No relevant context found for the query.'})}\n"
                    else:
                        # If it's an async generator, send chunks one by one
                        logger.info("Processing async generator response")
                        chunk_count = 0
                        async for chunk in response:
                            if chunk:  # Only send non-empty content
                                chunk_count += 1
                                logger.debug(f"Sending chunk {chunk_count}: {chunk[:50]}...")
                                yield f"{json.dumps({'chunk': chunk})}\n"

                        logger.info(f"Completed streaming {chunk_count} chunks")

                except Exception as e:
                    # Send error as final chunk
                    logger.error(f"Dataset streaming error: {e}")
                    error_data = {"error": str(e)}
                    yield f"{json.dumps(error_data)}\n"

            return StreamingResponse(
                generate_stream(),
                media_type="application/x-ndjson",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"  # Disable nginx buffering
                }
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to stream query for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.post(
        "/datasets/{dataset_id}/documents/paginated",
        response_model=PaginatedDocsResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def get_dataset_documents_paginated(
        dataset_id: str = Path(..., description="Dataset UUID"),
        request: DocumentsRequest = Body(..., description="Pagination request parameters")
    ):
        """
        Get documents with pagination support for a specific dataset.

        This endpoint retrieves documents with pagination, filtering, and sorting capabilities
        for a specific dataset, providing better performance for large document collections.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter
            adapter = DatasetAdapter(dataset_id, db_config)

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            dataset_rag = await rag_manager.get_instance(dataset_model)

            # Get paginated documents and status counts in parallel
            docs_task = dataset_rag.doc_status.get_docs_paginated(
                status_filter=request.status_filter,
                page=request.page,
                page_size=request.page_size,
                sort_field=request.sort_field,
                sort_direction=request.sort_direction,
            )
            status_counts_task = dataset_rag.doc_status.get_all_status_counts()

            # Execute both queries in parallel
            (documents_with_ids, total_count), status_counts = await asyncio.gather(
                docs_task, status_counts_task
            )

            # Convert to response format
            doc_responses = []
            for doc_id, doc_status in documents_with_ids:
                # Helper function to safely convert datetime to ISO format
                def safe_isoformat(dt_value):
                    if dt_value is None:
                        return ""
                    if isinstance(dt_value, str):
                        return dt_value  # Already a string
                    if hasattr(dt_value, 'isoformat'):
                        return dt_value.isoformat()
                    return str(dt_value)

                doc_responses.append(DocStatusResponse(
                    id=doc_id,
                    content_summary=doc_status.content_summary or "",
                    content_length=doc_status.content_length or 0,
                    status=doc_status.status,
                    created_at=safe_isoformat(doc_status.created_at),
                    updated_at=safe_isoformat(doc_status.updated_at),
                    track_id=doc_status.track_id,
                    chunks_count=doc_status.chunks_count,
                    error_msg=doc_status.error_msg,
                    metadata=doc_status.metadata,
                    file_path=doc_status.file_path or "",
                ))

            # Calculate pagination info
            total_pages = (total_count + request.page_size - 1) // request.page_size
            has_next = request.page < total_pages
            has_prev = request.page > 1

            pagination = PaginationInfo(
                page=request.page,
                page_size=request.page_size,
                total_count=total_count,
                total_pages=total_pages,
                has_next=has_next,
                has_prev=has_prev,
            )

            return PaginatedDocsResponse(
                documents=doc_responses,
                pagination=pagination,
                status_counts=status_counts,
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get paginated documents for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.delete(
        "/datasets/{dataset_id}/documents",
        response_model=DeleteDocByIdResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def clear_dataset_documents(
        dataset_id: str = Path(..., description="Dataset UUID"),
        background_tasks: BackgroundTasks = BackgroundTasks()
    ):
        """
        Clear all documents from a specific dataset.

        This endpoint deletes all documents and their associated data from a dataset,
        including their status, text chunks, vector embeddings, and any related graph data.
        The deletion process runs in the background to avoid blocking the client connection.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            rag = await rag_manager.get_instance(dataset_model)

            # Create dataset-aware document manager
            from ..config import global_args
            doc_manager = DocumentManager(global_args.input_dir, workspace=global_args.workspace)

            # Import background deletion function
            from lightrag.kg.shared_storage import get_pipeline_status_lock, get_namespace_data

            # Get pipeline status
            pipeline_status = await get_namespace_data("pipeline_status")

            # Check if pipeline is busy
            if pipeline_status.get("busy", False):
                return DeleteDocByIdResponse(
                    status="busy",
                    message="Cannot clear documents while pipeline is busy",
                    doc_id="all",
                )

            # Add clear task to background tasks
            background_tasks.add_task(
                background_clear_dataset_documents,
                rag,
                doc_manager,
            )

            return DeleteDocByIdResponse(
                status="deletion_started",
                message=f"Document clearing started for dataset {dataset_id}",
                doc_id="all",
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to clear documents from dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.delete(
        "/datasets/{dataset_id}/documents/delete_document",
        response_model=DeleteDocByIdResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def delete_dataset_documents(
        dataset_id: str = Path(..., description="Dataset UUID"),
        delete_request: DeleteDocRequest = Body(..., description="Delete request parameters"),
        background_tasks: BackgroundTasks = BackgroundTasks()
    ):
        """
        Delete documents from a specific dataset.

        This endpoint deletes specific documents and all their associated data from a dataset,
        including their status, text chunks, vector embeddings, and any related graph data.
        The deletion process runs in the background to avoid blocking the client connection.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter
            adapter = DatasetAdapter(dataset_id, db_config)

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            rag = await rag_manager.get_instance(dataset_model)

            # Create dataset-aware document manager
            from ..config import global_args
            doc_manager = DocumentManager(global_args.input_dir, workspace=global_args.workspace)

            # Import background deletion function
            from lightrag.kg.shared_storage import get_dataset_namespace_data
            from lightrag.kg.dataset_pipeline_manager import DatasetPipelineManager

            doc_ids = delete_request.doc_ids

            # Get dataset pipeline status
            pipeline_manager = DatasetPipelineManager(dataset_id)
            await pipeline_manager.initialize()
            pipeline_status = await get_dataset_namespace_data("pipeline_status", dataset_id)

            # Check if dataset pipeline is busy
            if pipeline_status.get("busy", False):
                return DeleteDocByIdResponse(
                    status="busy",
                    message="Cannot delete documents while dataset pipeline is busy",
                    doc_id=", ".join(doc_ids),
                )

            # Note: Unlike the global document deletion endpoint, dataset-aware deletion
            # doesn't need to check enable_llm_cache_for_entity_extract because deletion
            # operations don't require LLM functionality and should always be allowed.

            # Add dataset-aware deletion task to background tasks
            background_tasks.add_task(
                background_delete_dataset_documents,
                rag,
                doc_manager,
                doc_ids,
                delete_request.delete_file,
                dataset_id,
            )

            return DeleteDocByIdResponse(
                status="deletion_started",
                message=f"Document deletion started for {len(doc_ids)} documents in dataset {dataset_id}",
                doc_id=", ".join(doc_ids),
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to delete documents from dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets/{dataset_id}/documents/statistics",
        response_model=DatasetDocumentStatsResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def get_dataset_document_statistics(
        dataset_id: str = Path(..., description="Dataset UUID")
    ):
        """
        Get document statistics for a specific dataset.

        Returns comprehensive statistics about documents in the specified dataset.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter and get statistics
            adapter = DatasetAdapter(dataset_id, db_config)
            statistics = await adapter.get_dataset_statistics()

            return DatasetDocumentStatsResponse(
                statistics=statistics,
                dataset_id=dataset_id
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get document statistics for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.post(
        "/datasets/{dataset_id}/documents/scan",
        response_model=ScanResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def scan_dataset_documents(
        dataset_id: str = Path(..., description="Dataset UUID"),
        background_tasks: BackgroundTasks = BackgroundTasks()
    ):
        """
        Trigger the scanning process for new documents in a specific dataset.

        This endpoint initiates a background task that scans the input directory for new documents
        and processes them within the dataset's isolated environment.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            dataset_rag = await rag_manager.get_instance(dataset_model)

            # Create dataset-aware document manager
            from ..config import global_args
            doc_manager = DocumentManager(global_args.input_dir, workspace=global_args.workspace)

            # Generate track_id with "scan" prefix for scanning operation
            from ..routers.document_routes import generate_track_id
            track_id = generate_track_id("scan")

            # Start the scanning process in the background with track_id
            background_tasks.add_task(run_dataset_scanning_process, dataset_rag, doc_manager, track_id)

            return ScanResponse(
                status="scanning_started",
                message=f"Scanning process has been initiated in the background for dataset {dataset_id}",
                track_id=track_id,
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to start scan for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    # Dataset-aware query API endpoints

    @router.post(
        "/datasets/{dataset_id}/query",
        response_model=DatasetQueryResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def query_dataset(
        dataset_id: str,
        request: DatasetQueryRequest
    ):
        """
        Query a specific dataset.

        This endpoint performs a query within the specified dataset's isolated
        environment, ensuring results are limited to the dataset's content.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            dataset_rag = await rag_manager.get_instance(dataset_model)

            # Convert request to QueryParam
            from ..routers.query_routes import QueryParam
            param = QueryParam(
                mode=request.mode,
                only_need_context=request.only_need_context or False,
                only_need_prompt=request.only_need_prompt or False,
                response_type=request.response_type or "Multiple Paragraphs",
                stream=False,  # Non-streaming for this endpoint
                top_k=request.top_k or 60,
                chunk_top_k=request.chunk_top_k or 60,
                max_entity_tokens=request.max_entity_tokens,
                max_relation_tokens=request.max_relation_tokens,
                max_total_tokens=request.max_total_tokens,
                conversation_history=request.conversation_history or [],
                history_turns=request.history_turns,
                ids=request.ids,
                user_prompt=request.user_prompt,
                enable_rerank=request.enable_rerank or True
            )

            # Execute query using dataset-aware RAG
            response = await dataset_rag.aquery(request.query, param=param)

            # Handle different response types
            if isinstance(response, str):
                # Check if this is a context-only response that needs to be parsed
                if param.only_need_context and response.startswith("-----Entities(KG)-----"):
                    return _parse_dataset_context_response(response, dataset_id, request.mode)
                response_text = response
            elif isinstance(response, dict):
                # Check if this is structured context data
                if param.only_need_context and all(key in response for key in ["entities", "relationships", "chunks"]):
                    return DatasetQueryResponse(
                        response="",
                        dataset_id=dataset_id,
                        query_mode=request.mode,
                        entities=response["entities"],
                        relationships=response["relationships"],
                        chunks=response["chunks"]
                    )
                else:
                    import json
                    response_text = json.dumps(response, indent=2)
            else:
                response_text = str(response)

            return DatasetQueryResponse(
                response=response_text,
                dataset_id=dataset_id,
                query_mode=request.mode
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to query dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets/{dataset_id}/query/context",
        response_model=DatasetQueryContextResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def get_dataset_query_context(
        dataset_id: str = Path(..., description="Dataset UUID"),
        query: str = Query(..., min_length=1, description="Query to analyze")
    ):
        """
        Get query context statistics for a specific dataset.

        This endpoint analyzes what context is available for a given query
        within the specified dataset.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter and get context stats
            adapter = DatasetAdapter(dataset_id, db_config)
            context_stats = await adapter.get_query_context_stats(query)

            return DatasetQueryContextResponse(
                context_stats=context_stats,
                dataset_id=dataset_id
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get query context for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    # Cross-dataset query API endpoints

    @router.post(
        "/datasets/cross-query",
        response_model=CrossDatasetQueryResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            400: {"model": ErrorResponse, "description": "Invalid request parameters"},
            404: {"model": ErrorResponse, "description": "One or more datasets not found"},
        }
    )
    async def cross_dataset_query(
        request: CrossDatasetQueryRequest = Body(..., description="Cross-dataset query request parameters")
    ):
        """
        Query multiple datasets simultaneously.

        This endpoint performs a query across multiple datasets in parallel,
        merges the results, and applies cross-dataset reranking for optimal
        result quality. Supports document ID filtering per dataset and
        maintains full traceability of result sources.

        Features:
        - Parallel query execution across multiple datasets
        - Cross-dataset result merging and reranking
        - Document ID filtering per dataset
        - Source dataset identification for each result
        - Comprehensive error handling with partial results
        """
        try:
            # Import CrossDatasetQueryEngine
            from ...dataset.cross_query_engine import CrossDatasetQueryEngine

            # Create query engine
            query_engine = CrossDatasetQueryEngine(db_config)

            # Convert request to QueryParam
            from ..routers.query_routes import QueryParam
            query_params = QueryParam(
                mode=request.mode,
                only_need_context=request.only_need_context or False,
                only_need_prompt=request.only_need_prompt or False,
                response_type=request.response_type or "Multiple Paragraphs",
                stream=False,  # Non-streaming for this endpoint
                top_k=request.top_k or 60,
                chunk_top_k=request.chunk_top_k or 20,
                max_entity_tokens=request.max_entity_tokens or 8000,
                max_relation_tokens=request.max_relation_tokens or 8000,
                max_total_tokens=request.max_total_tokens or 32000,
                conversation_history=request.conversation_history or [],
                history_turns=request.history_turns or 0,
                user_prompt=request.user_prompt,
                enable_rerank=request.enable_rerank if request.enable_rerank is not None else True
            )

            # Execute cross-dataset query
            result = await query_engine.query_multiple_datasets(
                query=request.query,
                dataset_ids=request.dataset_ids,
                document_filters=request.document_filters,
                query_params=query_params,
                max_results_per_dataset=request.max_results_per_dataset or 20
            )

            # Return structured response
            return CrossDatasetQueryResponse(
                response=result["response"],
                query=result["query"],
                dataset_count=result["dataset_count"],
                total_chunks=result["total_chunks"],
                query_mode=result["query_mode"],
                dataset_results=result["dataset_results"],
                context=result.get("context"),
                performance_stats=result.get("performance_stats")
            )

        except HTTPException:
            raise
        except DatasetNotFoundError as e:
            logger.warning(f"Dataset not found in cross-dataset query: {e}")
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "DatasetNotFound",
                    "message": str(e),
                    "dataset_id": getattr(e, 'dataset_id', None)
                }
            )
        except DatasetConfigurationError as e:
            logger.warning(f"Configuration error in cross-dataset query: {e}")
            # Check if this is a "all datasets failed" error
            if "All" in str(e) and "datasets failed" in str(e):
                raise HTTPException(
                    status_code=422,  # Unprocessable Entity - query was valid but all datasets failed
                    detail={
                        "error": "AllDatasetsFailed",
                        "message": str(e),
                        "dataset_id": getattr(e, 'dataset_id', None),
                        "suggestion": "Check dataset configurations and query parameters. Common issues: missing token limits, invalid query mode, or dataset connectivity problems."
                    }
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "ConfigurationError",
                        "message": str(e),
                        "dataset_id": getattr(e, 'dataset_id', None)
                    }
                )
        except ValueError as e:
            logger.warning(f"Invalid parameters in cross-dataset query: {e}")
            raise HTTPException(
                status_code=400,
                detail={"error": "InvalidParameters", "message": str(e)}
            )
        except Exception as e:
            logger.error(f"Failed to execute cross-dataset query: {e}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.post(
        "/datasets/cross-query/context",
        response_model=CrossDatasetQueryContextResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            400: {"model": ErrorResponse, "description": "Invalid request parameters"},
            404: {"model": ErrorResponse, "description": "One or more datasets not found"},
        }
    )
    async def cross_dataset_query_context(
        request: CrossDatasetQueryRequest = Body(..., description="Cross-dataset context query request")
    ):
        """
        Get context information from multiple datasets without generating a response.

        This endpoint retrieves and merges context information from multiple datasets
        without generating a final response, useful for understanding what information
        is available across datasets for a given query.
        """
        try:
            # Import CrossDatasetQueryEngine
            from ...dataset.cross_query_engine import CrossDatasetQueryEngine

            # Create query engine
            query_engine = CrossDatasetQueryEngine(db_config)

            # Convert request to QueryParam with context-only mode
            from ..routers.query_routes import QueryParam
            query_params = QueryParam(
                mode=request.mode,
                only_need_context=True,  # Force context-only mode
                only_need_prompt=False,
                response_type=request.response_type or "Multiple Paragraphs",
                stream=False,
                top_k=request.top_k or 60,
                chunk_top_k=request.chunk_top_k or 20,
                max_entity_tokens=request.max_entity_tokens,
                max_relation_tokens=request.max_relation_tokens,
                max_total_tokens=request.max_total_tokens,
                conversation_history=request.conversation_history or [],
                history_turns=request.history_turns,
                user_prompt=request.user_prompt,
                enable_rerank=request.enable_rerank if request.enable_rerank is not None else True
            )

            # Execute cross-dataset context query
            result = await query_engine.query_multiple_datasets(
                query=request.query,
                dataset_ids=request.dataset_ids,
                document_filters=request.document_filters,
                query_params=query_params,
                max_results_per_dataset=request.max_results_per_dataset or 20
            )

            # Return context-only response
            return CrossDatasetQueryContextResponse(
                query=result["query"],
                dataset_count=result["dataset_count"],
                total_chunks=result["total_chunks"],
                context=result.get("context", {}),
                dataset_results=result["dataset_results"],
                performance_stats=result.get("performance_stats")
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to execute cross-dataset context query: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.post(
        "/datasets/cross-query/stream",
        dependencies=[Depends(combined_auth)],
        responses={
            400: {"model": ErrorResponse, "description": "Invalid request parameters"},
            404: {"model": ErrorResponse, "description": "One or more datasets not found"},
        }
    )
    async def cross_dataset_query_stream(
        request: CrossDatasetQueryRequest = Body(..., description="Cross-dataset streaming query request")
    ):
        """
        Stream query results from multiple datasets.

        This endpoint performs a streaming query across multiple datasets,
        providing real-time results as they become available from each dataset.
        Results are streamed in JSON format with dataset source identification.
        """
        try:
            # Import CrossDatasetQueryEngine
            from ...dataset.cross_query_engine import CrossDatasetQueryEngine

            # Create query engine
            query_engine = CrossDatasetQueryEngine(db_config)

            # Convert request to QueryParam with streaming enabled
            from ..routers.query_routes import QueryParam
            query_params = QueryParam(
                mode=request.mode,
                only_need_context=request.only_need_context or False,
                only_need_prompt=request.only_need_prompt or False,
                response_type=request.response_type or "Multiple Paragraphs",
                stream=True,  # Enable streaming
                top_k=request.top_k or 60,
                chunk_top_k=request.chunk_top_k or 20,
                max_entity_tokens=request.max_entity_tokens,
                max_relation_tokens=request.max_relation_tokens,
                max_total_tokens=request.max_total_tokens,
                conversation_history=request.conversation_history or [],
                history_turns=request.history_turns,
                user_prompt=request.user_prompt,
                enable_rerank=request.enable_rerank if request.enable_rerank is not None else True
            )

            async def generate_stream():
                """Generate streaming response for cross-dataset query."""
                try:
                    # Execute cross-dataset query
                    result = await query_engine.query_multiple_datasets(
                        query=request.query,
                        dataset_ids=request.dataset_ids,
                        document_filters=request.document_filters,
                        query_params=query_params,
                        max_results_per_dataset=request.max_results_per_dataset or 20
                    )

                    # Stream the merged response
                    import json

                    # Send initial metadata
                    metadata = {
                        "type": "metadata",
                        "query": result["query"],
                        "dataset_count": result["dataset_count"],
                        "total_chunks": result["total_chunks"],
                        "query_mode": result["query_mode"]
                    }
                    yield f"data: {json.dumps(metadata)}\n\n"

                    # Stream the main response
                    response_data = {
                        "type": "response",
                        "response": result["response"]
                    }
                    yield f"data: {json.dumps(response_data)}\n\n"

                    # Stream context information if available
                    if result.get("context"):
                        context_data = {
                            "type": "context",
                            "context": result["context"]
                        }
                        yield f"data: {json.dumps(context_data)}\n\n"

                    # Stream performance statistics
                    if result.get("performance_stats"):
                        perf_data = {
                            "type": "performance",
                            "performance_stats": result["performance_stats"]
                        }
                        yield f"data: {json.dumps(perf_data)}\n\n"

                    # Send completion marker
                    completion = {"type": "complete", "status": "success"}
                    yield f"data: {json.dumps(completion)}\n\n"

                except Exception as e:
                    # Send error information
                    error_data = {
                        "type": "error",
                        "error": str(e),
                        "status": "failed"
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"

            return StreamingResponse(
                generate_stream(),
                media_type="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/plain; charset=utf-8"
                }
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to stream cross-dataset query: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.post(
        "/datasets/{dataset_id}/search",
        response_model=DatasetSearchResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def search_dataset(
        dataset_id: str,
        request: DatasetSearchRequest
    ):
        """
        Search within a specific dataset.

        This endpoint performs a search for entities, relations, or chunks
        within the specified dataset's isolated environment.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Use cached dataset adapter for better performance
            adapter = await _get_cached_adapter(dataset_id, db_config)
            results = {}

            if request.search_type in ["entities", "all"]:
                results["entities"] = await adapter.search_entities(request.query, request.top_k)

            if request.search_type in ["relations", "all"]:
                results["relations"] = await adapter.search_relations(request.query, request.top_k)

            if request.search_type in ["chunks", "all"]:
                results["chunks"] = await adapter.search_chunks(request.query, request.top_k)

            return DatasetSearchResponse(
                results=results,
                dataset_id=dataset_id,
                query=request.query
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to search dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    # Dataset-aware graph API endpoints

    class DatasetGraphStatsResponse(BaseModel):
        graph_statistics: Dict[str, Any] = Field(description="Graph statistics")
        dataset_id: str = Field(description="Dataset ID")

    class DatasetGraphLabelsResponse(BaseModel):
        labels: List[str] = Field(description="List of graph node labels")
        dataset_id: str = Field(description="Dataset ID")

    class DatasetGraphHealthResponse(BaseModel):
        health_status: Dict[str, Any] = Field(description="Graph health status")
        dataset_id: str = Field(description="Dataset ID")

    class DatasetClearCacheRequest(BaseModel):
        """Request model for clearing dataset cache (optional, for API compatibility)."""
        pass

    class DatasetClearCacheResponse(BaseModel):
        """Response model for dataset cache clearing operation."""
        status: str = Field(description="Status of the clear operation")
        message: str = Field(description="Message describing the operation result")
        cache_entries_cleared: int = Field(description="Number of cache entries cleared")
        dataset_id: str = Field(description="Dataset ID")

    @router.get(
        "/datasets/{dataset_id}/graphs/statistics",
        response_model=DatasetGraphStatsResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def get_dataset_graph_statistics(
        dataset_id: str = Path(..., description="Dataset UUID")
    ):
        """
        Get graph statistics for a specific dataset.

        Returns comprehensive statistics about the knowledge graph
        in the specified dataset.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter and get graph statistics
            adapter = DatasetAdapter(dataset_id, db_config)
            graph_statistics = await adapter.get_graph_statistics()

            return DatasetGraphStatsResponse(
                graph_statistics=graph_statistics,
                dataset_id=dataset_id
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get graph statistics for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets/{dataset_id}/graphs/labels",
        response_model=DatasetGraphLabelsResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def get_dataset_graph_labels(
        dataset_id: str = Path(..., description="Dataset UUID")
    ):
        """
        Get available graph node labels for a specific dataset.

        Returns a list of all node labels available in the dataset's
        knowledge graph.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter and get graph labels
            adapter = DatasetAdapter(dataset_id, db_config)
            labels = await adapter.get_graph_labels()

            return DatasetGraphLabelsResponse(
                labels=labels,
                dataset_id=dataset_id
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get graph labels for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets/{dataset_id}/health",
        response_model=DatasetGraphHealthResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def get_dataset_health_status(
        dataset_id: str = Path(..., description="Dataset UUID")
    ):
        """
        Get health status for a specific dataset.

        Returns comprehensive health information about the dataset,
        including data availability, graph connectivity, and recommendations.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter and get health status
            adapter = DatasetAdapter(dataset_id, db_config)
            health_status = await adapter.get_health_status()

            return DatasetGraphHealthResponse(
                health_status=health_status,
                dataset_id=dataset_id
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get health status for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.get(
        "/datasets/{dataset_id}/graphs",
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def query_dataset_graphs(
        dataset_id: str = Path(..., description="Dataset UUID"),
        label: str = Query("*", description="Graph label to query"),
        max_depth: int = Query(2, ge=1, le=10, description="Maximum query depth"),
        max_nodes: int = Query(100, ge=1, le=1000, description="Maximum number of nodes to return")
    ):
        """
        Query knowledge graph data for a specific dataset.

        This endpoint retrieves graph data (nodes and edges) from the specified dataset's
        isolated graph schema, providing dataset-specific knowledge graph visualization.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Get cached dataset-aware RAG instance
            dataset_model = _dataset_info_to_model(dataset_info)
            dataset_rag = await rag_manager.get_instance(dataset_model)

            # Query graph data using dataset-specific graph storage
            try:
                # Use the RAG instance's get_knowledge_graph method directly
                graph_data = await dataset_rag.get_knowledge_graph(
                    node_label=label,
                    max_depth=max_depth,
                    max_nodes=max_nodes
                )

                return graph_data

            except Exception as graph_error:
                logger.error(f"Graph query failed for dataset {dataset_id}: {graph_error}")
                # Return empty graph data instead of failing
                return {
                    "nodes": [],
                    "edges": [],
                    "is_truncated": False,
                    "message": f"No graph data available for dataset {dataset_id}"
                }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to query graphs for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.post(
        "/datasets/{dataset_id}/clear_cache",
        response_model=DatasetClearCacheResponse,
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def clear_dataset_cache(
        dataset_id: str = Path(..., description="Dataset UUID"),
        request: DatasetClearCacheRequest = None
    ):
        """
        Clear LLM cache data for a specific dataset.

        This endpoint clears all cached LLM responses for the specified dataset only,
        providing dataset-isolated cache management.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Create dataset adapter and clear cache
            adapter = DatasetAdapter(dataset_id, db_config)
            result = await adapter.clear_cache()

            return DatasetClearCacheResponse(
                status="success",
                message=result['message'],
                cache_entries_cleared=result['cache_entries'],
                dataset_id=dataset_id
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to clear cache for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    # Dataset Pipeline Management Endpoints

    @router.get(
        "/datasets/{dataset_id}/pipeline/status",
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def get_dataset_pipeline_status(
        dataset_id: str = Path(..., description="Dataset UUID")
    ):
        """
        Get pipeline processing status for a specific dataset.

        Returns the current pipeline status including processing state,
        document counts, and recent messages for the specified dataset.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Get dataset pipeline status
            pipeline_manager = DatasetPipelineManager(dataset_id)
            pipeline_status = await pipeline_manager.get_status()

            return {
                "dataset_id": dataset_id,
                "dataset_name": dataset_info.get("name", "Unknown"),
                "pipeline_status": pipeline_status,
                "isolation_mode": "dataset"
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get pipeline status for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    @router.post(
        "/datasets/{dataset_id}/pipeline/clear_cache",
        dependencies=[Depends(combined_auth)],
        responses={
            404: {"model": ErrorResponse, "description": "Dataset not found"},
        }
    )
    async def clear_dataset_pipeline_cache(
        dataset_id: str = Path(..., description="Dataset UUID")
    ):
        """
        Clear pipeline cache for a specific dataset.

        Resets the pipeline status and clears any cached processing state
        for the specified dataset.
        """
        try:
            # Verify dataset exists
            dataset_info = await dataset_manager.get_dataset(dataset_id)
            if not dataset_info:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "DatasetNotFound", "message": f"Dataset not found: {dataset_id}", "dataset_id": dataset_id}
                )

            # Clear dataset pipeline cache
            pipeline_manager = DatasetPipelineManager(dataset_id)
            await pipeline_manager.clear_cache()

            return {
                "dataset_id": dataset_id,
                "dataset_name": dataset_info.get("name", "Unknown"),
                "status": "success",
                "message": "Dataset pipeline cache cleared successfully"
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to clear pipeline cache for dataset {dataset_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail={"error": "InternalError", "message": str(e)}
            )

    return router


async def run_dataset_scanning_process(
    dataset_rag: LightRAG, doc_manager: DocumentManager, track_id: str = None
):
    """Background task to scan and index documents for a specific dataset

    Args:
        dataset_rag: Dataset-specific LightRAG instance
        doc_manager: DocumentManager instance
        track_id: Optional tracking ID to pass to all scanned files
    """
    try:
        new_files = doc_manager.scan_directory_for_new_files()
        total_files = len(new_files)
        logger.info(f"Found {total_files} files to index for dataset.")

        if not new_files:
            return

        # Import pipeline functions from document_routes
        from ..routers.document_routes import pipeline_index_files

        # Process all files at once with track_id using dataset-specific RAG
        await pipeline_index_files(dataset_rag, new_files, track_id)
        logger.info(f"Dataset scanning process completed: {total_files} files processed.")

    except Exception as e:
        logger.error(f"Error during dataset scanning process: {str(e)}")
        logger.error(traceback.format_exc())


async def background_delete_dataset_documents(
    rag: LightRAG,
    doc_manager: DocumentManager,
    doc_ids: List[str],
    delete_file: bool = False,
    dataset_id: str = None,
):
    """Background task to delete multiple documents from a specific dataset"""
    from lightrag.kg.shared_storage import (
        get_dataset_namespace_data,
        get_dataset_pipeline_status_lock,
    )
    from lightrag.kg.dataset_pipeline_manager import DatasetPipelineManager
    from datetime import datetime

    if not dataset_id:
        logger.error("Dataset ID is required for dataset-aware document deletion")
        return

    # Initialize dataset pipeline manager
    pipeline_manager = DatasetPipelineManager(dataset_id)
    await pipeline_manager.initialize()

    pipeline_status = await get_dataset_namespace_data("pipeline_status", dataset_id)
    pipeline_status_lock = get_dataset_pipeline_status_lock(dataset_id)

    total_docs = len(doc_ids)
    successful_deletions = []
    failed_deletions = []

    # Double-check pipeline status before proceeding
    async with pipeline_status_lock:
        if pipeline_status.get("busy", False):
            logger.warning(f"Error: Unexpected pipeline busy state for dataset {dataset_id}, aborting deletion.")
            return  # Abort deletion operation

        # Set pipeline status to busy for deletion
        pipeline_status.update(
            {
                "busy": True,
                "job_name": f"Deleting {total_docs} Documents",
                "job_start": datetime.now().isoformat(),
                "docs": total_docs,
                "batchs": total_docs,
                "cur_batch": 0,
                "latest_message": "🚀 Initializing document deletion process...",
            }
        )
        # Use slice assignment to clear the list in place and add detailed start info
        pipeline_status["history_messages"][:] = [
            "🚀 Document Deletion Process Started",
            f"📊 Total documents to delete: {total_docs}",
            f"🗂️  Delete source files: {'Yes' if delete_file else 'No'}",
            f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 50
        ]

    try:
        # Loop through each document ID and delete them one by one
        for i, doc_id in enumerate(doc_ids, 1):
            async with pipeline_status_lock:
                start_msg = f"📄 [{i}/{total_docs}] Starting deletion of document: {doc_id}"
                logger.info(start_msg)
                pipeline_status["cur_batch"] = i
                pipeline_status["latest_message"] = start_msg
                pipeline_status["history_messages"].append(start_msg)

            file_path = "#"
            try:
                # Add detailed progress messages for deletion steps
                async with pipeline_status_lock:
                    step_msg = f"🔍 [{i}/{total_docs}] Analyzing document dependencies..."
                    pipeline_status["latest_message"] = step_msg
                    pipeline_status["history_messages"].append(step_msg)

                result = await rag.adelete_by_doc_id(doc_id)
                file_path = (
                    getattr(result, "file_path", "-") if "result" in locals() else "-"
                )

                if result.status == "success":
                    successful_deletions.append(doc_id)

                    # Add detailed success information
                    async with pipeline_status_lock:
                        # Show what was deleted
                        detail_msg = f"🗑️  [{i}/{total_docs}] Document data removed from storage"
                        pipeline_status["history_messages"].append(detail_msg)

                        # Show entities and relations cleanup
                        cleanup_msg = f"🔗 [{i}/{total_docs}] Cleaned up entities and relationships"
                        pipeline_status["history_messages"].append(cleanup_msg)

                        # Show knowledge graph update
                        kg_msg = f"🧠 [{i}/{total_docs}] Updated knowledge graph structure"
                        pipeline_status["history_messages"].append(kg_msg)

                        # Final success message
                        success_msg = f"✅ [{i}/{total_docs}] Successfully deleted: {doc_id}"
                        if file_path and file_path != "-":
                            success_msg += f" (source: {file_path})"

                        pipeline_status["latest_message"] = success_msg
                        pipeline_status["history_messages"].append(success_msg)

                    logger.info(success_msg)

                    # Handle file deletion if requested and file_path is available
                    if (
                        delete_file
                        and result.file_path
                        and result.file_path != "unknown_source"
                    ):
                        async with pipeline_status_lock:
                            file_check_msg = f"📁 [{i}/{total_docs}] Checking source file: {result.file_path}"
                            pipeline_status["latest_message"] = file_check_msg
                            pipeline_status["history_messages"].append(file_check_msg)

                        try:
                            file_path = doc_manager.input_dir / result.file_path
                            if file_path.exists():
                                file_path.unlink()
                                file_delete_msg = f"🗂️  [{i}/{total_docs}] ✅ Deleted source file: {result.file_path}"
                                logger.info(file_delete_msg)
                                async with pipeline_status_lock:
                                    pipeline_status["latest_message"] = file_delete_msg
                                    pipeline_status["history_messages"].append(file_delete_msg)
                            else:
                                file_not_found_msg = f"🗂️  [{i}/{total_docs}] ⚠️  Source file not found: {result.file_path}"
                                logger.warning(file_not_found_msg)
                                async with pipeline_status_lock:
                                    pipeline_status["latest_message"] = file_not_found_msg
                                    pipeline_status["history_messages"].append(file_not_found_msg)
                        except Exception as file_error:
                            file_error_msg = f"🗂️  [{i}/{total_docs}] ❌ Error deleting file {result.file_path}: {str(file_error)}"
                            logger.error(file_error_msg)
                            async with pipeline_status_lock:
                                pipeline_status["latest_message"] = file_error_msg
                                pipeline_status["history_messages"].append(file_error_msg)
                else:
                    failed_deletions.append(doc_id)
                    error_msg = f"❌ [{i}/{total_docs}] Failed to delete document: {doc_id}"
                    if hasattr(result, 'message') and result.message:
                        error_msg += f" - {result.message}"
                    logger.error(error_msg)
                    async with pipeline_status_lock:
                        pipeline_status["latest_message"] = error_msg
                        pipeline_status["history_messages"].append(error_msg)

            except Exception as e:
                failed_deletions.append(doc_id)
                error_msg = f"💥 [{i}/{total_docs}] Exception during deletion of {doc_id}: {str(e)}"
                logger.error(error_msg)
                async with pipeline_status_lock:
                    pipeline_status["latest_message"] = error_msg
                    pipeline_status["history_messages"].append(error_msg)

        # Final status update with detailed summary
        async with pipeline_status_lock:
            # Add summary separator
            pipeline_status["history_messages"].append("=" * 50)

            # Detailed completion summary
            if len(successful_deletions) > 0:
                success_summary = f"🎉 Successfully processed {len(successful_deletions)} documents:"
                pipeline_status["history_messages"].append(success_summary)
                for doc_id in successful_deletions:
                    pipeline_status["history_messages"].append(f"  ✅ {doc_id}")

            if len(failed_deletions) > 0:
                failure_summary = f"⚠️  Failed to process {len(failed_deletions)} documents:"
                pipeline_status["history_messages"].append(failure_summary)
                for doc_id in failed_deletions:
                    pipeline_status["history_messages"].append(f"  ❌ {doc_id}")

            # Final completion message
            completion_msg = f"🏁 Document deletion completed - Success: {len(successful_deletions)}, Failed: {len(failed_deletions)}"

            pipeline_status.update(
                {
                    "busy": False,
                    "latest_message": completion_msg,
                    "cur_batch": total_docs,
                }
            )
            pipeline_status["history_messages"].append(completion_msg)

        logger.info(f"Dataset {dataset_id} document deletion completed: {len(successful_deletions)} successful, {len(failed_deletions)} failed")

    except Exception as e:
        logger.error(f"Error during dataset {dataset_id} document deletion process: {str(e)}")
        async with pipeline_status_lock:
            # Add detailed error information
            pipeline_status["history_messages"].append("=" * 50)
            pipeline_status["history_messages"].append("💥 CRITICAL ERROR OCCURRED")

            error_msg = f"🚨 Document deletion process failed: {str(e)}"
            pipeline_status["history_messages"].append(error_msg)

            # Add recovery information
            recovery_msg = "🔧 Partial deletions may have occurred. Check individual document status."
            pipeline_status["history_messages"].append(recovery_msg)

            final_error_msg = f"❌ Process terminated due to error: {str(e)}"

            pipeline_status.update(
                {
                    "busy": False,
                    "latest_message": final_error_msg,
                }
            )
            pipeline_status["history_messages"].append(final_error_msg)


async def background_clear_dataset_documents(
    rag: LightRAG,
    doc_manager: DocumentManager,
):
    """Background task to clear all documents from a dataset"""
    from lightrag.kg.shared_storage import (
        get_namespace_data,
        get_pipeline_status_lock,
    )
    from datetime import datetime

    pipeline_status = await get_namespace_data("pipeline_status")
    pipeline_status_lock = get_pipeline_status_lock()

    # Double-check pipeline status before proceeding
    async with pipeline_status_lock:
        if pipeline_status.get("busy", False):
            logger.warning("Error: Unexpected pipeline busy state, aborting clearing.")
            return  # Abort clearing operation

        # Set pipeline status to busy for clearing
        pipeline_status.update(
            {
                "busy": True,
                "job_name": "Clearing All Dataset Documents",
                "job_start": datetime.now().isoformat(),
                "docs": 0,
                "batchs": 0,
                "cur_batch": 0,
                "request_pending": False,  # Clear any previous request
                "latest_message": "Starting dataset document clearing process",
            }
        )
        # Use slice assignment to clear the list in place
        pipeline_status["history_messages"][:] = ["Starting dataset document clearing process"]

    try:
        # Use drop method to clear all data
        drop_tasks = []
        storages = [
            rag.text_chunks,
            rag.full_docs,
            rag.full_entities,
            rag.full_relations,
            rag.entities_vdb,
            rag.relationships_vdb,
            rag.chunks_vdb,
            rag.chunk_entity_relation_graph,
            rag.doc_status,
        ]

        # Log storage drop start
        async with pipeline_status_lock:
            pipeline_status["history_messages"].append("Starting to drop storage components")

        for storage in storages:
            if storage is not None:
                drop_tasks.append(storage.drop())

        # Execute all drop operations concurrently
        drop_results = await asyncio.gather(*drop_tasks, return_exceptions=True)

        # Check results and log any errors
        errors = []
        for i, result in enumerate(drop_results):
            if isinstance(result, Exception):
                error_msg = f"Failed to drop storage {i}: {str(result)}"
                logger.error(error_msg)
                errors.append(error_msg)
                async with pipeline_status_lock:
                    pipeline_status["history_messages"].append(error_msg)
            else:
                success_msg = f"Successfully dropped storage {i}"
                logger.info(success_msg)
                async with pipeline_status_lock:
                    pipeline_status["history_messages"].append(success_msg)

        # Delete files from input directory (dataset-specific files only)
        deleted_files_count = 0
        file_errors_count = 0

        # For dataset-isolated clearing, we should only clear files that belong to this dataset
        # This is a simplified approach - in a full implementation, you might want to track
        # which files belong to which dataset
        for file_path in doc_manager.input_dir.glob("*"):
            if file_path.is_file():
                try:
                    file_path.unlink()
                    deleted_files_count += 1
                except Exception as e:
                    logger.error(f"Error deleting file {file_path}: {str(e)}")
                    file_errors_count += 1

        # Log file deletion results
        async with pipeline_status_lock:
            if file_errors_count > 0:
                pipeline_status["history_messages"].append(
                    f"Deleted {deleted_files_count} files with {file_errors_count} errors"
                )
                errors.append(f"Failed to delete {file_errors_count} files")
            else:
                pipeline_status["history_messages"].append(
                    f"Successfully deleted {deleted_files_count} files"
                )

        # Final status update
        if errors:
            final_message = f"Dataset clearing completed with {len(errors)} errors: {'; '.join(errors)}"
            logger.warning(final_message)
        else:
            final_message = f"Successfully cleared all dataset documents and deleted {deleted_files_count} files"
            logger.info(final_message)

        async with pipeline_status_lock:
            pipeline_status["history_messages"].append(final_message)

    except Exception as e:
        error_msg = f"Error clearing dataset documents: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        async with pipeline_status_lock:
            pipeline_status["history_messages"].append(error_msg)
    finally:
        # Reset busy status after completion
        async with pipeline_status_lock:
            pipeline_status["busy"] = False
            completion_msg = "Dataset document clearing process completed"
            pipeline_status["latest_message"] = completion_msg
            pipeline_status["history_messages"].append(completion_msg)