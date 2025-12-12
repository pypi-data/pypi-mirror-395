#!/usr/bin/env python3
"""
Comprehensive tests for Ceylon's memory system.

Tests cover:
- MemoryEntry creation and properties
"""

import pytest
import time
from ceylonai_next import InMemoryBackend, MemoryEntry, MemoryQuery


class TestMemoryEntry:
    """Test MemoryEntry creation and manipulation"""

    def test_create_entry(self):
        """Test creating a basic memory entry"""
        entry = MemoryEntry("Test content")
        assert entry.content == "Test content"
        assert entry.id is not None
        assert len(entry.id) > 0

    def test_entry_with_metadata(self):
        """Test adding metadata to an entry"""
        entry = MemoryEntry("Test content")
        entry.with_metadata("type", "user")
        entry.with_metadata("user_id", "alice")
        entry.with_metadata("count", 42)

        metadata = entry.metadata
        assert metadata["type"] == "user"
        assert metadata["user_id"] == "alice"
        assert metadata["count"] == 42

    def test_entry_with_ttl(self):
        """Test creating an entry with TTL"""
        entry = MemoryEntry("Temporary content")
        entry.with_ttl_seconds(10)

        assert entry.expires_at is not None
        assert not entry.is_expired()

    def test_entry_expiration_check(self):
        """Test that very short TTL entries are detected as expired"""
        entry = MemoryEntry("Expired content")
        entry.with_ttl_seconds(1)

        # Should not be expired immediately
        assert not entry.is_expired()

        # Wait for expiration
        time.sleep(2)

        # Should now be expired
        assert entry.is_expired()

    def test_entry_timestamps(self):
        """Test that entry has valid timestamps"""
        entry = MemoryEntry("Test content")
        assert entry.created_at is not None
        assert len(entry.created_at) > 0  # Should be ISO 8601 string

    def test_entry_repr(self):
        """Test entry string representation"""
        entry = MemoryEntry("Test content")
        repr_str = repr(entry)
        assert "MemoryEntry" in repr_str
        assert "Test content" in repr_str


class TestInMemoryBackend:
    """Test InMemoryBackend storage operations"""

    def test_create_backend(self):
        """Test creating an in-memory backend"""
        backend = InMemoryBackend()
        assert backend is not None

    def test_store_and_retrieve(self):
        """Test storing and retrieving an entry"""
        backend = InMemoryBackend()
        entry = MemoryEntry("Hello, world!")

        # Store entry
        entry_id = backend.store(entry)
        assert entry_id is not None

        # Retrieve entry
        retrieved = backend.get(entry_id)
        assert retrieved is not None
        assert retrieved.content == "Hello, world!"
        assert retrieved.id == entry_id

    def test_get_nonexistent(self):
        """Test retrieving a non-existent entry"""
        backend = InMemoryBackend()
        retrieved = backend.get("nonexistent-id")
        assert retrieved is None

    def test_count_entries(self):
        """Test counting entries in the backend"""
        backend = InMemoryBackend()
        assert backend.count() == 0

        backend.store(MemoryEntry("Entry 1"))
        assert backend.count() == 1

        backend.store(MemoryEntry("Entry 2"))
        assert backend.count() == 2

    def test_delete_entry(self):
        """Test deleting an entry"""
        backend = InMemoryBackend()
        entry = MemoryEntry("To be deleted")
        entry_id = backend.store(entry)

        # Verify entry exists
        assert backend.get(entry_id) is not None
        assert backend.count() == 1

        # Delete entry
        deleted = backend.delete(entry_id)
        assert deleted is True

        # Verify entry is gone
        assert backend.get(entry_id) is None
        assert backend.count() == 0

    def test_delete_nonexistent(self):
        """Test deleting a non-existent entry returns False"""
        backend = InMemoryBackend()
        deleted = backend.delete("nonexistent-id")
        assert deleted is False

    def test_clear_all_entries(self):
        """Test clearing all entries"""
        backend = InMemoryBackend()

        # Store multiple entries
        backend.store(MemoryEntry("Entry 1"))
        backend.store(MemoryEntry("Entry 2"))
        backend.store(MemoryEntry("Entry 3"))
        assert backend.count() == 3

        # Clear all
        backend.clear()
        assert backend.count() == 0


