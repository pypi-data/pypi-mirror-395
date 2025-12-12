use runtime::core::agent::{Agent, AgentContext};
use runtime::core::error::Result;
use runtime::core::message::Message;
use runtime::core::mesh::Mesh;
use runtime::local::LocalMesh;
use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Notify;
use std::time::Duration;

// --- Worker Agent ---
struct WorkerAgent {
    mesh: Arc<LocalMesh>,
}

#[async_trait]
impl Agent for WorkerAgent {
    fn name(&self) -> String {
        "worker".to_string()
    }

    async fn on_start(&mut self, _ctx: &mut AgentContext) -> Result<()> {
        println!("[Worker] Started and ready for tasks.");
        Ok(())
    }

    async fn on_message(&mut self, msg: Message, _ctx: &mut AgentContext) -> Result<()> {
        let content = String::from_utf8_lossy(&msg.payload);
        println!("[Worker] Received task from {}: {}", msg.sender, content);

        // Simulate processing
        tokio::time::sleep(Duration::from_millis(500)).await;

        // Send response
        let response = format!("Processed: {}", content);
        println!("[Worker] Sending response: {}", response);
        
        let reply_msg = Message::new("result", response.into_bytes(), self.name());
        self.mesh.send(reply_msg, &msg.sender).await?;
        
        Ok(())
    }
}

// --- Manager Agent ---
struct ManagerAgent {
    mesh: Arc<LocalMesh>,
    completion_notify: Arc<Notify>,
}

#[async_trait]
impl Agent for ManagerAgent {
    fn name(&self) -> String {
        "manager".to_string()
    }

    async fn on_start(&mut self, _ctx: &mut AgentContext) -> Result<()> {
        println!("[Manager] Started. Sending task to worker...");
        
        // Send a task to the worker
        let task_msg = Message::new("task", b"Analyze data".to_vec(), self.name());
        self.mesh.send(task_msg, "worker").await?;
        
        Ok(())
    }

    async fn on_message(&mut self, msg: Message, _ctx: &mut AgentContext) -> Result<()> {
        let content = String::from_utf8_lossy(&msg.payload);
        println!("[Manager] Received result from {}: {}", msg.sender, content);
        
        // Signal completion
        self.completion_notify.notify_one();
        Ok(())
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    // 1. Create the Mesh (wrapped in Arc for sharing)
    let mesh = Arc::new(LocalMesh::new("main_mesh"));
    
    // 2. Create Agents with reference to mesh
    let completion = Arc::new(Notify::new());
    
    let worker = Box::new(WorkerAgent { mesh: mesh.clone() });
    let manager = Box::new(ManagerAgent { 
        mesh: mesh.clone(),
        completion_notify: completion.clone() 
    });

    // 3. Register Agents
    mesh.add_agent(worker).await?;
    mesh.add_agent(manager).await?;

    // 4. Start Mesh
    mesh.start().await?;
    
    // Wait for the interaction to complete
    println!("Waiting for interaction to complete...");
    // Timeout after 5 seconds
    tokio::select! {
        _ = completion.notified() => {
            println!("Interaction completed successfully!");
        }
        _ = tokio::time::sleep(Duration::from_secs(5)) => {
            println!("Timeout waiting for interaction.");
        }
    }

    // 5. Stop Mesh
    mesh.stop().await?;
    
    Ok(())
}
