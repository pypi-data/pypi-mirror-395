"""Document manager for handling document operations."""

import base64
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

import requests

from ..errors import FileSizeError, ToothFairyError, ValidationError
from ..types import (
    Document,
    DocumentUpdateData,
    FileDownloadResult,
    FileUploadResult,
    ListResponse,
    get_content_type,
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
)

if TYPE_CHECKING:
    from ..client import ToothFairyClient


class DocumentManager:
    """Manager for document operations.

    This manager provides methods to upload, download, search, and manage documents.

    Example:
        >>> client = ToothFairyClient(api_key="...", workspace_id="...")
        >>> result = client.documents.upload("./document.pdf")
        >>> print(f"Uploaded: {result.filename}")
    """

    def __init__(self, client: "ToothFairyClient"):
        """Initialize the DocumentManager.

        Args:
            client: The ToothFairyClient instance.
        """
        self._client = client

    def create(
        self,
        user_id: str,
        title: str,
        doc_type: str = "readComprehensionFile",
        topics: Optional[List[str]] = None,
        folder_id: str = "mrcRoot",
        external_path: str = "",
        source: str = "",
        status: str = "published",
        scope: Optional[str] = None,
    ) -> Document:
        """Create a document record.

        Args:
            user_id: User identifier.
            title: Document title.
            doc_type: Document type (readComprehensionUrl, readComprehensionPdf, readComprehensionFile).
            topics: List of topic IDs.
            folder_id: Folder ID to place the document in.
            external_path: External path/URL of the document.
            source: Source of the document.
            status: Document status (default: "published").
            scope: Document scope.

        Returns:
            The created Document object.
        """
        data = {
            "data": [{
                "userid": user_id,
                "title": title,
                "type": doc_type,
                "topics": topics or [],
                "folderid": folder_id,
                "external_path": external_path,
                "source": source,
                "status": status,
            }]
        }
        if scope:
            data["data"][0]["scope"] = scope

        response = self._client.request("POST", "/doc/create", data=data)

        # Handle array response
        if isinstance(response, list) and len(response) > 0:
            return Document.from_dict(response[0])
        return Document.from_dict(response)

    def create_from_path(
        self,
        file_path: str,
        user_id: str,
        title: Optional[str] = None,
        folder_id: str = "mrcRoot",
        topics: Optional[List[str]] = None,
        status: str = "published",
        scope: Optional[str] = None,
    ) -> Document:
        """Create a document from a file path or URL.

        Args:
            file_path: Local file path or URL.
            user_id: User identifier.
            title: Document title (defaults to filename).
            folder_id: Folder ID to place the document in.
            topics: List of topic IDs.
            status: Document status.
            scope: Document scope.

        Returns:
            The created Document object.
        """
        # Determine document type based on path
        if file_path.startswith(("http://", "https://")):
            doc_type = "readComprehensionUrl"
            doc_title = title or file_path.split("/")[-1]
        elif file_path.lower().endswith(".pdf"):
            doc_type = "readComprehensionPdf"
            doc_title = title or os.path.basename(file_path)
        else:
            doc_type = "readComprehensionFile"
            doc_title = title or os.path.basename(file_path)

        return self.create(
            user_id=user_id,
            title=doc_title,
            doc_type=doc_type,
            topics=topics,
            folder_id=folder_id,
            external_path=file_path,
            status=status,
            scope=scope,
        )

    def get(self, document_id: str) -> Document:
        """Get a document by ID.

        Args:
            document_id: ID of the document to retrieve.

        Returns:
            The Document object.
        """
        response = self._client.request("GET", f"/doc/get/{document_id}")
        return Document.from_dict(response)

    def update(
        self,
        document_id: str,
        user_id: str,
        title: Optional[str] = None,
        topics: Optional[List[str]] = None,
        folder_id: Optional[str] = None,
        status: Optional[str] = None,
        scope: Optional[str] = None,
    ) -> Document:
        """Update a document.

        Args:
            document_id: ID of the document to update.
            user_id: User identifier.
            title: New title.
            topics: New topics list.
            folder_id: New folder ID.
            status: New status.
            scope: New scope.

        Returns:
            The updated Document object.
        """
        fields: Dict[str, Any] = {}
        if title is not None:
            fields["title"] = title
        if topics is not None:
            fields["topics"] = topics
        if folder_id is not None:
            fields["folderid"] = folder_id
        if status is not None:
            fields["status"] = status
        if scope is not None:
            fields["scope"] = scope

        data = {
            "id": document_id,
            "userid": user_id,
            "fields": fields,
        }

        response = self._client.request("POST", "/doc/update", data=data)
        return Document.from_dict(response)

    def delete(self, document_id: str) -> Dict[str, bool]:
        """Delete a document.

        Args:
            document_id: ID of the document to delete.

        Returns:
            A dictionary with success status.
        """
        self._client.request("DELETE", f"/doc/delete/{document_id}")
        return {"success": True}

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        folder_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> ListResponse:
        """List documents.

        Args:
            limit: Maximum number of documents to return.
            offset: Number of documents to skip.
            folder_id: Filter by folder ID.
            status: Filter by status.

        Returns:
            A ListResponse containing the documents.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if folder_id is not None:
            params["folderid"] = folder_id
        if status is not None:
            params["status"] = status

        response = self._client.request("GET", "/doc/list", params=params)

        items = []
        if isinstance(response, list):
            items = [Document.from_dict(item) for item in response]
        elif isinstance(response, dict):
            items = [Document.from_dict(item) for item in response.get("items", [])]

        return ListResponse(items=items)

    def search(
        self,
        text: str,
        top_k: int = 10,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Search documents using semantic search.

        Args:
            text: Search query text.
            top_k: Number of results to return (1-50, default: 10).
            metadata: Additional metadata filters.

        Returns:
            A list of search results.
        """
        if not 1 <= top_k <= 50:
            raise ValidationError("top_k must be between 1 and 50")

        data = {
            "text": text,
            "topK": top_k,
        }
        if metadata:
            data["metadata"] = metadata

        response = self._client.ai_request("POST", "/searcher", data=data)
        return response if isinstance(response, list) else response.get("results", [])

    def upload(
        self,
        file_path: str,
        folder_id: str = "mrcRoot",
        on_progress: Optional[Callable[[int, int, int], None]] = None,
    ) -> FileUploadResult:
        """Upload a file.

        Args:
            file_path: Path to the file to upload.
            folder_id: Folder ID to upload to.
            on_progress: Progress callback (percent, loaded, total).

        Returns:
            FileUploadResult with upload details.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            FileSizeError: If the file exceeds the size limit.
        """
        path = Path(file_path)
        if not path.exists():
            raise ToothFairyError(f"File not found: {file_path}", code="FILE_NOT_FOUND")

        file_size = path.stat().st_size
        if file_size > MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            raise FileSizeError(path.name, size_mb, MAX_FILE_SIZE_MB)

        # Get content type
        content_type = get_content_type(path.name)

        # Sanitize filename
        sanitized_name = self._sanitize_filename(path.name)

        # Get pre-signed URL
        presigned_response = self._client.request(
            "GET",
            "/documents/requestPreSignedURL",
            params={"filename": sanitized_name},
        )

        upload_url = presigned_response.get("url")
        final_filename = presigned_response.get("filename", sanitized_name)

        if not upload_url:
            raise ToothFairyError("Failed to get pre-signed URL", code="UPLOAD_ERROR")

        # Upload file to S3
        with open(file_path, "rb") as f:
            file_data = f.read()

        headers = {"Content-Type": content_type}

        response = requests.put(
            upload_url,
            data=file_data,
            headers=headers,
            timeout=self._client.config.timeout,
        )
        response.raise_for_status()

        if on_progress:
            on_progress(100, file_size, file_size)

        return FileUploadResult(
            success=True,
            original_filename=path.name,
            sanitized_filename=sanitized_name,
            filename=final_filename,
            import_type="file",
            content_type=content_type,
            size=file_size,
            size_in_mb=file_size / (1024 * 1024),
        )

    def upload_from_base64(
        self,
        base64_data: str,
        filename: str,
        content_type: str,
        folder_id: str = "mrcRoot",
        on_progress: Optional[Callable[[int, int, int], None]] = None,
    ) -> FileUploadResult:
        """Upload a file from base64 data.

        Args:
            base64_data: Base64-encoded file data.
            filename: Name for the file.
            content_type: MIME type of the file.
            folder_id: Folder ID to upload to.
            on_progress: Progress callback (percent, loaded, total).

        Returns:
            FileUploadResult with upload details.

        Raises:
            FileSizeError: If the file exceeds the size limit.
        """
        # Decode base64 to get actual size
        try:
            file_data = base64.b64decode(base64_data)
        except Exception as e:
            raise ValidationError(f"Invalid base64 data: {e}") from e

        file_size = len(file_data)
        if file_size > MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            raise FileSizeError(filename, size_mb, MAX_FILE_SIZE_MB)

        # Sanitize filename
        sanitized_name = self._sanitize_filename(filename)

        # Get pre-signed URL
        presigned_response = self._client.request(
            "GET",
            "/documents/requestPreSignedURL",
            params={"filename": sanitized_name},
        )

        upload_url = presigned_response.get("url")
        final_filename = presigned_response.get("filename", sanitized_name)

        if not upload_url:
            raise ToothFairyError("Failed to get pre-signed URL", code="UPLOAD_ERROR")

        # Upload to S3
        headers = {"Content-Type": content_type}

        response = requests.put(
            upload_url,
            data=file_data,
            headers=headers,
            timeout=self._client.config.timeout,
        )
        response.raise_for_status()

        if on_progress:
            on_progress(100, file_size, file_size)

        return FileUploadResult(
            success=True,
            original_filename=filename,
            sanitized_filename=sanitized_name,
            filename=final_filename,
            import_type="base64",
            content_type=content_type,
            size=file_size,
            size_in_mb=file_size / (1024 * 1024),
        )

    def download(
        self,
        filename: str,
        output_path: str,
        context: str = "documents",
        on_progress: Optional[Callable[[int, int, int], None]] = None,
    ) -> FileDownloadResult:
        """Download a file.

        Args:
            filename: Name of the file to download.
            output_path: Path to save the downloaded file.
            context: Download context (default: "documents").
            on_progress: Progress callback (percent, loaded, total).

        Returns:
            FileDownloadResult with download details.
        """
        # Get download URL
        download_response = self._client.request(
            "GET",
            "/documents/requestDownloadURLIncognito",
            params={"filename": filename, "context": context},
        )

        download_url = download_response.get("url")
        if not download_url:
            raise ToothFairyError("Failed to get download URL", code="DOWNLOAD_ERROR")

        # Download file
        response = requests.get(
            download_url,
            stream=True,
            timeout=self._client.config.timeout,
        )
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if on_progress and total_size > 0:
                        percent = int((downloaded / total_size) * 100)
                        on_progress(percent, downloaded, total_size)

        return FileDownloadResult(
            success=True,
            filename=filename,
            output_path=output_path,
            size=downloaded,
        )

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize a filename for upload.

        Args:
            filename: Original filename.

        Returns:
            Sanitized filename.
        """
        # Replace spaces and special characters
        import re

        sanitized = re.sub(r"[^\w\-_\.]", "_", filename)
        # Remove multiple underscores
        sanitized = re.sub(r"_+", "_", sanitized)
        return sanitized
