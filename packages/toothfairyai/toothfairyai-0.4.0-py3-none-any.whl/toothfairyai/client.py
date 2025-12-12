"""Main client for the ToothFairyAI SDK."""

from typing import Any, Dict, Optional

import requests

from .chat.chat_manager import ChatManager
from .documents.document_manager import DocumentManager
from .entities.entity_manager import EntityManager
from .errors import (
    ApiError,
    MissingApiKeyError,
    MissingWorkspaceIdError,
    NetworkError,
    ToothFairyError,
)
from .folders.folder_manager import FolderManager
from .prompts.prompt_manager import PromptManager
from .streaming.streaming_manager import StreamingManager
from .types import ToothFairyClientConfig


class ToothFairyClient:
    """Main client for interacting with the ToothFairyAI API.

    This client provides access to all ToothFairyAI API endpoints through
    specialized managers for different resource types.

    Example:
        >>> client = ToothFairyClient(
        ...     api_key="your-api-key",
        ...     workspace_id="your-workspace-id"
        ... )
        >>> response = client.chat.send_to_agent("Hello", "agent-id")
        >>> print(response.agent_response)
    """

    DEFAULT_BASE_URL = "https://api.toothfairyai.com"
    DEFAULT_AI_URL = "https://ai.toothfairyai.com"
    DEFAULT_AI_STREAM_URL = "https://ais.toothfairyai.com"
    DEFAULT_TIMEOUT = 120  # seconds

    def __init__(
        self,
        api_key: str,
        workspace_id: str,
        base_url: Optional[str] = None,
        ai_url: Optional[str] = None,
        ai_stream_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """Initialize the ToothFairyAI client.

        Args:
            api_key: Your ToothFairyAI API key.
            workspace_id: Your ToothFairyAI workspace ID.
            base_url: Base URL for the API. Defaults to https://api.toothfairyai.com
            ai_url: AI endpoint URL. Defaults to https://ai.toothfairyai.com
            ai_stream_url: Streaming endpoint URL. Defaults to https://ais.toothfairyai.com
            timeout: Request timeout in seconds. Defaults to 120.

        Raises:
            MissingApiKeyError: If api_key is not provided.
            MissingWorkspaceIdError: If workspace_id is not provided.
        """
        if not api_key:
            raise MissingApiKeyError()
        if not workspace_id:
            raise MissingWorkspaceIdError()

        self.config = ToothFairyClientConfig(
            api_key=api_key,
            workspace_id=workspace_id,
            base_url=base_url or self.DEFAULT_BASE_URL,
            ai_url=ai_url or self.DEFAULT_AI_URL,
            ai_stream_url=ai_stream_url or self.DEFAULT_AI_STREAM_URL,
            timeout=timeout or self.DEFAULT_TIMEOUT,
        )

        # Create session with default headers
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "x-api-key": self.config.api_key,
            }
        )

        # Initialize managers
        self.chat = ChatManager(self)
        self.streaming = StreamingManager(self)
        self.documents = DocumentManager(self)
        self.entities = EntityManager(self)
        self.folders = FolderManager(self)
        self.prompts = PromptManager(self)

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make a request to the base API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            endpoint: API endpoint (without base URL).
            data: Request body data (for POST/PUT).
            params: Query parameters (for GET).
            **kwargs: Additional arguments passed to requests.

        Returns:
            The API response data.

        Raises:
            ApiError: If the API returns an error response.
            NetworkError: If a network error occurs.
        """
        url = f"{self.config.base_url}{endpoint}"
        return self._make_request(method, url, data, params, **kwargs)

    def ai_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make a request to the AI API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            endpoint: API endpoint (without base URL).
            data: Request body data (for POST/PUT).
            params: Query parameters (for GET).
            **kwargs: Additional arguments passed to requests.

        Returns:
            The API response data.

        Raises:
            ApiError: If the API returns an error response.
            NetworkError: If a network error occurs.
        """
        url = f"{self.config.ai_url}{endpoint}"
        return self._make_request(method, url, data, params, **kwargs)

    def _make_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make an HTTP request.

        This method handles workspace ID injection and error handling.

        Args:
            method: HTTP method.
            url: Full URL.
            data: Request body data.
            params: Query parameters.
            **kwargs: Additional arguments.

        Returns:
            The API response data.

        Raises:
            ApiError: If the API returns an error response.
            NetworkError: If a network error occurs.
        """
        # Inject workspace ID into request body for POST/PUT
        if method.upper() in ("POST", "PUT", "PATCH") and data is not None:
            data = {**data, "workspaceid": self.config.workspace_id}

        # Inject workspace ID into query params for GET
        if method.upper() == "GET":
            params = params or {}
            params["workspaceid"] = self.config.workspace_id

        try:
            response = self._session.request(
                method=method,
                url=url,
                json=data if method.upper() in ("POST", "PUT", "PATCH") else None,
                params=params,
                timeout=kwargs.pop("timeout", self.config.timeout),
                **kwargs,
            )
            response.raise_for_status()
            return response.json() if response.text else None

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            response_data = None
            try:
                response_data = e.response.json() if e.response else None
            except Exception:
                response_data = e.response.text if e.response else None

            error_message = str(e)
            if response_data and isinstance(response_data, dict):
                error_message = response_data.get("message", str(e))

            raise ApiError(
                message=error_message,
                status_code=status_code,
                response=response_data,
            ) from e

        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {e}") from e

        except requests.exceptions.Timeout as e:
            raise NetworkError(f"Request timeout: {e}") from e

        except requests.exceptions.RequestException as e:
            raise ToothFairyError(f"Request error: {e}") from e

    def get_streaming_url(self) -> str:
        """Get the streaming API URL.

        Returns:
            The streaming API base URL.
        """
        return self.config.ai_stream_url

    def test_connection(self) -> bool:
        """Test the connection to the API.

        Returns:
            True if the connection is successful, False otherwise.
        """
        try:
            self.chat.list(limit=1)
            return True
        except ToothFairyError:
            return False

    def get_health(self) -> Dict[str, str]:
        """Get the API health status.

        Returns:
            A dictionary containing the health status.

        Raises:
            ApiError: If the health check fails.
        """
        url = f"{self.config.base_url}/health"
        try:
            response = self._session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise ApiError(f"Health check failed: {e}") from e
