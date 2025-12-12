use distributed::{DistributedMesh, registry::InMemoryRegistry};
use runtime::{Agent, AgentContext, Message, Mesh};
use runtime::core::error::Result;
use std::sync::Arc;
use tokio::time::Duration;

struct TestAgent {
    name: String,
    received_messages: Arc<tokio::sync::Mutex<Vec<String>>>,
}

#[async_trait::async_trait]
impl Agent for TestAgent {
    fn name(&self) -> String {
        self.name.clone()
    }

    async fn on_message(&mut self, msg: Message, _ctx: &mut AgentContext) -> Result<()> {
        let content = String::from_utf8(msg.payload).unwrap_or_default();
        self.received_messages.lock().await.push(content);
        Ok(())
    }
}

#[tokio::test]
async fn test_discovery_and_messaging() -> Result<()> {
    let registry = Arc::new(InMemoryRegistry::new());

    // Mesh 1
    let mesh1 = DistributedMesh::with_registry("mesh1", 50061, registry.clone());
    mesh1.start().await?;
    let received1 = Arc::new(tokio::sync::Mutex::new(Vec::new()));
    mesh1.add_agent(Box::new(TestAgent { 
        name: "agent1".to_string(),
        received_messages: received1.clone(),
    })).await?;

    // Mesh 2
    let mesh2 = DistributedMesh::with_registry("mesh2", 50062, registry.clone());
    mesh2.start().await?;
    let received2 = Arc::new(tokio::sync::Mutex::new(Vec::new()));
    mesh2.add_agent(Box::new(TestAgent { 
        name: "agent2".to_string(),
        received_messages: received2.clone(),
    })).await?;

    // Give some time for servers to start
    tokio::time::sleep(Duration::from_secs(1)).await;

    // Send message from agent1 to agent2
    let msg = Message::new("chat", "Hello agent2".as_bytes().to_vec(), "agent1");
    mesh1.send(msg, "agent2").await?;

    // Wait for message delivery
    tokio::time::sleep(Duration::from_secs(1)).await;

    let messages = received2.lock().await;
    assert_eq!(messages.len(), 1);
    assert_eq!(messages[0], "Hello agent2");

    Ok(())
}
