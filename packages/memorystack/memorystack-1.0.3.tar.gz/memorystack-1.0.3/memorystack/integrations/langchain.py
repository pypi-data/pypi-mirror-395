"""LangChain integration for Memory OS"""

from typing import Any, Dict, List
from langchain.memory import BaseChatMemory
from memorystack import MemoryStackClient


class MemoryOSChatMemory(BaseChatMemory):
    """
    LangChain memory integration for Memory OS
    
    Example:
        >>> from memorystack.integrations import MemoryOSChatMemory
        >>> from langchain.chains import ConversationChain
        >>> from langchain.chat_models import ChatOpenAI
        >>> 
        >>> memory = MemoryOSChatMemory(
        ...     api_key="your-key",
        ...     user_id="user_123"
        ... )
        >>> 
        >>> chain = ConversationChain(
        ...     llm=ChatOpenAI(),
        ...     memory=memory
        ... )
        >>> 
        >>> response = chain.run("Hello!")
    """
    
    def __init__(
        self,
        api_key: str,
        user_id: str = None,
        base_url: str = None,
        memory_key: str = "history"
    ):
        super().__init__()
        self.client = MemoryStackClient(api_key=api_key, base_url=base_url)
        self.user_id = user_id
        self.memory_key = memory_key
    
    @property
    def memory_variables(self) -> List[str]:
        """Return memory variables"""
        return [self.memory_key]
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load conversation history from Memory OS
        
        Args:
            inputs: Input variables (not used)
            
        Returns:
            Dictionary with memory history
        """
        try:
            memories = self.client.list_memories(
                user_id=self.user_id,
                limit=10,
                order="desc"
            )
            
            # Format memories as conversation history
            history = "\n".join([
                f"[{m.memory_type}] {m.content}"
                for m in memories.results
            ])
            
            return {self.memory_key: history}
        except Exception as e:
            print(f"Error loading memories: {e}")
            return {self.memory_key: ""}
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """
        Save conversation to Memory OS
        
        Args:
            inputs: Input dictionary with user message
            outputs: Output dictionary with AI response
        """
        try:
            user_message = inputs.get("input") or inputs.get("question") or ""
            ai_message = outputs.get("output") or outputs.get("answer") or ""
            
            if user_message and ai_message:
                self.client.add_conversation(
                    user_message,
                    ai_message,
                    user_id=self.user_id
                )
        except Exception as e:
            print(f"Error saving context: {e}")
    
    def clear(self) -> None:
        """Clear memory (no-op for now)"""
        # Memory OS doesn't support bulk delete yet
        pass


