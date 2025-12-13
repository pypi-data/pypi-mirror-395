# MemoryStack - Python SDK

Official Python SDK for [MemoryStack](https://memorystack.app) - The memory layer for AI applications.

[![PyPI](https://img.shields.io/pypi/v/memorystack)](https://pypi.org/project/memorystack/)
[![Website](https://img.shields.io/badge/Website-memorystack.app-purple)](https://memorystack.app)
[![Documentation](https://img.shields.io/badge/Docs-memorystack.app%2Fdocs-blue)](https://memorystack.app/docs)

## What is MemoryStack?

MemoryStack is a **semantic memory layer** that gives your AI applications persistent, searchable memory. Instead of losing context between conversations, your AI can:

- **Remember** user preferences, facts, and conversation history
- **Search** through memories using natural language
- **Learn** from past interactions to provide personalized responses
- **Scale** from personal assistants to multi-tenant B2B applications

Think of it as a brain for your AI - it stores information intelligently and retrieves it when needed.

## Installation

```bash
pip install memorystack
```

## Quick Start

```python
from memorystack import MemoryStackClient

client = MemoryStackClient(api_key="your-api-key")

# Store a memory
client.add("User prefers dark mode")

# Search memories
results = client.search("user preferences")
print(results["results"])
```

That's it! Two methods - `add()` and `search()` - handle 90% of use cases.

## Core API

### `add()` - Store Memories

The `add()` method accepts either a simple string or a list of messages:

```python
# Simple text
client.add("User likes Python")

# With user ID (for B2B apps)
client.add("User prefers morning meetings", user_id="user_123")

# Conversation format
client.add([
    {"role": "user", "content": "What is my favorite color?"},
    {"role": "assistant", "content": "Based on our conversations, you prefer blue!"}
])

# With metadata
client.add(
    "Important project deadline is Friday",
    user_id="user_123",
    metadata={"category": "work", "priority": "high"}
)
```

### `search()` - Find Memories

The `search()` method finds relevant memories using semantic search:

```python
# Simple search
results = client.search("user preferences")

# With user ID filter
results = client.search("favorite color", user_id="user_123")

# Limit results
results = client.search("meetings", limit=5)
```

## Common Use Cases

### Chatbot with Memory

```python
from memorystack import MemoryStackClient
from openai import OpenAI

memory = MemoryStackClient(api_key=os.environ["MEMORYSTACK_API_KEY"])
openai = OpenAI()

def chat(user_id: str, message: str) -> str:
    # Get relevant context from memory
    context = memory.search(message, user_id=user_id, limit=5)
    
    # Build prompt with memory context
    memory_context = "\n".join([f"- {m['content']}" for m in context["results"]])
    system_prompt = f"""You are a helpful assistant. Here's what you remember about this user:
{memory_context}"""

    # Generate response
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    reply = response.choices[0].message.content

    # Save conversation to memory
    memory.add([
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ], user_id=user_id)

    return reply
```

### Personal Assistant

```python
# Store preferences
client.add("I wake up at 6am every day")
client.add("I prefer coffee over tea")
client.add("My favorite restaurant is Olive Garden")

# Later, retrieve relevant info
results = client.search("morning routine")
# Returns: "I wake up at 6am every day"

results = client.search("food preferences")
# Returns: "My favorite restaurant is Olive Garden", "I prefer coffee over tea"
```

### Multi-Tenant B2B App

```python
# Each user has isolated memories
client.add("Prefers dark mode", user_id="alice_123")
client.add("Prefers light mode", user_id="bob_456")

# Search only returns that user's memories
alice_prefs = client.search("theme preference", user_id="alice_123")
# Returns: "Prefers dark mode"
```

## Additional Methods

While `add()` and `search()` cover most needs, the SDK also provides:

```python
# List all memories with pagination
memories = client.list_memories(limit=50)

# Get usage statistics
stats = client.get_stats()
print(f"Total memories: {stats.totals['total_memories']}")

# Update a memory
client.update_memory("memory-id", content="Updated content")

# Delete a memory
client.delete_memory("memory-id")
```

## Error Handling

```python
from memorystack import (
    MemoryStackError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)

try:
    client.add("Hello world")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded, retry later")
except ValidationError as e:
    print(f"Invalid input: {e.message}")
except MemoryStackError as e:
    print(f"Error: {e.message}")
```

## Configuration Options

```python
client = MemoryStackClient(
    api_key=os.environ["MEMORYSTACK_API_KEY"],
    
    # Optional settings
    base_url="https://www.memorystack.app",  # Custom API URL
    timeout=30,                               # Request timeout (seconds)
    enable_logging=True,                      # Enable debug logging
    
    # Retry configuration
    max_retries=3,
    retry_delay=1.0,
)
```

## Framework Integrations

### LangChain

```python
from memorystack import MemoryStackClient
from langchain.memory import ConversationBufferMemory

# Use MemoryStack as your LangChain memory backend
client = MemoryStackClient(api_key=os.environ["MEMORYSTACK_API_KEY"])

# Store conversation
client.add([
    {"role": "user", "content": "My name is Alice"},
    {"role": "assistant", "content": "Nice to meet you, Alice!"}
], user_id="alice")

# Retrieve for context
context = client.search("user name", user_id="alice")
```

### CrewAI

```python
from memorystack import MemoryStackClient
from crewai import Agent, Task, Crew

memory = MemoryStackClient(api_key=os.environ["MEMORYSTACK_API_KEY"])

# Agents can share memories
memory.add("Project deadline is next Friday", metadata={"team": "engineering"})

# Search shared context
context = memory.search("deadlines")
```

## Links

- 🌐 **Website**: https://memorystack.app
- 📚 **Documentation**: https://memorystack.app/docs
- 🚀 **Quick Start**: https://memorystack.app/docs/quickstart
- 💰 **Pricing**: https://memorystack.app/pricing
- 📧 **Support**: support@memorystack.app

## License

MIT
