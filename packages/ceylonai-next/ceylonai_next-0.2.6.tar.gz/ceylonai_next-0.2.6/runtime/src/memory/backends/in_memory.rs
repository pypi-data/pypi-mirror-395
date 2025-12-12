use crate::core::error::Result;
use crate::core::memory::{Memory, MemoryEntry, MemoryQuery};
use async_trait::async_trait;
use dashmap::DashMap;
use std::sync::Arc;

/// In-memory storage backend with TTL support
pub struct InMemoryBackend {
    store: Arc<DashMap<String, MemoryEntry>>,
    max_entries: Option<usize>,
    default_ttl_seconds: Option<i64>,
}

impl InMemoryBackend {
    /// Create a new in-memory backend
    pub fn new() -> Self {
        Self {
            store: Arc::new(DashMap::new()),
            max_entries: None,
            default_ttl_seconds: None,
        }
    }

    /// Create with maximum entry limit
    pub fn with_max_entries(mut self, max: usize) -> Self {
        self.max_entries = Some(max);
        self
    }

    /// Create with default TTL
    pub fn with_ttl_seconds(mut self, seconds: i64) -> Self {
        self.default_ttl_seconds = Some(seconds);
        self
    }

    /// Check if entry is expired
    fn is_expired(&self, entry: &MemoryEntry) -> bool {
        entry.is_expired()
    }

    /// Remove all expired entries
    fn cleanup_expired(&self) {
        self.store.retain(|_, entry| !self.is_expired(entry));
    }

    /// Evict oldest entry to make room
    fn evict_oldest(&self) {
        if let Some(oldest) = self
            .store
            .iter()
            .min_by_key(|e| e.value().created_at)
            .map(|e| e.key().clone())
        {
            self.store.remove(&oldest);
        }
    }
}

impl Default for InMemoryBackend {
    fn default() -> Self {
        Self::new()
    }
}

#[async_trait]
impl Memory for InMemoryBackend {
    async fn store(&self, mut entry: MemoryEntry) -> Result<String> {
        // Apply default TTL if not set
        if entry.expires_at.is_none() {
            if let Some(ttl) = self.default_ttl_seconds {
                entry = entry.with_ttl_seconds(ttl);
            }
        }

        // Cleanup expired entries first
        self.cleanup_expired();

        // Enforce max entries limit
        if let Some(max) = self.max_entries {
            while self.store.len() >= max {
                self.evict_oldest();
            }
        }

        let id = entry.id.clone();
        self.store.insert(id.clone(), entry);
        crate::metrics::metrics().record_memory_write();
        Ok(id)
    }

    async fn get(&self, id: &str) -> Result<Option<MemoryEntry>> {
        if let Some(entry) = self.store.get(id) {
            if self.is_expired(&entry) {
                // Remove expired entry
                drop(entry); // Release read lock
                self.store.remove(id);
                crate::metrics::metrics().record_memory_miss();
                Ok(None)
            } else {
                crate::metrics::metrics().record_memory_hit();
                Ok(Some(entry.clone()))
            }
        } else {
            crate::metrics::metrics().record_memory_miss();
            Ok(None)
        }
    }

    async fn search(&self, query: MemoryQuery) -> Result<Vec<MemoryEntry>> {
        // Cleanup expired entries
        self.cleanup_expired();

        let mut results: Vec<MemoryEntry> = self
            .store
            .iter()
            .map(|e| e.value().clone())
            .filter(|entry| {
                // Apply metadata filters - all filters must match
                let matches_filters = query
                    .filters
                    .iter()
                    .all(|(key, value)| entry.metadata.get(key) == Some(value));

                // Apply semantic query (keyword search) if present
                let matches_query = if let Some(ref q) = query.semantic_query {
                    entry.content.to_lowercase().contains(&q.to_lowercase())
                } else {
                    true
                };

                matches_filters && matches_query
            })
            .collect();

        // Sort by creation time (newest first) for consistent ordering
        results.sort_by(|a, b| b.created_at.cmp(&a.created_at));

        // Apply limit
        if let Some(limit) = query.limit {
            results.truncate(limit);
        }

        Ok(results)
    }

    async fn delete(&self, id: &str) -> Result<bool> {
        Ok(self.store.remove(id).is_some())
    }

    async fn clear(&self) -> Result<()> {
        self.store.clear();
        Ok(())
    }

    async fn count(&self) -> Result<usize> {
        self.cleanup_expired();
        Ok(self.store.len())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[tokio::test]
    async fn test_basic_storage() {
        let backend = InMemoryBackend::new();

        let entry = MemoryEntry::new("test content");
        let id = backend.store(entry.clone()).await.unwrap();

        let retrieved = backend.get(&id).await.unwrap();
        assert!(retrieved.is_some());
        assert_eq!(retrieved.unwrap().content, "test content");
    }

    #[tokio::test]
    async fn test_ttl_expiration() {
        let backend = InMemoryBackend::new();

        // Create entry that expires in 1 second
        let entry = MemoryEntry::new("expires soon").with_ttl_seconds(1);
        let id = backend.store(entry).await.unwrap();

        // Should exist immediately
        assert!(backend.get(&id).await.unwrap().is_some());

        // Wait for expiration
        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;

        // Should be gone
        assert!(backend.get(&id).await.unwrap().is_none());
    }

    #[tokio::test]
    async fn test_metadata_search() {
        let backend = InMemoryBackend::new();

        let entry1 = MemoryEntry::new("user message")
            .with_metadata("type", json!("user"))
            .with_metadata("user_id", json!("123"));

        let entry2 = MemoryEntry::new("system message").with_metadata("type", json!("system"));

        backend.store(entry1).await.unwrap();
        backend.store(entry2).await.unwrap();

        // Search for user messages
        let query = MemoryQuery::new().with_filter("type", json!("user"));
        let results = backend.search(query).await.unwrap();

        assert_eq!(results.len(), 1);
        assert_eq!(results[0].content, "user message");
    }

    #[tokio::test]
    async fn test_max_entries() {
        let backend = InMemoryBackend::new().with_max_entries(2);

        backend.store(MemoryEntry::new("first")).await.unwrap();
        tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;

        backend.store(MemoryEntry::new("second")).await.unwrap();
        tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;

        backend.store(MemoryEntry::new("third")).await.unwrap();

        // Should only have 2 entries (oldest evicted)
        assert_eq!(backend.count().await.unwrap(), 2);

        // First entry should be evicted
        let results = backend.search(MemoryQuery::new()).await.unwrap();
        assert!(!results.iter().any(|e| e.content == "first"));
    }

    #[tokio::test]
    async fn test_delete() {
        let backend = InMemoryBackend::new();

        let entry = MemoryEntry::new("to delete");
        let id = backend.store(entry).await.unwrap();

        assert!(backend.delete(&id).await.unwrap());
        assert!(backend.get(&id).await.unwrap().is_none());
        assert!(!backend.delete(&id).await.unwrap()); // Already deleted
    }

    #[tokio::test]
    async fn test_clear() {
        let backend = InMemoryBackend::new();

        backend.store(MemoryEntry::new("entry 1")).await.unwrap();
        backend.store(MemoryEntry::new("entry 2")).await.unwrap();

        assert_eq!(backend.count().await.unwrap(), 2);

        backend.clear().await.unwrap();
        assert_eq!(backend.count().await.unwrap(), 0);
    }
}
