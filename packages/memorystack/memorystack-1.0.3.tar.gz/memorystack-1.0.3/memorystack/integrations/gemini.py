"""Google Gemini integration for Memory OS"""

from memorystack import MemoryStackClient
from typing import Optional


class GeminiWithMemory:
    """
    Google Gemini integration helper for Memory OS
    
    Example:
        >>> from memorystack.integrations import GeminiWithMemory
        >>> import google.generativeai as genai
        >>> 
        >>> genai.configure(api_key="your-google-key")
        >>> 
        >>> helper = GeminiWithMemory(
        ...     memory_api_key="your-memory-key",
        ...     model_name="gemini-pro"
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
        model_name: str = "gemini-pro",
        base_url: Optional[str] = None
    ):
        """
        Initialize Gemini with Memory helper
        
        Args:
            memory_api_key: Memory OS API key
            model_name: Gemini model name
            base_url: Optional custom Memory OS base URL
        """
        self.memory_client = MemoryStackClient(
            api_key=memory_api_key,
            base_url=base_url
        )
        self.model_name = model_name
        
        # Import here to avoid requiring google-generativeai for all users
        import google.generativeai as genai
        self.genai = genai
        self.model = genai.GenerativeModel(model_name)
    
    def chat(
        self,
        message: str,
        user_id: Optional[str] = None,
        system_prompt: str = "You are a helpful assistant.",
        max_memories: int = 5
    ) -> str:
        """
        Chat with Gemini using Memory OS context
        
        Args:
            message: User message
            user_id: Optional user ID
            system_prompt: System prompt
            max_memories: Maximum memories to load
            
        Returns:
            AI response string
        """
        # Get memories for context
        memories = self.memory_client.list_memories(
            user_id=user_id,
            limit=max_memories,
            order="desc"
        )
        
        # Build context
        context = "\n".join([
            f"[{m.memory_type}] {m.content}"
            for m in memories.results
        ])
        
        # Create prompt with context
        prompt = f"{system_prompt}\n\nContext about the user:\n{context}\n\nUser: {message}"
        
        # Generate response
        response = self.model.generate_content(prompt)
        ai_response = response.text
        
        # Save to Memory OS
        self.memory_client.add_conversation(message, ai_response, user_id=user_id)
        
        return ai_response
    
    def stream_chat(
        self,
        message: str,
        user_id: Optional[str] = None,
        system_prompt: str = "You are a helpful assistant.",
        max_memories: int = 5
    ):
        """
        Stream chat with Gemini using Memory OS context
        
        Args:
            message: User message
            user_id: Optional user ID
            system_prompt: System prompt
            max_memories: Maximum memories to load
            
        Yields:
            Chunks of AI response
        """
        # Get context
        memories = self.memory_client.list_memories(
            user_id=user_id,
            limit=max_memories,
            order="desc"
        )
        
        context = "\n".join([
            f"[{m.memory_type}] {m.content}"
            for m in memories.results
        ])
        
        prompt = f"{system_prompt}\n\nContext: {context}\n\nUser: {message}"
        
        # Stream response
        response = self.model.generate_content(prompt, stream=True)
        
        full_response = ""
        for chunk in response:
            text = chunk.text
            full_response += text
            yield text
        
        # Save after streaming
        self.memory_client.add_conversation(message, full_response, user_id=user_id)


