"""
Client for interacting with RAG Agent API.
"""

import logging
import re
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, TypeVar, Union
import httpx

from rag_agent.client.light_rag_server_api_client.api.default import async_get_health
from rag_agent.client.light_rag_server_api_client.api.documents import (
    async_get_documents,
    async_get_pipeline_status,
    async_insert_document,
    async_insert_file,
    async_insert_texts,
    async_scan_for_new_documents,
    async_upload_document,
)
from rag_agent.client.light_rag_server_api_client.api.graph import (
    async_create_entity,
    async_create_relation,
    async_delete_by_doc_id,
    async_delete_entity,
    async_edit_entity,
    async_edit_relation,
    async_get_graph_labels,
    async_merge_entities,
)
from rag_agent.client.light_rag_server_api_client.api.query import (
    async_query_document,
)
from rag_agent.client.light_rag_server_api_client.client import AuthenticatedClient
from rag_agent.client.light_rag_server_api_client.models import (
    BodyInsertFileDocumentsFilePost,
    BodyUploadToInputDirDocumentsUploadPost,
    DocsStatusesResponse,
    HTTPValidationError,
    InsertResponse,
    InsertTextRequest,
    InsertTextsRequest,
    PipelineStatusResponse,
    QueryRequest,
    QueryRequestMode,
    QueryResponse,
    relation_request,
    relation_response,
)
from rag_agent.client.light_rag_server_api_client.models.entity_request import EntityRequest
from rag_agent.client.light_rag_server_api_client.models.entity_response import EntityResponse
from rag_agent.client.light_rag_server_api_client.models.merge_entities_request import (
    MergeEntitiesRequest,
)
from rag_agent.client.light_rag_server_api_client.models.merge_entities_request_merge_strategy_type_0 import (
    MergeEntitiesRequestMergeStrategyType0,
)
from rag_agent.client.light_rag_server_api_client.models.status_message_response import (
    StatusMessageResponse,
)
from rag_agent.client.light_rag_server_api_client.types import File

from .client.light_rag_server_api_client.errors import UnexpectedStatus

logger = logging.getLogger(__name__)

T = TypeVar("T", covariant=True)
ApiFunc = Callable[..., Awaitable[Union[T, HTTPValidationError, None]]]


