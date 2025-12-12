"""Tests for type definitions."""

import pytest

from toothfairyai.types import (
    Chat,
    Message,
    Document,
    Entity,
    Folder,
    Prompt,
    AgentResponse,
    FileUploadResult,
    FolderTreeNode,
    get_content_type,
)


class TestChatTypes:
    """Tests for chat-related types."""

    def test_chat_from_dict(self):
        """Test Chat.from_dict conversion."""
        data = {
            "id": "chat-123",
            "name": "Test Chat",
            "primaryRole": "user",
            "customerId": "customer-456",
            "customerInfo": {"name": "John"},
            "isAIReplying": True,
            "channelSettings": {"channel": "web", "provider": "default"},
        }
        chat = Chat.from_dict(data)

        assert chat.id == "chat-123"
        assert chat.name == "Test Chat"
        assert chat.primary_role == "user"
        assert chat.customer_id == "customer-456"
        assert chat.customer_info == {"name": "John"}
        assert chat.is_ai_replying is True
        assert chat.channel_settings is not None
        assert chat.channel_settings.channel == "web"

    def test_chat_from_dict_with_missing_fields(self):
        """Test Chat.from_dict with missing fields."""
        data = {"id": "chat-123"}
        chat = Chat.from_dict(data)

        assert chat.id == "chat-123"
        assert chat.name == ""
        assert chat.customer_info == {}
        assert chat.channel_settings is None

    def test_message_from_dict(self):
        """Test Message.from_dict conversion."""
        data = {
            "id": "msg-123",
            "chatID": "chat-456",
            "text": "Hello world",
            "role": "user",
            "userID": "user-789",
            "images": ["image1.jpg"],
        }
        message = Message.from_dict(data)

        assert message.id == "msg-123"
        assert message.chat_id == "chat-456"
        assert message.text == "Hello world"
        assert message.role == "user"
        assert message.images == ["image1.jpg"]


class TestDocumentTypes:
    """Tests for document-related types."""

    def test_document_from_dict(self):
        """Test Document.from_dict conversion."""
        data = {
            "id": "doc-123",
            "workspaceid": "ws-456",
            "userid": "user-789",
            "type": "readComprehensionPdf",
            "title": "Test Document",
            "topics": ["topic1", "topic2"],
            "folderid": "folder-123",
            "status": "published",
        }
        doc = Document.from_dict(data)

        assert doc.id == "doc-123"
        assert doc.workspace_id == "ws-456"
        assert doc.doc_type == "readComprehensionPdf"
        assert doc.title == "Test Document"
        assert doc.topics == ["topic1", "topic2"]

    def test_file_upload_result_from_dict(self):
        """Test FileUploadResult.from_dict conversion."""
        data = {
            "success": True,
            "originalFilename": "test.pdf",
            "sanitizedFilename": "test.pdf",
            "filename": "uuid-test.pdf",
            "importType": "file",
            "contentType": "application/pdf",
            "size": 1024,
            "sizeInMB": 0.001,
        }
        result = FileUploadResult.from_dict(data)

        assert result.success is True
        assert result.original_filename == "test.pdf"
        assert result.content_type == "application/pdf"
        assert result.size == 1024


class TestEntityTypes:
    """Tests for entity-related types."""

    def test_entity_from_dict(self):
        """Test Entity.from_dict conversion."""
        data = {
            "id": "entity-123",
            "workspaceid": "ws-456",
            "createdBy": "user-789",
            "label": "Dental Cleaning",
            "type": "topic",
            "description": "Professional cleaning",
            "emoji": "🦷",
        }
        entity = Entity.from_dict(data)

        assert entity.id == "entity-123"
        assert entity.label == "Dental Cleaning"
        assert entity.entity_type == "topic"
        assert entity.emoji == "🦷"


class TestFolderTypes:
    """Tests for folder-related types."""

    def test_folder_from_dict(self):
        """Test Folder.from_dict conversion."""
        data = {
            "id": "folder-123",
            "workspaceID": "ws-456",
            "createdBy": "user-789",
            "name": "Documents",
            "description": "Main documents folder",
            "status": "active",
            "parent": None,
        }
        folder = Folder.from_dict(data)

        assert folder.id == "folder-123"
        assert folder.name == "Documents"
        assert folder.status == "active"
        assert folder.parent is None

    def test_folder_tree_node_from_folder(self):
        """Test FolderTreeNode.from_folder conversion."""
        folder = Folder(
            id="folder-123",
            workspace_id="ws-456",
            created_by="user-789",
            name="Parent",
        )
        children = []
        node = FolderTreeNode.from_folder(folder, children)

        assert node.id == "folder-123"
        assert node.name == "Parent"
        assert node.children == []


class TestPromptTypes:
    """Tests for prompt-related types."""

    def test_prompt_from_dict(self):
        """Test Prompt.from_dict conversion."""
        data = {
            "id": "prompt-123",
            "workspaceID": "ws-456",
            "createdBy": "user-789",
            "type": "greeting",
            "label": "Welcome Prompt",
            "promptLength": 50,
            "interpolationString": "Hello {{name}}!",
            "availableToAgents": ["agent-1", "agent-2"],
        }
        prompt = Prompt.from_dict(data)

        assert prompt.id == "prompt-123"
        assert prompt.label == "Welcome Prompt"
        assert prompt.prompt_type == "greeting"
        assert prompt.interpolation_string == "Hello {{name}}!"
        assert prompt.available_to_agents == ["agent-1", "agent-2"]


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_get_content_type_pdf(self):
        """Test content type detection for PDF."""
        assert get_content_type("document.pdf") == "application/pdf"

    def test_get_content_type_image(self):
        """Test content type detection for images."""
        assert get_content_type("image.jpg") == "image/jpeg"
        assert get_content_type("image.jpeg") == "image/jpeg"
        assert get_content_type("image.png") == "image/png"

    def test_get_content_type_unknown(self):
        """Test content type detection for unknown extension."""
        assert get_content_type("file.xyz") == "application/octet-stream"

    def test_get_content_type_case_insensitive(self):
        """Test that content type detection is case insensitive."""
        assert get_content_type("document.PDF") == "application/pdf"
        assert get_content_type("image.JPG") == "image/jpeg"
