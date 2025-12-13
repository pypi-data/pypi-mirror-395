"""Amazon Bedrock integration for Memory OS"""

import json
from memorystack import MemoryStackClient
from typing import Optional


class BedrockWithMemory:
    """
    Amazon Bedrock integration helper for Memory OS
    
    Example:
        >>> from memorystack.integrations import BedrockWithMemory
        >>> import boto3
        >>> 
        >>> bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        >>> 
        >>> helper = BedrockWithMemory(
        ...     memory_api_key="your-memory-key",
        ...     bedrock_client=bedrock
        ... )
        >>> 
        >>> response = helper.chat_claude(
        ...     message="What are my preferences?",
        ...     user_id="user_123"
        ... )
    """
    
    def __init__(
        self,
        memory_api_key: str,
        bedrock_client,
        base_url: Optional[str] = None
    ):
        """
        Initialize Bedrock with Memory helper
        
        Args:
            memory_api_key: Memory OS API key
            bedrock_client: Initialized boto3 bedrock-runtime client
            base_url: Optional custom Memory OS base URL
        """
        self.memory_client = MemoryStackClient(
            api_key=memory_api_key,
            base_url=base_url
        )
        self.bedrock_client = bedrock_client
    
    def chat_claude(
        self,
        message: str,
        user_id: Optional[str] = None,
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        system_prompt: str = "You are a helpful assistant.",
        max_memories: int = 5,
        max_tokens: int = 1000
    ) -> str:
        """
        Chat with Claude via Bedrock using Memory OS context
        
        Args:
            message: User message
            user_id: Optional user ID
            model_id: Bedrock model ID
            system_prompt: System prompt
            max_memories: Maximum memories to load
            max_tokens: Maximum tokens in response
            
        Returns:
            AI response string
        """
        # Get memories
        memories = self.memory_client.list_memories(
            user_id=user_id,
            limit=max_memories,
            order="desc"
        )
        
        context = "\n".join([
            f"[{m.memory_type}] {m.content}"
            for m in memories.results
        ])
        
        # Prepare Claude request
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": f"{system_prompt}\n\nContext:\n{context}\n\nUser: {message}"
                }
            ]
        }
        
        # Invoke Claude
        response = self.bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )
        
        result = json.loads(response['body'].read())
        ai_response = result['content'][0]['text']
        
        # Save to Memory OS
        self.memory_client.add_conversation(message, ai_response, user_id=user_id)
        
        return ai_response
    
    def chat_llama(
        self,
        message: str,
        user_id: Optional[str] = None,
        model_id: str = "meta.llama3-70b-instruct-v1:0",
        max_memories: int = 5,
        max_gen_len: int = 512
    ) -> str:
        """
        Chat with Llama via Bedrock using Memory OS context
        
        Args:
            message: User message
            user_id: Optional user ID
            model_id: Bedrock model ID
            max_memories: Maximum memories to load
            max_gen_len: Maximum generation length
            
        Returns:
            AI response string
        """
        # Get context
        memories = self.memory_client.list_memories(
            user_id=user_id,
            limit=max_memories,
            order="desc"
        )
        
        context = "\n".join([m.content for m in memories.results])
        
        # Prepare Llama request
        payload = {
            "prompt": f"Context: {context}\n\nUser: {message}\n\nAssistant:",
            "max_gen_len": max_gen_len,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        # Invoke Llama
        response = self.bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )
        
        result = json.loads(response['body'].read())
        ai_response = result['generation']
        
        # Save to Memory OS
        self.memory_client.add_conversation(message, ai_response, user_id=user_id)
        
        return ai_response