class TestMemoryQuery:
    """Test MemoryQuery and search functionality"""

    def test_create_query(self):
        """Test creating a memory query"""
        query = MemoryQuery()
        assert query is not None

    def test_search_all(self):
        """Test searching without filters returns all entries"""
        backend = InMemoryBackend()

        # Store entries
        backend.store(MemoryEntry("Entry 1"))
        backend.store(MemoryEntry("Entry 2"))
        backend.store(MemoryEntry("Entry 3"))

        # Search without filters
        query = MemoryQuery()
        results = backend.search(query)
        assert len(results) == 3

    def test_search_with_metadata_filter(self):
        """Test searching with metadata filters"""
        backend = InMemoryBackend()

        # Store entries with different types
        entry1 = MemoryEntry("User message")
        entry1.with_metadata("type", "user")
        backend.store(entry1)

        entry2 = MemoryEntry("System message")
        entry2.with_metadata("type", "system")
        backend.store(entry2)

        entry3 = MemoryEntry("Another user message")
        entry3.with_metadata("type", "user")
        backend.store(entry3)

        # Search for user messages
        query = MemoryQuery()
        query.with_filter("type", "user")
        results = backend.search(query)

        assert len(results) == 2
        for result in results:
            assert result.metadata["type"] == "user"

    def test_search_with_multiple_filters(self):
        """Test searching with multiple metadata filters (AND logic)"""
        backend = InMemoryBackend()

        # Store entries
        entry1 = MemoryEntry("Alice's greeting")
        entry1.with_metadata("user_id", "alice")
        entry1.with_metadata("type", "greeting")
        backend.store(entry1)

        entry2 = MemoryEntry("Alice's question")
        entry2.with_metadata("user_id", "alice")
        entry2.with_metadata("type", "question")
        backend.store(entry2)

        entry3 = MemoryEntry("Bob's greeting")
        entry3.with_metadata("user_id", "bob")
        entry3.with_metadata("type", "greeting")
        backend.store(entry3)

        # Search for Alice's greetings
        query = MemoryQuery()
        query.with_filter("user_id", "alice")
        query.with_filter("type", "greeting")
        results = backend.search(query)

        assert len(results) == 1
        assert results[0].content == "Alice's greeting"

    def test_search_with_limit(self):
        """Test limiting search results"""
        backend = InMemoryBackend()

        # Store 5 entries
        for i in range(5):
            backend.store(MemoryEntry(f"Entry {i}"))

        # Search with limit of 2
        query = MemoryQuery()
        query.with_limit(2)
        results = backend.search(query)

        assert len(results) == 2

    def test_search_ordering(self):
        """Test that search results are ordered by creation time (newest first)"""
        backend = InMemoryBackend()

        # Store entries with delays to ensure different timestamps
        entry1 = MemoryEntry("First entry")
        entry1.with_metadata("order", 1)
        backend.store(entry1)
        time.sleep(0.01)

        entry2 = MemoryEntry("Second entry")
        entry2.with_metadata("order", 2)
        backend.store(entry2)
        time.sleep(0.01)

        entry3 = MemoryEntry("Third entry")
        entry3.with_metadata("order", 3)
        backend.store(entry3)

        # Search all
        query = MemoryQuery()
        results = backend.search(query)

        # Should be in reverse order (newest first)
        assert results[0].content == "Third entry"
        assert results[1].content == "Second entry"
        assert results[2].content == "First entry"


class TestTTLExpiration:
    """Test TTL (Time To Live) expiration functionality"""

    def test_ttl_entry_expires(self):
        """Test that entries with TTL expire and are removed"""
        backend = InMemoryBackend()

        # Store entry with 1-second TTL
        entry = MemoryEntry("Temporary data")
        entry.with_ttl_seconds(1)
        entry_id = backend.store(entry)

        # Should exist immediately
        assert backend.get(entry_id) is not None
        assert backend.count() == 1

        # Wait for expiration
        time.sleep(2)

        # Should be gone
        assert backend.get(entry_id) is None

    def test_expired_entries_excluded_from_search(self):
        """Test that expired entries are excluded from search results"""
        backend = InMemoryBackend()

        # Store permanent entry
        permanent = MemoryEntry("Permanent entry")
        backend.store(permanent)

        # Store entry with 1-second TTL
        temporary = MemoryEntry("Temporary entry")
        temporary.with_ttl_seconds(1)
        backend.store(temporary)

        # Both should be in results
        query = MemoryQuery()
        results = backend.search(query)
        assert len(results) == 2

        # Wait for expiration
        time.sleep(2)

        # Only permanent should remain
        results = backend.search(query)
        assert len(results) == 1
        assert results[0].content == "Permanent entry"

    def test_backend_with_default_ttl(self):
        """Test backend with default TTL for all entries"""
        # Create backend with 2-second default TTL
        backend = InMemoryBackend.with_ttl_seconds(2)

        # Store entry without explicit TTL
        entry = MemoryEntry("Auto-expiring entry")
        entry_id = backend.store(entry)

        # Should exist immediately
        assert backend.get(entry_id) is not None

        # Wait for expiration
        time.sleep(3)

        # Should be gone
        assert backend.get(entry_id) is None


