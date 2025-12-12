use crate::core::agent::Agent;
use crate::core::error::Result;
use crate::core::message::Message;
use async_trait::async_trait;

#[async_trait]
pub trait Mesh: Send + Sync {
    async fn start(&self) -> Result<()>;
    async fn stop(&self) -> Result<()>;
    async fn add_agent(&self, agent: Box<dyn Agent + 'static>) -> Result<()>;
    async fn send(&self, message: Message, target: &str) -> Result<()>;
}
