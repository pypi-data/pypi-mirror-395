"""
MemoryStackClient Unit Tests
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from memorystack import MemoryStackClient, Message
from memorystack.exceptions import (
    MemoryStackError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    NetworkError,
)


class TestMemoryStackClient:
    """Test MemoryStackClient class"""

    @pytest.fixture
    def client(self):
        """Create a client instance for testing"""
        return MemoryStackClient(
            api_key="test-api-key",
            base_url="https://api.test.com/api/v1",
        )

    @pytest.fixture
    def mock_response(self):
        """Create a mock response"""
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"success": True}
        response.headers = {}
        response.ok = True
        return response

    def test_client_initialization(self):
        """Test client initialization"""
        client = MemoryStackClient(
            api_key="test-key",
            base_url="https://api.test.com/api/v1",
        )
        assert client.api_key == "test-key"
        assert client.base_url == "https://api.test.com/api/v1"

    def test_client_initialization_missing_api_key(self):
        """Test that missing API key raises ValidationError"""
        with pytest.raises(ValidationError, match="API key is required"):
            MemoryStackClient(api_key="", base_url="https://api.test.com/api/v1")

    def test_client_initialization_missing_base_url(self):
        """Test that missing base_url raises ValidationError"""
        with pytest.raises(ValidationError, match="base_url is required"):
            MemoryStackClient(api_key="test-key", base_url=None)

    def test_base_url_normalization(self):
        """Test that base URL is normalized correctly"""
        # Test with /api/v1 already present
        client1 = MemoryStackClient(
            api_key="test-key",
            base_url="https://api.test.com/api/v1",
        )
        assert client1.base_url.endswith("/api/v1")

        # Test without /api/v1
        client2 = MemoryStackClient(
            api_key="test-key",
            base_url="https://api.test.com",
        )
        assert client2.base_url.endswith("/api/v1")

    @patch("memory_os.client.MemoryStackClient._make_request")
    def test_create_memory_success(self, mock_request, client):
        """Test successful memory creation"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "success": True,
            "memories_created": 1,
            "memory_ids": ["mem-123"],
            "owner_id": "owner-123",
            "user_id": None,
        }

        result = client.create_memory(
            messages=[
                Message(role="user", content="Test message"),
                Message(role="assistant", content="Test response"),
            ]
        )

        assert result.memories_created == 1
        assert "mem-123" in result.memory_ids

    def test_create_memory_empty_messages(self, client):
        """Test that empty messages raises ValidationError"""
        with pytest.raises(ValidationError, match="At least one message"):
            client.create_memory(messages=[])

    @patch("memory_os.client.MemoryStackClient._make_request")
    def test_search_memories_success(self, mock_request, client):
        """Test successful memory search"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "success": True,
            "count": 2,
            "mode": "hybrid",
            "results": [
                {"id": "mem-1", "content": "Memory 1"},
                {"id": "mem-2", "content": "Memory 2"},
            ],
        }

        result = client.search_memories(query="test query", limit=10)

        assert result["count"] == 2
        assert len(result["results"]) == 2

    def test_search_memories_empty_query(self, client):
        """Test that empty query raises ValidationError"""
        with pytest.raises(ValidationError, match="Search query is required"):
            client.search_memories(query="", limit=10)

    def test_search_memories_invalid_mode(self, client):
        """Test that invalid mode raises ValidationError"""
        with pytest.raises(ValidationError, match="Invalid search mode"):
            client.search_memories(query="test", mode="invalid")

    def test_search_memories_invalid_limit(self, client):
        """Test that invalid limit raises ValidationError"""
        with pytest.raises(ValidationError, match="Invalid limit"):
            client.search_memories(query="test", limit=0)

        with pytest.raises(ValidationError, match="Invalid limit"):
            client.search_memories(query="test", limit=100)

    @patch("memory_os.client.MemoryStackClient._make_request")
    def test_list_memories_success(self, mock_request, client):
        """Test successful memory listing"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "success": True,
            "count": 5,
            "next_cursor": "cursor-123",
            "results": [
                {"id": "mem-1", "content": "Memory 1"},
                {"id": "mem-2", "content": "Memory 2"},
            ],
        }

        result = client.list_memories(limit=20)

        assert result.count == 5
        assert len(result.results) == 2

    def test_list_memories_invalid_limit(self, client):
        """Test that invalid limit raises ValidationError"""
        with pytest.raises(ValidationError, match="Invalid limit"):
            client.list_memories(limit=0)

        with pytest.raises(ValidationError, match="Invalid limit"):
            client.list_memories(limit=200)

    @patch("memory_os.client.MemoryStackClient._make_request")
    def test_get_memory_success(self, mock_request, client):
        """Test successful memory retrieval"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "success": True,
            "memory": {
                "id": "mem-123",
                "content": "Test memory",
                "memory_type": "fact",
                "confidence": 0.9,
            },
        }

        result = client.get_memory("mem-123")

        assert result.id == "mem-123"
        assert result.content == "Test memory"

    def test_get_memory_empty_id(self, client):
        """Test that empty memory ID raises ValidationError"""
        with pytest.raises(ValidationError, match="Memory ID is required"):
            client.get_memory("")

    @patch("memory_os.client.MemoryStackClient._make_request")
    def test_update_memory_success(self, mock_request, client):
        """Test successful memory update"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "success": True,
            "memory": {
                "id": "mem-123",
                "content": "Updated content",
                "memory_type": "fact",
                "confidence": 0.95,
            },
        }

        result = client.update_memory(
            "mem-123", content="Updated content", confidence=0.95
        )

        assert result.content == "Updated content"
        assert result.confidence == 0.95

    def test_update_memory_empty_id(self, client):
        """Test that empty memory ID raises ValidationError"""
        with pytest.raises(ValidationError, match="Memory ID is required"):
            client.update_memory("", content="test")

    def test_update_memory_no_updates(self, client):
        """Test that no updates raises ValidationError"""
        with pytest.raises(ValidationError, match="At least one field"):
            client.update_memory("mem-123")

    @patch("memory_os.client.MemoryStackClient._make_request")
    def test_delete_memory_success(self, mock_request, client):
        """Test successful memory deletion"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "success": True,
            "deleted_count": 1,
            "hard_delete": False,
        }

        result = client.delete_memory("mem-123", hard=False)

        assert result["deleted_count"] == 1
        assert result["hard_delete"] is False

    def test_delete_memory_empty_id(self, client):
        """Test that empty memory ID raises ValidationError"""
        with pytest.raises(ValidationError, match="Memory ID is required"):
            client.delete_memory("")

    def test_error_handling_401(self, client):
        """Test 401 AuthenticationError handling"""
        response = Mock()
        response.status_code = 401
        response.json.return_value = {"error": "Invalid API key"}
        response.headers = {}
        response.ok = False

        with patch.object(client, "_make_request", return_value=response):
            with pytest.raises(AuthenticationError):
                client._handle_response(response)

    def test_error_handling_429(self, client):
        """Test 429 RateLimitError handling"""
        response = Mock()
        response.status_code = 429
        response.json.return_value = {"error": "Rate limit exceeded"}
        response.headers = {
            "x-ratelimit-limit": "100",
            "x-ratelimit-remaining": "0",
            "x-ratelimit-reset": "1234567890",
        }
        response.ok = False

        with patch.object(client, "_make_request", return_value=response):
            with pytest.raises(RateLimitError) as exc_info:
                client._handle_response(response)
            assert exc_info.value.limit == 100
            assert exc_info.value.remaining == 0

    def test_error_handling_400(self, client):
        """Test 400 ValidationError handling"""
        response = Mock()
        response.status_code = 400
        response.json.return_value = {
            "error": "Validation failed",
            "details": {"field": "content"},
        }
        response.headers = {}
        response.ok = False

        with patch.object(client, "_make_request", return_value=response):
            with pytest.raises(ValidationError) as exc_info:
                client._handle_response(response)
            assert exc_info.value.details == {"field": "content"}

    def test_error_handling_404(self, client):
        """Test 404 NotFoundError handling"""
        response = Mock()
        response.status_code = 404
        response.json.return_value = {"error": "Not found"}
        response.headers = {}
        response.ok = False

        with patch.object(client, "_make_request", return_value=response):
            with pytest.raises(NotFoundError):
                client._handle_response(response)

    def test_retry_logic(self, client):
        """Test retry logic on network errors"""
        import requests

        # Mock requests to fail first time, succeed second time
        call_count = [0]

        def mock_request(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] < 2:
                raise requests.exceptions.ConnectionError("Network error")
            response = Mock()
            response.status_code = 200
            response.json.return_value = {"success": True}
            response.headers = {}
            response.ok = True
            return response

        with patch.object(client.session, "request", side_effect=mock_request):
            # This should retry and eventually succeed
            result = client._make_request("GET", "https://api.test.com/test")
            assert result.status_code == 200
            assert call_count[0] == 2  # Should have retried once





