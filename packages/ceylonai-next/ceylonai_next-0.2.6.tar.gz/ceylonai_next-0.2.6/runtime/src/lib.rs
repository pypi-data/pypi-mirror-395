pub mod core;
pub mod llm;
pub mod local;
pub mod logging;
pub mod memory;
pub mod metrics;

pub use core::agent::{Agent, AgentContext};
pub use core::memory::{Memory, MemoryEntry, MemoryQuery, VectorMemory};
pub use core::mesh::Mesh;
pub use core::message::Message;
pub use llm::{LLMConfig, LlmAgent, UniversalLLMClient};
pub use local::LocalMesh;
pub use memory::InMemoryBackend;

#[cfg(feature = "sqlite")]
pub use memory::SqliteBackend;
