"""Streaming manager for real-time AI responses."""

import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Generator, Iterator, List, Optional

import requests

from ..errors import StreamError


if TYPE_CHECKING:
    from ..client import ToothFairyClient


#
@dataclass
class StreamEvent:
    """A single event from the stream.

    Attributes:
        event_type: Type of event (token, message, status, progress, complete, error, etc.)
        data: The event data/payload
        text: Extracted text content (convenience attribute for token/message events)
        chat_id: Chat ID if available
        message_id: Message ID if available
    """

    event_type: str
    data: Dict[str, Any] = field(default_factory=dict)
    text: str = ""
    chat_id: Optional[str] = None
    message_id: Optional[str] = None

    @property
    def is_token(self) -> bool:
        """Check if this is a token event."""
        return self.event_type == "token"

    @property
    def is_complete(self) -> bool:
        """Check if this is a completion event."""
        return self.event_type in ("complete", "fulfilled", "done")

    @property
    def is_error(self) -> bool:
        """Check if this is an error event."""
        return self.event_type == "error"


class StreamResponse:
    """An iterable stream response from the AI agent.

    This class allows you to iterate over streaming events similar to OpenAI's API.

    Example:
        >>> stream = client.streaming.send_to_agent("Hello", "agent-id")
        >>> for event in stream:
        ...     if event.text:
        ...         print(event.text, end="", flush=True)
        >>> print(f"\\nChat ID: {stream.chat_id}")
    """

    def __init__(
        self,
        response: requests.Response,
        raw_stream: bool = True,
    ):
        """Initialize the stream response.

        Args:
            response: The requests Response object with streaming enabled.
            raw_stream: Whether raw token streaming is enabled.
        """
        self._response = response
        self._raw_stream = raw_stream
        self._chat_id: Optional[str] = None
        self._message_id: Optional[str] = None
        self._accumulated_text: str = ""
        self._consumed: bool = False

    @property
    def chat_id(self) -> Optional[str]:
        """Get the chat ID (available after iteration)."""
        return self._chat_id

    @property
    def message_id(self) -> Optional[str]:
        """Get the message ID (available after iteration)."""
        return self._message_id

    @property
    def text(self) -> str:
        """Get the accumulated text (available after iteration)."""
        return self._accumulated_text

    def __iter__(self) -> Iterator[StreamEvent]:
        """Iterate over stream events."""
        if self._consumed:
            raise RuntimeError("Stream has already been consumed")
        self._consumed = True
        return self._iterate_events()

    def _iterate_events(self) -> Generator[StreamEvent, None, None]:
        """Generator that yields stream events."""
        buffer = ""

        try:
            for chunk in self._response.iter_content(chunk_size=None, decode_unicode=True):
                if not chunk:
                    continue

                buffer += chunk
                lines = buffer.split("\n")
                buffer = lines[-1]  # Keep incomplete line in buffer

                for line in lines[:-1]:
                    event = self._process_sse_line(line)
                    if event:
                        yield event

            # Process any remaining buffer
            if buffer:
                event = self._process_sse_line(buffer)
                if event:
                    yield event

            # Yield final done event
            yield StreamEvent(
                event_type="done",
                data={"status": "complete"},
                chat_id=self._chat_id,
                message_id=self._message_id,
            )

        except requests.exceptions.RequestException as e:
            yield StreamEvent(
                event_type="error",
                data={"message": str(e), "code": "STREAM_ERROR"},
            )

    def _process_sse_line(self, line: str) -> Optional[StreamEvent]:
        """Process a single SSE line and return an event if applicable."""
        line = line.strip()
        if not line or line.startswith(":"):
            return None

        if not line.startswith("data:"):
            return None

        data_str = line[5:].strip()
        if not data_str:
            return None

        try:
            data = json.loads(data_str)
            return self._create_event(data)
        except json.JSONDecodeError:
            # Handle plain text data
            if data_str:
                self._accumulated_text += data_str
                return StreamEvent(
                    event_type="token",
                    data={"chunk": data_str},
                    text=data_str,
                    chat_id=self._chat_id,
                    message_id=self._message_id,
                )
            return None

    def _create_event(self, data: Dict[str, Any]) -> StreamEvent:
        """Create a StreamEvent from parsed SSE data."""
        # Extract IDs
        if "chatId" in data:
            self._chat_id = data["chatId"]
        if "message_id" in data:
            self._message_id = data["message_id"]
        if "messageId" in data:
            self._message_id = data["messageId"]

        event_type = data.get("type", "")
        status = data.get("status", "")
        text = ""

        # Determine event type and extract text
        if event_type == "token":
            chunk = data.get("chunk", "")
            if chunk:
                self._accumulated_text += chunk
                text = chunk
            return StreamEvent(
                event_type="token",
                data=data,
                text=text,
                chat_id=self._chat_id,
                message_id=data.get("message_id"),
            )

        elif event_type == "message":
            text = data.get("text", "")
            return StreamEvent(
                event_type="message",
                data=data,
                text=text,
                chat_id=data.get("chatId"),
                message_id=data.get("message_id"),
            )

        elif status == "inProgress":
            return StreamEvent(
                event_type="progress",
                data=data,
                chat_id=self._chat_id,
                message_id=self._message_id,
            )

        elif status in ("complete", "fulfilled"):
            return StreamEvent(
                event_type="complete",
                data=data,
                chat_id=self._chat_id,
                message_id=self._message_id,
            )

        elif status == "connected":
            return StreamEvent(
                event_type="connected",
                data=data,
                chat_id=self._chat_id,
                message_id=self._message_id,
            )

        elif "error" in data:
            return StreamEvent(
                event_type="error",
                data=data,
                chat_id=self._chat_id,
                message_id=self._message_id,
            )

        elif "callback" in data or event_type == "callback":
            return StreamEvent(
                event_type="callback",
                data=data,
                chat_id=self._chat_id,
                message_id=self._message_id,
            )

        elif "metadata" in data:
            return StreamEvent(
                event_type="metadata",
                data=data.get("metadata", {}),
                chat_id=self._chat_id,
                message_id=self._message_id,
            )

        else:
            return StreamEvent(
                event_type="unknown",
                data=data,
                chat_id=self._chat_id,
                message_id=self._message_id,
            )

    def collect(self) -> str:
        """Consume all events and return the accumulated text.

        This is a convenience method that iterates through all events
        and returns the final text.

        Returns:
            The complete accumulated text from all token/message events.
        """
        for _ in self:
            pass
        return self._accumulated_text


