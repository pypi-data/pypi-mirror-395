# Memory System Example

## Overview

This example demonstrates **Ceylon's memory system** for storing, retrieving, and querying information. You'll learn how to use in-memory backends to persist agent state, conversation history, and any information your agents need to remember.

The memory system is fundamental for building agents that learn from interactions and maintain context over time.

## What You'll Learn

- **Memory Backends**: How to create and configure memory storage
- **Memory Entries**: Storing structured data with metadata
- **Basic Operations**: Store, retrieve, delete, and clear entries
- **Metadata Filtering**: Query entries based on custom metadata
- **TTL Expiration**: Automatically expire old entries
- **LRU Eviction**: Limit storage with automatic cleanup
- **Search Queries**: Find relevant entries efficiently
- **Realistic Patterns**: Conversation history and session management

## Prerequisites

Before starting, make sure you have:

- Python 3.8 or higher
- Ceylon SDK: `pip install ceylon`
- Basic understanding of Python dictionaries and lists
- Familiarity with agent concepts from simple-agent example
- Optional: Basic understanding of databases/caching

## Step-by-Step Guide

### Step 1: Understand Memory Concepts

The Ceylon memory system has three key components:

1. **Memory Backend**: Where entries are stored
   - `InMemoryBackend`: Stores data in RAM
   - Supports different configurations
   - Can limit size and set expiration

2. **Memory Entry**: Individual piece of information
   - Contains content (the actual data)
   - Has metadata (tags, categorization)
   - Tracks creation time and expiration
   - Gets a unique ID

3. **Memory Query**: Search criteria
   - Filter entries by metadata
   - Limit results
   - Find relevant information

### Step 2: Create a Memory Backend

```python
from ceylonai_next import InMemoryBackend, MemoryEntry

# Create a basic in-memory backend
backend = InMemoryBackend()
```

This creates a simple memory store in your program's RAM. It will:
- Keep all entries in memory
- Not persist to disk
- Grow until you delete entries or the program ends

### Step 3: Store Information

```python
from ceylonai_next import MemoryEntry

# Create an entry
entry = MemoryEntry("Hello, world!")

# Store it
entry_id = backend.store(entry)
print(f"Stored with ID: {entry_id}")
```

Breaking this down:

- **`MemoryEntry(content)`**: Create an entry with content
- **`backend.store(entry)`**: Save the entry, get back a unique ID
- **ID**: Used to retrieve the specific entry later

### Step 4: Retrieve Information

```python
# Get entry by ID
retrieved = backend.get(entry_id)

if retrieved:
    print(f"Content: {retrieved.content}")
    print(f"ID: {retrieved.id}")
    print(f"Created: {retrieved.created_at}")
else:
    print("Entry not found")
```

What you get back:

- **`content`**: The original data you stored
- **`id`**: The unique identifier
- **`created_at`**: When the entry was created
- **`metadata`**: Any tags/categories you added

### Step 5: Add Metadata

```python
entry = MemoryEntry("User said: What's the weather?")

# Add metadata tags
entry.with_metadata("speaker", "user")
entry.with_metadata("topic", "weather")
entry.with_metadata("user_id", "alice")

backend.store(entry)
```

Metadata allows you to:
- Categorize entries
- Filter results
- Track who said what
- Organize by topic
- Add any custom attributes

### Step 6: Query with Filters

```python
from ceylonai_next import MemoryQuery

# Create a query
query = MemoryQuery()

# Add filters
query.with_filter("speaker", "user")
query.with_filter("topic", "weather")

# Search
results = backend.search(query)

for entry in results:
    print(f"Found: {entry.content}")
```

This finds all entries where:
- `speaker` equals `"user"`
- AND `topic` equals `"weather"`

Multiple filters are combined with AND logic.

### Step 7: Configure Backend Options

```python
# Backend with max 50 entries (LRU eviction)
backend = InMemoryBackend.with_max_entries(50)

# Backend where entries auto-expire after 1 hour
backend = InMemoryBackend.with_ttl_seconds(3600)

# Set TTL on specific entry
entry = MemoryEntry("Temporary data")
entry.with_ttl_seconds(300)  # Expires in 5 minutes
backend.store(entry)
```

**Max Entries**: When full, oldest entries are automatically removed (LRU - Least Recently Used)

**TTL (Time To Live)**: Entries automatically disappear after time limit

### Step 8: Count and Clear

```python
# Count total entries
total = backend.count()
print(f"Total entries: {total}")

# Delete one entry by ID
deleted = backend.delete(entry_id)

# Clear all entries
backend.clear()
```

