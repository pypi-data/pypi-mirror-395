use distributed::{DistributedMesh, registry::InMemoryRegistry};
use runtime::{Agent, AgentContext, Message, Mesh};
use runtime::core::error::Result;
use std::sync::Arc;
use tokio::time::Duration;

struct EchoAgent {
    name: String,
}

#[async_trait::async_trait]
impl Agent for EchoAgent {
    fn name(&self) -> String {
        self.name.clone()
    }

    async fn on_message(&mut self, msg: Message, _ctx: &mut AgentContext) -> Result<()> {
        println!("Agent {} received: {:?}", self.name, msg);
        Ok(())
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let registry = Arc::new(InMemoryRegistry::new());

    // Mesh 1
    let mesh1 = DistributedMesh::with_registry("mesh1", 50051, registry.clone());
    mesh1.start().await?;
    mesh1.add_agent(Box::new(EchoAgent { name: "agent1".to_string() })).await?;

    // Mesh 2
    let mesh2 = DistributedMesh::with_registry("mesh2", 50052, registry.clone());
    mesh2.start().await?;
    mesh2.add_agent(Box::new(EchoAgent { name: "agent2".to_string() })).await?;

    // Give some time for servers to start
    tokio::time::sleep(Duration::from_secs(1)).await;

    // Send message from agent1 to agent2
    println!("Sending message from agent1 to agent2...");
    let msg = Message::new("chat", "Hello from agent1".as_bytes().to_vec(), "agent1");
    mesh1.send(msg, "agent2").await?;

    // Wait for message delivery
    tokio::time::sleep(Duration::from_secs(1)).await;

    Ok(())
}
