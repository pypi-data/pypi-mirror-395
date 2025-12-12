use crate::core::error::{Error, Result};
use crate::core::memory::{Memory, MemoryEntry, MemoryQuery};
use async_trait::async_trait;
use redis::{aio::ConnectionManager, AsyncCommands, RedisError};
use serde_json::Value;
use std::collections::HashMap;

/// Redis-backed memory storage with persistence and advanced features
///
/// Features:
/// - Persistent storage across restarts
/// - Native TTL support via Redis EXPIRE
/// - Metadata filtering with JSON queries
/// - Connection pooling for high performance
/// - Atomic operations
/// - Optional key prefix for namespace isolation
///
/// # Storage Format
///
/// Each memory entry is stored as a Redis Hash with the following fields:
/// - `content`: The actual content string
/// - `metadata`: JSON-encoded metadata HashMap
/// - `embedding`: JSON-encoded embedding vector (if present)
/// - `created_at`: ISO 8601 timestamp
/// - `expires_at`: ISO 8601 timestamp (if TTL set)
///
/// # Key Format
///
/// Keys are stored as: `{prefix}:memory:{entry_id}`
/// An index set is maintained at: `{prefix}:memory:index`
///
#[derive(Clone)]
pub struct RedisBackend {
    /// Connection manager for connection pooling
    connection: ConnectionManager,

    /// Key prefix for namespace isolation
    key_prefix: String,

    /// Default TTL in seconds (applied if entry doesn't specify TTL)
    default_ttl_seconds: Option<i64>,
}

impl RedisBackend {
    /// Create a new Redis backend with connection string
    ///
    /// # Arguments
    ///
    /// * `redis_url` - Redis connection URL (e.g., "redis://localhost:6379")
    ///
    /// # Examples
    ///
    /// ```no_run
    /// # use runtime::memory::backends::RedisBackend;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let backend = RedisBackend::new("redis://localhost:6379").await?;
    /// # Ok(())
    /// # }
    /// ```
    pub async fn new(redis_url: impl AsRef<str>) -> Result<Self> {
        let client =
            redis::Client::open(redis_url.as_ref()).map_err(|e| Error::Unknown(e.into()))?;

        let connection = ConnectionManager::new(client)
            .await
            .map_err(|e| Error::Unknown(e.into()))?;

        Ok(Self {
            connection,
            key_prefix: "ceylon".to_string(),
            default_ttl_seconds: None,
        })
    }

    /// Set a custom key prefix for namespace isolation
    ///
    /// Useful for running multiple applications on the same Redis instance
    pub fn with_prefix(mut self, prefix: impl Into<String>) -> Self {
        self.key_prefix = prefix.into();
        self
    }

    /// Set default TTL for entries that don't specify expiration
    pub fn with_ttl_seconds(mut self, seconds: i64) -> Self {
        self.default_ttl_seconds = Some(seconds);
        self
    }

    /// Generate the full Redis key for an entry ID
    fn entry_key(&self, id: &str) -> String {
        format!("{}:memory:{}", self.key_prefix, id)
    }

    /// Get the index set key (contains all entry IDs)
    fn index_key(&self) -> String {
        format!("{}:memory:index", self.key_prefix)
    }

    /// Serialize a MemoryEntry to Redis hash fields
    fn entry_to_fields(&self, entry: &MemoryEntry) -> Result<Vec<(String, String)>> {
        let mut fields = Vec::new();

        fields.push(("content".to_string(), entry.content.clone()));
        fields.push((
            "metadata".to_string(),
            serde_json::to_string(&entry.metadata)?,
        ));
        fields.push(("created_at".to_string(), entry.created_at.to_rfc3339()));

        if let Some(ref embedding) = entry.embedding {
            fields.push(("embedding".to_string(), serde_json::to_string(embedding)?));
        }

        if let Some(expires_at) = entry.expires_at {
            fields.push(("expires_at".to_string(), expires_at.to_rfc3339()));
        }

        Ok(fields)
    }

    /// Deserialize Redis hash fields to a MemoryEntry
    fn fields_to_entry(&self, id: String, fields: HashMap<String, String>) -> Result<MemoryEntry> {
        let content = fields
            .get("content")
            .ok_or_else(|| Error::Unknown(anyhow::anyhow!("Missing content field")))?
            .clone();

        let metadata: HashMap<String, Value> = fields
            .get("metadata")
            .and_then(|s| serde_json::from_str(s).ok())
            .unwrap_or_default();

        let embedding: Option<Vec<f32>> = fields
            .get("embedding")
            .and_then(|s| serde_json::from_str(s).ok());

        let created_at = fields
            .get("created_at")
            .and_then(|s| chrono::DateTime::parse_from_rfc3339(s).ok())
            .map(|dt| dt.with_timezone(&chrono::Utc))
            .ok_or_else(|| Error::Unknown(anyhow::anyhow!("Invalid created_at")))?;

        let expires_at = fields
            .get("expires_at")
            .and_then(|s| chrono::DateTime::parse_from_rfc3339(s).ok())
            .map(|dt| dt.with_timezone(&chrono::Utc));

        Ok(MemoryEntry {
            id,
            content,
            metadata,
            embedding,
            created_at,
            expires_at,
        })
    }

