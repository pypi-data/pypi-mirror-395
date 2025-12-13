"""MemoryStack Client"""

import requests
import time
import uuid
import logging
from typing import Optional, List, Dict, Any, Callable, Union
from .types import (
    Message,
    CreateMemoryRequest,
    CreateMemoryResponse,
    ListMemoriesRequest,
    ListMemoriesResponse,
    Memory,
    UsageStats,
    GraphData,
    GraphNode,
    GraphLink,
)
from .exceptions import (
    MemoryStackError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    NetworkError,
)


class MemoryStackClient:
    """Client for interacting with MemoryStack API"""
    
    SDK_VERSION = "1.0.3"

    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        agent_name: str = None,
        agent_type: str = None,
        session_id: str = None,
        project_name: str = None,
        timeout: Optional[int] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        max_retry_delay: float = 10.0,
        retryable_status_codes: Optional[List[int]] = None,
        enable_logging: bool = False,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize MemoryStack client
        
        Args:
            api_key: Your MemoryStack API key
            base_url: Optional custom API base URL
            agent_name: Optional agent name (auto-detected if not provided)
            agent_type: Optional agent type (e.g., 'support', 'sales')
            session_id: Optional session ID for conversation tracking
            project_name: Optional project name (default: 'default')
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries for network errors (default: 3)
            retry_delay: Initial retry delay in seconds (default: 1.0)
            max_retry_delay: Maximum retry delay in seconds (default: 10.0)
            retryable_status_codes: HTTP status codes to retry (default: [408, 429, 500, 502, 503, 504])
            enable_logging: Enable request/response logging (default: False)
            logger: Custom logger instance (optional, uses default if not provided)
        """
        if not api_key:
            raise ValidationError("API key is required")
        
        self.api_key = api_key
        
        # Use default production URL if not provided
        if not base_url:
            base_url = "https://www.memorystack.app"
        
        # Normalize base URL
        base_url = base_url.strip()
        if base_url.endswith('/api/v1'):
            base_url = base_url[:-7]  # Remove /api/v1
        if not base_url.endswith('/api/v1'):
            base_url = f"{base_url}/api/v1"
        
        self.base_url = base_url
        self.timeout = timeout or 30
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_retry_delay = max_retry_delay
        self.retryable_status_codes = retryable_status_codes or [408, 429, 500, 502, 503, 504]
        self.enable_logging = enable_logging
        
        # Setup logger
        if logger:
            self.logger = logger
        elif enable_logging:
            self.logger = logging.getLogger(__name__)
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[MemoryStack] %(levelname)s: %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.setLevel(logging.DEBUG)
        else:
            # Create a no-op logger
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(logging.NullHandler())
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "X-API-Key": api_key,  # Fallback for environments that strip Authorization header
            "X-SDK-Version": self.SDK_VERSION,
            "User-Agent": f"memorystack-python-sdk/{self.SDK_VERSION}",
        })
        self.session.timeout = self.timeout
        
        # Optional agent context
        self.agent_id: Optional[str] = None
        self.project_id: Optional[str] = None
        self.session_id = session_id
        self.agent_name = agent_name
        self.agent_type = agent_type
        
        # Auto-detect agent framework if not explicitly provided
        if not self.agent_name:
            detected = self._detect_agent_framework()
            if detected:
                self.agent_name = detected.get('name')
                self.agent_type = detected.get('type')
        
        # Initialize agent if name is provided or detected
        if self.agent_name:
            try:
                self._initialize_agent(project_name or 'default')
            except Exception as e:
                print(f"Warning: Failed to initialize agent: {e}")

    def _generate_request_id(self) -> str:
        """Generate a unique request ID"""
        return f"req_{int(time.time() * 1000)}_{uuid.uuid4().hex[:9]}"

    def _sleep(self, seconds: float) -> None:
        """Sleep for specified seconds"""
        time.sleep(seconds)

    def _detect_agent_framework(self) -> Optional[Dict[str, str]]:
        """Detect if SDK is being used within an agent framework"""
        import sys
        import logging
        
        try:
            main_module = sys.modules.get('__main__')
            if not main_module:
                return None
            
            # Check for CrewAI
            if hasattr(main_module, '__crewai_agent__'):
                agent = getattr(main_module, '__crewai_agent__')
                return {
                    'name': getattr(agent, 'role', 'CrewAI Agent'),
                    'type': getattr(agent, 'role', 'crewai')
                }
            
            # Check for LangGraph
            if hasattr(main_module, '__langgraph_agent__'):
                agent = getattr(main_module, '__langgraph_agent__')
                return {
                    'name': getattr(agent, 'name', 'LangGraph Agent'),
                    'type': 'langgraph'
                }
            
            # Check for AutoGPT
            if hasattr(main_module, '__autogpt_agent__'):
                agent = getattr(main_module, '__autogpt_agent__')
                return {
                    'name': getattr(agent, 'name', 'AutoGPT Agent'),
                    'type': 'autonomous'
                }
            
            return None
        except Exception as e:
            # Don't fail initialization if detection fails
            logging.getLogger(__name__).debug(f"Agent detection failed: {e}")
            return None

    def _initialize_agent(self, project_name: str) -> None:
        """Initialize agent (create initial memory to register agent)"""
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Agent initialization happens automatically on first memory creation
            # via /memories/agents endpoint which handles agent_name parameter
            # No need to pre-create agent - it will be created on first use
            logger.info(f'Agent "{self.agent_name}" will be initialized on first memory creation')
        except Exception as e:
            # Silently fail - agent features are optional
            logger.warning(f"Agent initialization note: {e}")

    def _make_request(
        self,
        method: str,
        url: str,
        retry_count: int = 0,
        **kwargs
    ) -> requests.Response:
        """
        Make HTTP request with retry logic
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            retry_count: Current retry attempt
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        request_id = self._generate_request_id()
        kwargs.setdefault('headers', {})['X-Request-ID'] = request_id
        
        if self.enable_logging:
            self.logger.debug(f"Request: {method} {url}", extra={
                'request_id': request_id,
                'method': method,
                'url': url,
            })
        
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            
            # Check for retryable status codes
            if response.status_code in self.retryable_status_codes and retry_count < self.max_retries:
                delay = min(
                    self.retry_delay * (2 ** retry_count),
                    self.max_retry_delay
                )
                
                if self.enable_logging:
                    self.logger.warning(
                        f"Retrying request (attempt {retry_count + 1}/{self.max_retries}) "
                        f"after {delay}s: Status {response.status_code}",
                        extra={'request_id': request_id}
                    )
                
                self._sleep(delay)
                return self._make_request(method, url, retry_count + 1, **kwargs)
            
            if self.enable_logging:
                self.logger.debug(f"Response: {response.status_code} {url}", extra={
                    'request_id': request_id,
                    'status_code': response.status_code,
                })
            
            return response
            
        except (requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            
            # Check if we should retry
            is_retryable = retry_count < self.max_retries
            
            if is_retryable:
                delay = min(
                    self.retry_delay * (2 ** retry_count),
                    self.max_retry_delay
                )
                
                if self.enable_logging:
                    self.logger.warning(
                        f"Retrying request (attempt {retry_count + 1}/{self.max_retries}) "
                        f"after {delay}s: {str(e)}",
                        extra={'request_id': request_id}
                    )
                
                self._sleep(delay)
                return self._make_request(method, url, retry_count + 1, **kwargs)
            
            # No more retries
            if self.enable_logging:
                self.logger.error(f"Request failed after {retry_count} retries: {str(e)}", extra={
                    'request_id': request_id,
                })
            
            raise NetworkError(
                f"Network request failed after {retry_count} retries: {str(e)}",
                original_error=e
            )
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions"""
        try:
            data = response.json()
        except ValueError:
            data = {}
        
        # Handle network errors (no response received)
        if response.status_code == 0 or response.raw is None:
            raise NetworkError(
                "Network request failed - no response received",
                original_error=None
            )

        if response.status_code == 401:
            raise AuthenticationError(
                data.get("error", "Authentication failed"),
                status_code=response.status_code,
                details=data.get("details"),
            )
        elif response.status_code == 429:
            # Extract rate limit headers
            limit = response.headers.get('x-ratelimit-limit')
            remaining = response.headers.get('x-ratelimit-remaining')
            reset = response.headers.get('x-ratelimit-reset')
            raise RateLimitError(
                data.get("error", "Rate limit exceeded"),
                status_code=response.status_code,
                details=data.get("details"),
                limit=int(limit) if limit else None,
                remaining=int(remaining) if remaining else None,
                reset=int(reset) if reset else None,
            )
        elif response.status_code == 400:
            raise ValidationError(
                data.get("error", "Validation failed"),
                status_code=response.status_code,
                details=data.get("details"),
            )
        elif response.status_code == 404:
            raise NotFoundError(
                data.get("error", "Resource not found"),
                status_code=response.status_code,
                details=data.get("details"),
            )
        elif not response.ok:
            raise MemoryStackError(
                data.get("error", "API request failed"),
                status_code=response.status_code,
                details=data.get("details"),
            )

        return data

    def add(
        self,
        content: Union[str, List[Message], List[Dict[str, str]]],
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CreateMemoryResponse:
        """
        Add a memory - the simplest way to store information.
        
        Examples:
            # Simple text
            client.add("User prefers dark mode")
            
            # With user ID (for B2B apps)
            client.add("User prefers dark mode", user_id="user_123")
            
            # Conversation format
            client.add([
                {"role": "user", "content": "I love Python"},
                {"role": "assistant", "content": "Great choice!"}
            ])
        
        Args:
            content: Text string or list of messages
            user_id: Optional end user ID for B2B use cases
            metadata: Optional metadata dictionary
            
        Returns:
            CreateMemoryResponse with created memory IDs
        """
        # Normalize content to messages
        if isinstance(content, str):
            messages = [{"role": "user", "content": content}]
        elif isinstance(content, list):
            messages = []
            for msg in content:
                if isinstance(msg, dict):
                    messages.append(msg)
                else:
                    messages.append({"role": msg.role, "content": msg.content})
        else:
            raise ValidationError("Content must be a string or list of messages")
        
        # Validate
        if not messages:
            raise ValidationError("At least one message is required")
        if len(messages) > 100:
            raise ValidationError("Maximum 100 messages per request")
        for msg in messages:
            if not msg.get('role') or not msg.get('content'):
                raise ValidationError(f"Message missing role or content: {msg}")
        
        # Build payload
        payload = {"messages": messages}
        if user_id is not None:
            payload["user_id"] = user_id
        if metadata is not None:
            payload["metadata"] = metadata
        if self.session_id:
            payload["session_id"] = self.session_id
        if self.agent_name:
            payload["agent_name"] = self.agent_name
        if self.agent_type:
            payload["agent_type"] = self.agent_type

        endpoint = f"{self.base_url}/memories/agents" if self.agent_name else f"{self.base_url}/memories"
        response = self._make_request('POST', endpoint, json=payload)
        data = self._handle_response(response)

        if data.get("agent_id"):
            self.agent_id = data["agent_id"]
        if data.get("project_id"):
            self.project_id = data["project_id"]

        return CreateMemoryResponse(
            success=data.get("success", True),
            memories_created=data.get("memories_created", 1),
            memory_ids=data.get("memory_ids", []),
            owner_id=data.get("owner_id") or data.get("owner_clerk_id") or "",
            user_id=data.get("user_id") or data.get("end_user_id"),
            message=data.get("message"),
            agent_id=data.get("agent_id"),
            project_id=data.get("project_id"),
        )

    def create_memory(
        self,
        messages: List[Message],
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CreateMemoryResponse:
        """Deprecated: Use add() instead - simpler API"""
        return self.add(messages, user_id=user_id, metadata=metadata)

    def list_memories(
        self,
        user_id: Optional[str] = None,
        limit: int = 20,
        cursor: Optional[str] = None,
        order: str = "desc",
        memory_type: Optional[str] = None,
        min_confidence: Optional[float] = None,
        include_embedding: bool = False,
    ) -> ListMemoriesResponse:
        """
        List memories with optional filtering and pagination
        
        Args:
            user_id: Filter by user ID ('self', 'all', or specific ID)
            limit: Maximum number of results (1-100)
            cursor: Pagination cursor
            order: Sort order ('asc' or 'desc')
            memory_type: Filter by memory type
            min_confidence: Minimum confidence score (0-1)
            include_embedding: Include embedding vectors
            
        Returns:
            ListMemoriesResponse with paginated memories
        """
        # Validate limit
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise ValidationError(
                f"Invalid limit: {limit}. Must be an integer between 1 and 100"
            )
        
        # Validate order
        if order not in ['asc', 'desc']:
            raise ValidationError(
                f'Invalid order: "{order}". Must be "asc" or "desc"'
            )
        
        # Validate min_confidence
        if min_confidence is not None:
            if not isinstance(min_confidence, (int, float)) or min_confidence < 0 or min_confidence > 1:
                raise ValidationError(
                    f"Invalid min_confidence: {min_confidence}. Must be a number between 0 and 1"
                )
        
        params = {"limit": limit, "order": order}
        
        if user_id is not None:
            params["user_id"] = user_id
        if cursor is not None:
            params["cursor"] = cursor
        if memory_type is not None:
            params["memory_type"] = memory_type
        if min_confidence is not None:
            params["min_confidence"] = min_confidence
        if include_embedding:
            params["include_embedding"] = "true"

        response = self._make_request('GET', f"{self.base_url}/memories", params=params)
        data = self._handle_response(response)

        memories = [self._deserialize_memory(m) for m in data["results"]]

        return ListMemoriesResponse(
            success=data["success"],
            count=data["count"],
            next_cursor=data.get("next_cursor"),
            results=memories,
        )

    def get_stats(self) -> UsageStats:
        """
        Get usage statistics for the authenticated user
        
        Returns:
            UsageStats with API calls, storage, and limits
        """
        response = self._make_request('GET', f"{self.base_url}/stats")
        data = self._handle_response(response)

        return UsageStats(
            success=data["success"],
            owner_id=data["owner_id"],
            plan_tier=data.get("plan_tier"),
            totals=data["totals"],
            usage=data["usage"],
            storage=data["storage"],
        )

    def get_graph(self) -> GraphData:
        """
        Get knowledge graph data
        
        Note: This endpoint typically requires Clerk authentication
        
        Returns:
            GraphData with nodes and links
        """
        response = self._make_request('GET', f"{self.base_url}/graph")
        data = self._handle_response(response)

        nodes = [
            GraphNode(
                id=n["id"],
                label=n["label"],
                type=n["type"],
                group=n["group"],
                content=n.get("content"),
            )
            for n in data.get("nodes", [])
        ]

        links = [
            GraphLink(
                source=l["source"],
                target=l["target"],
                label=l["label"],
            )
            for l in data.get("links", [])
        ]

        return GraphData(
            nodes=nodes,
            links=links,
            error=data.get("error"),
        )

    def search(
        self,
        query: str,
        user_id: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Search memories - find relevant information.
        
        Examples:
            # Simple search
            results = client.search("user preferences")
            
            # With user ID (for B2B apps)
            results = client.search("user preferences", user_id="user_123")
            
            # With limit
            results = client.search("user preferences", limit=5)
        
        Args:
            query: Search query
            user_id: Optional end user ID filter
            limit: Maximum results (1-50, default: 10)
            
        Returns:
            Dict with 'success', 'count', and 'results' keys
        """
        if not query or not query.strip():
            raise ValidationError("Search query is required")
        
        if not isinstance(limit, int) or limit < 1 or limit > 50:
            raise ValidationError("Limit must be between 1 and 50")
        
        params = {
            "query": query,
            "limit": limit,
            "mode": "hybrid",  # Best default mode - user doesn't need to know
        }
        if user_id:
            params["user_id"] = user_id
        
        response = self._make_request('GET', f"{self.base_url}/memories/search", params=params)
        data = self._handle_response(response)
        
        return {
            "success": data.get("success", True),
            "count": len(data.get("results", [])),
            "results": data.get("results", [])
        }

    # Legacy methods - kept for backward compatibility but deprecated
    def add_conversation(self, user_message: str, assistant_message: str, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> CreateMemoryResponse:
        """Deprecated: Use add() instead"""
        return self.add([{"role": "user", "content": user_message}, {"role": "assistant", "content": assistant_message}], user_id=user_id, metadata=metadata)

    def add_message(self, message: str, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> CreateMemoryResponse:
        """Deprecated: Use add() instead"""
        return self.add(message, user_id=user_id, metadata=metadata)

    def get_user_memories(self, user_id: str, limit: int = 20) -> ListMemoriesResponse:
        """Deprecated: Use list_memories() instead"""
        return self.list_memories(user_id=user_id, limit=limit)

    def get_personal_memories(self, limit: int = 20) -> ListMemoriesResponse:
        """Deprecated: Use list_memories() instead"""
        return self.list_memories(user_id="self", limit=limit)

    def get_all_memories(self, limit: int = 20) -> ListMemoriesResponse:
        """Deprecated: Use list_memories() instead"""
        return self.list_memories(user_id="all", limit=limit)

    def search_memories(
        self,
        query: str,
        user_id: Optional[str] = None,
        limit: int = 10,
        **kwargs  # Accept but ignore legacy params like mode, threshold, etc.
    ) -> Dict[str, Any]:
        """Deprecated: Use search() instead - simpler API"""
        return self.search(query, user_id=user_id, limit=limit)
        params = {
            "query": query,
            "limit": limit,
            "mode": mode,
        }
        
        if user_id:
            params["user_id"] = user_id
        
        # Metadata filters (JSONB column)
        if agent_id:
            params["agent_id"] = agent_id
        if conversation_id:
            params["conversation_id"] = conversation_id
        if session_id:
            params["session_id"] = session_id
        if team_id:
            params["team_id"] = team_id
        
        if memory_type:
            params["memory_type"] = memory_type
        if min_confidence is not None:
            params["min_confidence"] = min_confidence
        if threshold is not None:
            params["threshold"] = threshold
        
        response = self._make_request('GET', f"{self.base_url}/memories/search", params=params)
        data = self._handle_response(response)
        
        # Return dict with mode included
        return {
            "success": data.get("success", True),
            "count": len(data.get("results", [])),
            "mode": data.get("mode", mode),
            "results": data.get("results", [])
        }

    # Serialization helpers

    def _serialize_message(self, message: Message) -> Dict[str, Any]:
        """Serialize Message to dict"""
        content = message.content
        
        if isinstance(content, str):
            serialized_content = content
        elif isinstance(content, list):
            serialized_content = [self._serialize_part(part) for part in content]
        else:
            serialized_content = self._serialize_part(content)

        return {
            "role": message.role,
            "content": serialized_content,
        }

    def _serialize_part(self, part) -> Dict[str, Any]:
        """Serialize message part to dict"""
        if hasattr(part, "type"):
            result = {"type": part.type}
            
            if part.type == "text":
                result["text"] = part.text
            elif part.type == "image":
                result["data"] = part.data
                result["mimeType"] = part.mime_type
            elif part.type == "document":
                result["data"] = part.data
                if part.mime_type:
                    result["mimeType"] = part.mime_type
            elif part.type == "audio":
                result["data"] = part.data
                if part.mime_type:
                    result["mimeType"] = part.mime_type
            
            return result
        
        return {"type": "text", "text": str(part)}

    def _deserialize_memory(self, data: Dict[str, Any]) -> Memory:
        """Deserialize memory from API response"""
        return Memory(
            id=data.get("id", ""),
            owner_clerk_id=data.get("owner_clerk_id") or data.get("owner_id") or "",
            end_user_id=data.get("end_user_id") or data.get("user_id"),
            content=data.get("content", ""),
            memory_type=data.get("memory_type", "fact"),
            confidence=data.get("confidence", 0.8),
            metadata=data.get("metadata", {}),
            source_type=data.get("source_type", "text"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", data.get("created_at", "")),
            embedding=data.get("embedding"),
        )

    # New methods

    def get_memory(self, memory_id: str) -> Memory:
        """
        Get a single memory by ID
        
        Args:
            memory_id: Memory ID to retrieve
            
        Returns:
            Memory object
            
        Raises:
            NotFoundError: If memory not found or GET endpoint not implemented
        """
        try:
            response = self._make_request('GET', f"{self.base_url}/memories/{memory_id}")
            data = self._handle_response(response)
            
            return self._deserialize_memory(data["memory"])
        except NotFoundError as e:
            # Provide helpful error message if endpoint doesn't exist
            raise NotFoundError(
                f"Memory not found or GET endpoint not implemented. Memory ID: {memory_id}",
                status_code=404,
                details={"memory_id": memory_id}
            )

    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        memory_type: Optional[str] = None,
        confidence: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Memory:
        """
        Update an existing memory
        
        Args:
            memory_id: Memory ID to update
            content: New content (optional)
            memory_type: New memory type (optional)
            confidence: New confidence score (optional)
            metadata: New metadata (optional)
            
        Returns:
            Updated Memory object
        """
        # Validate memory_id
        if not memory_id or not memory_id.strip():
            raise ValidationError("Memory ID is required")
        
        # Validate that at least one field is being updated
        if content is None and memory_type is None and confidence is None and metadata is None:
            raise ValidationError("At least one field must be provided for update")
        
        # Validate content if provided
        if content is not None and not content.strip():
            raise ValidationError("Content cannot be empty")
        
        # Validate confidence if provided
        if confidence is not None:
            if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
                raise ValidationError(
                    f"Invalid confidence: {confidence}. Must be a number between 0 and 1"
                )
        """
        Update an existing memory
        
        Args:
            memory_id: Memory ID to update
            content: New content (optional)
            memory_type: New memory type (optional)
            confidence: New confidence score (optional)
            metadata: New metadata (optional)
            
        Returns:
            Updated Memory object
        """
        updates = {}
        if content is not None:
            updates["content"] = content
        if memory_type is not None:
            updates["memory_type"] = memory_type
        if confidence is not None:
            updates["confidence"] = confidence
        if metadata is not None:
            updates["metadata"] = metadata

        response = self._make_request('PATCH', f"{self.base_url}/memories/{memory_id}", json=updates)
        data = self._handle_response(response)

        return self._deserialize_memory(data["memory"])

    def delete_memory(
        self,
        memory_id: str,
        hard: bool = False,
    ) -> Dict[str, Any]:
        """
        Delete a single memory
        
        Args:
            memory_id: Memory ID to delete
            hard: Permanently delete (True) or soft delete (False)
            
        Returns:
            Dict with deletion results
        """
        # Validate memory_id
        if not memory_id or not memory_id.strip():
            raise ValidationError("Memory ID is required")
        """
        Delete a single memory
        
        Args:
            memory_id: Memory ID to delete
            hard: Permanently delete (True) or soft delete (False)
            
        Returns:
            Dict with deletion results
        """
        params = {"hard": "true" if hard else "false"}
        response = self._make_request('DELETE', f"{self.base_url}/memories/{memory_id}", params=params)
        return self._handle_response(response)

    def delete_memories(
        self,
        memory_ids: List[str],
        hard: bool = False,
    ) -> Dict[str, Any]:
        """
        Delete multiple memories at once
        
        Args:
            memory_ids: List of memory IDs to delete
            hard: Permanently delete (True) or soft delete (False)
            
        Returns:
            Dict with deletion results
        """
        payload = {
            "memory_ids": memory_ids,
            "hard": hard,
        }

        response = self._make_request('DELETE', f"{self.base_url}/memories/batch", json=payload)
        return self._handle_response(response)



    def list_agent_memories(
        self,
        limit: int = 50,
        include_team: bool = True,
        include_project: bool = True,
    ) -> Dict[str, Any]:
        """
        List memories for the current agent
        
        Args:
            limit: Maximum results (1-100)
            include_team: Include team memories
            include_project: Include project memories
            
        Returns:
            Dict with agent memories
        """
        # Validate limit
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise ValidationError(
                f"Invalid limit: {limit}. Must be an integer between 1 and 100"
            )
        """
        List memories for the current agent
        
        Args:
            limit: Maximum results (1-100)
            include_team: Include team memories
            include_project: Include project memories
            
        Returns:
            Dict with agent memories
        """
        if not self.agent_id:
            raise Exception('Agent not initialized. Create a memory first or provide agent_name in constructor.')

        params = {
            "agent_id": self.agent_id,
            "limit": limit,
            "include_team": str(include_team).lower(),
            "include_project": str(include_project).lower()
        }

        response = self._make_request('GET', f"{self.base_url}/memories/agents", params=params)
        data = self._handle_response(response)

        # Deserialize memories in data
        if "data" in data:
            data["data"] = [self._deserialize_memory(m) for m in data["data"]]

        return data

    def detect_contradictions(
        self,
        content: str,
        user_id: Optional[str] = None,
        confidence: float = 0.8,
    ) -> Dict[str, Any]:
        """
        Detect if new content contradicts existing memories
        
        Args:
            content: New memory content to check
            user_id: Optional end user ID
            confidence: Confidence score for new content (0-1)
            
        Returns:
            Dict with contradiction detection results
        """
        # Validate content
        if not content or not content.strip():
            raise ValidationError("Content is required for contradiction detection")
        
        # Validate confidence
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            raise ValidationError(
                f"Invalid confidence: {confidence}. Must be a number between 0 and 1"
            )
        """
        Detect if new content contradicts existing memories
        
        Args:
            content: New memory content to check
            user_id: Optional end user ID
            confidence: Confidence score for new content (0-1)
            
        Returns:
            Dict with contradiction detection results
        """
        payload = {
            "content": content,
            "confidence": confidence,
        }
        if user_id is not None:
            payload["user_id"] = user_id

        response = self._make_request('POST', f"{self.base_url}/memories/detect-contradictions", json=payload)
        return self._handle_response(response)

    def update_belief(
        self,
        content: str,
        user_id: Optional[str] = None,
        confidence: float = 0.8,
        strategy: str = "auto",
        contradicting_memory_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update belief when new evidence contradicts existing memory
        
        Args:
            content: New memory content
            user_id: Optional end user ID
            confidence: Confidence score (0-1)
            strategy: Resolution strategy ('auto', 'supersede', 'merge', 'adjust', 'manual')
            contradicting_memory_id: Specific memory ID to update (optional)
            metadata: Optional metadata
            
        Returns:
            Dict with update results
        """
        # Validate content
        if not content or not content.strip():
            raise ValidationError("Content is required for belief update")
        
        # Validate confidence
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            raise ValidationError(
                f"Invalid confidence: {confidence}. Must be a number between 0 and 1"
            )
        
        # Validate strategy
        if strategy not in ['auto', 'supersede', 'merge', 'adjust', 'manual']:
            raise ValidationError(
                f'Invalid strategy: "{strategy}". Must be "auto", "supersede", "merge", "adjust", or "manual"'
            )
        """
        Update belief when new evidence contradicts existing memory
        
        Args:
            content: New memory content
            user_id: Optional end user ID
            confidence: Confidence score (0-1)
            strategy: Resolution strategy ('auto', 'supersede', 'merge', 'adjust', 'manual')
            contradicting_memory_id: Specific memory ID to update (optional)
            metadata: Optional metadata
            
        Returns:
            Dict with update results
        """
        payload = {
            "content": content,
            "confidence": confidence,
            "strategy": strategy,
        }
        if user_id is not None:
            payload["user_id"] = user_id
        if contradicting_memory_id is not None:
            payload["contradicting_memory_id"] = contradicting_memory_id
        if metadata is not None:
            payload["metadata"] = metadata

        response = self._make_request('POST', f"{self.base_url}/memories/update-belief", json=payload)
        return self._handle_response(response)

    def get_memory_lineage(
        self,
        memory_id: str,
        format: str = "full",
    ) -> Dict[str, Any]:
        """
        Get complete provenance and lineage of a memory
        
        Args:
            memory_id: Memory ID to get lineage for
            format: Response format ('full', 'timeline', or 'chain')
            
        Returns:
            Dict with lineage information
        """
        # Validate memory_id
        if not memory_id or not memory_id.strip():
            raise ValidationError("Memory ID is required")
        
        # Validate format
        if format not in ['full', 'timeline', 'chain']:
            raise ValidationError(
                f'Invalid format: "{format}". Must be "full", "timeline", or "chain"'
            )
        """
        Get complete provenance and lineage of a memory
        
        Args:
            memory_id: Memory ID to get lineage for
            format: Response format ('full', 'timeline', or 'chain')
            
        Returns:
            Dict with lineage information
        """
        params = {"format": format}
        
        response = self._make_request('GET', f"{self.base_url}/memories/{memory_id}/lineage", params=params)
        return self._handle_response(response)

    def reflect_on_memories(
        self,
        time_window_days: int = 7,
        analysis_depth: str = "shallow",
        dry_run: bool = False,
        min_pattern_strength: float = 0.7,
        use_batch: bool = False,
    ) -> Dict[str, Any]:
        """
        Run reflection analysis on memories to generate insights
        
        Automatically uses batch API for >100 memories (50% cost savings)
        
        Args:
            time_window_days: Number of days to analyze (1-90)
            analysis_depth: 'shallow' or 'deep' analysis
            dry_run: Preview insights without storing
            min_pattern_strength: Minimum pattern strength (0-1)
            use_batch: Force batch mode even for small memory sets
            
        Returns:
            Dict with reflection results or batch job info
        """
        # Validate time_window_days
        if not isinstance(time_window_days, int) or time_window_days < 1 or time_window_days > 90:
            raise ValidationError(
                f"Invalid time_window_days: {time_window_days}. Must be an integer between 1 and 90"
            )
        
        # Validate analysis_depth
        if analysis_depth not in ['shallow', 'deep']:
            raise ValidationError(
                f'Invalid analysis_depth: "{analysis_depth}". Must be "shallow" or "deep"'
            )
        
        # Validate min_pattern_strength
        if not isinstance(min_pattern_strength, (int, float)) or min_pattern_strength < 0 or min_pattern_strength > 1:
            raise ValidationError(
                f"Invalid min_pattern_strength: {min_pattern_strength}. Must be a number between 0 and 1"
            )
        """
        Run reflection analysis on memories to generate insights
        
        Automatically uses batch API for >100 memories (50% cost savings)
        
        Args:
            time_window_days: Number of days to analyze (1-90)
            analysis_depth: 'shallow' or 'deep' analysis
            dry_run: Preview insights without storing
            min_pattern_strength: Minimum pattern strength (0-1)
            use_batch: Force batch mode even for small memory sets
            
        Returns:
            Dict with reflection results or batch job info
        """
        payload = {
            "timeWindowDays": time_window_days,
            "analysisDepth": analysis_depth,
            "dryRun": dry_run,
            "minPatternStrength": min_pattern_strength,
            "useBatch": use_batch,
        }

        response = self._make_request('POST', f"{self.base_url}/memories/reflect", json=payload)
        return self._handle_response(response)

    def get_batch_job_status(
        self,
        job_id: str,
    ) -> Dict[str, Any]:
        """
        Get status of a batch job
        
        Args:
            job_id: Batch job ID from reflect or consolidate response
            
        Returns:
            Dict with job status and progress
        """
        # Validate job_id
        if not job_id or not job_id.strip():
            raise ValidationError("Job ID is required")
        """
        Get status of a batch job
        
        Args:
            job_id: Batch job ID from reflect or consolidate response
            
        Returns:
            Dict with job status and progress
        """
        response = self._make_request('GET', f"{self.base_url}/batch-jobs/{job_id}")
        return self._handle_response(response)

    def import_memories(
        self,
        memories: List[Dict[str, Any]],
        use_batch: bool = True,
    ) -> Dict[str, Any]:
        """
        Import memories from another platform
        
        Args:
            memories: List of memory objects to import
            use_batch: Use batch create for large imports (recommended)
            
        Returns:
            Dict with import results
        """
        if use_batch and len(memories) > 10:
            # Use batch create endpoint for efficiency
            return self.create_memories_batch(memories)
        else:
            # Use regular import endpoint
            payload = {
                "version": "1.0",
                "memories": memories,
            }

            response = self._make_request('POST', f"{self.base_url}/memories/import", json=payload)
            return self._handle_response(response)

    def create_memories_batch(
        self,
        memories: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Create multiple memories at once (batch operation)
        
        More efficient than creating memories one by one
        
        Args:
            memories: List of memory objects with content, metadata, etc.
            
        Returns:
            Dict with batch creation results
        """
        # Validate memories array
        if not memories or len(memories) == 0:
            raise ValidationError("At least one memory is required for batch creation")
        
        if len(memories) > 1000:
            raise ValidationError("Maximum 1000 memories per batch request")
        
        # Validate each memory
        for i, memory in enumerate(memories):
            if not isinstance(memory, dict):
                raise ValidationError(f"Memory at index {i} must be a dictionary")
            
            if 'content' not in memory or not str(memory.get('content', '')).strip():
                raise ValidationError(f"Memory at index {i} is missing content")
            
            if 'confidence' in memory:
                confidence = memory['confidence']
                if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
                    raise ValidationError(
                        f"Invalid confidence at index {i}: {confidence}. Must be between 0 and 1"
                    )
        """
        Create multiple memories at once (batch operation)
        
        More efficient than creating memories one by one
        
        Args:
            memories: List of memory objects with content, metadata, etc.
            
        Returns:
            Dict with batch creation results
        """
        # Use new batch create endpoint
        payload = {
            "memories": memories,
            "generate_embeddings": True,
        }
        
        response = self._make_request('POST', f"{self.base_url}/memories/batch/create", json=payload)
        return self._handle_response(response)

    def export_memories(
        self,
        format: str = "json",
        user_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        min_confidence: Optional[float] = None,
        include_embeddings: bool = False,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Export memories in bulk
        
        For large exports (>10k memories), creates a batch job
        
        Args:
            format: Export format ('json' or 'csv')
            user_id: Filter by user ID
            memory_type: Filter by memory type
            min_confidence: Minimum confidence threshold
            include_embeddings: Include embedding vectors
            date_from: Filter from date (ISO format)
            date_to: Filter to date (ISO format)
            
        Returns:
            Dict with export data or batch job info
        """
        payload = {
            "format": format,
        }
        
        if user_id is not None:
            payload["user_id"] = user_id
        if memory_type is not None:
            payload["memory_type"] = memory_type
        if min_confidence is not None:
            payload["min_confidence"] = min_confidence
        if include_embeddings:
            payload["include_embeddings"] = include_embeddings
        if date_from is not None:
            payload["date_from"] = date_from
        if date_to is not None:
            payload["date_to"] = date_to

        response = self._make_request('POST', f"{self.base_url}/memories/batch/export", json=payload)
        return self._handle_response(response)

    def cancel_batch_job(
        self,
        job_id: str,
    ) -> Dict[str, Any]:
        """
        Cancel a running or pending batch job
        
        Args:
            job_id: Batch job ID to cancel
            
        Returns:
            Dict with cancellation result
        """
        response = self._make_request('POST', f"{self.base_url}/batch-jobs/{job_id}/cancel")
        return self._handle_response(response)

    def retry_batch_job(
        self,
        job_id: str,
    ) -> Dict[str, Any]:
        """
        Retry a failed batch job
        
        Args:
            job_id: Batch job ID to retry
            
        Returns:
            Dict with new batch job info
        """
        response = self._make_request('POST', f"{self.base_url}/batch-jobs/{job_id}/retry")
        return self._handle_response(response)

    def generate_embeddings_batch(
        self,
        memory_ids: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        regenerate_all: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate or regenerate embeddings for memories
        
        Use cases:
        - Regenerate embeddings after model upgrade
        - Generate embeddings for imported memories
        - Fix missing embeddings
        
        Automatically uses batch API for >100 memories (50% cost savings)
        
        Args:
            memory_ids: Specific memory IDs to process (optional)
            user_id: Filter by user ID (optional)
            memory_type: Filter by memory type (optional)
            regenerate_all: Regenerate even if embeddings exist
            
        Returns:
            Dict with generation results or batch job info
        """
        payload = {
            "regenerate_all": regenerate_all,
        }
        
        if memory_ids is not None:
            payload["memory_ids"] = memory_ids
        if user_id is not None:
            payload["user_id"] = user_id
        if memory_type is not None:
            payload["memory_type"] = memory_type

        response = self._make_request('POST', f"{self.base_url}/memories/batch/embeddings", json=payload)
        return self._handle_response(response)

    def get_embedding_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about embeddings coverage
        
        Returns:
            Dict with embedding statistics and recommendations
        """
        response = self._make_request('GET', f"{self.base_url}/memories/batch/embeddings")
        return self._handle_response(response)

    def consolidate_memories(
        self,
        similarity_threshold: float = 0.90,
        check_redundancy: bool = True,
        dry_run: bool = False,
        use_batch: bool = False,
    ) -> Dict[str, Any]:
        """
        Consolidate duplicate or similar memories
        
        Automatically uses batch API for >500 memories (50% cost savings)
        
        Args:
            similarity_threshold: Similarity threshold (0-1)
            check_redundancy: Check for redundant memories
            dry_run: Preview consolidation without applying
            use_batch: Force batch mode
            
        Returns:
            Dict with consolidation results or batch job info
        """
        # Validate similarity_threshold
        if not isinstance(similarity_threshold, (int, float)) or similarity_threshold < 0 or similarity_threshold > 1:
            raise ValidationError(
                f"Invalid similarity_threshold: {similarity_threshold}. Must be a number between 0 and 1"
            )
        """
        Consolidate duplicate or similar memories
        
        Automatically uses batch API for >500 memories (50% cost savings)
        
        Args:
            similarity_threshold: Similarity threshold (0-1)
            check_redundancy: Check for redundant memories
            dry_run: Preview consolidation without applying
            use_batch: Force batch mode
            
        Returns:
            Dict with consolidation results or batch job info
        """
        payload = {
            "similarity_threshold": similarity_threshold,
            "check_redundancy": check_redundancy,
            "dry_run": dry_run,
            "use_batch": use_batch,
        }

        response = self._make_request('POST', f"{self.base_url}/memories/consolidate", json=payload)
        return self._handle_response(response)


    # Auto-maintenance configuration methods
    
    def configure_auto_consolidation(
        self,
        enabled: bool = True,
        frequency: str = "weekly",
        similarity_threshold: float = 0.95,
        notify_on_merge: bool = False,
    ) -> Dict[str, Any]:
        """
        Configure automatic memory consolidation
        
        Args:
            enabled: Enable/disable auto-consolidation
            frequency: 'daily', 'weekly', or 'monthly'
            similarity_threshold: Similarity threshold (0-1)
            notify_on_merge: Send notification when memories are merged
            
        Returns:
            Dict with updated configuration
        """
        payload = {
            "consolidation_enabled": enabled,
            "consolidation_frequency": frequency,
            "consolidation_similarity_threshold": similarity_threshold,
            "consolidation_notify_on_merge": notify_on_merge,
        }

        response = self._make_request('POST', f"{self.base_url}/auto-maintenance/config",
            json=payload
        )
        return self._handle_response(response)

    def configure_auto_reflection(
        self,
        enabled: bool = True,
        frequency: str = "weekly",
        time_window_days: int = 7,
        analysis_depth: str = "shallow",
        min_pattern_strength: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Configure automatic memory reflection
        
        Args:
            enabled: Enable/disable auto-reflection
            frequency: 'daily', 'weekly', or 'monthly'
            time_window_days: Number of days to analyze (1-90)
            analysis_depth: 'shallow' or 'deep'
            min_pattern_strength: Minimum pattern strength (0-1)
            
        Returns:
            Dict with updated configuration
        """
        payload = {
            "reflection_enabled": enabled,
            "reflection_frequency": frequency,
            "reflection_time_window_days": time_window_days,
            "reflection_analysis_depth": analysis_depth,
            "reflection_min_pattern_strength": min_pattern_strength,
        }

        response = self._make_request('POST', f"{self.base_url}/auto-maintenance/config",
            json=payload
        )
        return self._handle_response(response)

    def configure_auto_embeddings(
        self,
        enabled: bool = True,
        check_frequency: str = "daily",
    ) -> Dict[str, Any]:
        """
        Configure automatic embedding generation
        
        Args:
            enabled: Enable/disable auto-embedding generation
            check_frequency: 'daily' or 'weekly'
            
        Returns:
            Dict with updated configuration
        """
        payload = {
            "embedding_generation_enabled": enabled,
            "embedding_check_frequency": check_frequency,
        }

        response = self._make_request('POST', f"{self.base_url}/auto-maintenance/config",
            json=payload
        )
        return self._handle_response(response)

    def get_auto_maintenance_config(self) -> Dict[str, Any]:
        """
        Get current auto-maintenance configuration
        
        Returns:
            Dict with current configuration
        """
        response = self._make_request('GET', f"{self.base_url}/auto-maintenance/config")
        return self._handle_response(response)

    def update_auto_maintenance_config(
        self,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update auto-maintenance configuration
        
        Args:
            config: Configuration dictionary with any settings to update
            
        Returns:
            Dict with updated configuration
        """
        response = self._make_request('POST', f"{self.base_url}/auto-maintenance/config",
            json=config
        )
        return self._handle_response(response)

    def disable_auto_maintenance(self) -> Dict[str, Any]:
        """
        Disable all auto-maintenance features
        
        Returns:
            Dict with confirmation
        """
        payload = {
            "consolidation_enabled": False,
            "reflection_enabled": False,
            "embedding_generation_enabled": False,
        }

        response = self._make_request('POST', f"{self.base_url}/auto-maintenance/config",
            json=payload
        )
        return self._handle_response(response)

    def reset_auto_maintenance_config(self) -> Dict[str, Any]:
        """
        Reset auto-maintenance configuration to defaults
        
        Returns:
            Dict with confirmation
        """
        response = self._make_request('DELETE', f"{self.base_url}/auto-maintenance/config")
        return self._handle_response(response)