# Type alias for attachments
Attachments = Dict[str, List[str]]


class StreamingManager:
    """Manager for streaming AI responses.

    This manager provides methods to stream responses from AI agents
    using an iterator pattern similar to OpenAI's Python SDK.

    Example:
        >>> stream = client.streaming.send_to_agent("Hello", "agent-id")
        >>> for event in stream:
        ...     if event.text:
        ...         print(event.text, end="", flush=True)
        >>> print()
        >>> print(f"Chat ID: {stream.chat_id}")
    """

    STREAMING_TIMEOUT = 300  # 5 minutes

    def __init__(self, client: "ToothFairyClient"):
        """Initialize the StreamingManager.

        Args:
            client: The ToothFairyClient instance.
        """
        self._client = client

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
        raw_stream: bool = True,
    ) -> StreamResponse:
        """Send a message to an agent and receive a streaming response.

        Args:
            message: The message text to send.
            agent_id: ID of the agent to send the message to.
            chat_id: ID of an existing chat (optional).
            phone_number: Phone number for the conversation.
            customer_id: Customer identifier.
            provider_id: Provider identifier.
            customer_info: Additional customer information.
            attachments: Attachments to include with the message.
            raw_stream: Enable token-by-token streaming (default: True).

        Returns:
            A StreamResponse that can be iterated over to receive events.

        Example:
            >>> # Simple iteration - like OpenAI
            >>> stream = client.streaming.send_to_agent("Hello", "agent-id")
            >>> for event in stream:
            ...     print(event.text, end="", flush=True)
            >>> print()

            >>> # Access metadata after streaming
            >>> print(f"Chat: {stream.chat_id}")
            >>> print(f"Message: {stream.message_id}")

            >>> # Collect all text at once
            >>> stream = client.streaming.send_to_agent("Hello", "agent-id")
            >>> full_response = stream.collect()
            >>> print(full_response)

            >>> # Filter by event type
            >>> stream = client.streaming.send_to_agent("Hello", "agent-id")
            >>> for event in stream:
            ...     if event.is_token:
            ...         print(event.text, end="")
            ...     elif event.is_error:
            ...         print(f"Error: {event.data}")
        """
        url = f"{self._client.get_streaming_url()}/agent"

        # Build request data
        content = message
        if attachments:
            content_parts = [message]
            for key, urls in attachments.items():
                if urls:
                    for attachment_url in urls:
                        content_parts.append(f"[{key}:{attachment_url}]")
            content = "\n".join(content_parts)

        data: Dict[str, Any] = {
            "messages": [{"role": "user", "content": content}],
            "agentid": agent_id,
            "raw_stream": raw_stream,
            "workspaceid": self._client.config.workspace_id,
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

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self._client.config.api_key,
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache",
        }

        response = requests.post(
            url,
            json=data,
            headers=headers,
            stream=True,
            timeout=self.STREAMING_TIMEOUT,
        )
        response.raise_for_status()

        return StreamResponse(response, raw_stream=raw_stream)
