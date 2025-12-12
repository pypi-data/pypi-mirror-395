#!/usr/bin/env python3
"""
Memory System Demo

This example demonstrates how to use Ceylon's memory system to store,
retrieve, and query information. The memory system provides a flexible
way for agents to persist and recall information.

Features demonstrated:
- Basic storage and retrieval
- Metadata filtering
- TTL (Time To Live) expiration
- Max entries with LRU eviction
- Search queries
"""

import time
from ceylonai_next import InMemoryBackend, MemoryEntry, MemoryQuery


def demo_basic_storage():
    """Demonstrate basic storage and retrieval"""
    print("=" * 60)
    print("DEMO 1: Basic Storage and Retrieval")
    print("=" * 60)

    # Create a memory backend
    backend = InMemoryBackend()

    # Create and store a memory entry
    entry = MemoryEntry("Hello, world!")
    entry_id = backend.store(entry)
    print(f"✓ Stored entry with ID: {entry_id}")

    # Retrieve the entry
    retrieved = backend.get(entry_id)
    if retrieved:
        print(f"✓ Retrieved entry: {retrieved.content}")
        print(f"  - ID: {retrieved.id}")
        print(f"  - Created at: {retrieved.created_at}")
    else:
        print("✗ Entry not found")

    # Count entries
    count = backend.count()
    print(f"✓ Total entries: {count}")

    print()


def demo_metadata_filtering():
    """Demonstrate metadata filtering and search"""
    print("=" * 60)
    print("DEMO 2: Metadata Filtering and Search")
    print("=" * 60)

    backend = InMemoryBackend()

    # Store multiple entries with different metadata
    entries = [
        ("User said: Hello!", {"type": "user", "user_id": "alice", "topic": "greeting"}),
        ("User said: How are you?", {"type": "user", "user_id": "alice", "topic": "conversation"}),
        ("Assistant: I'm doing well!", {"type": "assistant", "topic": "conversation"}),
        ("User said: What's the weather?", {"type": "user", "user_id": "bob", "topic": "weather"}),
        ("System: Session started", {"type": "system", "topic": "admin"}),
    ]

    for content, metadata in entries:
        entry = MemoryEntry(content)
        for key, value in metadata.items():
            entry.with_metadata(key, value)
        backend.store(entry)
        print(f"✓ Stored: {content[:40]}")

    print(f"\n✓ Total entries: {backend.count()}\n")

    # Query 1: Find all user messages
    print("Query 1: All user messages")
    query = MemoryQuery()
    query.with_filter("type", "user")
    results = backend.search(query)
    print(f"Found {len(results)} user messages:")
    for result in results:
        print(f"  - {result.content}")

    # Query 2: Find alice's messages
    print("\nQuery 2: Alice's messages")
    query = MemoryQuery()
    query.with_filter("type", "user")
    query.with_filter("user_id", "alice")
    results = backend.search(query)
    print(f"Found {len(results)} messages from Alice:")
    for result in results:
        print(f"  - {result.content}")

    # Query 3: Find conversation-related messages (limit to 2)
    print("\nQuery 3: Conversation messages (limit 2)")
    query = MemoryQuery()
    query.with_filter("topic", "conversation")
    query.with_limit(2)
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

    # Store an entry that expires in 2 seconds
    entry = MemoryEntry("This message will expire soon!")
    entry.with_ttl_seconds(2)
    entry_id = backend.store(entry)
    print(f"✓ Stored entry with 2-second TTL: {entry_id}")

    # Immediately retrieve it
    retrieved = backend.get(entry_id)
    if retrieved:
        print(f"✓ Entry exists: {retrieved.content}")
        print(f"  - Expires at: {retrieved.expires_at}")
        print(f"  - Is expired: {retrieved.is_expired()}")

    # Wait for expiration
    print("\nWaiting 3 seconds for entry to expire...")
    time.sleep(3)

    # Try to retrieve again
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

    # Create backend with max 3 entries
    backend = InMemoryBackend.with_max_entries(3)
    print("Created backend with max 3 entries")

    # Store 5 entries (oldest 2 will be evicted)
    for i in range(1, 6):
        entry = MemoryEntry(f"Entry {i}")
        entry.with_metadata("number", i)
        backend.store(entry)
        print(f"✓ Stored: Entry {i}")
        time.sleep(0.1)  # Small delay to ensure creation time ordering

    # Check count
    count = backend.count()
    print(f"\n✓ Total entries after storing 5: {count} (max 3)")

    # Search to see which entries remain
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

    # Create backend where all entries expire in 3 seconds by default
    backend = InMemoryBackend.with_ttl_seconds(3)
    print("Created backend with default 3-second TTL")

    # Store entries without explicit TTL
    for i in range(1, 4):
        entry = MemoryEntry(f"Auto-expiring entry {i}")
        backend.store(entry)
        print(f"✓ Stored: Auto-expiring entry {i}")

    print(f"\n✓ Total entries: {backend.count()}")

    print("\nWaiting 4 seconds for all entries to expire...")
    time.sleep(4)

    count = backend.count()
    print(f"✓ Total entries after expiration: {count}")

    print()