    /// Check if an entry matches the query filters
    fn matches_query(&self, entry: &MemoryEntry, query: &MemoryQuery) -> bool {
        // Check metadata filters - all must match
        let matches_filters = query
            .filters
            .iter()
            .all(|(key, value)| entry.metadata.get(key) == Some(value));

        // Check semantic query (simple keyword search)
        let matches_query = if let Some(ref q) = query.semantic_query {
            entry.content.to_lowercase().contains(&q.to_lowercase())
        } else {
            true
        };

        matches_filters && matches_query
    }
}

#[async_trait]
impl Memory for RedisBackend {
    async fn store(&self, mut entry: MemoryEntry) -> Result<String> {
        // Apply default TTL if not set
        if entry.expires_at.is_none() {
            if let Some(ttl) = self.default_ttl_seconds {
                entry = entry.with_ttl_seconds(ttl);
            }
        }

        let key = self.entry_key(&entry.id);
        let fields = self.entry_to_fields(&entry)?;

        let mut conn = self.connection.clone();

        // Store the hash
        let _: () = conn
            .hset_multiple(&key, &fields)
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        // Add to index set
        let _: () = conn
            .sadd(self.index_key(), &entry.id)
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        // Set expiration if specified
        if let Some(expires_at) = entry.expires_at {
            let ttl_seconds = (expires_at - chrono::Utc::now()).num_seconds();
            if ttl_seconds > 0 {
                let _: () = conn
                    .expire(&key, ttl_seconds as i64)
                    .await
                    .map_err(|e: RedisError| Error::Unknown(e.into()))?;
            }
        }

        crate::metrics::metrics().record_memory_write();
        Ok(entry.id)
    }

    async fn get(&self, id: &str) -> Result<Option<MemoryEntry>> {
        let key = self.entry_key(id);
        let mut conn = self.connection.clone();

        // Check if key exists
        let exists: bool = conn
            .exists(&key)
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        if !exists {
            crate::metrics::metrics().record_memory_miss();
            return Ok(None);
        }

        // Get all hash fields
        let fields: HashMap<String, String> = conn
            .hgetall(&key)
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        if fields.is_empty() {
            crate::metrics::metrics().record_memory_miss();
            return Ok(None);
        }

        let entry = self.fields_to_entry(id.to_string(), fields)?;

        // Check if expired
        if entry.is_expired() {
            // Delete expired entry
            self.delete(id).await?;
            crate::metrics::metrics().record_memory_miss();
            return Ok(None);
        }

        crate::metrics::metrics().record_memory_hit();
        Ok(Some(entry))
    }

    async fn search(&self, query: MemoryQuery) -> Result<Vec<MemoryEntry>> {
        let mut conn = self.connection.clone();

        // Get all entry IDs from the index
        let ids: Vec<String> = conn
            .smembers(self.index_key())
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        let mut results = Vec::new();

        // Fetch and filter each entry
        for id in ids {
            if let Some(entry) = self.get(&id).await? {
                if self.matches_query(&entry, &query) {
                    results.push(entry);
                }
            }
        }

        // Sort by creation time (newest first)
        results.sort_by(|a, b| b.created_at.cmp(&a.created_at));

        // Apply limit
        if let Some(limit) = query.limit {
            results.truncate(limit);
        }

        Ok(results)
    }

    async fn delete(&self, id: &str) -> Result<bool> {
        let key = self.entry_key(id);
        let mut conn = self.connection.clone();

        // Delete the hash
        let deleted: i32 = conn
            .del(&key)
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        // Remove from index
        let _: () = conn
            .srem(self.index_key(), id)
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        Ok(deleted > 0)
    }

    async fn clear(&self) -> Result<()> {
        let mut conn = self.connection.clone();

        // Get all IDs
        let ids: Vec<String> = conn
            .smembers(self.index_key())
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        // Delete all entries
        for id in ids {
            self.delete(&id).await?;
        }

        Ok(())
    }

