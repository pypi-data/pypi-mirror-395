use async_trait::async_trait;
use distributed::DistributedMesh;
use runtime::core::error::Result;
use runtime::{Agent, AgentContext, Mesh, Message};

struct EchoAgent;

#[async_trait]
impl Agent for EchoAgent {
    fn name(&self) -> String {
        "echo_agent".to_string()
    }

    async fn on_start(&mut self, _ctx: &mut AgentContext) -> Result<()> {
        println!("EchoAgent started!");
        Ok(())
    }

    async fn on_stop(&mut self, _ctx: &mut AgentContext) -> Result<()> {
        println!("EchoAgent stopped!");
        Ok(())
    }

    async fn on_message(&mut self, msg: Message, _ctx: &mut AgentContext) -> Result<()> {
        println!(
            "EchoAgent received message: {:?}",
            String::from_utf8_lossy(&msg.payload)
        );
        // In a real scenario, we might send a reply back.
        // For now, just logging is enough to prove it works.
        Ok(())
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    // Create the mesh on port 50051
    let mesh = DistributedMesh::new("server_node", 50051);

    // Add the echo agent
    mesh.add_agent(Box::new(EchoAgent)).await?;

    // Start the mesh (starts gRPC server)
    mesh.start().await?;

    println!("Server running on port 50051. Press Ctrl+C to stop.");

    // Keep running until Ctrl+C
    tokio::signal::ctrl_c()
        .await
        .map_err(|e| runtime::core::error::Error::Unknown(e.into()))?;

    println!("Shutting down...");
    mesh.stop().await?;

    Ok(())
}
