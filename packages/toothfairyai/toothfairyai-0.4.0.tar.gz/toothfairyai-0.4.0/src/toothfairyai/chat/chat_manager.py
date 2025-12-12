"""Chat manager for handling chat and message operations."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import (
    AgentMessage,
    AgentResponse,
    Attachments,
    Chat,
    ChatCreateData,
    ListResponse,
    Message,
    MessageCreateData,
)

if TYPE_CHECKING:
    from ..client import ToothFairyClient


class ChatManager:
    """Manager for chat and message operations.

    This manager provides methods to create, update, and manage chat conversations,
    as well as send messages to AI agents.

    Example:
        >>> client = ToothFairyClient(api_key="...", workspace_id="...")
        >>> chat = client.chat.create(name="Support Chat", customer_id="cust-123")
        >>> response = client.chat.send_to_agent("Hello", "agent-id", chat_id=chat.id)
    """

    def __init__(self, client: "ToothFairyClient"):
        """Initialize the ChatManager.

        Args:
            client: The ToothFairyClient instance.
        """
        self._client = client

    def create(
        self,
        name: str = "",
        customer_id: str = "",
        customer_info: Optional[Dict[str, Any]] = None,
        primary_role: str = "user",
        external_participant_id: str = "",
        channel_settings: Optional[Dict[str, str]] = None,
    ) -> Chat:
        """Create a new chat.

        Args:
            name: Name of the chat.
            customer_id: Customer identifier.
            customer_info: Additional customer information.
            primary_role: Primary role for the chat (default: "user").
            external_participant_id: External participant identifier.
            channel_settings: Channel configuration.

        Returns:
            The created Chat object.
        """
        data = {
            "name": name,
            "customerId": customer_id,
            "customerInfo": customer_info or {},
            "primaryRole": primary_role,
            "externalParticipantId": external_participant_id,
        }
        if channel_settings:
            data["channelSettings"] = channel_settings

        response = self._client.request("POST", "/chat/create", data=data)
        return Chat.from_dict(response)

    def update(
        self,
        chat_id: str,
        name: Optional[str] = None,
        customer_id: Optional[str] = None,
        customer_info: Optional[Dict[str, Any]] = None,
        primary_role: Optional[str] = None,
        external_participant_id: Optional[str] = None,
        channel_settings: Optional[Dict[str, str]] = None,
    ) -> Chat:
        """Update an existing chat.

        Args:
            chat_id: ID of the chat to update.
            name: New name for the chat.
            customer_id: New customer identifier.
            customer_info: New customer information.
            primary_role: New primary role.
            external_participant_id: New external participant identifier.
            channel_settings: New channel configuration.

        Returns:
            The updated Chat object.
        """
        data: Dict[str, Any] = {"id": chat_id}

        if name is not None:
            data["name"] = name
        if customer_id is not None:
            data["customerId"] = customer_id
        if customer_info is not None:
            data["customerInfo"] = customer_info
        if primary_role is not None:
            data["primaryRole"] = primary_role
        if external_participant_id is not None:
            data["externalParticipantId"] = external_participant_id
        if channel_settings is not None:
            data["channelSettings"] = channel_settings

        response = self._client.request("POST", "/chat/update", data=data)
        return Chat.from_dict(response)

    def get(self, chat_id: str) -> Chat:
        """Get a chat by ID.

        Args:
            chat_id: ID of the chat to retrieve.

        Returns:
            The Chat object.
        """
        response = self._client.request("GET", f"/chat/get/{chat_id}")
        return Chat.from_dict(response)

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> ListResponse:
        """List all chats.

        Args:
            limit: Maximum number of chats to return.
            offset: Number of chats to skip.

        Returns:
            A ListResponse containing the chats.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client.request("GET", "/chat/list", params=params)

        items = []
        if isinstance(response, list):
            items = [Chat.from_dict(item) for item in response]
        elif isinstance(response, dict):
            items = [Chat.from_dict(item) for item in response.get("items", [])]

        return ListResponse(items=items)

    def delete(self, chat_id: str) -> Dict[str, bool]:
        """Delete a chat.

        Args:
            chat_id: ID of the chat to delete.

        Returns:
            A dictionary with success status.
        """
        self._client.request("DELETE", f"/chat/delete/{chat_id}")
        return {"success": True}

    def create_message(
        self,
        chat_id: str,
        text: str,
        role: str = "user",
        user_id: str = "",
        images: Optional[List[str]] = None,
        audios: Optional[List[str]] = None,
        videos: Optional[List[str]] = None,
        files: Optional[List[str]] = None,
    ) -> Message:
        """Create a message in a chat.

        Args:
            chat_id: ID of the chat.
            text: Message text content.
            role: Message role ("user", "assistant", "system").
            user_id: User identifier.
            images: List of image URLs.
            audios: List of audio URLs.
            videos: List of video URLs.
            files: List of file URLs.

        Returns:
            The created Message object.
        """
        data = {
            "chatID": chat_id,
            "text": text,
            "role": role,
            "userID": user_id,
            "images": images or [],
            "audios": audios or [],
            "videos": videos or [],
            "files": files or [],
        }

        response = self._client.request("POST", "/chat_message/create", data=data)
        return Message.from_dict(response)

    def get_message(self, message_id: str) -> Message:
        """Get a message by ID.

        Args:
            message_id: ID of the message to retrieve.

        Returns:
            The Message object.
        """
        response = self._client.request("GET", f"/chat_message/get/{message_id}")
        return Message.from_dict(response)

    def send_to_agent(
        self,
        message: str,
        agent_id: str,
        chat_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        customer_id: Optional[str] = None,
        provider_id: Optional[str] = None,
        customer_info: Optional[Dict[str, Any]] = None,
        attachments: Optional[Attachments] = None,
    ) -> AgentResponse:
        """Send a message to an AI agent.

        This method sends a message to an agent and returns the response.
        If no chat_id is provided, a new chat will be created automatically.

        Args:
            message: The message text to send.
            agent_id: ID of the agent to send the message to.
            chat_id: ID of an existing chat (optional, will create new if not provided).
            phone_number: Phone number for the conversation.
            customer_id: Customer identifier.
            provider_id: Provider identifier.
            customer_info: Additional customer information.
            attachments: Attachments to include with the message.

        Returns:
            The AgentResponse containing the agent's reply.

        Example:
            >>> response = client.chat.send_to_agent(
            ...     message="Hello, how can you help?",
            ...     agent_id="agent-123",
            ...     attachments={"images": ["https://example.com/image.jpg"]}
            ... )
            >>> print(response.agent_response)
        """
        # Build the message object
        agent_message = AgentMessage(role="user", content=message)

        # Add attachments to content if provided
        if attachments:
            content_parts = [message]
            for key, urls in attachments.items():
                if urls:
                    for url in urls:
                        content_parts.append(f"[{key}:{url}]")
            agent_message = AgentMessage(role="user", content="\n".join(content_parts))

        data: Dict[str, Any] = {
            "messages": [{"role": agent_message.role, "content": agent_message.content}],
            "agentid": agent_id,
            "raw_stream": False,
        }

        if chat_id:
            data["chatid"] = chat_id
        if phone_number:
            data["phoneNumber"] = phone_number
        if customer_id:
            data["customerId"] = customer_id
        if provider_id:
            data["providerId"] = provider_id
        if customer_info:
            data["customerInfo"] = customer_info

        response = self._client.ai_request("POST", "/chatter", data=data)
        return AgentResponse.from_dict(response)
