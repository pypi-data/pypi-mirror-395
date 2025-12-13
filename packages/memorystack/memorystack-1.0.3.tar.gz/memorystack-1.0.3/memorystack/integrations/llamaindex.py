"""LlamaIndex integration for Memory OS"""

from memorystack import MemoryStackClient
from typing import Optional


class LlamaIndexMemoryHelper:
    """
    LlamaIndex integration helper for Memory OS
    
    Example:
        >>> from memorystack.integrations import LlamaIndexMemoryHelper
        >>> from llama_index import VectorStoreIndex
        >>> 
        >>> helper = LlamaIndexMemoryHelper(api_key="your-key")
        >>> 
        >>> # Use in your LlamaIndex queries
        >>> context = helper.get_user_context("user_123")
        >>> # Add context to your queries
    """
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize LlamaIndex memory helper
        
        Args:
            api_key: Memory OS API key
            base_url: Optional custom base URL
        """
        self.client = MemoryStackClient(api_key=api_key, base_url=base_url)
    
    def get_user_context(
        self,
        user_id: str,
        limit: int = 10,
        min_confidence: float = 0.7
    ) -> str:
        """
        Get user context for LlamaIndex queries
        
        Args:
            user_id: User ID
            limit: Maximum memories
            min_confidence: Minimum confidence score
            
        Returns:
            Formatted context string
        """
        try:
            memories = self.client.list_memories(
                user_id=user_id,
                limit=limit,
                min_confidence=min_confidence
            )
            
            return "User Information:\n" + "\n".join([
                f"- {m.content}"
                for m in memories.results
            ])
        except Exception as e:
            print(f"Error getting context: {e}")
            return ""
    
    def save_query_result(
        self,
        query: str,
        response: str,
        user_id: str
    ) -> None:
        """
        Save query and response to Memory OS
        
        Args:
            query: User query
            response: System response
            user_id: User ID
        """
        try:
            self.client.add_conversation(query, response, user_id=user_id)
        except Exception as e:
            print(f"Error saving query result: {e}")
    
    def get_memories_as_documents(self, user_id: str, limit: int = 20) -> list:
        """
        Get memories formatted as LlamaIndex documents
        
        Args:
            user_id: User ID
            limit: Maximum memories
            
        Returns:
            List of memory contents
        """
        try:
            memories = self.client.list_memories(
                user_id=user_id,
                limit=limit
            )
            
            return [m.content for m in memories.results]
        except Exception as e:
            print(f"Error getting memories: {e}")
            return []


