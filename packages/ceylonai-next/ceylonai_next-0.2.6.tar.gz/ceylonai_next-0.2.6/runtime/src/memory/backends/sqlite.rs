#[cfg(feature = "sqlite")]
use crate::core::error::Result;
#[cfg(feature = "sqlite")]
use crate::core::memory::{Memory, MemoryEntry, MemoryQuery};
#[cfg(feature = "sqlite")]
use async_trait::async_trait;
#[cfg(feature = "sqlite")]
use sqlx::{sqlite::SqlitePool, Row};
#[cfg(feature = "sqlite")]
use std::path::Path;

#[cfg(feature = "sqlite")]
pub struct SqliteBackend {
    pool: SqlitePool,
}

#[cfg(feature = "sqlite")]
impl SqliteBackend {
    pub async fn new(path: impl AsRef<Path>) -> Result<Self> {
        let path_str = path
            .as_ref()
            .to_str()
            .ok_or_else(|| crate::core::error::Error::MeshError("Invalid path".to_string()))?;

        let database_url = format!("sqlite:{}", path_str);
        let pool = SqlitePool::connect(&database_url)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;

        sqlx::query(
            r#"CREATE TABLE IF NOT EXISTS memory_entries (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                metadata TEXT NOT NULL,
                embedding BLOB,
                created_at INTEGER NOT NULL,
                expires_at INTEGER
            )"#,
        )
        .execute(&pool)
        .await
        .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;

        sqlx::query("CREATE INDEX IF NOT EXISTS idx_expires_at ON memory_entries(expires_at)")
            .execute(&pool)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;

        Ok(Self { pool })
    }

    pub async fn in_memory() -> Result<Self> {
        Self::new(":memory:").await
    }

    async fn cleanup_expired(&self) -> Result<()> {
        let now = chrono::Utc::now().timestamp();
        sqlx::query("DELETE FROM memory_entries WHERE expires_at IS NOT NULL AND expires_at < ?")
            .bind(now)
            .execute(&self.pool)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        Ok(())
    }

    fn row_to_entry(&self, row: &sqlx::sqlite::SqliteRow) -> Result<MemoryEntry> {
        use chrono::TimeZone;

        let id: String = row
            .try_get("id")
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        let content: String = row
            .try_get("content")
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        let metadata_json: String = row
            .try_get("metadata")
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        let embedding_bytes: Option<Vec<u8>> = row
            .try_get("embedding")
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        let created_at_ts: i64 = row
            .try_get("created_at")
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        let expires_at_ts: Option<i64> = row
            .try_get("expires_at")
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;

        let metadata = serde_json::from_str(&metadata_json)?;
        let embedding = embedding_bytes
            .map(|bytes| bincode::deserialize(&bytes))
            .transpose()
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;

        let created_at = chrono::Utc
            .timestamp_opt(created_at_ts, 0)
            .single()
            .ok_or_else(|| crate::core::error::Error::MeshError("Invalid timestamp".to_string()))?;
        let expires_at = expires_at_ts.and_then(|ts| chrono::Utc.timestamp_opt(ts, 0).single());

        Ok(MemoryEntry {
            id,
            content,
            metadata,
            embedding,
            created_at,
            expires_at,
        })
    }
}

#[cfg(feature = "sqlite")]
#[async_trait]
impl Memory for SqliteBackend {
    async fn store(&self, entry: MemoryEntry) -> Result<String> {
        let metadata_json = serde_json::to_string(&entry.metadata)?;
        let embedding_bytes = entry
            .embedding
            .as_ref()
            .map(|e| bincode::serialize(e))
            .transpose()
            .map_err(|e: bincode::Error| crate::core::error::Error::MeshError(e.to_string()))?;

        sqlx::query(
            r#"INSERT OR REPLACE INTO memory_entries 
            (id, content, metadata, embedding, created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?)"#,
        )
        .bind(&entry.id)
        .bind(&entry.content)
        .bind(&metadata_json)
        .bind(embedding_bytes)
        .bind(entry.created_at.timestamp())
        .bind(entry.expires_at.map(|t| t.timestamp()))
        .execute(&self.pool)
        .await
        .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;

        Ok(entry.id)
    }

    async fn get(&self, id: &str) -> Result<Option<MemoryEntry>> {
        let row = sqlx::query("SELECT * FROM memory_entries WHERE id = ?")
            .bind(id)
            .fetch_optional(&self.pool)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;

        if let Some(row) = row {
            let entry = self.row_to_entry(&row)?;
            if entry.is_expired() {
                self.delete(id).await?;
                Ok(None)
            } else {
                Ok(Some(entry))
            }
        } else {
            Ok(None)
        }
    }

