"""Type definitions for the ToothFairyAI SDK."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union


# Type aliases.
EntityType = Literal["intent", "ner", "topic"]
DocumentType = Literal["readComprehensionUrl", "readComprehensionPdf", "readComprehensionFile"]
MessageRole = Literal["user", "assistant", "system"]


# Configuration types
@dataclass
class ToothFairyClientConfig:
    """Configuration for the ToothFairyClient."""

    api_key: str
    workspace_id: str
    base_url: str = "https://api.toothfairyai.com"
    ai_url: str = "https://ai.toothfairyai.com"
    ai_stream_url: str = "https://ais.toothfairyai.com"
    timeout: int = 120  # seconds


# Chat types
@dataclass
class ChannelSettings:
    """Channel settings for a chat."""

    channel: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class Chat:
    """Represents a chat conversation."""

    id: str
    name: str = ""
    primary_role: str = ""
    external_participant_id: str = ""
    channel_settings: Optional[ChannelSettings] = None
    customer_id: str = ""
    customer_info: Dict[str, Any] = field(default_factory=dict)
    is_ai_replying: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chat":
        """Create a Chat instance from a dictionary."""
        channel_settings = None
        if data.get("channelSettings"):
            channel_settings = ChannelSettings(
                channel=data["channelSettings"].get("channel"),
                provider=data["channelSettings"].get("provider"),
            )
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            primary_role=data.get("primaryRole", ""),
            external_participant_id=data.get("externalParticipantId", ""),
            channel_settings=channel_settings,
            customer_id=data.get("customerId", ""),
            customer_info=data.get("customerInfo", {}),
            is_ai_replying=data.get("isAIReplying", False),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
        )


@dataclass
class ChatCreateData:
    """Data for creating a chat."""

    name: str = ""
    customer_id: str = ""
    customer_info: Dict[str, Any] = field(default_factory=dict)
    primary_role: str = "user"
    external_participant_id: str = ""
    channel_settings: Optional[Dict[str, str]] = None


@dataclass
class Message:
    """Represents a chat message."""

    id: str
    chat_id: str
    text: str
    role: MessageRole
    user_id: str = ""
    images: List[str] = field(default_factory=list)
    audios: List[str] = field(default_factory=list)
    videos: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create a Message instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            chat_id=data.get("chatID", ""),
            text=data.get("text", ""),
            role=data.get("role", "user"),
            user_id=data.get("userID", ""),
            images=data.get("images", []),
            audios=data.get("audios", []),
            videos=data.get("videos", []),
            files=data.get("files", []),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
        )


@dataclass
class MessageCreateData:
    """Data for creating a message."""

    chat_id: str
    text: str
    role: MessageRole = "user"
    user_id: str = ""
    images: List[str] = field(default_factory=list)
    audios: List[str] = field(default_factory=list)
    videos: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)


class Attachments(TypedDict, total=False):
    """Attachments for agent messages."""

    images: List[str]
    audios: List[str]
    videos: List[str]
    files: List[str]


@dataclass
class AgentMessage:
    """Message to send to an agent."""

    role: MessageRole
    content: str


@dataclass
class AgentRequest:
    """Request to send to an agent."""

    messages: List[AgentMessage]
    agentid: str
    chatid: Optional[str] = None
    raw_stream: bool = False
    phone_number: Optional[str] = None
    customer_id: Optional[str] = None
    provider_id: Optional[str] = None
    customer_info: Optional[Dict[str, Any]] = None


@dataclass
class AgentResponse:
    """Response from an agent."""

    chat_id: str
    message_id: str
    agent_response: Any

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentResponse":
        """Create an AgentResponse instance from a dictionary."""
        return cls(
            chat_id=data.get("chatId", ""),
            message_id=data.get("messageId", ""),
            agent_response=data.get("agentResponse"),
        )


# Document types
@dataclass
class Document:
    """Represents a document."""

    id: str
    workspace_id: str = ""
    user_id: str = ""
    doc_type: DocumentType = "readComprehensionFile"
    title: str = ""
    topics: List[str] = field(default_factory=list)
    folder_id: str = ""
    external_path: str = ""
    source: str = ""
    status: str = ""
    scope: Optional[str] = None
    rawtext: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create a Document instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            workspace_id=data.get("workspaceid", ""),
            user_id=data.get("userid", ""),
            doc_type=data.get("type", "readComprehensionFile"),
            title=data.get("title", ""),
            topics=data.get("topics", []),
            folder_id=data.get("folderid", ""),
            external_path=data.get("external_path", ""),
            source=data.get("source", ""),
            status=data.get("status", ""),
            scope=data.get("scope"),
            rawtext=data.get("rawtext"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
        )


@dataclass
class DocumentCreateData:
    """Data for creating a document."""

    user_id: str
    title: str
    doc_type: DocumentType = "readComprehensionFile"
    topics: List[str] = field(default_factory=list)
    folder_id: str = "mrcRoot"
    external_path: str = ""
    source: str = ""
    status: str = "published"
    scope: Optional[str] = None


@dataclass
class DocumentUpdateData:
    """Data for updating a document."""

    title: Optional[str] = None
    topics: Optional[List[str]] = None
    folder_id: Optional[str] = None
    status: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class FileUploadOptions:
    """Options for file upload."""

    folder_id: str = "mrcRoot"
    on_progress: Optional[Callable[[int, int, int], None]] = None


@dataclass
class Base64FileUploadOptions:
    """Options for base64 file upload."""

    filename: str
    content_type: str
    folder_id: str = "mrcRoot"
    on_progress: Optional[Callable[[int, int, int], None]] = None


@dataclass
class FileUploadResult:
    """Result of a file upload."""

    success: bool
    original_filename: str
    sanitized_filename: str
    filename: str
    import_type: str
    content_type: str
    size: int
    size_in_mb: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileUploadResult":
        """Create a FileUploadResult instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            original_filename=data.get("originalFilename", ""),
            sanitized_filename=data.get("sanitizedFilename", ""),
            filename=data.get("filename", ""),
            import_type=data.get("importType", ""),
            content_type=data.get("contentType", ""),
            size=data.get("size", 0),
            size_in_mb=data.get("sizeInMB", 0.0),
        )


