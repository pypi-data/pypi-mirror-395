use async_trait::async_trait;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use crate::core::error::Result;

/// Entry stored in memory
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemoryEntry {
    /// Unique identifier
    pub id: String,

    /// Content to store
    pub content: String,

    /// Optional metadata for filtering
    pub metadata: HashMap<String, Value>,

    /// Optional embedding vector for semantic search
    #[serde(skip_serializing_if = "Option::is_none")]
    pub embedding: Option<Vec<f32>>,

    /// Timestamp when created
    pub created_at: DateTime<Utc>,

    /// Optional expiration time (TTL)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<DateTime<Utc>>,
}

impl MemoryEntry {
    /// Create a new memory entry with generated ID
    pub fn new(content: impl Into<String>) -> Self {
        Self {
            id: uuid::Uuid::new_v4().to_string(),
            content: content.into(),
            metadata: HashMap::new(),
            embedding: None,
            created_at: Utc::now(),
            expires_at: None,
        }
    }

    /// Create with specific ID
    pub fn with_id(id: impl Into<String>, content: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            content: content.into(),
            metadata: HashMap::new(),
            embedding: None,
            created_at: Utc::now(),
            expires_at: None,
        }
    }

    /// Add metadata
    pub fn with_metadata(mut self, key: impl Into<String>, value: Value) -> Self {
        self.metadata.insert(key.into(), value);
        self
    }

    /// Set embedding vector
    pub fn with_embedding(mut self, embedding: Vec<f32>) -> Self {
        self.embedding = Some(embedding);
        self
    }

    /// Set expiration time
    pub fn with_expiration(mut self, expires_at: DateTime<Utc>) -> Self {
        self.expires_at = Some(expires_at);
        self
    }

    /// Set TTL in seconds from now
    pub fn with_ttl_seconds(mut self, seconds: i64) -> Self {
        self.expires_at = Some(Utc::now() + chrono::Duration::seconds(seconds));
        self
    }

    /// Check if entry has expired
    pub fn is_expired(&self) -> bool {
        if let Some(expires_at) = self.expires_at {
            expires_at < Utc::now()
        } else {
            false
        }
    }
}

/// Query filter for memory retrieval
#[derive(Debug, Clone, Default)]
pub struct MemoryQuery {
    /// Metadata filters (exact match)
    pub filters: HashMap<String, Value>,

    /// Limit number of results
    pub limit: Option<usize>,

    /// Semantic search query (if vector backend)
    pub semantic_query: Option<String>,

    /// Similarity threshold for vector search (0.0 to 1.0)
    pub similarity_threshold: Option<f32>,
}

impl MemoryQuery {
    /// Create a new empty query
    pub fn new() -> Self {
        Self::default()
    }

    /// Add a metadata filter
    pub fn with_filter(mut self, key: impl Into<String>, value: Value) -> Self {
        self.filters.insert(key.into(), value);
        self
    }

    /// Set result limit
    pub fn with_limit(mut self, limit: usize) -> Self {
        self.limit = Some(limit);
        self
    }

    /// Set semantic search query
    pub fn with_semantic_query(mut self, query: impl Into<String>) -> Self {
        self.semantic_query = Some(query.into());
        self
    }

    /// Set similarity threshold
    pub fn with_threshold(mut self, threshold: f32) -> Self {
        self.similarity_threshold = Some(threshold);
        self
    }
}

/// Base memory trait - all backends must implement this
#[async_trait]
pub trait Memory: Send + Sync {
    /// Store an entry
    async fn store(&self, entry: MemoryEntry) -> Result<String>;

    /// Retrieve by ID
    async fn get(&self, id: &str) -> Result<Option<MemoryEntry>>;

    /// Search with filters
    async fn search(&self, query: MemoryQuery) -> Result<Vec<MemoryEntry>>;

    /// Delete an entry
    async fn delete(&self, id: &str) -> Result<bool>;

    /// Clear all entries
    async fn clear(&self) -> Result<()>;

    /// Count entries
    async fn count(&self) -> Result<usize>;
}

/// Extended trait for vector-based semantic search
#[async_trait]
pub trait VectorMemory: Memory {
    /// Generate embedding for text
    async fn embed(&self, text: &str) -> Result<Vec<f32>>;

    /// Semantic similarity search
    /// Returns entries with similarity scores (higher = more similar)
    async fn similarity_search(
        &self,
        query: &str,
        limit: Option<usize>,
        threshold: Option<f32>,
    ) -> Result<Vec<(MemoryEntry, f32)>>;
}