## Complete Code with Inline Comments

```python
#!/usr/bin/env python3
"""
Memory System Demo

This example demonstrates how to use Ceylon's memory system to store,
retrieve, and query information. Perfect for agents that need to remember
conversations, user preferences, or any persistent state.

Features demonstrated:
- Basic storage and retrieval
- Metadata filtering and search
- TTL (Time To Live) expiration
- Max entries with LRU eviction
- Realistic conversation history use case
"""

import time
from ceylonai_next import InMemoryBackend, MemoryEntry, MemoryQuery


def demo_basic_storage():
    """Demonstrate basic storage and retrieval"""
    print("=" * 60)
    print("DEMO 1: Basic Storage and Retrieval")
    print("=" * 60)

    # STEP 1: Create a memory backend
    backend = InMemoryBackend()

    # STEP 2: Create an entry with some content
    entry = MemoryEntry("Hello, world!")
    # STEP 3: Store the entry and get its ID
    entry_id = backend.store(entry)
    print(f"✓ Stored entry with ID: {entry_id}")

    # STEP 4: Retrieve the entry by ID
    retrieved = backend.get(entry_id)
    if retrieved:
        print(f"✓ Retrieved entry: {retrieved.content}")
        print(f"  - ID: {retrieved.id}")
        print(f"  - Created at: {retrieved.created_at}")
    else:
        print("✗ Entry not found")

    # STEP 5: Count total entries
    count = backend.count()
    print(f"✓ Total entries: {count}")

    print()


def demo_metadata_filtering():
    """Demonstrate metadata filtering and search"""
    print("=" * 60)
    print("DEMO 2: Metadata Filtering and Search")
    print("=" * 60)

    backend = InMemoryBackend()

    # STEP 1: Store multiple entries with different metadata
    # Each entry represents something different (user message, assistant response, etc.)
    entries = [
        ("User said: Hello!", {"type": "user", "user_id": "alice", "topic": "greeting"}),
        ("User said: How are you?", {"type": "user", "user_id": "alice", "topic": "conversation"}),
        ("Assistant: I'm doing well!", {"type": "assistant", "topic": "conversation"}),
        ("User said: What's the weather?", {"type": "user", "user_id": "bob", "topic": "weather"}),
        ("System: Session started", {"type": "system", "topic": "admin"}),
    ]

    # Store all entries
    for content, metadata in entries:
        entry = MemoryEntry(content)
        # Add each metadata tag
        for key, value in metadata.items():
            entry.with_metadata(key, value)
        backend.store(entry)
        print(f"✓ Stored: {content[:40]}")

    print(f"\n✓ Total entries: {backend.count()}\n")

    # STEP 2: Query 1 - Find all user messages
    print("Query 1: All user messages")
    query = MemoryQuery()
    query.with_filter("type", "user")
    results = backend.search(query)
    print(f"Found {len(results)} user messages:")
    for result in results:
        print(f"  - {result.content}")

    # STEP 3: Query 2 - Find alice's messages
    print("\nQuery 2: Alice's messages")
    query = MemoryQuery()
    query.with_filter("type", "user")
    query.with_filter("user_id", "alice")
    results = backend.search(query)
    print(f"Found {len(results)} messages from Alice:")
    for result in results:
        print(f"  - {result.content}")

    # STEP 4: Query 3 - Find conversation topics (limited to 2 results)
    print("\nQuery 3: Conversation messages (limit 2)")
    query = MemoryQuery()
    query.with_filter("topic", "conversation")
    query.with_limit(2)  # Only return first 2 results
    results = backend.search(query)
    print(f"Found {len(results)} conversation messages:")
    for result in results:
        metadata = result.metadata
        msg_type = metadata.get("type") if metadata else "unknown"
        print(f"  - [{msg_type}] {result.content}")

    print()


def demo_ttl_expiration():
    """Demonstrate TTL (Time To Live) expiration"""
    print("=" * 60)
    print("DEMO 3: TTL (Time To Live) Expiration")
    print("=" * 60)

    backend = InMemoryBackend()

    # STEP 1: Create an entry that expires automatically
    entry = MemoryEntry("This message will expire soon!")
    # Set TTL to 2 seconds
    entry.with_ttl_seconds(2)
    entry_id = backend.store(entry)
    print(f"✓ Stored entry with 2-second TTL: {entry_id}")

    # STEP 2: Immediately retrieve it (still exists)
    retrieved = backend.get(entry_id)
    if retrieved:
        print(f"✓ Entry exists: {retrieved.content}")
        print(f"  - Expires at: {retrieved.expires_at}")
        print(f"  - Is expired: {retrieved.is_expired()}")

    # STEP 3: Wait for expiration
    print("\nWaiting 3 seconds for entry to expire...")
    time.sleep(3)

    # STEP 4: Try to retrieve again (should be gone)
    retrieved = backend.get(entry_id)
    if retrieved:
        print(f"✗ Entry still exists (unexpected): {retrieved.content}")
    else:
        print("✓ Entry has expired and was removed")

    print()


def demo_max_entries_lru():
    """Demonstrate max entries with LRU eviction"""
    print("=" * 60)
    print("DEMO 4: Max Entries with LRU Eviction")
    print("=" * 60)

    # STEP 1: Create backend with max 3 entries
    # When we store more than 3, oldest entries are automatically removed
    backend = InMemoryBackend.with_max_entries(3)
    print("Created backend with max 3 entries")

    # STEP 2: Store 5 entries (oldest 2 will be evicted)
    for i in range(1, 6):
        entry = MemoryEntry(f"Entry {i}")
        entry.with_metadata("number", i)
        backend.store(entry)
        print(f"✓ Stored: Entry {i}")
        time.sleep(0.1)  # Small delay to ensure creation order

    # STEP 3: Check count
    count = backend.count()
    print(f"\n✓ Total entries after storing 5: {count} (max 3)")

    # STEP 4: Search to see which entries remain
    print("\nRemaining entries (newest 3):")
    query = MemoryQuery()
    results = backend.search(query)
    for result in results:
        print(f"  - {result.content}")

    print()


def demo_default_ttl():
    """Demonstrate backend with default TTL"""
    print("=" * 60)
    print("DEMO 5: Backend with Default TTL")
    print("=" * 60)

    # STEP 1: Create backend where all entries expire in 3 seconds by default
    backend = InMemoryBackend.with_ttl_seconds(3)
    print("Created backend with default 3-second TTL")

    # STEP 2: Store entries without specifying individual TTL
    for i in range(1, 4):
        entry = MemoryEntry(f"Auto-expiring entry {i}")
        backend.store(entry)
        print(f"✓ Stored: Auto-expiring entry {i}")

    print(f"\n✓ Total entries: {backend.count()}")

    # STEP 3: Wait for expiration
    print("\nWaiting 4 seconds for all entries to expire...")
    time.sleep(4)

    # STEP 4: Check if all are gone
    count = backend.count()
    print(f"✓ Total entries after expiration: {count}")

    print()


def demo_clear_and_delete():
    """Demonstrate delete and clear operations"""
    print("=" * 60)
    print("DEMO 6: Delete and Clear Operations")
    print("=" * 60)

    backend = InMemoryBackend()

    # STEP 1: Store some entries
    entry1 = MemoryEntry("Entry 1")
    entry2 = MemoryEntry("Entry 2")
    entry3 = MemoryEntry("Entry 3")

    id1 = backend.store(entry1)
    id2 = backend.store(entry2)
    id3 = backend.store(entry3)

    print(f"✓ Stored 3 entries")
    print(f"✓ Total entries: {backend.count()}")

    # STEP 2: Delete one specific entry
    deleted = backend.delete(id2)
    print(f"\n✓ Deleted entry {id2}: {deleted}")
    print(f"✓ Total entries: {backend.count()}")

    # STEP 3: Try to delete again (already gone)
    deleted = backend.delete(id2)
    print(f"✓ Try to delete again: {deleted} (already deleted)")

    # STEP 4: Clear all remaining entries
    print("\nClearing all entries...")
    backend.clear()
    print(f"✓ Total entries after clear: {backend.count()}")

    print()


def demo_conversation_history():
    """Realistic example: Conversation history storage"""
    print("=" * 60)
    print("DEMO 7: Realistic Use Case - Conversation History")
    print("=" * 60)

    # STEP 1: Create backend configured like a conversation store
    # Keep last 50 messages, auto-expire after 1 hour
    backend = InMemoryBackend.with_max_entries(50)

    # STEP 2: Simulate a realistic conversation
    conversation = [
        ("user", "alice", "Hello, I need help with Python"),
        ("assistant", "bot", "Hi Alice! I'd be happy to help with Python. What do you need?"),
        ("user", "alice", "How do I read a file?"),
        ("assistant", "bot", "You can use open() function with a file path..."),
        ("user", "alice", "Thanks! What about writing to a file?"),
        ("assistant", "bot", "To write, use open() with 'w' mode..."),
    ]

    # STEP 3: Store each message with metadata
    print("Storing conversation:")
    for speaker, user_id, message in conversation:
        entry = MemoryEntry(message)
        entry.with_metadata("speaker", speaker)
        entry.with_metadata("user_id", user_id)
        entry.with_metadata("session", "session_123")
        backend.store(entry)
        print(f"  [{speaker:9s}] {message}")

    # STEP 4: Retrieve full conversation
    print("\nRetrieving full conversation:")
    query = MemoryQuery()
    query.with_filter("session", "session_123")
    results = backend.search(query)

    print(f"Found {len(results)} messages in session:")
    for result in results:
        metadata = result.metadata
        speaker = metadata.get("speaker") if metadata else "unknown"
        print(f"  [{speaker:9s}] {result.content}")

    # STEP 5: Get only user messages (useful for analysis)
    print("\nRetrieving only user messages:")
    query = MemoryQuery()
    query.with_filter("speaker", "user")
    query.with_filter("session", "session_123")
    results = backend.search(query)

    print(f"Found {len(results)} user messages:")
    for result in results:
        print(f"  - {result.content}")

    print()


def main():
    """Run all demo functions"""
    # Print header
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "Ceylon Memory System Demo" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # Run each demo
    demo_basic_storage()
    demo_metadata_filtering()
    demo_ttl_expiration()
    demo_max_entries_lru()
    demo_default_ttl()
    demo_clear_and_delete()
    demo_conversation_history()

    # Print footer
    print("=" * 60)
    print("All demos completed successfully!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
```

