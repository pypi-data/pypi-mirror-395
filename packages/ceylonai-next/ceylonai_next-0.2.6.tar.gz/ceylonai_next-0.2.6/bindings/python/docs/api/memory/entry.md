# MemoryEntry

The `MemoryEntry` class represents a single piece of information stored in an agent's memory. It supports content storage, metadata tagging, TTL-based expiration, and timestamp tracking.

## Class Signature

```python
class MemoryEntry(PyMemoryEntry):
    def __init__(self, content: str) -> None:
        ...
```

## Description

`MemoryEntry` is a Python wrapper around `PyMemoryEntry` that provides a fluent API for creating and configuring memory entries. Each entry is automatically assigned a unique ID and creation timestamp.

## Constructor

### `__init__(content: str)`

Creates a new memory entry with the given content.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | `str` | The content/data to store |

**Returns:** MemoryEntry instance

**Example:**
```python
from ceylonai_next import MemoryEntry

# Simple entry
entry = MemoryEntry("User said hello")

# Multi-line content
entry = MemoryEntry("""
Question: What is Python?
Answer: Python is a high-level programming language.
""")
```

## Properties

### `content: str`

Returns the entry's content.

**Type:** `str` (read-only)

**Example:**
```python
entry = MemoryEntry("Important fact")
print(entry.content)  # Output: Important fact
```

---

### `id: str`

Returns the unique identifier for this entry.

**Type:** `str` (read-only)

**Notes:**
- Automatically generated on creation
- Unique across all entries in a memory backend
- Can be used to retrieve specific entries

**Example:**
```python
entry = MemoryEntry("Some data")
entry_id = entry.id
print(f"Entry ID: {entry_id}")

# Later, retrieve using ID
backend = InMemoryBackend()
backend.store(entry)
retrieved = backend.get(entry_id)
```

---

### `metadata: Dict[str, Any]`

Returns the metadata dictionary for this entry.

**Type:** `Dict[str, Any]` (read-only)

**Example:**
```python
entry = MemoryEntry("User interaction")
entry.with_metadata("user_id", "alice")
entry.with_metadata("session", "s123")
entry.with_metadata("priority", 5)

metadata = entry.metadata
print(metadata)
# Output: {'user_id': 'alice', 'session': 's123', 'priority': 5}
```

---

### `created_at: str`

Returns the ISO 8601 creation timestamp.

**Type:** `str` (read-only)

**Example:**
```python
entry = MemoryEntry("Created now")
print(entry.created_at)  # Output: 2024-01-15T10:30:45.123Z
```

---

### `expires_at: str | None`

Returns the expiration timestamp if TTL is set, otherwise None.

**Type:** `str | None` (read-only)

**Example:**
```python
entry = MemoryEntry("Temporary data")
print(entry.expires_at)  # Output: None

entry.with_ttl_seconds(3600)
print(entry.expires_at)  # Output: 2024-01-15T11:30:45.123Z
```

## Methods

### `with_metadata(key: str, value: Any) -> MemoryEntry`

Add or update a metadata key-value pair.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | `str` | Metadata key |
| `value` | `Any` | Metadata value (typically str, int, float, bool) |

**Returns:** `MemoryEntry` - Returns self for method chaining

**Example:**
```python
entry = MemoryEntry("User conversation")

# Fluent API - chain multiple calls
entry.with_metadata("user_id", "alice") \
     .with_metadata("speaker", "user") \
     .with_metadata("sentiment", "positive") \
     .with_metadata("language", "en")

# Or call separately
entry = MemoryEntry("Another entry")
entry.with_metadata("type", "system_message")
entry.with_metadata("priority", 10)
```

---

### `with_ttl_seconds(seconds: int) -> MemoryEntry`

Set the Time-To-Live (TTL) for this entry in seconds.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `seconds` | `int` | Number of seconds until expiration |

**Returns:** `MemoryEntry` - Returns self for method chaining

**Notes:**
- Sets an expiration timestamp
- Entries expire based on this TTL
- Memory backends may clean up expired entries

**Example:**
```python
# Short-lived temporary data
temp_entry = MemoryEntry("Session token")
temp_entry.with_ttl_seconds(300)  # 5 minutes

# Long-lived important data
important_entry = MemoryEntry("Important note")
important_entry.with_ttl_seconds(86400)  # 24 hours

# No expiration (permanent)
permanent_entry = MemoryEntry("Permanent record")
# Don't call with_ttl_seconds() to keep it permanent
```

---

### `is_expired() -> bool`

Check if the entry has expired based on its TTL.

**Parameters:** None

**Returns:** `bool` - True if entry has expired, False otherwise

**Example:**
```python
import time
from ceylonai_next import MemoryEntry

# Create entry with short TTL
entry = MemoryEntry("Temporary")
entry.with_ttl_seconds(1)

print(entry.is_expired())  # Output: False

# Wait for expiration
time.sleep(2)

print(entry.is_expired())  # Output: True
```

## Complete Examples

### Example 1: Basic Entry Creation and Storage

```python
from ceylonai_next import MemoryEntry, InMemoryBackend

# Create entry
entry = MemoryEntry("Hello, World!")

# Store in backend
backend = InMemoryBackend()
entry_id = backend.store(entry)

# Retrieve
retrieved = backend.get(entry_id)
print(f"Content: {retrieved.content}")
print(f"ID: {retrieved.id}")
print(f"Created: {retrieved.created_at}")
```

### Example 2: Entry with Metadata