@dataclass
class FileDownloadOptions:
    """Options for file download."""

    context: str = "documents"
    on_progress: Optional[Callable[[int, int, int], None]] = None


@dataclass
class FileDownloadResult:
    """Result of a file download."""

    success: bool
    filename: str
    output_path: str
    size: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileDownloadResult":
        """Create a FileDownloadResult instance from a dictionary."""
        return cls(
            success=data.get("success", False),
            filename=data.get("filename", ""),
            output_path=data.get("outputPath", ""),
            size=data.get("size", 0),
        )


# Entity types
@dataclass
class Entity:
    """Represents an entity (topic, intent, or NER)."""

    id: str
    workspace_id: str = ""
    created_by: str = ""
    label: str = ""
    entity_type: EntityType = "topic"
    description: Optional[str] = None
    emoji: Optional[str] = None
    parent_entity: Optional[str] = None
    background_color: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entity":
        """Create an Entity instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            workspace_id=data.get("workspaceid", ""),
            created_by=data.get("createdBy", ""),
            label=data.get("label", ""),
            entity_type=data.get("type", "topic"),
            description=data.get("description"),
            emoji=data.get("emoji"),
            parent_entity=data.get("parentEntity"),
            background_color=data.get("backgroundColor"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
        )


@dataclass
class EntityCreateOptions:
    """Options for creating an entity."""

    description: Optional[str] = None
    emoji: Optional[str] = None
    parent_entity: Optional[str] = None
    background_color: Optional[str] = None


@dataclass
class EntityUpdateData:
    """Data for updating an entity."""

    label: Optional[str] = None
    description: Optional[str] = None
    emoji: Optional[str] = None
    parent_entity: Optional[str] = None
    background_color: Optional[str] = None


# Folder types
@dataclass
class Folder:
    """Represents a folder."""

    id: str
    workspace_id: str = ""
    created_by: str = ""
    name: str = ""
    description: Optional[str] = None
    emoji: Optional[str] = None
    status: Optional[str] = None
    parent: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Folder":
        """Create a Folder instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            workspace_id=data.get("workspaceID", ""),
            created_by=data.get("createdBy", ""),
            name=data.get("name", ""),
            description=data.get("description"),
            emoji=data.get("emoji"),
            status=data.get("status"),
            parent=data.get("parent"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
        )


@dataclass
class FolderCreateOptions:
    """Options for creating a folder."""

    description: Optional[str] = None
    emoji: Optional[str] = None
    status: str = "active"
    parent: Optional[str] = None


@dataclass
class FolderUpdateData:
    """Data for updating a folder."""

    name: Optional[str] = None
    description: Optional[str] = None
    emoji: Optional[str] = None
    status: Optional[str] = None
    parent: Optional[str] = None


@dataclass
class FolderTreeNode:
    """A folder in a tree structure."""

    id: str
    workspace_id: str
    created_by: str
    name: str
    description: Optional[str]
    emoji: Optional[str]
    status: Optional[str]
    parent: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    children: List["FolderTreeNode"] = field(default_factory=list)

    @classmethod
    def from_folder(
        cls, folder: Folder, children: List["FolderTreeNode"] = None
    ) -> "FolderTreeNode":
        """Create a FolderTreeNode from a Folder."""
        return cls(
            id=folder.id,
            workspace_id=folder.workspace_id,
            created_by=folder.created_by,
            name=folder.name,
            description=folder.description,
            emoji=folder.emoji,
            status=folder.status,
            parent=folder.parent,
            created_at=folder.created_at,
            updated_at=folder.updated_at,
            children=children or [],
        )