    async fn count(&self) -> Result<usize> {
        let mut conn = self.connection.clone();

        let count: usize = conn
            .scard(self.index_key())
            .await
            .map_err(|e: RedisError| Error::Unknown(e.into()))?;

        Ok(count)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    // Helper to get test Redis URL from environment or use default
    fn get_redis_url() -> String {
        std::env::var("REDIS_URL").unwrap_or_else(|_| "redis://localhost:6379".to_string())
    }

    async fn create_test_backend() -> RedisBackend {
        let url = get_redis_url();
        RedisBackend::new(url)
            .await
            .expect("Failed to connect to Redis")
            .with_prefix("test_ceylon")
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_basic_storage() {
        let backend = create_test_backend().await;
        backend.clear().await.unwrap();

        let entry = MemoryEntry::new("test content");
        let id = backend.store(entry.clone()).await.unwrap();

        let retrieved = backend.get(&id).await.unwrap();
        assert!(retrieved.is_some());
        assert_eq!(retrieved.unwrap().content, "test content");

        backend.clear().await.unwrap();
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_ttl_expiration() {
        let backend = create_test_backend().await;
        backend.clear().await.unwrap();

        let entry = MemoryEntry::new("expires soon").with_ttl_seconds(2);
        let id = backend.store(entry).await.unwrap();

        // Should exist immediately
        assert!(backend.get(&id).await.unwrap().is_some());

        // Wait for expiration
        tokio::time::sleep(tokio::time::Duration::from_secs(3)).await;

        // Should be gone (Redis automatically deletes expired keys)
        assert!(backend.get(&id).await.unwrap().is_none());

        backend.clear().await.unwrap();
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_metadata_search() {
        let backend = create_test_backend().await;
        backend.clear().await.unwrap();

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

        backend.clear().await.unwrap();
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_semantic_query() {
        let backend = create_test_backend().await;
        backend.clear().await.unwrap();

        backend
            .store(MemoryEntry::new("The quick brown fox"))
            .await
            .unwrap();
        backend
            .store(MemoryEntry::new("jumps over the lazy dog"))
            .await
            .unwrap();
        backend
            .store(MemoryEntry::new("completely different content"))
            .await
            .unwrap();

        let query = MemoryQuery::new().with_semantic_query("fox").with_limit(10);
        let results = backend.search(query).await.unwrap();

        assert_eq!(results.len(), 1);
        assert!(results[0].content.contains("fox"));

        backend.clear().await.unwrap();
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_delete() {
        let backend = create_test_backend().await;
        backend.clear().await.unwrap();

        let entry = MemoryEntry::new("to delete");
        let id = backend.store(entry).await.unwrap();

        assert!(backend.delete(&id).await.unwrap());
        assert!(backend.get(&id).await.unwrap().is_none());
        assert!(!backend.delete(&id).await.unwrap()); // Already deleted

        backend.clear().await.unwrap();
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_count() {
        let backend = create_test_backend().await;
        backend.clear().await.unwrap();

        assert_eq!(backend.count().await.unwrap(), 0);

        backend.store(MemoryEntry::new("entry 1")).await.unwrap();
        backend.store(MemoryEntry::new("entry 2")).await.unwrap();

        assert_eq!(backend.count().await.unwrap(), 2);

        backend.clear().await.unwrap();
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_clear() {
        let backend = create_test_backend().await;
        backend.clear().await.unwrap();

        backend.store(MemoryEntry::new("entry 1")).await.unwrap();
        backend.store(MemoryEntry::new("entry 2")).await.unwrap();

        assert_eq!(backend.count().await.unwrap(), 2);

        backend.clear().await.unwrap();
        assert_eq!(backend.count().await.unwrap(), 0);
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_embedding_storage() {
        let backend = create_test_backend().await;
        backend.clear().await.unwrap();

        let embedding = vec![0.1, 0.2, 0.3, 0.4, 0.5];
        let entry = MemoryEntry::new("with embedding").with_embedding(embedding.clone());

        let id = backend.store(entry).await.unwrap();
        let retrieved = backend.get(&id).await.unwrap().unwrap();

        assert_eq!(retrieved.embedding, Some(embedding));

        backend.clear().await.unwrap();
    }

    #[tokio::test]
    #[ignore] // Requires Redis server
    async fn test_prefix_isolation() {
        let backend1 = RedisBackend::new(get_redis_url())
            .await
            .unwrap()
            .with_prefix("test_app1");

        let backend2 = RedisBackend::new(get_redis_url())
            .await
            .unwrap()
            .with_prefix("test_app2");

        backend1.clear().await.unwrap();
        backend2.clear().await.unwrap();

        backend1.store(MemoryEntry::new("app1 data")).await.unwrap();
        backend2.store(MemoryEntry::new("app2 data")).await.unwrap();

        assert_eq!(backend1.count().await.unwrap(), 1);
        assert_eq!(backend2.count().await.unwrap(), 1);

        let results1 = backend1.search(MemoryQuery::new()).await.unwrap();
        let results2 = backend2.search(MemoryQuery::new()).await.unwrap();

        assert_eq!(results1[0].content, "app1 data");
        assert_eq!(results2[0].content, "app2 data");

        backend1.clear().await.unwrap();
        backend2.clear().await.unwrap();
    }
}
