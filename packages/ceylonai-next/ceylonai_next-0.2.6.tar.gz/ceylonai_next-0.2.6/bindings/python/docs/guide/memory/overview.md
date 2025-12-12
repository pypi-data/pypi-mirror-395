# Memory System - Overview

Ceylon AI's memory system gives agents the ability to store, retrieve, and search information. This enables persistent knowledge, context retention, and RAG (Retrieval-Augmented Generation) patterns.

## Quick Start

```python
from ceylonai_next import InMemoryBackend, MemoryEntry, LlmAgent

# Create memory backend
memory = InMemoryBackend()

# Store information
entry = MemoryEntry("Ceylon is a Rust-based agent framework")
entry.with_metadata("category", "knowledge")
entry_id = memory.store(entry)

# Use with agent
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_memory(memory)
agent.build()

# Agent can now access stored information
response = agent.send_message("What is Ceylon?")
```

## Core Concepts

### Memory Entry

A **MemoryEntry** is a piece of information stored in memory:

```python
entry = MemoryEntry("Important information here")

# Add metadata for organization and searching
entry.with_metadata("category", "facts")
entry.with_metadata("importance", "high")
entry.with_metadata("source", "user")

# Set expiration (optional)
entry.with_ttl_seconds(3600)  # Expires in 1 hour

# Store it
entry_id = memory.store(entry)
```

**Key Features:**
- Content (text data)
- Metadata (key-value pairs)
- TTL (Time-To-Live) - automatic expiration
- Unique ID

### Memory Backend

A **Memory Backend** handles storage and retrieval:

```python
# In-memory storage (default)
memory = InMemoryBackend()

# With configuration
memory = InMemoryBackend.with_max_entries(1000)
memory = InMemoryBackend.with_ttl_seconds(7200)  # 2 hours default TTL
```

**Built-in Backends:**
- `InMemoryBackend`: Fast, in-process storage
- `SqliteBackend`: Persistent storage (coming soon)
- Custom backends: Implement your own

### Memory Query

**MemoryQuery** searches for stored information:

```python
from ceylonai_next import MemoryQuery

# Create a query
query = MemoryQuery()
query.with_filter("category", "facts")
query.with_filter("importance", "high")
query.with_limit(10)

# Execute search
results = memory.search(query)

for entry in results:
    print(entry.content)
    print(entry.metadata)
```

## Storage Operations

### Store Data

```python
# Simple storage
entry = MemoryEntry("Python is a programming language")
entry_id = memory.store(entry)

# With metadata
entry = MemoryEntry("Rust is fast and memory-safe")
entry.with_metadata("topic", "programming")
entry.with_metadata("language", "rust")
entry.with_metadata("verified", "true")
entry_id = memory.store(entry)

# With expiration
entry = MemoryEntry("Temporary note")
entry.with_ttl_seconds(300)  # Expires in 5 minutes
entry_id = memory.store(entry)
```

### Retrieve Data

```python
# By ID
entry = memory.get(entry_id)
if entry:
    print(entry.content)
    print(entry.metadata)
else:
    print("Entry not found or expired")

# By search
query = MemoryQuery()
query.with_filter("topic", "programming")
results = memory.search(query)
```

### Update Data

```python
# Retrieve, modify, and store again
entry = memory.get(entry_id)
if entry:
    # Create new entry with updated content
    updated = MemoryEntry(entry.content + " [Updated]")
    for key, value in entry.metadata.items():
        updated.with_metadata(key, value)
    updated.with_metadata("updated", "true")

    # Store with same ID (if backend supports updates)
    memory.store(updated)
```

### Delete Data

```python
# Delete single entry
success = memory.delete(entry_id)

# Clear all entries
memory.clear()
```

### Count Entries

```python
total = memory.count()
print(f"Total entries: {total}")
```

## Using with Agents

### Basic Integration

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry

# Create memory
memory = InMemoryBackend()

# Store knowledge
facts = [
    "Ceylon is built with Rust for high performance",
    "Ceylon supports multiple LLM providers",
    "Ceylon has built-in memory and RAG support"
]

for fact in facts:
    entry = MemoryEntry(fact)
    entry.with_metadata("type", "fact")
    memory.store(entry)

# Create agent with memory
agent = LlmAgent("knowledgeable_agent", "ollama::llama3.2:latest")
agent.with_system_prompt(
    "You are a knowledgeable assistant. "
    "Use information from your memory to answer questions accurately."
)
agent.with_memory(memory)
agent.build()

# Agent can access memories
response = agent.send_message("Tell me about Ceylon's features")
print(response)
```

### Conversational Memory

Store conversation history:

```python
class ConversationalAgent:
    def __init__(self, model="ollama::llama3.2:latest"):
        self.memory = InMemoryBackend()
        self.agent = LlmAgent("chatbot", model)
        self.agent.with_memory(self.memory)
        self.agent.with_system_prompt(
            "You are a friendly chatbot. Remember previous conversations."
        )
        self.agent.build()

    def chat(self, user_message):
        # Store user message
        user_entry = MemoryEntry(f"User: {user_message}")
        user_entry.with_metadata("type", "user_message")
        user_entry.with_metadata("timestamp", str(datetime.now()))
        self.memory.store(user_entry)

        # Get response
        response = self.agent.send_message(user_message)

        # Store agent response
        agent_entry = MemoryEntry(f"Assistant: {response}")
        agent_entry.with_metadata("type", "agent_response")
        agent_entry.with_metadata("timestamp", str(datetime.now()))
        self.memory.store(agent_entry)

        return response