class TestMaxEntries:
    """Test max entries limit with LRU eviction"""

    def test_max_entries_limit(self):
        """Test that backend enforces max entries limit"""
        # Create backend with max 3 entries
        backend = InMemoryBackend.with_max_entries(3)

        # Store 5 entries
        ids = []
        for i in range(5):
            entry = MemoryEntry(f"Entry {i}")
            entry_id = backend.store(entry)
            ids.append(entry_id)
            time.sleep(0.01)  # Ensure different timestamps

        # Should only have 3 entries (max limit)
        assert backend.count() == 3

    def test_lru_eviction_order(self):
        """Test that oldest entries are evicted first (LRU)"""
        backend = InMemoryBackend.with_max_entries(3)

        # Store entries with delays
        entry1 = MemoryEntry("First (oldest)")
        id1 = backend.store(entry1)
        time.sleep(0.01)

        entry2 = MemoryEntry("Second")
        id2 = backend.store(entry2)
        time.sleep(0.01)

        entry3 = MemoryEntry("Third")
        id3 = backend.store(entry3)
        time.sleep(0.01)

        # All should exist
        assert backend.get(id1) is not None
        assert backend.get(id2) is not None
        assert backend.get(id3) is not None

        # Store fourth entry (should evict first)
        entry4 = MemoryEntry("Fourth")
        id4 = backend.store(entry4)

        # First should be evicted
        assert backend.get(id1) is None
        assert backend.get(id2) is not None
        assert backend.get(id3) is not None
        assert backend.get(id4) is not None


class TestComplexScenarios:
    """Test complex real-world scenarios"""

    def test_conversation_history(self):
        """Test storing and querying conversation history"""
        backend = InMemoryBackend.with_max_entries(100)

        # Simulate conversation
        messages = [
            ("user", "alice", "Hello"),
            ("assistant", "bot", "Hi Alice!"),
            ("user", "alice", "How are you?"),
            ("assistant", "bot", "I'm doing well, thanks!"),
            ("user", "bob", "Hey there"),
            ("assistant", "bot", "Hello Bob!"),
        ]

        for speaker, user_id, content in messages:
            entry = MemoryEntry(content)
            entry.with_metadata("speaker", speaker)
            entry.with_metadata("user_id", user_id)
            entry.with_metadata("session", "session_1")
            backend.store(entry)

        # Get all messages
        query = MemoryQuery()
        query.with_filter("session", "session_1")
        all_messages = backend.search(query)
        assert len(all_messages) == 6

        # Get only user messages
        query = MemoryQuery()
        query.with_filter("session", "session_1")
        query.with_filter("speaker", "user")
        user_messages = backend.search(query)
        assert len(user_messages) == 3

        # Get Alice's messages
        query = MemoryQuery()
        query.with_filter("user_id", "alice")
        alice_messages = backend.search(query)
        assert len(alice_messages) == 2

    def test_multiple_sessions(self):
        """Test handling multiple independent sessions"""
        backend = InMemoryBackend()

        # Session 1
        entry1 = MemoryEntry("Session 1 message")
        entry1.with_metadata("session_id", "session_1")
        backend.store(entry1)

        # Session 2
        entry2 = MemoryEntry("Session 2 message")
        entry2.with_metadata("session_id", "session_2")
        backend.store(entry2)

        # Another Session 1 message
        entry3 = MemoryEntry("Another session 1 message")
        entry3.with_metadata("session_id", "session_1")
        backend.store(entry3)

        # Query session 1
        query = MemoryQuery()
        query.with_filter("session_id", "session_1")
        session1_messages = backend.search(query)
        assert len(session1_messages) == 2

        # Query session 2
        query = MemoryQuery()
        query.with_filter("session_id", "session_2")
        session2_messages = backend.search(query)
        assert len(session2_messages) == 1

    def test_mixed_ttl_and_permanent(self):
        """Test mixing entries with TTL and permanent entries"""
        backend = InMemoryBackend()

        # Permanent entries
        perm1 = MemoryEntry("Permanent 1")
        perm1.with_metadata("type", "permanent")
        backend.store(perm1)

        perm2 = MemoryEntry("Permanent 2")
        perm2.with_metadata("type", "permanent")
        backend.store(perm2)

        # Temporary entries
        temp1 = MemoryEntry("Temporary 1")
        temp1.with_metadata("type", "temporary")
        temp1.with_ttl_seconds(1)
        backend.store(temp1)

        temp2 = MemoryEntry("Temporary 2")
        temp2.with_metadata("type", "temporary")
        temp2.with_ttl_seconds(1)
        backend.store(temp2)

        # All should exist
        assert backend.count() == 4

        # Wait for temporary entries to expire
        time.sleep(2)

        # Only permanent should remain
        assert backend.count() == 2

        query = MemoryQuery()
        query.with_filter("type", "permanent")
        results = backend.search(query)
        assert len(results) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