# Prompt types
@dataclass
class Prompt:
    """Represents a prompt template."""

    id: str
    workspace_id: str = ""
    created_by: str = ""
    prompt_type: str = ""
    label: str = ""
    prompt_length: int = 0
    interpolation_string: str = ""
    scope: Optional[str] = None
    style: Optional[str] = None
    domain: Optional[str] = None
    prompt_placeholder: Optional[str] = None
    available_to_agents: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prompt":
        """Create a Prompt instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            workspace_id=data.get("workspaceID", ""),
            created_by=data.get("createdBy", ""),
            prompt_type=data.get("type", ""),
            label=data.get("label", ""),
            prompt_length=data.get("promptLength", 0),
            interpolation_string=data.get("interpolationString", ""),
            scope=data.get("scope"),
            style=data.get("style"),
            domain=data.get("domain"),
            prompt_placeholder=data.get("promptPlaceholder"),
            available_to_agents=data.get("availableToAgents", []),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
        )


@dataclass
class PromptCreateData:
    """Data for creating a prompt."""

    label: str
    prompt_type: str
    interpolation_string: str
    scope: Optional[str] = None
    style: Optional[str] = None
    domain: Optional[str] = None
    prompt_placeholder: Optional[str] = None
    available_to_agents: List[str] = field(default_factory=list)


@dataclass
class PromptUpdateData:
    """Data for updating a prompt."""

    label: Optional[str] = None
    prompt_type: Optional[str] = None
    interpolation_string: Optional[str] = None
    scope: Optional[str] = None
    style: Optional[str] = None
    domain: Optional[str] = None
    prompt_placeholder: Optional[str] = None
    available_to_agents: Optional[List[str]] = None


# Response types
@dataclass
class ListResponse:
    """Generic list response."""

    items: List[Any]
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


# Streaming types
class StreamingOptions(TypedDict, total=False):
    """Options for streaming requests."""

    chat_id: str
    phone_number: str
    customer_id: str
    provider_id: str
    customer_info: Dict[str, Any]
    attachments: Attachments
    show_progress: bool
    raw_stream: bool


@dataclass
class StreamEventData:
    """Data from a stream event."""

    text: str = ""
    message_type: str = ""
    message_id: str = ""
    chat_id: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StreamEventData":
        """Create a StreamEventData instance from a dictionary."""
        return cls(
            text=data.get("text", ""),
            message_type=data.get("type", ""),
            message_id=data.get("message_id", ""),
            chat_id=data.get("chatId", ""),
        )


@dataclass
class StreamStatusEvent:
    """Status event from a stream."""

    status: str
    processing_status: Optional[str] = None
    metadata_parsed: Optional[Dict[str, Any]] = None


@dataclass
class StreamingResult:
    """Result of a streaming request."""

    chat_id: str
    message_id: str


# Content type mapping
CONTENT_TYPE_MAP: Dict[str, str] = {
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".txt": "text/plain",
    ".csv": "text/csv",
    ".json": "application/json",
    ".xml": "application/xml",
    ".html": "text/html",
    ".htm": "text/html",
    ".md": "text/markdown",
    ".rtf": "application/rtf",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".avi": "video/x-msvideo",
    ".mov": "video/quicktime",
    ".zip": "application/zip",
    ".rar": "application/vnd.rar",
    ".7z": "application/x-7z-compressed",
    ".tar": "application/x-tar",
    ".gz": "application/gzip",
    ".py": "text/x-python",
    ".js": "application/javascript",
    ".ts": "application/typescript",
    ".java": "text/x-java-source",
    ".c": "text/x-c",
    ".cpp": "text/x-c++",
    ".h": "text/x-c",
    ".hpp": "text/x-c++",
    ".cs": "text/x-csharp",
    ".go": "text/x-go",
    ".rs": "text/x-rust",
    ".rb": "text/x-ruby",
    ".php": "text/x-php",
    ".swift": "text/x-swift",
    ".kt": "text/x-kotlin",
    ".scala": "text/x-scala",
}


def get_content_type(filename: str) -> str:
    """Get content type from filename extension."""
    import os

    ext = os.path.splitext(filename)[1].lower()
    return CONTENT_TYPE_MAP.get(ext, "application/octet-stream")


# Max file size constant
MAX_FILE_SIZE_MB = 15
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