## Running the Example

### 1. Set Up Your Environment

```bash
cd bindings/python/examples

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Ceylon
pip install ceylon
```

### 2. Run the Script

```bash
python demo_memory.py
```

### 3. Expected Output

```
╔══════════════════════════════════════════════════════════╗
║             Ceylon Memory System Demo                    ║
╚══════════════════════════════════════════════════════════╝

============================================================
DEMO 1: Basic Storage and Retrieval
============================================================

✓ Stored entry with ID: abc123
✓ Retrieved entry: Hello, world!
  - ID: abc123
  - Created at: 2024-11-22 10:15:32.123456
✓ Total entries: 1

============================================================
DEMO 2: Metadata Filtering and Search
============================================================

✓ Stored: User said: Hello!
✓ Stored: User said: How are you?
✓ Stored: Assistant: I'm doing well!
✓ Stored: User said: What's the weather?
✓ Stored: System: Session started

✓ Total entries: 5

Query 1: All user messages
Found 3 user messages:
  - User said: Hello!
  - User said: How are you?
  - User said: What's the weather?

Query 2: Alice's messages
Found 2 messages from Alice:
  - User said: Hello!
  - User said: How are you?

Query 3: Conversation messages (limit 2)
Found 2 conversation messages:
  - [user] User said: How are you?
  - [assistant] Assistant: I'm doing well!

============================================================
DEMO 3: TTL (Time To Live) Expiration
============================================================

✓ Stored entry with 2-second TTL: xyz789
✓ Entry exists: This message will expire soon!
  - Expires at: 2024-11-22 10:15:35.123456
  - Is expired: False

Waiting 3 seconds for entry to expire...
✓ Entry has expired and was removed

...
```

