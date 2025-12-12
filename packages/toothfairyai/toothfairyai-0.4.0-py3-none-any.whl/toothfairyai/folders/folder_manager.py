"""Folder manager for handling folder operations."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Folder, FolderTreeNode, ListResponse

if TYPE_CHECKING:
    from ..client import ToothFairyClient


class FolderManager:
    """Manager for folder operations.

    This manager provides methods to create, update, and manage folders
    including hierarchical operations.

    Example:
        >>> client = ToothFairyClient(api_key="...", workspace_id="...")
        >>> folder = client.folders.create(
        ...     user_id="user-123",
        ...     name="Documents"
        ... )
    """

    def __init__(self, client: "ToothFairyClient"):
        """Initialize the FolderManager.

        Args:
            client: The ToothFairyClient instance.
        """
        self._client = client

    def create(
        self,
        user_id: str,
        name: str,
        description: Optional[str] = None,
        emoji: Optional[str] = None,
        status: str = "active",
        parent: Optional[str] = None,
    ) -> Folder:
        """Create a new folder.

        Args:
            user_id: User identifier.
            name: Folder name.
            description: Folder description.
            emoji: Folder emoji.
            status: Folder status (default: "active").
            parent: Parent folder ID for subfolders.

        Returns:
            The created Folder object.
        """
        data: Dict[str, Any] = {
            "createdBy": user_id,
            "name": name,
            "status": status,
        }

        if description is not None:
            data["description"] = description
        if emoji is not None:
            data["emoji"] = emoji
        if parent is not None:
            data["parent"] = parent

        response = self._client.request("POST", "/folder/create", data=data)
        return Folder.from_dict(response)

    def get(self, folder_id: str) -> Folder:
        """Get a folder by ID.

        Args:
            folder_id: ID of the folder to retrieve.

        Returns:
            The Folder object.
        """
        response = self._client.request("GET", f"/folder/get/{folder_id}")
        return Folder.from_dict(response)

    def update(
        self,
        folder_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        emoji: Optional[str] = None,
        status: Optional[str] = None,
        parent: Optional[str] = None,
    ) -> Folder:
        """Update a folder.

        Args:
            folder_id: ID of the folder to update.
            name: New name.
            description: New description.
            emoji: New emoji.
            status: New status.
            parent: New parent folder ID.

        Returns:
            The updated Folder object.
        """
        data: Dict[str, Any] = {"id": folder_id}

        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if emoji is not None:
            data["emoji"] = emoji
        if status is not None:
            data["status"] = status
        if parent is not None:
            data["parent"] = parent

        response = self._client.request("POST", "/folder/update", data=data)
        return Folder.from_dict(response)

    def delete(self, folder_id: str) -> Dict[str, bool]:
        """Delete a folder.

        Args:
            folder_id: ID of the folder to delete.

        Returns:
            A dictionary with success status.
        """
        self._client.request("DELETE", f"/folder/delete/{folder_id}")
        return {"success": True}

    def list(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> ListResponse:
        """List folders.

        Args:
            status: Filter by status.
            limit: Maximum number of folders to return.
            offset: Number of folders to skip.

        Returns:
            A ListResponse containing the folders.
        """
        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client.request("GET", "/folder/list", params=params)

        items = []
        if isinstance(response, list):
            items = [Folder.from_dict(item) for item in response]
        elif isinstance(response, dict):
            items = [Folder.from_dict(item) for item in response.get("items", [])]

        return ListResponse(items=items)

    def get_root_folders(self) -> List[Folder]:
        """Get all root folders (folders without a parent).

        Returns:
            A list of root Folder objects.
        """
        all_folders = self.list()
        return [folder for folder in all_folders.items if not folder.parent]

    def get_subfolders(self, parent_id: str) -> List[Folder]:
        """Get all subfolders of a parent folder.

        Args:
            parent_id: ID of the parent folder.

        Returns:
            A list of child Folder objects.
        """
        all_folders = self.list()
        return [folder for folder in all_folders.items if folder.parent == parent_id]

    def get_tree(self) -> List[FolderTreeNode]:
        """Get the folder hierarchy as a tree structure.

        Returns:
            A list of root FolderTreeNode objects with nested children.
        """
        all_folders = self.list()

        # Build a map of folder ID to folder
        folder_map: Dict[str, Folder] = {folder.id: folder for folder in all_folders.items}

        # Build a map of parent ID to children
        children_map: Dict[str, List[Folder]] = {}
        root_folders: List[Folder] = []

        for folder in all_folders.items:
            if folder.parent:
                if folder.parent not in children_map:
                    children_map[folder.parent] = []
                children_map[folder.parent].append(folder)
            else:
                root_folders.append(folder)

        def build_tree_node(folder: Folder) -> FolderTreeNode:
            """Recursively build a tree node."""
            children = children_map.get(folder.id, [])
            child_nodes = [build_tree_node(child) for child in children]
            return FolderTreeNode.from_folder(folder, child_nodes)

        return [build_tree_node(folder) for folder in root_folders]

    def search(self, search_term: str) -> List[Folder]:
        """Search folders by name.

        Args:
            search_term: Term to search for in folder names.

        Returns:
            A list of matching Folder objects.
        """
        all_folders = self.list()
        search_lower = search_term.lower()
        return [
            folder
            for folder in all_folders.items
            if search_lower in folder.name.lower()
        ]
