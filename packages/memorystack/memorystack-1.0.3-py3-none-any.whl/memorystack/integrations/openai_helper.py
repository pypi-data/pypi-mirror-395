"""OpenAI integration helper for Memory OS"""

from typing import Optional, Generator
from memorystack import MemoryStackClient


class OpenAIWithMemory:
    """
    OpenAI integration helper for Memory OS
    
    Example:
        >>> from memorystack.integrations import OpenAIWithMemory
        >>> from openai import OpenAI
        >>> 
        >>> helper = OpenAIWithMemory(
        ...     memory_api_key="your-memory-key",
        ...     openai_client=OpenAI()
        ... )
        >>> 
        >>> response = helper.chat(
        ...     message="What are my preferences?",
        ...     user_id="user_123"
        ... )
    """
    
    def __init__(
        self,
        memory_api_key: str,
        openai_client,
        base_url: Optional[str] = None
    ):
        """
        Initialize OpenAI with Memory helper
        
        Args:
            memory_api_key: Memory OS API key
            openai_client: Initialized OpenAI client
            base_url: Optional custom Memory OS base URL
        """
        self.memory_client = MemoryStackClient(
            api_key=memory_api_key,
            base_url=base_url
        )
        self.openai_client = openai_client
    
    def chat(
        self,
        message: str,
        user_id: Optional[str] = None,
        model: str = "gpt-4",
        system_prompt: str = "You are a helpful assistant.",
        max_memories: int = 5
    ) -> str:
        """
        Chat with OpenAI using Memory OS context
        
        Args:
            message: User message
            user_id: Optional user ID for memory isolation
            model: OpenAI model to use
            system_prompt: System prompt
            max_memories: Maximum number of memories to load
            
        Returns:
            AI response string
        """
        # Get memories for context
        memories = self.memory_client.list_memories(
            user_id=user_id,
            limit=max_memories,
            order="desc"
        )
        
        # Build context from memories
        context = "\n".join([
            f"[{m.memory_type}] {m.content}"
            for m in memories.results
        ])
        
        # Call OpenAI with context
        completion = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"{system_prompt}\n\nContext about the user:\n{context}"
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        
        ai_response = completion.choices[0].message.content or ""
        
        # Save conversation to Memory OS
        self.memory_client.add_conversation(message, ai_response, user_id=user_id)
        
        return ai_response
    
    def stream_chat(
        self,
        message: str,
        user_id: Optional[str] = None,
        model: str = "gpt-4",
        system_prompt: str = "You are a helpful assistant.",
        max_memories: int = 5
    ) -> Generator[str, None, None]:
        """
        Stream chat with OpenAI using Memory OS context
        
        Args:
            message: User message
            user_id: Optional user ID for memory isolation
            model: OpenAI model to use
            system_prompt: System prompt
            max_memories: Maximum number of memories to load
            
        Yields:
            Chunks of AI response
        """
        # Get memories for context
        memories = self.memory_client.list_memories(
            user_id=user_id,
            limit=max_memories,
            order="desc"
        )
        
        context = "\n".join([
            f"[{m.memory_type}] {m.content}"
            for m in memories.results
        ])
        
        # Stream OpenAI response
        stream = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"{system_prompt}\n\nContext:\n{context}"
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            stream=True
        )
        
        full_response = ""
        
        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            full_response += content
            yield content
        
        # Save after streaming completes
        self.memory_client.add_conversation(message, full_response, user_id=user_id)