    async fn search(&self, query: MemoryQuery) -> Result<Vec<MemoryEntry>> {
        self.cleanup_expired().await?;
        let mut sql = "SELECT * FROM memory_entries WHERE 1=1".to_string();
        let mut bindings = Vec::new();

        for (key, value) in &query.filters {
            sql.push_str(&format!(" AND json_extract(metadata, '$.{}') = ?", key));
            bindings.push(value.to_string());
        }

        sql.push_str(" ORDER BY created_at DESC");
        if let Some(limit) = query.limit {
            sql.push_str(&format!(" LIMIT {}", limit));
        }

        let mut query_builder = sqlx::query(&sql);
        for binding in bindings {
            query_builder = query_builder.bind(binding);
        }

        let rows = query_builder
            .fetch_all(&self.pool)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;

        rows.iter().map(|row| self.row_to_entry(row)).collect()
    }

    async fn delete(&self, id: &str) -> Result<bool> {
        let result = sqlx::query("DELETE FROM memory_entries WHERE id = ?")
            .bind(id)
            .execute(&self.pool)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        Ok(result.rows_affected() > 0)
    }

    async fn clear(&self) -> Result<()> {
        sqlx::query("DELETE FROM memory_entries")
            .execute(&self.pool)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        Ok(())
    }

    async fn count(&self) -> Result<usize> {
        self.cleanup_expired().await?;
        let row = sqlx::query("SELECT COUNT(*) as count FROM memory_entries")
            .fetch_one(&self.pool)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        let count: i64 = row
            .try_get("count")
            .map_err(|e| crate::core::error::Error::MeshError(e.to_string()))?;
        Ok(count as usize)
    }
}

#[cfg(all(test, feature = "sqlite"))]
mod tests {
    use super::*;
    use serde_json::json;

    #[tokio::test]
    async fn test_sqlite_basic_storage() {
        let backend = SqliteBackend::in_memory().await.unwrap();
        let entry = MemoryEntry::new("test content");
        let id = backend.store(entry.clone()).await.unwrap();
        let retrieved = backend.get(&id).await.unwrap();
        assert!(retrieved.is_some());
        assert_eq!(retrieved.unwrap().content, "test content");
    }

    #[tokio::test]
    async fn test_sqlite_persistence() {
        let temp_file = std::env::temp_dir().join("test_memory.db");
        {
            let backend = SqliteBackend::new(&temp_file).await.unwrap();
            backend
                .store(MemoryEntry::new("persistent data"))
                .await
                .unwrap();
        }
        {
            let backend = SqliteBackend::new(&temp_file).await.unwrap();
            let results = backend.search(MemoryQuery::new()).await.unwrap();
            assert_eq!(results.len(), 1);
            assert_eq!(results[0].content, "persistent data");
        }
        let _ = std::fs::remove_file(temp_file);
    }

    #[tokio::test]
    async fn test_sqlite_metadata_search() {
        let backend = SqliteBackend::in_memory().await.unwrap();
        backend
            .store(MemoryEntry::new("user message").with_metadata("type", json!("user")))
            .await
            .unwrap();
        backend
            .store(MemoryEntry::new("system message").with_metadata("type", json!("system")))
            .await
            .unwrap();
        let query = MemoryQuery::new().with_filter("type", json!("user"));
        let results = backend.search(query).await.unwrap();
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].content, "user message");
    }

    #[tokio::test]
    async fn test_sqlite_ttl() {
        let backend = SqliteBackend::in_memory().await.unwrap();
        let entry = MemoryEntry::new("expires soon").with_ttl_seconds(1);
        let id = backend.store(entry).await.unwrap();
        assert!(backend.get(&id).await.unwrap().is_some());
        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;
        assert!(backend.get(&id).await.unwrap().is_none());
    }

    #[tokio::test]
    async fn test_sqlite_delete() {
        let backend = SqliteBackend::in_memory().await.unwrap();
        let entry = MemoryEntry::new("to delete");
        let id = backend.store(entry).await.unwrap();
        assert!(backend.delete(&id).await.unwrap());
        assert!(backend.get(&id).await.unwrap().is_none());
        assert!(!backend.delete(&id).await.unwrap());
    }
}
