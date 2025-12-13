"""
Cognee SDK Client

Main client class for interacting with Cognee API server.
"""

import asyncio
import json
import mimetypes
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any, BinaryIO
from uuid import UUID

import httpx

from cognee_sdk.exceptions import (
    AuthenticationError,
    CogneeAPIError,
    CogneeSDKError,
    NotFoundError,
    ServerError,
    TimeoutError,
    ValidationError,
)
from cognee_sdk.models import (
    AddResult,
    CognifyResult,
    CombinedSearchResult,
    DataItem,
    Dataset,
    DeleteResult,
    GraphData,
    HealthStatus,
    MemifyResult,
    PipelineRunStatus,
    SearchHistoryItem,
    SearchResult,
    SearchType,
    SyncResult,
    SyncStatus,
    UpdateResult,
    User,
)


class CogneeClient:
    """
    Cognee SDK Client.

    A lightweight, type-safe, and fully asynchronous Python client for Cognee API.

    Args:
        api_url: Base URL of the Cognee API server (e.g., "http://localhost:8000")
        api_token: Optional authentication token for Bearer token authentication
        timeout: Request timeout in seconds (default: 300.0)
        max_retries: Maximum number of retry attempts (default: 3)
        retry_delay: Initial retry delay in seconds (default: 1.0)

    Example:
        >>> import asyncio
        >>> from cognee_sdk import CogneeClient
        >>>
        >>> async def main():
        >>>     client = CogneeClient(api_url="http://localhost:8000")
        >>>     try:
        >>>         datasets = await client.list_datasets()
        >>>         print(f"Found {len(datasets)} datasets")
        >>>     finally:
        >>>         await client.close()
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_url: str,
        api_token: str | None = None,
        timeout: float = 300.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """
        Initialize Cognee client.

        Args:
            api_url: Base URL of the Cognee API server
            api_token: Optional authentication token
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Initial retry delay in seconds
        """
        self.api_url = api_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Create HTTP client with connection pool
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout, connect=10.0),
            limits=httpx.Limits(
                max_keepalive_connections=10,
                max_connections=20,
            ),
            follow_redirects=True,
        )

    def _get_headers(self, content_type: str = "application/json") -> dict[str, str]:
        """
        Get request headers with authentication.

        Args:
            content_type: Content-Type header value

        Returns:
            Dictionary of headers
        """
        headers: dict[str, str] = {"Content-Type": content_type}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers

    async def _handle_error_response(self, response: httpx.Response) -> None:
        """
        Handle error responses and raise appropriate exceptions.

        Args:
            response: HTTP response object

        Raises:
            AuthenticationError: For 401 status codes
            NotFoundError: For 404 status codes
            ValidationError: For 400 status codes
            ServerError: For 5xx status codes
            CogneeAPIError: For other error status codes
        """
        error_data: dict | None = None
        try:
            error_data = response.json()
            error_message = (
                error_data.get("error")
                or error_data.get("detail")
                or error_data.get("message")
                or response.text
            )
        except Exception:
            error_message = response.text or f"HTTP {response.status_code}"

        status_code = response.status_code

        if status_code == 401 or status_code == 403:
            raise AuthenticationError(error_message, status_code, error_data)
        elif status_code == 404:
            raise NotFoundError(error_message, status_code, error_data)
        elif status_code == 400:
            raise ValidationError(error_message, status_code, error_data)
        elif status_code >= 500:
            raise ServerError(error_message, status_code, error_data)
        else:
            raise CogneeAPIError(error_message, status_code, error_data)

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Send HTTP request with retry mechanism.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path (e.g., "/api/v1/datasets")
            **kwargs: Additional arguments to pass to httpx request

        Returns:
            HTTP response object

        Raises:
            TimeoutError: If request times out after all retries
            CogneeSDKError: If request fails after all retries
        """
        url = f"{self.api_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        base_headers = self._get_headers()

        # Merge headers, custom headers take precedence
        merged_headers = {**base_headers, **headers}

        last_exception: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                response = await self.client.request(
                    method,
                    url,
                    headers=merged_headers,
                    **kwargs,
                )

                # Handle error responses
                if response.status_code >= 400:
                    await self._handle_error_response(response)

                return response

            except httpx.TimeoutException as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2**attempt))  # Exponential backoff
                else:
                    raise TimeoutError(f"Request timeout after {self.max_retries} attempts") from e

            except httpx.RequestError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2**attempt))
                else:
                    raise CogneeSDKError(f"Request failed: {str(e)}") from e

        if last_exception:
            raise last_exception
        raise CogneeSDKError("Request failed for unknown reason")

    async def health_check(self) -> HealthStatus:
        """
        Check API server health.

        Returns:
            Health status information

        Raises:
            CogneeAPIError: If health check fails
        """
        response = await self._request("GET", "/health")
        data = response.json()
        return HealthStatus(**data)

    async def close(self) -> None:
        """Close HTTP client and release resources."""
        await self.client.aclose()

    async def __aenter__(self) -> "CogneeClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    # ==================== Core API Methods (P0) ====================

    async def add(
        self,
        data: str | bytes | Path | BinaryIO | list[str | bytes | Path | BinaryIO],
        dataset_name: str | None = None,
        dataset_id: UUID | None = None,
        node_set: list[str] | None = None,
    ) -> AddResult:
        """
        Add data to Cognee for processing.

        Supports multiple input types: strings, bytes, file paths, file objects, or lists of these.

        Args:
            data: Data to add. Can be:
                - Single text string
                - Bytes data
                - File path (Path object or string)
                - File object (BinaryIO)
                - List of any of the above
            dataset_name: Name of the dataset to add data to
            dataset_id: UUID of an existing dataset (alternative to dataset_name)
            node_set: Optional list of node identifiers for graph organization

        Returns:
            AddResult with operation status and created data ID

        Raises:
            ValidationError: If neither dataset_name nor dataset_id is provided
            AuthenticationError: If authentication fails
            ServerError: If server error occurs

        Example:
            >>> # Add text data
            >>> result = await client.add(
            ...     data="Cognee turns documents into AI memory.",
            ...     dataset_name="my-dataset"
            ... )
            >>>
            >>> # Add file
            >>> result = await client.add(
            ...     data=Path("document.pdf"),
            ...     dataset_name="my-dataset"
            ... )
        """
        if not dataset_name and not dataset_id:
            raise ValidationError(
                "Either dataset_name or dataset_id must be provided",
                400,
            )

        # Handle single item or list
        if not isinstance(data, list):
            data_list = [data]
        else:
            data_list = data

        # Prepare files for multipart/form-data
        files: list[tuple] = []
        for item in data_list:
            if isinstance(item, str):
                # Check if it's a file path
                if item.startswith(("/", "file://", "s3://")):
                    file_path = Path(item.replace("file://", ""))
                    if file_path.exists() and file_path.is_file():
                        mime_type, _ = mimetypes.guess_type(str(file_path))
                        try:
                            with open(file_path, "rb") as f:
                                file_content = f.read()
                            files.append(
                                (
                                    "data",
                                    (
                                        file_path.name,
                                        file_content,
                                        mime_type or "application/octet-stream",
                                    ),
                                )
                            )
                        except OSError as e:
                            raise CogneeSDKError(
                                f"Failed to read file {file_path}: {str(e)}"
                            ) from e
                    else:
                        # Treat as text string
                        files.append(("data", ("data.txt", item.encode("utf-8"), "text/plain")))
                else:
                    # Plain text string
                    files.append(("data", ("data.txt", item.encode("utf-8"), "text/plain")))
            elif isinstance(item, bytes):
                files.append(("data", ("data.bin", item, "application/octet-stream")))
            elif isinstance(item, Path):
                mime_type, _ = mimetypes.guess_type(str(item))
                try:
                    with open(item, "rb") as f:
                        file_content = f.read()
                    files.append(
                        (
                            "data",
                            (item.name, file_content, mime_type or "application/octet-stream"),
                        )
                    )
                except OSError as e:
                    raise CogneeSDKError(f"Failed to read file {item}: {str(e)}") from e
            elif hasattr(item, "read"):
                # File-like object
                file_name = getattr(item, "name", "data.bin")
                content = item.read() if hasattr(item, "read") else item
                mime_type, _ = mimetypes.guess_type(file_name)
                files.append(
                    (
                        "data",
                        (file_name, content, mime_type or "application/octet-stream"),
                    )
                )
            else:
                # Fallback: convert to string
                files.append(("data", ("data.txt", str(item).encode("utf-8"), "text/plain")))

        # Prepare form data
        form_data: dict[str, Any] = {}
        if dataset_name:
            form_data["datasetName"] = dataset_name
        if dataset_id:
            form_data["datasetId"] = str(dataset_id)
        if node_set:
            form_data["node_set"] = json.dumps(node_set)

        # Send request (don't set Content-Type for multipart/form-data)
        response = await self._request(
            "POST",
            "/api/v1/add",
            files=files,
            data=form_data,
            headers={},  # Let httpx set Content-Type for multipart
        )

        result_data = response.json()
        return AddResult(**result_data)

    async def delete(
        self,
        data_id: UUID,
        dataset_id: UUID,
        mode: str = "soft",
    ) -> DeleteResult:
        """
        Delete data from a dataset.

        Args:
            data_id: UUID of the data to delete
            dataset_id: UUID of the dataset containing the data
            mode: Deletion mode - "soft" (default) or "hard"

        Returns:
            DeleteResult with operation status

        Raises:
            NotFoundError: If data or dataset not found
            ValidationError: If invalid parameters provided
        """
        params = {
            "data_id": str(data_id),
            "dataset_id": str(dataset_id),
            "mode": mode,
        }

        response = await self._request("DELETE", "/api/v1/delete", params=params)
        result_data = response.json()
        return DeleteResult(**result_data)

    async def cognify(
        self,
        datasets: list[str] | None = None,
        dataset_ids: list[UUID] | None = None,
        run_in_background: bool = False,
        custom_prompt: str | None = None,
    ) -> dict[str, CognifyResult]:
        """
        Transform datasets into structured knowledge graphs.

        Args:
            datasets: List of dataset names to process
            dataset_ids: List of dataset UUIDs to process
            run_in_background: Whether to run processing in background
            custom_prompt: Custom prompt for entity extraction

        Returns:
            Dictionary mapping dataset IDs to CognifyResult objects

        Raises:
            ValidationError: If neither datasets nor dataset_ids provided
            ServerError: If processing fails

        Example:
            >>> result = await client.cognify(
            ...     datasets=["my-dataset"],
            ...     run_in_background=False
            ... )
        """
        if (not datasets or len(datasets) == 0) and (not dataset_ids or len(dataset_ids) == 0):
            raise ValidationError(
                "Either datasets or dataset_ids must be provided",
                400,
            )

        payload: dict[str, Any] = {
            "run_in_background": run_in_background,
        }
        if datasets:
            payload["datasets"] = datasets
        if dataset_ids:
            payload["dataset_ids"] = [str(did) for did in dataset_ids]
        if custom_prompt:
            payload["custom_prompt"] = custom_prompt

        response = await self._request("POST", "/api/v1/cognify", json=payload)

        result_data = response.json()
        # Handle dictionary of results (one per dataset)
        if isinstance(result_data, dict):
            # Check if it's already a dict with dataset keys or a single result
            if "pipeline_run_id" in result_data or "status" in result_data:
                # Single result, wrap in "default" key
                return {"default": CognifyResult(**result_data)}
            else:
                # Dictionary of results (one per dataset)
                return {
                    key: CognifyResult(**value) if isinstance(value, dict) else value
                    for key, value in result_data.items()
                }
        return {"default": CognifyResult(**result_data)}

    async def search(
        self,
        query: str,
        search_type: SearchType = SearchType.GRAPH_COMPLETION,
        datasets: list[str] | None = None,
        dataset_ids: list[UUID] | None = None,
        system_prompt: str | None = None,
        node_name: list[str] | None = None,
        top_k: int = 10,
        only_context: bool = False,
        use_combined_context: bool = False,
    ) -> list[SearchResult] | CombinedSearchResult | list[dict[str, Any]]:
        """
        Search the knowledge graph.

        Args:
            query: Search query string
            search_type: Type of search to perform
            datasets: List of dataset names to search within
            dataset_ids: List of dataset UUIDs to search within
            system_prompt: System prompt for completion searches
            node_name: Filter results to specific node names
            top_k: Maximum number of results to return
            only_context: Return only context without LLM completion
            use_combined_context: Use combined context for search

        Returns:
            Search results - type depends on search_type:
            - List[SearchResult] for most search types
            - CombinedSearchResult for combined searches
            - List[Dict] for raw results

        Raises:
            ValidationError: If query is empty
            ServerError: If search fails

        Example:
            >>> results = await client.search(
            ...     query="What is Cognee?",
            ...     search_type=SearchType.GRAPH_COMPLETION,
            ...     datasets=["my-dataset"]
            ... )
        """
        if not query:
            raise ValidationError("Query cannot be empty", 400)

        payload: dict[str, Any] = {
            "query": query,
            "search_type": search_type.value,
            "top_k": top_k,
            "only_context": only_context,
            "use_combined_context": use_combined_context,
        }
        if datasets:
            payload["datasets"] = datasets
        if dataset_ids:
            payload["dataset_ids"] = [str(did) for did in dataset_ids]
        if system_prompt:
            payload["system_prompt"] = system_prompt
        if node_name:
            payload["node_name"] = node_name

        response = await self._request("POST", "/api/v1/search", json=payload)
        result_data = response.json()

        # Handle different response types
        if isinstance(result_data, dict) and "result" in result_data:
            return CombinedSearchResult(**result_data)
        elif isinstance(result_data, list):
            # Try to parse as SearchResult objects
            try:
                return [
                    SearchResult(**item) if isinstance(item, dict) else item for item in result_data
                ]
            except Exception:
                # Return raw data if parsing fails
                return result_data
        else:
            return result_data

    async def list_datasets(self) -> list[Dataset]:
        """
        Get all datasets accessible to the authenticated user.

        Returns:
            List of Dataset objects

        Raises:
            AuthenticationError: If authentication fails
            ServerError: If request fails
        """
        response = await self._request("GET", "/api/v1/datasets")
        result_data = response.json()
        return [Dataset(**item) for item in result_data]

    async def create_dataset(self, name: str) -> Dataset:
        """
        Create a new dataset or return existing dataset with the same name.

        Args:
            name: Name of the dataset to create

        Returns:
            Dataset object (created or existing)

        Raises:
            ValidationError: If name is empty
            ServerError: If creation fails

        Example:
            >>> dataset = await client.create_dataset("my-dataset")
            >>> print(f"Dataset ID: {dataset.id}")
        """
        if not name:
            raise ValidationError("Dataset name cannot be empty", 400)

        payload = {"name": name}
        response = await self._request("POST", "/api/v1/datasets", json=payload)
        result_data = response.json()
        return Dataset(**result_data)

    # ==================== Dataset Management API (P1) ====================

    async def update(
        self,
        data_id: UUID,
        dataset_id: UUID,
        data: str | bytes | Path | BinaryIO,
        node_set: list[str] | None = None,
    ) -> UpdateResult:
        """
        Update existing data in a dataset.

        Args:
            data_id: UUID of the data to update
            dataset_id: UUID of the dataset containing the data
            data: New data content (string, bytes, file path, or file object)
            node_set: Optional list of node identifiers

        Returns:
            UpdateResult with operation status

        Raises:
            NotFoundError: If data or dataset not found
            ValidationError: If invalid parameters provided
        """
        # Prepare file for upload
        files: list[tuple] = []
        if isinstance(data, str):
            if data.startswith(("/", "file://")):
                file_path = Path(data.replace("file://", ""))
                if file_path.exists() and file_path.is_file():
                    mime_type, _ = mimetypes.guess_type(str(file_path))
                    try:
                        with open(file_path, "rb") as f:
                            file_content = f.read()
                        files.append(
                            (
                                "data",
                                (
                                    file_path.name,
                                    file_content,
                                    mime_type or "application/octet-stream",
                                ),
                            )
                        )
                    except OSError as e:
                        raise CogneeSDKError(f"Failed to read file {file_path}: {str(e)}") from e
                else:
                    files.append(("data", ("data.txt", data.encode("utf-8"), "text/plain")))
            else:
                files.append(("data", ("data.txt", data.encode("utf-8"), "text/plain")))
        elif isinstance(data, bytes):
            files.append(("data", ("data.bin", data, "application/octet-stream")))
        elif isinstance(data, Path):
            mime_type, _ = mimetypes.guess_type(str(data))
            try:
                with open(data, "rb") as f:
                    file_content = f.read()
                files.append(
                    ("data", (data.name, file_content, mime_type or "application/octet-stream"))
                )
            except OSError as e:
                raise CogneeSDKError(f"Failed to read file {data}: {str(e)}") from e
        elif hasattr(data, "read"):
            file_name = getattr(data, "name", "data.bin")
            content = data.read() if hasattr(data, "read") else data
            mime_type, _ = mimetypes.guess_type(file_name)
            files.append(("data", (file_name, content, mime_type or "application/octet-stream")))
        else:
            files.append(("data", ("data.txt", str(data).encode("utf-8"), "text/plain")))

        form_data: dict[str, Any] = {}
        if node_set:
            form_data["node_set"] = json.dumps(node_set)

        params = {
            "data_id": str(data_id),
            "dataset_id": str(dataset_id),
        }

        response = await self._request(
            "PATCH",
            "/api/v1/update",
            files=files,
            data=form_data,
            params=params,
            headers={},
        )

        result_data = response.json()
        # Handle dictionary of results (one per dataset)
        if isinstance(result_data, dict):
            return UpdateResult(**result_data)
        return UpdateResult(status="success", message="Update completed")

    async def delete_dataset(self, dataset_id: UUID) -> None:
        """
        Delete a dataset by its ID.

        Args:
            dataset_id: UUID of the dataset to delete

        Raises:
            NotFoundError: If dataset not found
            AuthenticationError: If user doesn't have permission
        """
        await self._request("DELETE", f"/api/v1/datasets/{dataset_id}")

    async def get_dataset_data(self, dataset_id: UUID) -> list[DataItem]:
        """
        Get all data items in a dataset.

        Args:
            dataset_id: UUID of the dataset

        Returns:
            List of DataItem objects

        Raises:
            NotFoundError: If dataset not found
        """
        from cognee_sdk.models import DataItem

        response = await self._request("GET", f"/api/v1/datasets/{dataset_id}/data")
        result_data = response.json()
        return [DataItem(**item) for item in result_data]

    async def get_dataset_graph(self, dataset_id: UUID) -> GraphData:
        """
        Get the knowledge graph data for a dataset.

        Args:
            dataset_id: UUID of the dataset

        Returns:
            GraphData with nodes and edges

        Raises:
            NotFoundError: If dataset not found
        """
        response = await self._request("GET", f"/api/v1/datasets/{dataset_id}/graph")
        result_data = response.json()
        return GraphData(**result_data)

    async def get_dataset_status(self, dataset_ids: list[UUID]) -> dict[UUID, PipelineRunStatus]:
        """
        Get the processing status of datasets.

        Args:
            dataset_ids: List of dataset UUIDs to check

        Returns:
            Dictionary mapping dataset IDs to their processing status

        Raises:
            ValidationError: If dataset_ids is empty
        """
        if not dataset_ids:
            raise ValidationError("dataset_ids cannot be empty", 400)

        params = {"dataset": [str(did) for did in dataset_ids]}
        response = await self._request("GET", "/api/v1/datasets/status", params=params)
        result_data = response.json()

        # Convert string keys to UUID and status strings to enum
        return {
            UUID(key): PipelineRunStatus(value) if isinstance(value, str) else value
            for key, value in result_data.items()
        }

    async def download_raw_data(self, dataset_id: UUID, data_id: UUID) -> bytes:
        """
        Download the raw data file for a specific data item.

        Args:
            dataset_id: UUID of the dataset
            data_id: UUID of the data item

        Returns:
            Raw data as bytes

        Raises:
            NotFoundError: If data or dataset not found
        """
        response = await self._request("GET", f"/api/v1/datasets/{dataset_id}/data/{data_id}/raw")
        return response.content

    # ==================== Authentication API (P1) ====================

    async def login(self, email: str, password: str) -> str:
        """
        Login and get authentication token.

        Args:
            email: User email address
            password: User password

        Returns:
            Authentication token

        Raises:
            AuthenticationError: If credentials are invalid
            ValidationError: If email or password is empty
        """
        if not email or not password:
            raise ValidationError("Email and password are required", 400)

        payload = {"username": email, "password": password}
        response = await self._request("POST", "/api/v1/auth/login", json=payload)

        # Extract token from response (format may vary)
        result_data = response.json()
        token = result_data.get("access_token") or result_data.get("token")
        if token:
            self.api_token = token
            return token
        raise AuthenticationError("Token not found in response", response.status_code)

    async def register(self, email: str, password: str) -> "User":
        """
        Register a new user.

        Args:
            email: User email address
            password: User password

        Returns:
            User object

        Raises:
            ValidationError: If email or password is invalid
            ServerError: If registration fails
        """
        if not email or not password:
            raise ValidationError("Email and password are required", 400)

        payload = {"email": email, "password": password}
        response = await self._request("POST", "/api/v1/auth/register", json=payload)
        result_data = response.json()
        return User(**result_data)

    async def get_current_user(self) -> User:
        """
        Get current authenticated user information.

        Returns:
            User object

        Raises:
            AuthenticationError: If not authenticated
        """
        response = await self._request("GET", "/api/v1/auth/me")
        result_data = response.json()
        return User(**result_data)

    # ==================== Memify API (P1) ====================

    async def memify(
        self,
        dataset_name: str | None = None,
        dataset_id: UUID | None = None,
        extraction_tasks: list[str] | None = None,
        enrichment_tasks: list[str] | None = None,
        data: str | None = None,
        node_name: list[str] | None = None,
        run_in_background: bool = False,
    ) -> MemifyResult:
        """
        Enrich knowledge graph with memory algorithms.

        Args:
            dataset_name: Name of the dataset to memify
            dataset_id: UUID of the dataset to memify
            extraction_tasks: List of extraction tasks to execute
            enrichment_tasks: List of enrichment tasks to execute
            data: Custom data to process (optional)
            node_name: Filter graph to specific named entities
            run_in_background: Whether to run in background

        Returns:
            MemifyResult with operation status

        Raises:
            ValidationError: If neither dataset_name nor dataset_id provided
        """
        if not dataset_name and not dataset_id:
            raise ValidationError(
                "Either dataset_name or dataset_id must be provided",
                400,
            )

        payload: dict[str, Any] = {
            "run_in_background": run_in_background,
        }
        if dataset_name:
            payload["dataset_name"] = dataset_name
        if dataset_id:
            payload["dataset_id"] = str(dataset_id)
        if extraction_tasks:
            payload["extraction_tasks"] = extraction_tasks
        if enrichment_tasks:
            payload["enrichment_tasks"] = enrichment_tasks
        if data:
            payload["data"] = data
        if node_name:
            payload["node_name"] = node_name

        response = await self._request("POST", "/api/v1/memify", json=payload)
        result_data = response.json()
        return MemifyResult(**result_data)

    async def get_search_history(self) -> list[SearchHistoryItem]:
        """
        Get search history for the authenticated user.

        Returns:
            List of SearchHistoryItem objects

        Raises:
            AuthenticationError: If not authenticated
        """
        response = await self._request("GET", "/api/v1/search")
        result_data = response.json()
        return [SearchHistoryItem(**item) for item in result_data]

    # ==================== Visualization API (P2) ====================

    async def visualize(self, dataset_id: UUID) -> str:
        """
        Generate HTML visualization of the dataset's knowledge graph.

        Args:
            dataset_id: UUID of the dataset to visualize

        Returns:
            HTML content as string

        Raises:
            NotFoundError: If dataset not found
        """
        response = await self._request(
            "GET", "/api/v1/visualize", params={"dataset_id": str(dataset_id)}
        )
        return response.text

    # ==================== Sync API (P2) ====================

    async def sync_to_cloud(self, dataset_ids: list[UUID] | None = None) -> SyncResult:
        """
        Sync local data to Cognee Cloud.

        Args:
            dataset_ids: List of dataset UUIDs to sync (None = all datasets)

        Returns:
            SyncResult with operation status

        Raises:
            ServerError: If sync fails
        """
        payload: dict[str, Any] = {}
        if dataset_ids:
            payload["dataset_ids"] = [str(did) for did in dataset_ids]

        response = await self._request("POST", "/api/v1/sync", json=payload)
        result_data = response.json()

        # Handle dictionary of results
        if isinstance(result_data, dict) and "run_id" in result_data:
            return SyncResult(**result_data)
        # If multiple results, return the first one
        elif isinstance(result_data, dict):
            first_key = next(iter(result_data))
            return SyncResult(**result_data[first_key])
        return SyncResult(**result_data)

    async def get_sync_status(self) -> SyncStatus:
        """
        Get status of running sync operations.

        Returns:
            SyncStatus with information about running syncs
        """
        response = await self._request("GET", "/api/v1/sync/status")
        result_data = response.json()
        return SyncStatus(**result_data)

    # ==================== WebSocket Support (P2) ====================

    async def subscribe_cognify_progress(
        self, pipeline_run_id: UUID
    ) -> "AsyncIterator[dict[str, Any]]":
        """
        Subscribe to Cognify processing progress via WebSocket.

        Args:
            pipeline_run_id: UUID of the pipeline run to monitor

        Yields:
            Progress updates as dictionaries with status and payload

        Raises:
            ImportError: If websockets package is not installed
            AuthenticationError: If authentication fails
            ServerError: If WebSocket connection fails

        Example:
            >>> async for update in client.subscribe_cognify_progress(pipeline_run_id):
            ...     print(f"Status: {update['status']}")
            ...     if update['status'] == 'completed':
            ...         break
        """
        try:
            import websockets
        except ImportError as err:
            raise ImportError(
                "websockets package is required for WebSocket support. "
                "Install it with: pip install cognee-sdk[websocket]"
            ) from err

        # Convert HTTP URL to WebSocket URL
        ws_url = self.api_url.replace("http://", "ws://").replace("https://", "wss://")
        endpoint = f"/api/v1/cognify/subscribe/{pipeline_run_id}"

        # Prepare headers
        headers: dict[str, str] = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        # Connect to WebSocket
        async with websockets.connect(
            f"{ws_url}{endpoint}",
            extra_headers=headers,
        ) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    yield data

                    # Exit when processing is completed
                    if data.get("status") in ("completed", "PipelineRunCompleted"):
                        break
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    raise ServerError(f"WebSocket error: {str(e)}", 500) from e

    # ==================== Advanced Features (P2) ====================

    async def add_batch(
        self,
        data_list: list[str | bytes | Path | BinaryIO],
        dataset_name: str | None = None,
        dataset_id: UUID | None = None,
        node_set: list[str] | None = None,
    ) -> list[AddResult]:
        """
        Add multiple data items in batch.

        Args:
            data_list: List of data items to add
            dataset_name: Name of the dataset
            dataset_id: UUID of the dataset
            node_set: Optional list of node identifiers

        Returns:
            List of AddResult objects

        Example:
            >>> results = await client.add_batch(
            ...     data_list=["text1", "text2", "text3"],
            ...     dataset_name="my-dataset"
            ... )
        """
        tasks = [
            self.add(
                data=item,
                dataset_name=dataset_name,
                dataset_id=dataset_id,
                node_set=node_set,
            )
            for item in data_list
        ]
        return await asyncio.gather(*tasks)