```python
from ceylonai_next import MemoryEntry, InMemoryBackend, MemoryQuery

# Create entry with metadata
entry = MemoryEntry("User asked about Python")
entry.with_metadata("user_id", "alice")
entry.with_metadata("topic", "programming")
entry.with_metadata("language", "python")
entry.with_metadata("helpfulness", 5)

# Store
backend = InMemoryBackend()
backend.store(entry)

# Search by metadata
query = MemoryQuery()
query.with_filter("user_id", "alice")
query.with_filter("topic", "programming")

results = backend.search(query)
for result in results:
    print(f"Entry: {result.content}")
    print(f"Metadata: {result.metadata}")
```

### Example 3: TTL and Expiration

```python
import time
from ceylonai_next import MemoryEntry, InMemoryBackend

backend = InMemoryBackend()

# Create permanent entry
perm = MemoryEntry("Keep this forever")
perm_id = backend.store(perm)

# Create temporary entry
temp = MemoryEntry("Delete me soon")
temp.with_ttl_seconds(2)
temp_id = backend.store(temp)

print(f"Count before: {backend.count()}")  # 2

# Immediately retrieve both
print(f"Permanent: {backend.get(perm_id) is not None}")  # True
print(f"Temporary: {backend.get(temp_id) is not None}")  # True

# Wait for expiration
time.sleep(3)

print(f"Count after: {backend.count()}")   # 1
print(f"Permanent: {backend.get(perm_id) is not None}")  # True
print(f"Temporary: {backend.get(temp_id) is not None}")  # False
```

### Example 4: Conversation History

```python
from ceylonai_next import MemoryEntry, InMemoryBackend, MemoryQuery

def create_message_entry(speaker, user_id, message, session_id):
    """Helper to create conversation message entries"""
    entry = MemoryEntry(message)
    entry.with_metadata("speaker", speaker)
    entry.with_metadata("user_id", user_id)
    entry.with_metadata("session_id", session_id)
    entry.with_metadata("type", "message")
    return entry

# Create memory backend
backend = InMemoryBackend.with_max_entries(1000)

# Simulate conversation
messages = [
    ("user", "alice", "Hello bot"),
    ("assistant", "bot", "Hi Alice! How can I help?"),
    ("user", "alice", "What's 2+2?"),
    ("assistant", "bot", "2+2 equals 4"),
    ("user", "bob", "Hey there"),
    ("assistant", "bot", "Hello Bob!"),
]

session_id = "session_001"

for speaker, user_id, message in messages:
    entry = create_message_entry(speaker, user_id, message, session_id)
    backend.store(entry)

# Query: Get all messages from Alice
query = MemoryQuery()
query.with_filter("user_id", "alice")
query.with_filter("session_id", session_id)
alice_messages = backend.search(query)

print(f"Alice's messages ({len(alice_messages)}):")
for entry in alice_messages:
    print(f"  {entry.content}")

# Query: Get all user messages
query = MemoryQuery()
query.with_filter("session_id", session_id)
query.with_filter("speaker", "user")
user_messages = backend.search(query)

print(f"\nAll user messages ({len(user_messages)}):")
for entry in user_messages:
    print(f"  [{entry.metadata['user_id']}]: {entry.content}")
```

### Example 5: Fluent Builder Pattern

```python
from ceylonai_next import MemoryEntry, InMemoryBackend

# Create complex entry using fluent API
entry = MemoryEntry("Technical discussion about memory systems") \
    .with_metadata("type", "documentation") \
    .with_metadata("category", "architecture") \
    .with_metadata("author", "system") \
    .with_metadata("complexity", "advanced") \
    .with_metadata("reviewed", True) \
    .with_ttl_seconds(86400)  # 24 hour expiration

# Store and verify
backend = InMemoryBackend()
entry_id = backend.store(entry)

retrieved = backend.get(entry_id)
print(f"Content: {retrieved.content}")
print(f"Metadata Keys: {list(retrieved.metadata.keys())}")
print(f"Expires At: {retrieved.expires_at}")
```

### Example 6: Memory Entry in LLM Agent

```python
import asyncio
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry, MemoryQuery

async def main():
    # Create backend and agent
    memory = InMemoryBackend()
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.with_memory(memory)
    agent.with_system_prompt(
        "You are a helpful assistant with memory. "
        "Use the memory system to store and recall information."
    )
    agent.build()

    # Have a conversation that uses memory
    messages = [
        "Remember: My name is Alice",
        "What's my name?",
        "I live in San Francisco",
        "Where do I live?",
    ]

    for msg in messages:
        print(f"User: {msg}")
        response = await agent.send_message_async(msg)
        print(f"Assistant: {response}\n")

    # Inspect memory directly
    print("=== Memory Contents ===")
    query = MemoryQuery()
    entries = memory.search(query)

    for entry in entries:
        print(f"- {entry.content[:50]}...")
        if entry.metadata:
            print(f"  Metadata: {entry.metadata}")

asyncio.run(main())
```

## Related APIs

- **[InMemoryBackend](./in-memory.md)** - Memory storage backend
- **[MemoryQuery](./memory-query.md)** - Query interface for searching memory
- **[Memory](./memory-interface.md)** - Custom memory interface

## See Also

- [Memory System Guide](../../guide/memory.md)
- [LLM Agent with Memory](../../guide/llm-agent-memory.md)
- [Memory Patterns](../../guide/memory-patterns.md)
- [Memory Examples](../../examples/memory-examples.md)