# Usage
chatbot = ConversationalAgent()
print(chatbot.chat("Hi, my name is Alice"))
print(chatbot.chat("What's my name?"))  # Should remember
```

## Advanced Features

### Metadata Filtering

```python
# Complex metadata queries
query = MemoryQuery()
query.with_filter("category", "important")
query.with_filter("verified", "true")
query.with_filter("language", "python")
query.with_limit(20)

results = memory.search(query)
```

### TTL Management

```python
# Short-term memory
temp_entry = MemoryEntry("Temporary info")
temp_entry.with_ttl_seconds(300)  # 5 minutes
memory.store(temp_entry)

# Long-term memory
perm_entry = MemoryEntry("Permanent info")
# No TTL = never expires
memory.store(perm_entry)

# Custom TTL per entry
cache_entry = MemoryEntry("Cached data")
cache_entry.with_ttl_seconds(1800)  # 30 minutes
memory.store(cache_entry)
```

### Capacity Management

```python
# Create backend with limits
memory = InMemoryBackend.with_max_entries(100)

# LRU eviction when full
for i in range(150):
    entry = MemoryEntry(f"Entry {i}")
    memory.store(entry)

# Only the 100 most recent entries remain
print(memory.count())  # 100
```

## RAG (Retrieval-Augmented Generation)

Use memory for RAG patterns:

```python
from ceylonai_next import InMemoryBackend, MemoryEntry, MemoryQuery, LlmAgent

class RAGAgent:
    def __init__(self, knowledge_base: list):
        # Create memory with knowledge
        self.memory = InMemoryBackend()

        # Index knowledge base
        for idx, doc in enumerate(knowledge_base):
            entry = MemoryEntry(doc)
            entry.with_metadata("doc_id", str(idx))
            entry.with_metadata("indexed", "true")
            self.memory.store(entry)

        # Create LLM agent
        self.agent = LlmAgent("rag_agent", "ollama::llama3.2:latest")
        self.agent.with_system_prompt(
            "You are a helpful assistant. "
            "Use the provided context from the knowledge base to answer questions. "
            "If information isn't in the knowledge base, say so."
        )
        self.agent.with_memory(self.memory)
        self.agent.build()

    def query(self, question: str):
        """Query the knowledge base and get an answer."""
        # The agent automatically retrieves relevant memories
        return self.agent.send_message(question)

# Usage
knowledge = [
    "Ceylon is a Rust-based agent framework for Python",
    "Ceylon supports Ollama, OpenAI, and Anthropic LLMs",
    "Ceylon has built-in memory backends for RAG",
    "Ceylon uses PyO3 for Python-Rust bindings"
]

rag = RAGAgent(knowledge)
answer = rag.query("What LLM providers does Ceylon support?")
print(answer)
```

## Custom Memory Backend

Implement your own storage:

```python
from ceylonai_next import Memory, MemoryEntry, MemoryQuery
from typing import List, Optional

class RedisMemory(Memory):
    """Custom memory backend using Redis."""

    def __init__(self, redis_client):
        self.redis = redis_client

    def store(self, entry: MemoryEntry) -> str:
        """Store entry in Redis."""
        entry_id = entry.id or str(uuid.uuid4())
        self.redis.set(
            f"memory:{entry_id}",
            json.dumps({
                "content": entry.content,
                "metadata": entry.metadata
            })
        )
        return entry_id

    def get(self, id: str) -> Optional[MemoryEntry]:
        """Retrieve entry from Redis."""
        data = self.redis.get(f"memory:{id}")
        if data:
            obj = json.loads(data)
            entry = MemoryEntry(obj["content"])
            for key, value in obj["metadata"].items():
                entry.with_metadata(key, value)
            return entry
        return None

    def search(self, query: MemoryQuery) -> List[MemoryEntry]:
        """Search entries (basic implementation)."""
        # Implement search logic
        pass

    def delete(self, id: str) -> bool:
        """Delete entry from Redis."""
        return bool(self.redis.delete(f"memory:{id}"))

    def clear(self):
        """Clear all entries."""
        for key in self.redis.keys("memory:*"):
            self.redis.delete(key)

    def count(self) -> int:
        """Count entries."""
        return len(self.redis.keys("memory:*"))

# Usage
import redis
redis_client = redis.Redis(host='localhost', port=6379)
memory = RedisMemory(redis_client)

agent = LlmAgent("agent", "ollama::llama3.2:latest")
agent.with_memory(memory)
agent.build()
```

## Best Practices

### 1. Organize with Metadata

```python
entry.with_metadata("category", "user_info")
entry.with_metadata("importance", "high")
entry.with_metadata("source", "user_input")
entry.with_metadata("created_at", str(datetime.now()))
```

### 2. Use Appropriate TTL

```python
# Session data - short TTL
entry.with_ttl_seconds(3600)  # 1 hour

# Cache data - medium TTL
entry.with_ttl_seconds(86400)  # 24 hours

# Knowledge - no TTL (permanent)
# Don't set TTL
```

### 3. Limit Entry Size

```python
# Truncate large content
content = large_text[:1000]  # Limit to 1000 chars
entry = MemoryEntry(content)
```

### 4. Handle Errors

```python
try:
    entry_id = memory.store(entry)
except Exception as e:
    print(f"Failed to store: {e}")

try:
    entry = memory.get(entry_id)
    if not entry:
        print("Entry not found or expired")
except Exception as e:
    print(f"Failed to retrieve: {e}")
```

## Next Steps

- [LLM Agents](../agents/llm-agents.md) - Combine memory with AI agents
- [Agents Overview](../agents/overview.md) - Agent fundamentals
- [Async Operations](../async/overview.md) - Use memory in concurrent operations
- [RAG Example](../../examples/rag/markdown-rag.md) - Build a knowledge-based system
- [Basic Memory Example](../../examples/memory/basic-memory.md) - Complete memory examples