def demo_clear_and_delete():
    """Demonstrate delete and clear operations"""
    print("=" * 60)
    print("DEMO 6: Delete and Clear Operations")
    print("=" * 60)

    backend = InMemoryBackend()

    # Store some entries
    entry1 = MemoryEntry("Entry 1")
    entry2 = MemoryEntry("Entry 2")
    entry3 = MemoryEntry("Entry 3")

    id1 = backend.store(entry1)
    id2 = backend.store(entry2)
    id3 = backend.store(entry3)

    print(f"✓ Stored 3 entries")
    print(f"✓ Total entries: {backend.count()}")

    # Delete one entry
    deleted = backend.delete(id2)
    print(f"\n✓ Deleted entry {id2}: {deleted}")
    print(f"✓ Total entries: {backend.count()}")

    # Try to delete again (should return False)
    deleted = backend.delete(id2)
    print(f"✓ Try to delete again: {deleted} (already deleted)")

    # Clear all entries
    print("\nClearing all entries...")
    backend.clear()
    print(f"✓ Total entries after clear: {backend.count()}")

    print()


def demo_conversation_history():
    """Realistic example: Conversation history storage"""
    print("=" * 60)
    print("DEMO 7: Realistic Use Case - Conversation History")
    print("=" * 60)

    # Create backend for storing conversation history
    # Keep last 50 messages, auto-expire after 1 hour
    backend = InMemoryBackend.with_max_entries(50)

    # Simulate a conversation
    conversation = [
        ("user", "alice", "Hello, I need help with Python"),
        ("assistant", "bot", "Hi Alice! I'd be happy to help with Python. What do you need?"),
        ("user", "alice", "How do I read a file?"),
        ("assistant", "bot", "You can use open() function with a file path..."),
        ("user", "alice", "Thanks! What about writing to a file?"),
        ("assistant", "bot", "To write, use open() with 'w' mode..."),
    ]

    print("Storing conversation:")
    for speaker, user_id, message in conversation:
        entry = MemoryEntry(message)
        entry.with_metadata("speaker", speaker)
        entry.with_metadata("user_id", user_id)
        entry.with_metadata("session", "session_123")
        backend.store(entry)
        print(f"  [{speaker:9s}] {message}")

    # Retrieve conversation history
    print("\nRetrieving full conversation:")
    query = MemoryQuery()
    query.with_filter("session", "session_123")
    results = backend.search(query)

    print(f"Found {len(results)} messages in session:")
    for result in results:
        metadata = result.metadata
        speaker = metadata.get("speaker") if metadata else "unknown"
        print(f"  [{speaker:9s}] {result.content}")

    # Get only user messages
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
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "Ceylon Memory System Demo" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    demo_basic_storage()
    demo_metadata_filtering()
    demo_ttl_expiration()
    demo_max_entries_lru()
    demo_default_ttl()
    demo_clear_and_delete()
    demo_conversation_history()

    print("=" * 60)
    print("All demos completed successfully!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
