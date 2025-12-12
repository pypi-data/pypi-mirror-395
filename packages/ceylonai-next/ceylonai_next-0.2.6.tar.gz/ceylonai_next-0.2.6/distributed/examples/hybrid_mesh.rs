use distributed::{DistributedMesh, registry::InMemoryRegistry};
use runtime::{Agent, AgentContext, Message, Mesh};
use runtime::core::error::Result;
use std::sync::Arc;
use tokio::time::Duration;

// An agent that can send messages to a target
struct CommunicatingAgent {
    name: String,
    mesh: Arc<dyn Mesh + Send + Sync>,
    target: Option<String>,
}

#[async_trait::async_trait]
impl Agent for CommunicatingAgent {
    fn name(&self) -> String {
        self.name.clone()
    }

    async fn on_message(&mut self, msg: Message, _ctx: &mut AgentContext) -> Result<()> {
        let content = String::from_utf8(msg.payload.clone()).unwrap_or_default();
        println!("[{}] Received: '{}' from {}", self.name, content, msg.sender);

        if content == "trigger" {
            if let Some(target) = &self.target {
                println!("[{}] Triggered! Sending 'Hello' to {}", self.name, target);
                let response = Message::new("chat", "Hello".as_bytes().to_vec(), self.name.clone());
                if let Err(e) = self.mesh.send(response, target).await {
                    eprintln!("[{}] Failed to send to {}: {:?}", self.name, target, e);
                }
            } else {
                println!("[{}] Triggered but no target set.", self.name);
            }
        }
        Ok(())
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    // Shared registry for discovery
    let registry = Arc::new(InMemoryRegistry::new());

    // --- Node 1 (Port 50081) ---
    let mesh1 = Arc::new(DistributedMesh::with_registry("node1", 50081, registry.clone()));
    mesh1.start().await?;

    // Agent 1 on Node 1 (Will send to Agent 2 on Node 2)
    let agent1 = Box::new(CommunicatingAgent {
        name: "agent1".to_string(),
        mesh: mesh1.clone(),
        target: Some("agent2".to_string()),
    });
    mesh1.add_agent(agent1).await?;

    // Agent 3 on Node 1 (Local peer to Agent 1)
    let agent3 = Box::new(CommunicatingAgent {
        name: "agent3".to_string(),
        mesh: mesh1.clone(),
        target: None,
    });
    mesh1.add_agent(agent3).await?;


    // --- Node 2 (Port 50082) ---
    let mesh2 = Arc::new(DistributedMesh::with_registry("node2", 50082, registry.clone()));
    mesh2.start().await?;

    // Agent 2 on Node 2 (Will send to Agent 3 on Node 1)
    let agent2 = Box::new(CommunicatingAgent {
        name: "agent2".to_string(),
        mesh: mesh2.clone(),
        target: Some("agent3".to_string()),
    });
    mesh2.add_agent(agent2).await?;

    // Give time for startup
    tokio::time::sleep(Duration::from_secs(1)).await;

    println!("\n--- Scenario 1: Distributed Communication (Agent 1 -> Agent 2) ---");
    // Trigger Agent 1 to send to Agent 2
    let trigger_msg = Message::new("control", "trigger".as_bytes().to_vec(), "user");
    mesh1.send(trigger_msg, "agent1").await?;

    // Wait for delivery
    tokio::time::sleep(Duration::from_secs(1)).await;


    println!("\n--- Scenario 2: Distributed + Local Communication (Agent 2 -> Agent 3) ---");
    // Trigger Agent 2 to send to Agent 3 (Distributed response)
    // Note: In this setup, Agent 2 is configured to target Agent 3.
    let trigger_msg2 = Message::new("control", "trigger".as_bytes().to_vec(), "user");
    mesh2.send(trigger_msg2, "agent2").await?;

    // Wait for delivery
    tokio::time::sleep(Duration::from_secs(1)).await;


    println!("\n--- Scenario 3: Local Communication (Agent 1 -> Agent 3) ---");
    // Let's dynamically add an agent 4 on Node 1 that targets Agent 3 (Local)
    let agent4 = Box::new(CommunicatingAgent {
        name: "agent4".to_string(),
        mesh: mesh1.clone(),
        target: Some("agent3".to_string()),
    });
    mesh1.add_agent(agent4).await?;
    
    // Trigger Agent 4
    let trigger_msg3 = Message::new("control", "trigger".as_bytes().to_vec(), "user");
    mesh1.send(trigger_msg3, "agent4").await?;

    // Wait for delivery
    tokio::time::sleep(Duration::from_secs(1)).await;

    Ok(())
}
