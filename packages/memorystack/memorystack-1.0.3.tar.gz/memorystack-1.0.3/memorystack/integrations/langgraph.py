"""LangGraph integration for Memory OS"""

from typing import TypedDict, Any, Dict
from memorystack import MemoryStackClient


class MemoryOSStateManager:
    """
    LangGraph state manager with Memory OS integration
    
    Example:
        >>> from memorystack.integrations import MemoryOSStateManager
        >>> from langgraph.graph import StateGraph
        >>> 
        >>> manager = MemoryOSStateManager(
        ...     api_key="your-key",
        ...     user_id="user_123"
        ... )
        >>> 
        >>> # Use in your LangGraph nodes
        >>> def agent_node(state):
        ...     context = manager.load_context(state["user_id"])
        ...     # ... your agent logic
        ...     manager.save_interaction(user_msg, ai_response, state["user_id"])
    """
    
    def __init__(self, api_key: str, user_id: str = None, base_url: str = None):
        """
        Initialize LangGraph state manager
        
        Args:
            api_key: Memory OS API key
            user_id: Optional default user ID
            base_url: Optional custom base URL
        """
        self.client = MemoryStackClient(api_key=api_key, base_url=base_url)
        self.default_user_id = user_id
    
    def load_context(self, user_id: str = None, limit: int = 10) -> str:
        """
        Load memory context for LangGraph state
        
        Args:
            user_id: User ID (uses default if not provided)
            limit: Maximum number of memories to load
            
        Returns:
            Formatted context string
        """
        uid = user_id or self.default_user_id
        
        try:
            memories = self.client.list_memories(
                user_id=uid,
                limit=limit,
                order="desc"
            )
            
            return "\n".join([
                f"[{m.memory_type}] {m.content}"
                for m in memories.results
            ])
        except Exception as e:
            print(f"Error loading context: {e}")
            return ""
    
    def save_interaction(
        self,
        user_message: str,
        ai_response: str,
        user_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Save agent interaction to Memory OS
        
        Args:
            user_message: User's message
            ai_response: Agent's response
            user_id: User ID (uses default if not provided)
            metadata: Optional metadata
        """
        uid = user_id or self.default_user_id
        
        try:
            self.client.create_memory(
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": ai_response}
                ],
                user_id=uid,
                metadata=metadata
            )
        except Exception as e:
            print(f"Error saving interaction: {e}")
    
    def get_memories_by_type(
        self,
        memory_type: str,
        user_id: str = None,
        limit: int = 10
    ) -> list:
        """
        Get memories filtered by type
        
        Args:
            memory_type: Type of memory (preference, fact, etc.)
            user_id: User ID
            limit: Maximum results
            
        Returns:
            List of memory objects
        """
        uid = user_id or self.default_user_id
        
        try:
            memories = self.client.list_memories(
                user_id=uid,
                memory_type=memory_type,
                limit=limit
            )
            return memories.results
        except Exception as e:
            print(f"Error getting memories: {e}")
            return []


