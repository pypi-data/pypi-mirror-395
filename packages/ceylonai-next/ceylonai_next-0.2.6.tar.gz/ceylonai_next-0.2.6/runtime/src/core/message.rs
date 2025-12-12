use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Message {
    pub id: String,
    pub topic: String,
    pub payload: Vec<u8>,
    pub sender: String,
    pub metadata: HashMap<String, String>,
    pub created_at: i64,
}

impl Message {
    pub fn new(topic: impl Into<String>, payload: Vec<u8>, sender: impl Into<String>) -> Self {
        Self {
            id: Uuid::new_v4().to_string(),
            topic: topic.into(),
            payload,
            sender: sender.into(),
            metadata: HashMap::new(),
            created_at: chrono::Utc::now().timestamp_micros(),
        }
    }

    pub fn correlation_id(&self) -> Option<String> {
        self.metadata.get("correlation_id").cloned()
    }

    pub fn set_correlation_id(&mut self, id: &str) {
        self.metadata
            .insert("correlation_id".to_string(), id.to_string());
    }
}

/// A generic message used by agents for simple string communication
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GenericMessage {
    pub content: String,
    pub metadata: std::collections::HashMap<String, String>,
}

impl GenericMessage {
    pub fn new(content: impl Into<String>) -> Self {
        Self {
            content: content.into(),
            metadata: std::collections::HashMap::new(),
        }
    }
}

/// A generic response returned by agents after processing a GenericMessage
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GenericResponse {
    pub content: String,
}

impl GenericResponse {
    pub fn new(content: impl Into<String>) -> Self {
        Self {
            content: content.into(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Envelope {
    pub message: Message,
    pub target_agent: Option<String>,
    pub target_node: Option<String>,
}
