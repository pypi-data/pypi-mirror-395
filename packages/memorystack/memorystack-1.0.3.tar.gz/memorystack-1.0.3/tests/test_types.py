"""
Type Definitions Unit Tests
"""

import pytest
from memorystack.types import (
    Message,
    TextPart,
    ImagePart,
    CreateMemoryRequest,
    Memory,
    ListMemoriesRequest,
)


class TestMessage:
    """Test Message type"""

    def test_text_message(self):
        """Test text message creation"""
        message = Message(role="user", content="Hello")
        assert message.role == "user"
        assert message.content == "Hello"

    def test_message_with_parts(self):
        """Test message with multiple parts"""
        message = Message(
            role="user",
            content=[
                TextPart(type="text", text="Hello"),
                ImagePart(type="image", data="base64data", mime_type="image/png"),
            ],
        )
        assert isinstance(message.content, list)
        assert len(message.content) == 2


class TestMessageParts:
    """Test message part types"""

    def test_text_part(self):
        """Test TextPart creation"""
        part = TextPart(type="text", text="Hello")
        assert part.type == "text"
        assert part.text == "Hello"

    def test_image_part(self):
        """Test ImagePart creation"""
        part = ImagePart(type="image", data="base64data", mime_type="image/png")
        assert part.type == "image"
        assert part.data == "base64data"
        assert part.mime_type == "image/png"


class TestCreateMemoryRequest:
    """Test CreateMemoryRequest type"""

    def test_create_memory_request(self):
        """Test create memory request creation"""
        request = CreateMemoryRequest(
            messages=[
                Message(role="user", content="Test"),
                Message(role="assistant", content="Response"),
            ],
            user_id="user-123",
            metadata={"key": "value"},
        )
        assert len(request.messages) == 2
        assert request.user_id == "user-123"
        assert request.metadata == {"key": "value"}


class TestMemory:
    """Test Memory type"""

    def test_memory_creation(self):
        """Test memory object creation"""
        memory = Memory(
            id="mem-123",
            owner_clerk_id="owner-123",
            end_user_id="user-123",
            content="Test content",
            memory_type="fact",
            confidence=0.9,
            metadata={},
            source_type="conversation",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )
        assert memory.id == "mem-123"
        assert memory.confidence == 0.9
        assert memory.memory_type == "fact"

    def test_memory_dict_access(self):
        """Test memory dict-like access for backwards compatibility"""
        memory = Memory(
            id="mem-123",
            owner_clerk_id="owner-123",
            end_user_id=None,
            content="Test",
            memory_type="fact",
            confidence=0.9,
            metadata={},
            source_type="conversation",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )
        # Test __getitem__
        assert memory["id"] == "mem-123"
        assert memory["content"] == "Test"

        # Test get method
        assert memory.get("id") == "mem-123"
        assert memory.get("nonexistent", "default") == "default"


class TestListMemoriesRequest:
    """Test ListMemoriesRequest type"""

    def test_list_memories_request(self):
        """Test list memories request creation"""
        request = ListMemoriesRequest(
            user_id="user-123",
            limit=20,
            cursor="cursor-123",
            order="desc",
            memory_type="fact",
            min_confidence=0.8,
            include_embedding=False,
        )
        assert request.user_id == "user-123"
        assert request.limit == 20
        assert request.order == "desc"





