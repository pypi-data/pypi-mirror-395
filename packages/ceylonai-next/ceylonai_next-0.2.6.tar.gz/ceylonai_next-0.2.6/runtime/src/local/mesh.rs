use crate::core::agent::{Agent, AgentContext};
use crate::core::error::{Error, Result};
use crate::core::mesh::Mesh;
use crate::core::message::Message;
use async_trait::async_trait;
use dashmap::DashMap;
use tokio::sync::mpsc::{self, Sender};
use tokio::task::JoinHandle;

pub struct LocalMesh {
    name: String,
    agents: DashMap<String, Sender<Message>>,
    tasks: DashMap<String, JoinHandle<()>>,
}

impl LocalMesh {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            agents: DashMap::new(),
            tasks: DashMap::new(),
        }
    }
}

#[async_trait]
impl Mesh for LocalMesh {
    async fn start(&self) -> Result<()> {
        // For local mesh, start might just be a signal,
        // but agents are started when added for now.
        Ok(())
    }

    async fn stop(&self) -> Result<()> {
        for entry in self.tasks.iter() {
            entry.value().abort();
        }
        self.tasks.clear();
        self.agents.clear();
        Ok(())
    }

    async fn add_agent(&self, mut agent: Box<dyn Agent + 'static>) -> Result<()> {
        let name = agent.name();
        if self.agents.contains_key(&name) {
            return Err(Error::MeshError(format!("Agent {} already exists", name)));
        }

        let (tx, mut rx) = mpsc::channel(100);
        self.agents.insert(name.clone(), tx);

        let mesh_name = self.name.clone();
        let agent_name = name.clone(); // Clone name for use in async block

        // Spawn agent loop
        let handle = tokio::spawn(async move {
            let mut ctx = AgentContext::new(mesh_name);
            if let Err(e) = agent.on_start(&mut ctx).await {
                eprintln!("Error starting agent {}: {:?}", agent_name, e);
                return;
            }

            while let Some(msg) = rx.recv().await {
                let now = chrono::Utc::now().timestamp_micros();
                let latency = (now - msg.created_at).max(0) as u64;
                crate::metrics::metrics().record_message(latency);

                let start = std::time::Instant::now();
                if let Err(e) = agent.on_message(msg, &mut ctx).await {
                    eprintln!("Error processing message in agent {}: {:?}", agent_name, e);
                    crate::metrics::metrics().record_error("agent_message_error");
                }
                let duration = start.elapsed().as_micros() as u64;
                crate::metrics::metrics().record_agent_execution(duration);
            }

            if let Err(e) = agent.on_stop(&mut ctx).await {
                eprintln!("Error stopping agent {}: {:?}", agent_name, e);
            }
        });

        self.tasks.insert(name, handle);
        Ok(())
    }

    async fn send(&self, message: Message, target: &str) -> Result<()> {
        if let Some(sender) = self.agents.get(target) {
            sender
                .send(message)
                .await
                .map_err(|_| Error::MeshError(format!("Failed to send to agent {}", target)))?;
            Ok(())
        } else {
            Err(Error::AgentNotFound(target.to_string()))
        }
    }
}
