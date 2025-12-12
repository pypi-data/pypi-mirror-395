use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use runtime::core::error::Result;
use async_trait::async_trait;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum HealthStatus {
    Healthy,
    Unhealthy,
    Unknown,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentMetadata {
    pub id: String,
    pub name: String,
    pub address: String,
    pub capabilities: Vec<String>,
    pub health_status: HealthStatus,
    pub last_heartbeat: u64,
}

#[async_trait]
pub trait Registry: Send + Sync {
    async fn register(&self, metadata: AgentMetadata) -> Result<()>;
    async fn deregister(&self, agent_id: &str) -> Result<()>;
    async fn get_agent(&self, agent_id: &str) -> Result<Option<AgentMetadata>>;
    async fn list_agents(&self) -> Result<Vec<AgentMetadata>>;
    async fn heartbeat(&self, agent_id: &str) -> Result<()>;
}

pub struct InMemoryRegistry {
    agents: Arc<RwLock<HashMap<String, AgentMetadata>>>,
}

impl InMemoryRegistry {
    pub fn new() -> Self {
        Self {
            agents: Arc::new(RwLock::new(HashMap::new())),
        }
    }
}

#[async_trait]
impl Registry for InMemoryRegistry {
    async fn register(&self, metadata: AgentMetadata) -> Result<()> {
        let mut agents = self.agents.write().await;
        agents.insert(metadata.id.clone(), metadata);
        Ok(())
    }

    async fn deregister(&self, agent_id: &str) -> Result<()> {
        let mut agents = self.agents.write().await;
        agents.remove(agent_id);
        Ok(())
    }

    async fn get_agent(&self, agent_id: &str) -> Result<Option<AgentMetadata>> {
        let agents = self.agents.read().await;
        Ok(agents.get(agent_id).cloned())
    }

    async fn list_agents(&self) -> Result<Vec<AgentMetadata>> {
        let agents = self.agents.read().await;
        Ok(agents.values().cloned().collect())
    }

    async fn heartbeat(&self, agent_id: &str) -> Result<()> {
        let mut agents = self.agents.write().await;
        if let Some(agent) = agents.get_mut(agent_id) {
            agent.last_heartbeat = std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_secs();
            agent.health_status = HealthStatus::Healthy;
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_register_and_get_agent() {
        let registry = InMemoryRegistry::new();
        let metadata = AgentMetadata {
            id: "agent1".to_string(),
            name: "Agent 1".to_string(),
            address: "http://localhost:8080".to_string(),
            capabilities: vec!["chat".to_string()],
            health_status: HealthStatus::Healthy,
            last_heartbeat: 0,
        };

        registry.register(metadata.clone()).await.unwrap();

        let retrieved = registry.get_agent("agent1").await.unwrap();
        assert!(retrieved.is_some());
        assert_eq!(retrieved.unwrap().id, "agent1");
    }

    #[tokio::test]
    async fn test_deregister_agent() {
        let registry = InMemoryRegistry::new();
        let metadata = AgentMetadata {
            id: "agent1".to_string(),
            name: "Agent 1".to_string(),
            address: "http://localhost:8080".to_string(),
            capabilities: vec![],
            health_status: HealthStatus::Healthy,
            last_heartbeat: 0,
        };

        registry.register(metadata).await.unwrap();
        registry.deregister("agent1").await.unwrap();

        let retrieved = registry.get_agent("agent1").await.unwrap();
        assert!(retrieved.is_none());
    }

    #[tokio::test]
    async fn test_list_agents() {
        let registry = InMemoryRegistry::new();
        let metadata = AgentMetadata {
            id: "agent1".to_string(),
            name: "Agent 1".to_string(),
            address: "http://localhost:8080".to_string(),
            capabilities: vec![],
            health_status: HealthStatus::Healthy,
            last_heartbeat: 0,
        };

        registry.register(metadata).await.unwrap();
        let agents = registry.list_agents().await.unwrap();
        assert_eq!(agents.len(), 1);
        assert_eq!(agents[0].id, "agent1");
    }
}