## Key Concepts Explained

### Memory Entry Structure

```python
# Create entry
entry = MemoryEntry("My content")

# Add metadata
entry.with_metadata("key1", "value1")
entry.with_metadata("key2", "value2")

# Optionally set TTL
entry.with_ttl_seconds(300)

# After storing, you get:
entry.id          # Unique identifier
entry.content     # Your original content
entry.created_at  # When it was stored
entry.metadata    # Dictionary of tags
entry.expires_at  # When it will auto-delete
```

### Backend Configurations

**Basic Backend**:
```python
backend = InMemoryBackend()
# No limits
# Entries stay forever (until deleted)
# Good for: Development, testing
```

**With Size Limit**:
```python
backend = InMemoryBackend.with_max_entries(100)
# Maximum 100 entries
# Oldest entries automatically removed when full
# Good for: Bounded memory usage
```

**With TTL**:
```python
backend = InMemoryBackend.with_ttl_seconds(3600)
# All entries expire after 1 hour
# Auto-cleanup of old entries
# Good for: Temporary session data
```

**Combined**:
```python
backend = InMemoryBackend.with_max_entries(100)
entry = MemoryEntry("data")
entry.with_ttl_seconds(300)
backend.store(entry)
# Expires in 300s OR when 101st entry is added
```

### Query Patterns

**Single Filter**:
```python
query = MemoryQuery()
query.with_filter("type", "user")
results = backend.search(query)
# All entries where type == "user"
```

