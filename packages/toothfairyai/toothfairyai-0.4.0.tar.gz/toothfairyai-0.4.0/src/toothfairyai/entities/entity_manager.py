"""Entity manager for handling entity operations."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Entity, EntityType, ListResponse

if TYPE_CHECKING:
    from ..client import ToothFairyClient


class EntityManager:
    """Manager for entity operations.

    This manager provides methods to create, update, and manage entities
    (topics, intents, and NER).

    Example:
        >>> client = ToothFairyClient(api_key="...", workspace_id="...")
        >>> entity = client.entities.create(
        ...     user_id="user-123",
        ...     label="Dental Cleaning",
        ...     entity_type="topic"
        ... )
    """

    def __init__(self, client: "ToothFairyClient"):
        """Initialize the EntityManager.

        Args:
            client: The ToothFairyClient instance.
        """
        self._client = client

    def create(
        self,
        user_id: str,
        label: str,
        entity_type: EntityType = "topic",
        description: Optional[str] = None,
        emoji: Optional[str] = None,
        parent_entity: Optional[str] = None,
        background_color: Optional[str] = None,
    ) -> Entity:
        """Create a new entity.

        Args:
            user_id: User identifier.
            label: Entity label.
            entity_type: Type of entity ("topic", "intent", "ner").
            description: Entity description.
            emoji: Entity emoji.
            parent_entity: Parent entity ID for hierarchical entities.
            background_color: Background color for UI display.

        Returns:
            The created Entity object.
        """
        data: Dict[str, Any] = {
            "createdBy": user_id,
            "label": label,
            "type": entity_type,
        }

        if description is not None:
            data["description"] = description
        if emoji is not None:
            data["emoji"] = emoji
        if parent_entity is not None:
            data["parentEntity"] = parent_entity
        if background_color is not None:
            data["backgroundColor"] = background_color

        response = self._client.request("POST", "/entity/create", data=data)
        return Entity.from_dict(response)

    def get(self, entity_id: str) -> Entity:
        """Get an entity by ID.

        Args:
            entity_id: ID of the entity to retrieve.

        Returns:
            The Entity object.
        """
        response = self._client.request("GET", f"/entity/get/{entity_id}")
        return Entity.from_dict(response)

    def update(
        self,
        entity_id: str,
        label: Optional[str] = None,
        description: Optional[str] = None,
        emoji: Optional[str] = None,
        parent_entity: Optional[str] = None,
        background_color: Optional[str] = None,
    ) -> Entity:
        """Update an entity.

        Args:
            entity_id: ID of the entity to update.
            label: New label.
            description: New description.
            emoji: New emoji.
            parent_entity: New parent entity ID.
            background_color: New background color.

        Returns:
            The updated Entity object.
        """
        data: Dict[str, Any] = {"id": entity_id}

        if label is not None:
            data["label"] = label
        if description is not None:
            data["description"] = description
        if emoji is not None:
            data["emoji"] = emoji
        if parent_entity is not None:
            data["parentEntity"] = parent_entity
        if background_color is not None:
            data["backgroundColor"] = background_color

        response = self._client.request("POST", "/entity/update", data=data)
        return Entity.from_dict(response)

    def delete(self, entity_id: str) -> Dict[str, bool]:
        """Delete an entity.

        Args:
            entity_id: ID of the entity to delete.

        Returns:
            A dictionary with success status.
        """
        self._client.request("DELETE", f"/entity/delete/{entity_id}")
        return {"success": True}

    def list(
        self,
        limit: Optional[int] = None,
        entity_type: Optional[EntityType] = None,
    ) -> ListResponse:
        """List entities.

        Args:
            limit: Maximum number of entities to return.
            entity_type: Filter by entity type.

        Returns:
            A ListResponse containing the entities.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if entity_type is not None:
            params["type"] = entity_type

        response = self._client.request("GET", "/entity/list", params=params)

        items = []
        if isinstance(response, list):
            items = [Entity.from_dict(item) for item in response]
        elif isinstance(response, dict):
            items = [Entity.from_dict(item) for item in response.get("items", [])]

        return ListResponse(items=items)

    def get_by_type(
        self,
        entity_type: EntityType,
        limit: Optional[int] = None,
    ) -> List[Entity]:
        """Get entities by type.

        Args:
            entity_type: Type of entities to retrieve ("topic", "intent", "ner").
            limit: Maximum number of entities to return.

        Returns:
            A list of Entity objects.
        """
        result = self.list(limit=limit, entity_type=entity_type)
        return result.items

    def search(
        self,
        search_term: str,
        entity_type: Optional[EntityType] = None,
    ) -> List[Entity]:
        """Search entities by label.

        Args:
            search_term: Term to search for in entity labels.
            entity_type: Filter by entity type.

        Returns:
            A list of matching Entity objects.
        """
        # Get all entities of the specified type
        all_entities = self.list(entity_type=entity_type)

        # Filter by search term (case-insensitive)
        search_lower = search_term.lower()
        return [
            entity
            for entity in all_entities.items
            if search_lower in entity.label.lower()
        ]