class LightRAGClient:
    """
    Client for interacting with RAG Agent API.
    
    Supports two authentication modes:
    1. Service Key mode: Only apikey header with service_role key (admin privileges)
    2. Anon Key + JWT mode: apikey header with anon key + Authorization: Bearer {jwt}
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        auth_client: "SupabaseAuthClient | None" = None,
        basic_auth_client: "BasicAuthClient | None" = None,  # Kept for backward compatibility
    ):
        """
        Initialize RAG Agent API client.

        Args:
            base_url (str): Base API URL.
            api_key (str): API key (service_role key or anon key).
            auth_client (SupabaseAuthClient | None): Optional auth client for JWT authentication.
            basic_auth_client: Deprecated, kept for backward compatibility.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.auth_client = auth_client
        
        # Initialize client with apikey header
        # Service Key mode: only apikey header needed
        # JWT mode: apikey + Authorization header (set dynamically)
        initial_headers = {"apikey": api_key}
        
        # Don't use AuthenticatedClient's token parameter - we manage Authorization ourselves
        self.client = AuthenticatedClient(
            base_url=base_url, 
            token="",  # Empty token - we manage Authorization via headers
            verify_ssl=False
        ).with_headers(initial_headers)
        
        logger.info(f"Initialized RAG Agent API client: {base_url}")
        if auth_client:
            logger.info("JWT mode enabled - will obtain token via /login endpoint")
        else:
            logger.info("Service Key mode enabled - using apikey header only")
    
    async def _ensure_auth(self) -> None:
        """Ensure we have a valid authorization token.
        
        For JWT mode: Updates the Authorization header with a fresh JWT token.
        For Service Key mode: No action needed (apikey header is sufficient).
        """
        if self.auth_client:
            logger.debug("Ensuring JWT token is valid...")
            token = await self.auth_client.ensure_valid_token()
            # Update the Authorization header with the JWT token
            self._update_auth_header(f"Bearer {token}")
            logger.debug("JWT token updated in request headers")
        # Service Key mode doesn't need Authorization header
    
    def _update_auth_header(self, auth_header: str) -> None:
        """Update the Authorization header.
        
        Args:
            auth_header: Full Authorization header value (e.g., "Bearer token" or "Basic xxx")
        """
        # Update the stored headers for new client creation (must be done first)
        self.client._headers["Authorization"] = auth_header
        
        # Update headers on the underlying httpx client if it exists
        if self.client._async_client is not None:
            self.client._async_client.headers["Authorization"] = auth_header
        
        logger.debug(f"Updated Authorization header (length: {len(auth_header)} chars)")

    async def _handle_exception(self, e: Exception, operation_name: str) -> None:
        """
        Handle exceptions when calling API.

        Args:
            e: Exception
            operation_name: Operation name for logging

        Raises:
            Exception: Re-raises the exception
        """
        if isinstance(e, UnexpectedStatus):
            logger.error(f"HTTP error during {operation_name}: {e.status_code} - {e.content!r}")
        else:
            logger.error(f"Error during {operation_name}: {str(e)}")

    def _log_request_details(self, method: str, url: str, headers: dict = None, body: any = None) -> None:
        """Log detailed request information for debugging.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            headers: Request headers (sensitive values will be masked)
            body: Request body
        """
        import sys
        
        print("=== REQUEST DEBUG ===", file=sys.stderr)
        print(f"Method: {method}", file=sys.stderr)
        print(f"URL: {url}", file=sys.stderr)
        
        if headers:
            # Mask sensitive header values but show structure
            masked_headers = {}
            for key, value in headers.items():
                if key.lower() in ("authorization", "apikey"):
                    if value and len(value) > 20:
                        masked_headers[key] = f"{value[:15]}...{value[-10:]}"
                    else:
                        masked_headers[key] = value
                else:
                    masked_headers[key] = value
            print(f"Headers: {masked_headers}", file=sys.stderr)
        
        if body:
            print(f"Body: {body}", file=sys.stderr)
        print("=== END REQUEST DEBUG ===", file=sys.stderr)

    async def _call_api(
        self,
        api_func: Callable[..., Awaitable[Union[T, HTTPValidationError, None]]],
        operation_name: str,
        **kwargs,
    ) -> Union[T, HTTPValidationError, None]:
        """
        Universal method for calling API functions.

        Args:
            api_func: API function to call
            operation_name: Operation name for logging
            **kwargs: Additional arguments for the API function

        Returns:
            Union[T, HTTPValidationError, None]: API call result
        """
        try:
            # Ensure we have a valid auth token before making the API call
            await self._ensure_auth()
            
            # Log request details
            logger.info(f"Calling API: {operation_name}")
            logger.info(f"Client headers: {dict(self.client._headers)}")
            
            result = await api_func(**kwargs)
            logger.debug(f"API call successful: {operation_name}")
            return result
        except Exception as e:
            logger.error("API %s failed: %s %r", operation_name, type(e).__name__, e)
            if isinstance(e, httpx.ConnectError):
                logger.error("Unable to reach %s – verify host/port/network", self.base_url)
            raise


    async def query(
        self,
        query_text: str,
        mode: str = "mix",
        top_k: int = 10,
        only_need_context: bool = False,
        only_need_prompt: bool = False,
        response_type: str = "Multiple Paragraphs",
        max_token_for_text_unit: int = 1000,
        max_token_for_global_context: int = 1000,
        max_token_for_local_context: int = 1000,
        hl_keywords: list[str] = [],
        ll_keywords: list[str] = [],
        history_turns: int = 10,
    ) -> Union[QueryResponse, HTTPValidationError, None]:
        """
        Execute a query to RAG Agent API.

        Args:
            query_text (str): Query text
            mode (str, optional): Search mode (global, hybrid, local, mix, naive). Default is "mix".
            response_type (str, optional): Response format. Default is "Multiple Paragraphs".
            top_k (int, optional): Number of results. Default is 10.
            only_need_context (bool, optional): Return only context without LLM response. Default is False.
            only_need_prompt (bool, optional): Return only generated prompt without creating a response. Default is False.
            max_token_for_text_unit (int, optional): Maximum tokens for each text fragment. Default is 1000.
            max_token_for_global_context (int, optional): Maximum tokens for global context. Default is 1000.
            max_token_for_local_context (int, optional): Maximum tokens for local context. Default is 1000.
            hl_keywords (list[str], optional): List of high-level keywords for prioritization. Default is [].
            ll_keywords (list[str], optional): List of low-level keywords for search refinement. Default is [].
            history_turns (int, optional): Number of conversation turns in response context. Default is 10.

        Returns:
            Union[QueryResponse, HTTPValidationError, None]: Query result
        """
        logger.debug(f"Executing query: {query_text[:100]}...")

        request = QueryRequest(
            query=query_text,
            mode=QueryRequestMode(mode),
            response_type=response_type,
            top_k=top_k,
            only_need_context=only_need_context,
            only_need_prompt=only_need_prompt,
            max_token_for_text_unit=max_token_for_text_unit,
            max_token_for_global_context=max_token_for_global_context,
            max_token_for_local_context=max_token_for_local_context,
            hl_keywords=hl_keywords,
            ll_keywords=ll_keywords,
            history_turns=history_turns,
        )

        return await self._call_api(
            api_func=async_query_document,
            operation_name="query execution",
            client=self.client,
            body=request,
        )

    async def insert_text(
        self,
        text: Union[str, List[str]],
    ) -> Union[InsertResponse, HTTPValidationError, None]:
        """
        Add text to RAG Agent.

        Args:
            text (Union[str, List[str]]): Text or list of texts to add

        Returns:
            Union[InsertResponse, HTTPValidationError]: Operation result
        """
        logger.debug(f"Adding text: {str(text)[:100]}...")

        request: InsertTextRequest | InsertTextsRequest
        if isinstance(text, str):
            request = InsertTextRequest(text=text)
            return await self._call_api(
                api_func=async_insert_document,
                operation_name="text insertion",
                client=self.client,
                body=request,
            )
        else:
            request = InsertTextsRequest(texts=text)
            return await self._call_api(
                api_func=async_insert_texts,
                operation_name="multiple texts insertion",
                client=self.client,
                body=request,
            )

    async def upload_document(self, file_path: str) -> Union[Any, HTTPValidationError, None]:
        """
        Upload document from file to RAG Agent's /input directory and start indexing.

        Args:
            file_path (str): Path to file.

        Returns:
            Union[Any, HTTPValidationError]: Operation result.
        """
        logger.debug(f"Uploading document: {file_path}")

        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                file_name = path.name
                upload_request = BodyUploadToInputDirDocumentsUploadPost(
                    file=File(payload=f, file_name=file_name)
                )

                return await self._call_api(
                    api_func=async_upload_document,
                    operation_name=f"file upload {file_path}",
                    client=self.client,
                    body=upload_request,
                )
        except FileNotFoundError:
            logger.error(f"Файл не найден: {file_path}")
            raise
        except Exception as e:
            await self._handle_exception(e, f"загрузке файла {file_path}")
            raise

    async def insert_file(self, file_path: str) -> Union[InsertResponse, HTTPValidationError, None]:
        """
        Add document from a file_path directly to RAG Agent storage, without uploading to /input directory.

        Args:
            file_path (str): Path to file.

        Returns:
            Union[InsertResponse, HTTPValidationError]: Operation result.
        """
        logger.debug(f"Adding file: {file_path}")

        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                file_name = path.name
                insert_file_request = BodyInsertFileDocumentsFilePost(
                    file=File(payload=f, file_name=file_name)
                )

                return await self._call_api(
                    api_func=async_insert_file,
                    operation_name=f"file insertion {file_path}",
                    client=self.client,
                    body=insert_file_request,
                )
        except FileNotFoundError:
            logger.error(f"Файл не найден: {file_path}")
            raise
        except Exception as e:
            await self._handle_exception(e, f"добавлении файла {file_path}")
            raise

    async def insert_batch(
        self,
        directory_path: str,
        recursive: bool = False,
        depth: int = 1,
        include_only: list[str] = [],
        ignore_directories: list[str] = [],
        ignore_files: list[str] = [],
    ) -> Union[InsertResponse, HTTPValidationError, None]:
        """
        Add batch of documents from directory.

        Args:
            directory_path (str): Path to directory.
            recursive (bool, optional): Recursive addition. Defaults to False.
            depth (int, optional): Recursion depth. Defaults to 1.
            ignore_directories (list[str], optional): List of regexp to exclude directories from batch insertion. Defaults to [].
            ignore_files (list[str], optional): List of regexp to exclude files from batch insertion. Defaults to []. Either ignore_files or include_only must be specified, not both.
            include_only (list[str], optional): List of regexp to specify files to include. Defaults to []. Either include_only or ignore_files must be specified, not both.

        Returns:
            Union[InsertResponse, HTTPValidationError]: Operation result.
        """
        logger.debug(
            f"Adding batch of documents from directory: {directory_path} (recursive={recursive}, depth={depth})"
        )

        if include_only and ignore_files:
            error_message = "Cannot specify both include_only and ignore_files parameters"
            logger.error(error_message)
            raise ValueError(error_message)

        dir_path = Path(directory_path)
        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"Directory not found: {directory_path}")
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        include_patterns = [re.compile(pattern) for pattern in include_only] if include_only else []
        ignore_dir_patterns = (
            [re.compile(pattern) for pattern in ignore_directories] if ignore_directories else []
        )
        ignore_file_patterns = (
            [re.compile(pattern) for pattern in ignore_files] if ignore_files else []
        )

        def collect_file_paths(dir_path: Path, current_depth: int = 0) -> List[Path]:
            """Recursively collect file paths from directory"""
            file_paths = []
            try:
                for item in dir_path.iterdir():
                    if item.is_dir() and recursive and current_depth < depth:
                        # Check if directory should be ignored
                        dir_name = item.name
                        if any(pattern.search(dir_name) for pattern in ignore_dir_patterns):
                            logger.debug(f"Ignoring directory: {item} (matched ignore pattern)")
                            continue

                        # Process subdirectory
                        file_paths.extend(collect_file_paths(item, current_depth + 1))
                    elif item.is_file():
                        file_name = item.name

                        # Apply include_only filter if specified
                        if include_patterns:
                            if any(pattern.search(file_name) for pattern in include_patterns):
                                file_paths.append(item)
                                logger.debug(f"Including file: {item} (matched include pattern)")
                            else:
                                logger.debug(
                                    f"Skipping file: {item} (did not match any include pattern)"
                                )
                            continue

                        # Apply ignore_files filter if specified
                        if ignore_file_patterns:
                            if any(pattern.search(file_name) for pattern in ignore_file_patterns):
                                logger.debug(f"Ignoring file: {item} (matched ignore pattern)")
                                continue

                        # If we got here, the file is not filtered out
                        file_paths.append(item)
            except Exception as e:
                logger.error(f"Error collecting files from {dir_path}: {str(e)}")
            return file_paths

        try:
            file_paths = collect_file_paths(dir_path)
            logger.info(f"Found {len(file_paths)} files for processing after applying filters")

            success_count = 0
            failed_files = []

            for file_path in file_paths:
                try:
                    await self.insert_file(str(file_path))
                    success_count += 1
                    logger.debug(f"Successfully inserted file: {file_path}")
                except Exception as e:
                    logger.error(f"Error inserting file {file_path}: {str(e)}")
                    failed_files.append(str(file_path))

            if success_count == len(file_paths):
                status = "success"
                message = f"All {success_count} documents inserted successfully"
            elif success_count > 0:
                status = "partial_success"
                message = (
                    f"Successfully inserted {success_count} out of {len(file_paths)} documents"
                )
                if failed_files:
                    message += f". Failed files: {', '.join(failed_files)}"
            else:
                status = "failure"
                message = "No documents were successfully inserted"
                if failed_files:
                    message += f". Failed files: {', '.join(failed_files)}"

            return InsertResponse(status=status, message=message)
        except Exception as e:
            await self._handle_exception(e, f"inserting batch from {directory_path}")
            raise

    async def scan_for_new_documents(self) -> Union[Any, HTTPValidationError]:
        """
        Start scanning RAG Agent's /input directory for new documents.

        Returns:
            Union[Any, HTTPValidationError]: Operation result.
        """
        logger.debug("Starting scan for new documents...")
        return await self._call_api(
            api_func=async_scan_for_new_documents,
            operation_name="scanning for new documents",
            client=self.client,
        )

    async def get_documents(
        self,
    ) -> Union[DocsStatusesResponse, HTTPValidationError, None]:
        """
        Get list of all documents in RAG Agent.

        Returns:
            Union[DocsStatusesResponse, HTTPValidationError]: List of documents.
        """
        logger.debug("Getting list of documents...")
        return await self._call_api(
            api_func=async_get_documents,
            operation_name="getting documents list",
            client=self.client,
        )

    async def get_pipeline_status(
        self,
    ) -> Union[PipelineStatusResponse, HTTPValidationError, None]:
        """
        Get status of document processing in pipeline.

        Returns:
            Union[PipelineStatusResponse, HTTPValidationError]: Pipeline status.
        """
        logger.debug("Getting pipeline status...")
        return await self._call_api(
            api_func=async_get_pipeline_status,
            operation_name="getting pipeline status",
            client=self.client,
        )

    async def get_graph_labels(self) -> Union[Dict[str, List[str]], HTTPValidationError, None]:
        """
        Get graph labels from knowledge graph.

        Returns:
            Union[Dict[str, List[str]], HTTPValidationError]: Graph labels.
        """
        logger.debug("Getting graph labels...")
        return await self._call_api(
            api_func=async_get_graph_labels,
            operation_name="getting graph labels",
            client=self.client,
        )

    async def delete_by_entity(
        self, entity_name: str
    ) -> Union[StatusMessageResponse, HTTPValidationError, None]:
        """
        Delete entity from knowledge graph by name.

        Args:
            entity_name (str): Entity name

        Returns:
            Union[StatusMessageResponse, HTTPValidationError]: Operation result.
        """
        logger.debug(f"Deleting entity by name: {entity_name}")

        return await self._call_api(
            api_func=async_delete_entity,
            operation_name=f"deletion by entity name: {entity_name}",
            client=self.client,
            entity_name=entity_name,
        )

    async def delete_by_doc_id(
        self, doc_id: str
    ) -> Union[StatusMessageResponse, HTTPValidationError, None]:
        """
        Delete all entities and relationships associated with a document.

        Args:
            doc_id (str): Document ID

        Returns:
            Union[StatusMessageResponse, HTTPValidationError]: Operation result.
        """
        logger.debug(f"Deleting entities by document ID: {doc_id}")

        return await self._call_api(
            api_func=async_delete_by_doc_id,
            operation_name=f"deletion by document ID: {doc_id}",
            client=self.client,
            doc_id=doc_id,
        )

    async def create_entity(
        self, entity_name: str, entity_type: str, description: str, source_id: str
    ) -> Union[EntityResponse, HTTPValidationError, None]:
        """
        Create new entity in knowledge graph.

        Args:
            entity_name (str): Entity name.
            entity_type (str): Entity type.
            description (str): Entity description.
            source_id (str): Source ID (document).

        Returns:
            Union[EntityResponse, HTTPValidationError]: Created entity.
        """
        logger.debug(f"Creating entity: {entity_name} (type={entity_type})")

        request = EntityRequest(
            entity_type=entity_type,
            description=description,
            source_id=source_id,
        )

        return await self._call_api(
            api_func=async_create_entity,
            operation_name="entity creation",
            client=self.client,
            entity_name=entity_name,
            body=request,
        )

    async def edit_entity(
        self, entity_name: str, entity_type: str, description: str, source_id: str
    ) -> Union[EntityResponse, HTTPValidationError, None]:
        """
        Edit existing entity in knowledge graph.

        Args:
            entity_name (str): Entity name.
            entity_type (str): New entity type.
            description (str): New entity description.
            source_id (str): Source ID (document).

        Returns:
            Union[EntityResponse, HTTPValidationError]: Updated entity.
        """
        logger.debug(f"Editing entity: {entity_name}")

        request = EntityRequest(
            entity_type=entity_type,
            description=description,
            source_id=source_id,
        )

        return await self._call_api(
            api_func=async_edit_entity,
            operation_name="entity editing",
            client=self.client,
            entity_name=entity_name,
            body=request,
        )

    async def create_relation(
        self,
        source: str,
        target: str,
        description: str,
        keywords: str,
        source_id: str | None,
        weight: float | None,
    ) -> Union[relation_response.RelationResponse, HTTPValidationError, None]:
        """
        Create relationship between entities in knowledge graph.

        Args:
            source (str): Source entity name.
            target (str): Target entity name.
            description (str): Relationship description.
            keywords (str): Keywords for relationship.
            source_id (str | None): Source ID (document).
            weight (float | None): Relationship weight.

        Returns:
            Union[relation_response.RelationResponse, HTTPValidationError]: Created relationship.
        """
        logger.debug(f"Creating relationship: {source} -> {target}")

        request = relation_request.RelationRequest(
            description=description,
            keywords=keywords,
            source_id=source_id,
            weight=weight,
        )

        return await self._call_api(
            api_func=async_create_relation,
            operation_name="relationship creation",
            client=self.client,
            source=source,
            target=target,
            body=request,
        )

    async def edit_relation(
        self,
        source: str,
        target: str,
        description: str,
        keywords: str,
        source_id: str | None,
        weight: float | None,
        relation_type: str,
    ) -> Union[relation_response.RelationResponse, HTTPValidationError, None]:
        """
        Edit relationship between entities.

        Args:
            source (str): Source entity name.
            target (str): Target entity name.
            properties (Dict[str, Any]): New relationship properties.

        Returns:
            Union[Dict, HTTPValidationError]: Updated relationship.
        """
        logger.debug(f"Editing relationship: {source} -> {target}")

        request = relation_request.RelationRequest(
            description=description,
            keywords=keywords,
            source_id=source_id,
            weight=weight,
        )

        return await self._call_api(
            api_func=async_edit_relation,
            operation_name="relationship editing",
            client=self.client,
            source=source,
            target=target,
            body=request,
            relation_type=relation_type,
        )

    async def merge_entities(
        self,
        source_entities: List[str],
        target_entity: str,
        merge_strategy: Dict[str, str],
    ) -> Union[EntityResponse, HTTPValidationError, None]:
        """
        Merge multiple entities into one with relationship migration.

        Args:
            source_entities (List[str]): List of entity names to merge.
            target_entity (str): Target entity name.
            merge_strategy (Dict[str, str], optional): Property merge strategy.
                Possible values for strategies: 'max', 'min', 'concat', 'first', 'last'
                Example: {"description": "concat", "weight": "max"}

        Returns:
            Union[Dict, HTTPValidationError]: Merge operation result.
        """
        logger.debug(f"Merging entities: {', '.join(source_entities)} -> {target_entity}")

        request = MergeEntitiesRequest(
            source_entities=source_entities,
            target_entity=target_entity,
            merge_strategy=MergeEntitiesRequestMergeStrategyType0.from_dict(merge_strategy),
        )

        return await self._call_api(
            api_func=async_merge_entities,
            operation_name="entity merging",
            client=self.client,
            body=request,
        )

    async def get_health(self) -> Union[Any, HTTPValidationError]:
        """
        Check health status of RAG Agent service.

        Returns:
            Union[Any, HTTPValidationError]: Health status.
        """
        logger.debug("Checking service health status...")
        return await self._call_api(
            api_func=async_get_health,
            operation_name="health check",
            client=self.client,
        )

    # Dataset Management Methods

    async def create_dataset(
        self,
        name: str,
        description: str = None,
        rag_type: str = "rag",
        workspace: str = None,
        namespace_prefix: str = None,
        storage_type: str = "local",
        chunk_engine: str = "default",
        schedule: str = None,
        args: Dict[str, Any] = None,
        created_by: str = None,
        owner_id: str = None,
        visibility: str = "private",
        default_permission: str = "none",
        user_id: str = None,
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Create a new dataset.

        Args:
            name: Dataset name (must be unique)
            description: Optional dataset description
            rag_type: RAG type (default: 'rag')
            workspace: Optional workspace identifier
            namespace_prefix: Optional namespace prefix
            storage_type: Storage type (default: 'local')
            chunk_engine: Chunk engine type (default: 'default')
            schedule: Optional schedule configuration
            args: Additional arguments as JSON
            created_by: Creator identifier
            owner_id: Owner identifier
            visibility: Dataset visibility ('private', 'public')
            default_permission: Default permission level
            user_id: User UUID for dataset ownership

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Created dataset information
        """
        logger.debug(f"Creating dataset: {name}")

        request_body = {
            "name": name,
            "rag_type": rag_type,
            "storage_type": storage_type,
            "chunk_engine": chunk_engine,
            "visibility": visibility,
            "default_permission": default_permission,
        }

        # Only add optional fields if they are not None
        if description is not None:
            request_body["description"] = description
        if workspace is not None:
            request_body["workspace"] = workspace
        if namespace_prefix is not None:
            request_body["namespace_prefix"] = namespace_prefix
        if schedule is not None:
            request_body["schedule"] = schedule
        if args is not None:
            request_body["args"] = args
        if created_by is not None:
            request_body["created_by"] = created_by
        if owner_id is not None:
            request_body["owner_id"] = owner_id
        if user_id is not None:
            request_body["user_id"] = user_id

        try:
            # Ensure auth before request
            await self._ensure_auth()
            
            url = f"{self.base_url}/datasets"
            client = self.client.get_async_httpx_client()
            
            # Log request details
            self._log_request_details("POST", url, dict(client.headers), request_body)
            
            response = await client.post(url, json=request_body)
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            await self._handle_exception(e, f"creating dataset {name}")
            return None

    async def get_dataset(self, dataset_id: str) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Get dataset information by ID.

        Args:
            dataset_id: Dataset UUID

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Dataset information
        """
        import httpx

        # Ensure auth before request
        await self._ensure_auth()
        
        url = f"{self.base_url}/datasets/{dataset_id}"
        client = self.client.get_async_httpx_client()
        
        # Log request details
        self._log_request_details("GET", url, dict(client.headers))

        try:
            response = await client.get(url)
            logger.info(f"Response status: {response.status_code}")
            if response.status_code != 200:
                logger.info(f"Response body: {response.text[:500]}")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            logger.error(f"Connection error for {url}: {str(e)}")
            logger.error(f"Please check if RAG Agent API server is running at {self.base_url}")
            await self._handle_exception(e, f"connecting to {url}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            logger.error(f"Response content: {e.response.text[:500]}")
            if e.response.status_code == 404:
                logger.error(f"Dataset not found: {dataset_id}")
            await self._handle_exception(e, f"getting dataset (HTTP {e.response.status_code})")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {type(e).__name__}: {str(e)}")
            await self._handle_exception(e, f"getting dataset {dataset_id}")
            return None

    async def list_datasets(
        self,
        page: int = 1,
        page_size: int = 20,
        status: str = None,
        visibility: str = None,
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        List all datasets with pagination.

        Args:
            page: Page number (default: 1)
            page_size: Items per page (default: 20)
            status: Filter by status (optional)
            visibility: Filter by visibility (optional)

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: List of datasets with pagination info
        """
        # Ensure auth before request
        await self._ensure_auth()

        params = {
            "page": page,
            "page_size": page_size,
        }
        if status:
            params["status"] = status
        if visibility:
            params["visibility"] = visibility

        url = f"{self.base_url}/datasets"
        client = self.client.get_async_httpx_client()
        
        # Log request details - print actual httpx client headers
        import sys
        print(f"=== ACTUAL HTTPX CLIENT HEADERS ===", file=sys.stderr)
        print(f"client._headers: {self.client._headers}", file=sys.stderr)
        print(f"httpx_client.headers: {dict(client.headers)}", file=sys.stderr)
        print(f"=== END HEADERS ===", file=sys.stderr)
        
        self._log_request_details("GET", url, dict(client.headers), f"params={params}")

        try:
            response = await client.get(url, params=params)
            logger.info(f"Response status: {response.status_code}")
            if response.status_code != 200:
                logger.info(f"Response body: {response.text[:500]}")
            response.raise_for_status()
            result = response.json()
            return result
        except Exception as e:
            logger.error(f"Failed to list datasets: {type(e).__name__}: {str(e)}")
            await self._handle_exception(e, "listing datasets")
            return None

    async def update_dataset(
        self,
        dataset_id: str,
        updates: Dict[str, Any],
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Update dataset information.

        Args:
            dataset_id: Dataset UUID
            updates: Dictionary of fields to update

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Updated dataset information
        """
        logger.debug(f"Updating dataset: {dataset_id}")

        try:
            response = await self.client.get_async_httpx_client().put(
                f"{self.base_url}/datasets/{dataset_id}",
                json=updates,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            await self._handle_exception(e, f"updating dataset {dataset_id}")
            return None

    async def delete_dataset(self, dataset_id: str) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Delete a dataset.

        Args:
            dataset_id: Dataset UUID

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Deletion result
        """
        logger.debug(f"Deleting dataset: {dataset_id}")

        try:
            response = await self.client.get_async_httpx_client().delete(
                f"{self.base_url}/datasets/{dataset_id}",
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            await self._handle_exception(e, f"deleting dataset {dataset_id}")
            return None

    async def get_dataset_statistics(
        self, dataset_id: str
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Get comprehensive statistics for a dataset.

        This method retrieves both document statistics and graph statistics
        and combines them into a single response.

        Args:
            dataset_id: Dataset UUID

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Combined dataset statistics
                containing 'document_statistics' and 'graph_statistics' keys
        """
        import httpx
        import asyncio

        doc_stats_url = f"{self.base_url}/datasets/{dataset_id}/documents/statistics"
        graph_stats_url = f"{self.base_url}/datasets/{dataset_id}/graphs/statistics"

        logger.debug(f"Getting comprehensive statistics for dataset: {dataset_id}")
        logger.debug(f"Document statistics URL: {doc_stats_url}")
        logger.debug(f"Graph statistics URL: {graph_stats_url}")

        try:
            # Fetch both statistics in parallel
            doc_response, graph_response = await asyncio.gather(
                self.client.get_async_httpx_client().get(doc_stats_url),
                self.client.get_async_httpx_client().get(graph_stats_url),
                return_exceptions=True
            )

            result = {}

            # Process document statistics response
            if isinstance(doc_response, Exception):
                logger.error(f"Failed to get document statistics: {type(doc_response).__name__}: {str(doc_response)}")
                result["document_statistics"] = {"error": str(doc_response)}
            else:
                logger.debug(f"Document statistics response status: {doc_response.status_code}")
                try:
                    doc_response.raise_for_status()
                    result["document_statistics"] = doc_response.json()
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error {e.response.status_code} for document statistics")
                    logger.error(f"Response content: {e.response.text[:500]}")
                    result["document_statistics"] = {"error": f"HTTP {e.response.status_code}"}

            # Process graph statistics response
            if isinstance(graph_response, Exception):
                logger.error(f"Failed to get graph statistics: {type(graph_response).__name__}: {str(graph_response)}")
                result["graph_statistics"] = {"error": str(graph_response)}
            else:
                logger.debug(f"Graph statistics response status: {graph_response.status_code}")
                try:
                    graph_response.raise_for_status()
                    result["graph_statistics"] = graph_response.json()
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error {e.response.status_code} for graph statistics")
                    logger.error(f"Response content: {e.response.text[:500]}")
                    result["graph_statistics"] = {"error": f"HTTP {e.response.status_code}"}

            # Return combined result if at least one succeeded
            if "error" not in result.get("document_statistics", {}) or "error" not in result.get("graph_statistics", {}):
                return result
            else:
                logger.error(f"Both statistics requests failed for dataset {dataset_id}")
                return None

        except httpx.ConnectError as e:
            logger.error(f"Connection error for dataset statistics: {str(e)}")
            logger.error(f"Please check if RAG Agent API server is running at {self.base_url}")
            await self._handle_exception(e, f"connecting to dataset statistics endpoints")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting statistics for dataset {dataset_id}: {type(e).__name__}: {str(e)}")
            await self._handle_exception(e, f"getting statistics for dataset {dataset_id}")
            return None

    # Dataset Query Methods

    async def query_dataset(
        self,
        dataset_id: str,
        query_text: str,
        mode: str = "mix",
        top_k: int = 5,
        chunk_top_k: int = 20,
        only_need_context: bool = False,
        only_need_prompt: bool = False,
        enable_rerank: bool = True,
        response_type: str = "Multiple Paragraphs",
        max_token_for_text_unit: int = 1000,
        max_token_for_global_context: int = 1000,
        max_token_for_local_context: int = 1000,
        max_entity_tokens: int = 10000,
        max_relation_tokens: int = 10000,
        max_total_tokens: int = 32000,
        hl_keywords: List[str] = None,
        ll_keywords: List[str] = None,
        history_turns: int = 0,
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Query a specific dataset.

        Args:
            dataset_id: Dataset UUID
            query_text: Query text
            mode: Search mode (global, hybrid, local, mix, naive). Default is "mix"
            top_k: Number of results. Default is 5
            chunk_top_k: Number of chunks to retrieve. Default is 20
            only_need_context: Return only context without LLM response. Default is False
            only_need_prompt: Return only generated prompt. Default is False
            enable_rerank: Enable reranking of results. Default is True
            response_type: Response format. Default is "Multiple Paragraphs"
            max_token_for_text_unit: Maximum tokens for each text fragment. Default is 1000
            max_token_for_global_context: Maximum tokens for global context. Default is 1000
            max_token_for_local_context: Maximum tokens for local context. Default is 1000
            max_entity_tokens: Maximum tokens for entity context. Default is 10000
            max_relation_tokens: Maximum tokens for relation context. Default is 10000
            max_total_tokens: Maximum total tokens for response. Default is 32000
            hl_keywords: List of high-level keywords for prioritization
            ll_keywords: List of low-level keywords for search refinement
            history_turns: Number of conversation turns in response context. Default is 0

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Query result
        """
        logger.debug(f"Querying dataset {dataset_id}: {query_text[:100]}...")

        request_body = {
            "query": query_text,
            "mode": mode,
            "top_k": top_k,
            "chunk_top_k": chunk_top_k,
            "only_need_context": only_need_context,
            "only_need_prompt": only_need_prompt,
            "enable_rerank": enable_rerank,
            "response_type": response_type,
            "max_token_for_text_unit": max_token_for_text_unit,
            "max_token_for_global_context": max_token_for_global_context,
            "max_token_for_local_context": max_token_for_local_context,
            "max_entity_tokens": max_entity_tokens,
            "max_relation_tokens": max_relation_tokens,
            "max_total_tokens": max_total_tokens,
            "hl_keywords": hl_keywords or [],
            "ll_keywords": ll_keywords or [],
            "history_turns": history_turns,
        }

        try:
            response = await self.client.get_async_httpx_client().post(
                f"{self.base_url}/datasets/{dataset_id}/query",
                json=request_body,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            await self._handle_exception(e, f"querying dataset {dataset_id}")
            return None

    async def query_multiple_datasets(
        self,
        dataset_ids: List[str],
        query_text: str,
        mode: str = "mix",
        top_k: int = 10,
        only_need_context: bool = False,
        enable_rerank: bool = True,
        document_filters: Dict[str, List[str]] = None,
        response_type: str = "Multiple Paragraphs",
        max_token_for_text_unit: int = 1000,
        max_token_for_global_context: int = 1000,
        max_token_for_local_context: int = 1000,
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Query multiple datasets simultaneously (cross-dataset query).

        Args:
            dataset_ids: List of dataset UUIDs to query
            query_text: Query text
            mode: Search mode (global, hybrid, local, mix, naive). Default is "mix"
            top_k: Number of results per dataset. Default is 10
            only_need_context: Return only context without LLM response. Default is False
            enable_rerank: Enable cross-dataset reranking. Default is True
            document_filters: Optional document filters per dataset (dataset_id -> [doc_ids])
            response_type: Response format. Default is "Multiple Paragraphs"
            max_token_for_text_unit: Maximum tokens for each text fragment. Default is 1000
            max_token_for_global_context: Maximum tokens for global context. Default is 1000
            max_token_for_local_context: Maximum tokens for local context. Default is 1000

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Merged query results from all datasets
        """
        import httpx

        url = f"{self.base_url}/datasets/cross-query"
        logger.debug(f"Querying {len(dataset_ids)} datasets: {query_text[:100]}...")
        logger.debug(f"Request URL: {url}")

        request_body = {
            "dataset_ids": dataset_ids,
            "query": query_text,
            "mode": mode,
            "top_k": top_k,
            "only_need_context": only_need_context,
            "enable_rerank": enable_rerank,
            "document_filters": document_filters or {},
            "response_type": response_type,
            "max_token_for_text_unit": max_token_for_text_unit,
            "max_token_for_global_context": max_token_for_global_context,
            "max_token_for_local_context": max_token_for_local_context,
        }

        try:
            response = await self.client.get_async_httpx_client().post(
                url,
                json=request_body,
            )
            logger.debug(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            logger.error(f"Connection error for {url}: {str(e)}")
            logger.error(f"Please check if RAG Agent API server is running at {self.base_url}")
            await self._handle_exception(e, f"connecting to {url}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            logger.error(f"Response content: {e.response.text[:500]}")
            await self._handle_exception(e, f"querying multiple datasets (HTTP {e.response.status_code})")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {type(e).__name__}: {str(e)}")
            await self._handle_exception(e, f"querying multiple datasets")
            return None

    # Dataset Document Management Methods

    async def upload_document_to_dataset(
        self, dataset_id: str, file_path: str
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Upload document to a specific dataset.

        Args:
            dataset_id: Dataset UUID
            file_path: Path to file to upload

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Upload result
        """
        logger.debug(f"Uploading document to dataset {dataset_id}: {file_path}")

        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                files = {"file": (path.name, f, "application/octet-stream")}
                response = await self.client.get_async_httpx_client().post(
                    f"{self.base_url}/datasets/{dataset_id}/documents/upload",
                    files=files,
                )
                response.raise_for_status()
                return response.json()
        except FileNotFoundError:
            raise
        except Exception as e:
            await self._handle_exception(e, f"uploading document to dataset {dataset_id}")
            return None

    async def get_dataset_documents(
        self,
        dataset_id: str,
        page: int = 1,
        page_size: int = 20,
        status: str = None,
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Get list of documents in a dataset.

        Args:
            dataset_id: Dataset UUID
            page: Page number (default: 1)
            page_size: Items per page (default: 20)
            status: Filter by document status (optional)

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: List of documents with pagination
        """
        logger.debug(f"Getting documents for dataset {dataset_id}")

        params = {
            "page": page,
            "page_size": page_size,
        }
        if status:
            params["status"] = status

        try:
            response = await self.client.get_async_httpx_client().get(
                f"{self.base_url}/datasets/{dataset_id}/documents",
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            await self._handle_exception(e, f"getting documents for dataset {dataset_id}")
            return None

    async def delete_dataset_document(
        self, dataset_id: str, doc_id: str, delete_file: bool = False
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Delete a document from a dataset.

        Args:
            dataset_id: Dataset UUID
            doc_id: Document ID to delete
            delete_file: Whether to delete the physical file (default: False)

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Deletion result
        """
        import httpx

        url = f"{self.base_url}/datasets/{dataset_id}/documents/delete_document"
        logger.debug(f"Deleting document {doc_id} from dataset {dataset_id}")
        logger.debug(f"Request URL: {url}")

        request_body = {
            "doc_ids": [doc_id],
            "delete_file": delete_file
        }

        try:
            # Use generic request to support older httpx versions where delete() has no `json` kwarg
            response = await self.client.get_async_httpx_client().request(
                "DELETE",
                url,
                json=request_body,
            )
            logger.debug(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            logger.error(f"Connection error for {url}: {str(e)}")
            logger.error(f"Please check if RAG Agent API server is running at {self.base_url}")
            await self._handle_exception(e, f"connecting to {url}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            logger.error(f"Response content: {e.response.text[:500]}")
            await self._handle_exception(e, f"deleting document (HTTP {e.response.status_code})")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {type(e).__name__}: {str(e)}")
            await self._handle_exception(e, f"deleting document from dataset {dataset_id}")
            return None

    async def scan_dataset_documents(
        self, dataset_id: str
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Scan dataset's input directory for new documents.

        Args:
            dataset_id: Dataset UUID

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Scan result
        """
        logger.debug(f"Scanning documents for dataset {dataset_id}")

        try:
            response = await self.client.get_async_httpx_client().post(
                f"{self.base_url}/datasets/{dataset_id}/documents/scan",
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            await self._handle_exception(e, f"scanning documents for dataset {dataset_id}")
            return None

    # Dataset Graph Methods

    async def get_dataset_graph(
        self,
        dataset_id: str,
        node_label: str = None,
        max_depth: int = 3,
        max_nodes: int = 100,
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Get knowledge graph data for a dataset.

        Args:
            dataset_id: Dataset UUID
            node_label: Optional node label to filter
            max_depth: Maximum graph depth (default: 3)
            max_nodes: Maximum number of nodes (default: 100)

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Graph data
        """
        import httpx

        url = f"{self.base_url}/datasets/{dataset_id}/graphs"
        logger.debug(f"Getting graph for dataset {dataset_id}")
        logger.debug(f"Request URL: {url}")

        params = {
            "max_depth": max_depth,
            "max_nodes": max_nodes,
        }
        if node_label:
            params["node_label"] = node_label

        try:
            response = await self.client.get_async_httpx_client().get(
                url,
                params=params,
            )
            logger.debug(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            logger.error(f"Connection error for {url}: {str(e)}")
            logger.error(f"Please check if RAG Agent API server is running at {self.base_url}")
            await self._handle_exception(e, f"connecting to {url}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            logger.error(f"Response content: {e.response.text[:500]}")
            await self._handle_exception(e, f"getting graph (HTTP {e.response.status_code})")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {type(e).__name__}: {str(e)}")
            await self._handle_exception(e, f"getting graph for dataset {dataset_id}")
            return None

    async def get_dataset_graph_labels(
        self, dataset_id: str
    ) -> Union[Dict[str, Any], HTTPValidationError, None]:
        """
        Get graph labels for a dataset.

        Args:
            dataset_id: Dataset UUID

        Returns:
            Union[Dict[str, Any], HTTPValidationError, None]: Graph labels
        """
        import httpx

        url = f"{self.base_url}/datasets/{dataset_id}/graphs/labels"
        logger.debug(f"Getting graph labels for dataset {dataset_id}")
        logger.debug(f"Request URL: {url}")

        try:
            response = await self.client.get_async_httpx_client().get(url)
            logger.debug(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError as e:
            logger.error(f"Connection error for {url}: {str(e)}")
            logger.error(f"Please check if RAG Agent API server is running at {self.base_url}")
            await self._handle_exception(e, f"connecting to {url}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            logger.error(f"Response content: {e.response.text[:500]}")
            await self._handle_exception(e, f"getting graph labels (HTTP {e.response.status_code})")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {type(e).__name__}: {str(e)}")
            await self._handle_exception(e, f"getting graph labels for dataset {dataset_id}")
            return None

    async def close(self):
        """Close HTTP client and auth clients."""
        # Close auth clients if present
        if self.auth_client:
            await self.auth_client.close()
        if self.basic_auth_client:
            await self.basic_auth_client.close()
        
        # Close HTTP client
        await self.client.get_async_httpx_client().aclose()
        logger.info("RAG Agent API client closed.")