**Multiple Filters (AND)**:
```python
query = MemoryQuery()
query.with_filter("type", "user")
query.with_filter("user_id", "alice")
results = backend.search(query)
# All entries where type == "user" AND user_id == "alice"
```

**With Limit**:
```python
query = MemoryQuery()
query.with_filter("topic", "news")
query.with_limit(10)
results = backend.search(query)
# First 10 entries matching filter
```

## Troubleshooting

### Issue: Can't find entries after storing

**Problem**: Entries stored but not found in searches

**Solutions**:
1. Check entry ID matches: `backend.get(exact_id)`
2. Verify metadata filters: Try removing filters
3. Check TTL hasn't expired: Look at `entry.expires_at`
4. Verify backend hasn't hit max_entries limit

### Issue: Entries disappear unexpectedly

**Problem**: Entries work initially but then vanish

**Solutions**:
1. Check backend's default TTL: `with_ttl_seconds()`
2. Check max_entries limit: `with_max_entries()`
3. Look for explicit delete calls: `backend.delete(id)`
4. Verify time hasn't elapsed if using TTL

### Issue: Memory usage keeps growing

**Problem**: Memory not being cleaned up

**Solutions**:
```python
# Add size limit
backend = InMemoryBackend.with_max_entries(1000)

# Or manually clean old entries
import time
old_cutoff = time.time() - 3600  # 1 hour ago
for entry in backend.search(MemoryQuery()):
    if entry.created_at < old_cutoff:
        backend.delete(entry.id)
```

### Issue: Queries return no results

**Problem**: Metadata filters seem to not work

**Solutions**:
1. Print metadata to debug: `print(result.metadata)`
2. Check filter values match exactly (case-sensitive)
3. Try removing all filters: `backend.search(MemoryQuery())`
4. Verify entries were actually stored

## Advanced Patterns

### Conversation Memory

```python
class ConversationMemory:
    def __init__(self, session_id: str):
        self.backend = InMemoryBackend.with_max_entries(100)
        self.session_id = session_id

    def add_user_message(self, user_id: str, message: str):
        entry = MemoryEntry(message)
        entry.with_metadata("speaker", "user")
        entry.with_metadata("user_id", user_id)
        entry.with_metadata("session", self.session_id)
        return self.backend.store(entry)

    def get_conversation(self):
        query = MemoryQuery()
        query.with_filter("session", self.session_id)
        return self.backend.search(query)

    def get_user_messages(self, user_id: str):
        query = MemoryQuery()
        query.with_filter("speaker", "user")
        query.with_filter("user_id", user_id)
        query.with_filter("session", self.session_id)
        return self.backend.search(query)
```

### Knowledge Base Cache

```python
class KnowledgeCache:
    def __init__(self, ttl_hours: int = 24):
        self.backend = InMemoryBackend.with_ttl_seconds(ttl_hours * 3600)

    def cache_fact(self, topic: str, fact: str, source: str):
        entry = MemoryEntry(fact)
        entry.with_metadata("topic", topic)
        entry.with_metadata("source", source)
        return self.backend.store(entry)

    def get_facts(self, topic: str):
        query = MemoryQuery()
        query.with_filter("topic", topic)
        return self.backend.search(query)
```

### Session Management

```python
class SessionManager:
    def __init__(self):
        # Keep 1000 sessions, auto-expire after 48 hours
        self.backend = InMemoryBackend.with_max_entries(1000)

    def create_session(self, user_id: str, session_data: dict):
        entry = MemoryEntry(str(session_data))
        entry.with_metadata("user_id", user_id)
        entry.with_metadata("type", "session")
        entry.with_ttl_seconds(48 * 3600)
        return self.backend.store(entry)

    def get_user_sessions(self, user_id: str):
        query = MemoryQuery()
        query.with_filter("user_id", user_id)
        query.with_filter("type", "session")
        return self.backend.search(query)
```

## Next Steps

Explore these related topics:

1. **RAG System** (`../rag/markdown-rag.md`): Build knowledge-based systems
2. **Async Operations** (`../async/async-llm.md`): Use memory with concurrent operations
3. **Agent Integration**: Combine memory with your custom agents
4. **Persistence**: Implement disk storage for production use

## Summary

The memory system example demonstrates:
- ✅ Creating and configuring memory backends
- ✅ Storing and retrieving entries with metadata
- ✅ Filtering and searching stored information
- ✅ TTL expiration for automatic cleanup
- ✅ LRU eviction for bounded memory
- ✅ Realistic conversation history patterns

The memory system is essential for agents that need to persist and recall information across interactions.
