"""CrewAI integration for Memory OS"""

from memorystack import MemoryStackClient
from typing import Optional


class CrewAIMemoryTool:
    """
    Memory tool for CrewAI agents
    
    Example:
        >>> from memorystack.integrations import CrewAIMemoryTool
        >>> from crewai import Agent, Tool
        >>> 
        >>> memory_tool_helper = CrewAIMemoryTool(api_key="your-key")
        >>> 
        >>> memory_tool = Tool(
        ...     name="search_memories",
        ...     description="Search user memories",
        ...     func=lambda q: memory_tool_helper.search(q, "user_123")
        ... )
        >>> 
        >>> agent = Agent(
        ...     role='Assistant',
        ...     tools=[memory_tool],
        ...     # ... other config
        ... )
    """
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize CrewAI memory tool
        
        Args:
            api_key: Memory OS API key
            base_url: Optional custom base URL
        """
        self.client = MemoryStackClient(api_key=api_key, base_url=base_url)
    
    def search(self, query: str, user_id: str, limit: int = 10) -> str:
        """
        Search memories for CrewAI tool
        
        Args:
            query: Search query (not used for filtering, just for context)
            user_id: User ID
            limit: Maximum results
            
        Returns:
            Formatted memory string
        """
        try:
            memories = self.client.list_memories(
                user_id=user_id,
                limit=limit
            )
            
            if not memories.results:
                return "No memories found."
            
            return "\n".join([
                f"[{m.memory_type}] {m.content}"
                for m in memories.results
            ])
        except Exception as e:
            return f"Error searching memories: {str(e)}"
    
    def save_crew_output(
        self,
        task_description: str,
        result: str,
        user_id: str
    ) -> None:
        """
        Save crew task output to memory
        
        Args:
            task_description: Description of the task
            result: Task result
            user_id: User ID
        """
        try:
            self.client.add_message(
                f"Crew task: {task_description}\nResult: {result}",
                user_id=user_id
            )
        except Exception as e:
            print(f"Error saving crew output: {e}")
    
    def get_learnings(self, user_id: str, limit: int = 20) -> str:
        """
        Get past learnings for crew improvement
        
        Args:
            user_id: User ID
            limit: Maximum results
            
        Returns:
            Formatted learnings string
        """
        try:
            memories = self.client.list_memories(
                user_id=user_id,
                memory_type="experience",
                limit=limit
            )
            
            return "\n".join([m.content for m in memories.results])
        except Exception as e:
            return f"Error getting learnings: {str(e)}"


