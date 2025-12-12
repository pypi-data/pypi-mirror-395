use thiserror::Error;

#[derive(Error, Debug)]
pub enum Error {
    #[error("Agent not found: {0}")]
    AgentNotFound(String),
    #[error("Mesh error: {0}")]
    MeshError(String),
    #[error("Serialization error: {0}")]
    SerializationError(#[from] serde_json::Error),
    #[error("Action not found: {0}")]
    ActionNotFound(String),
    #[error("Action execution failed: {0}")]
    ActionExecutionError(String),
    #[error("Unknown error: {0}")]
    Unknown(#[from] anyhow::Error),
}

pub type Result<T> = std::result::Result<T, Error>;
