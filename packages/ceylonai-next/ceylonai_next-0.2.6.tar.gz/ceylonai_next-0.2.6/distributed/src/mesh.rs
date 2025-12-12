use crate::service::GrpcMeshService;
use crate::ceylon::mesh_service_server::MeshServiceServer;
use runtime::{Mesh, LocalMesh, Agent, Message};
use runtime::core::error::Result;
use std::sync::Arc;
use tonic::transport::Server;
use async_trait::async_trait;

use std::collections::HashMap;
use tokio::sync::RwLock;
use crate::ceylon::mesh_service_client::MeshServiceClient;
use crate::ceylon::Envelope;
use crate::registry::{Registry, InMemoryRegistry, AgentMetadata, HealthStatus};

pub struct DistributedMesh {
    local_mesh: Arc<LocalMesh>,
    port: u16,
    // Map of agent_name -> node_url
    peers: Arc<RwLock<HashMap<String, String>>>,
    registry: Arc<dyn Registry + Send + Sync>,
}

impl DistributedMesh {
    pub fn new(name: impl Into<String>, port: u16) -> Self {
        Self {
            local_mesh: Arc::new(LocalMesh::new(name)),
            port,
            peers: Arc::new(RwLock::new(HashMap::new())),
            registry: Arc::new(InMemoryRegistry::new()),
        }
    }

    pub fn with_registry(name: impl Into<String>, port: u16, registry: Arc<dyn Registry + Send + Sync>) -> Self {
        Self {
            local_mesh: Arc::new(LocalMesh::new(name)),
            port,
            peers: Arc::new(RwLock::new(HashMap::new())),
            registry,
        }
    }

    pub async fn connect_peer(&self, agent_name: String, url: String) {
        let mut peers = self.peers.write().await;
        peers.insert(agent_name, url);
    }
}

#[async_trait]
impl Mesh for DistributedMesh {
    async fn start(&self) -> Result<()> {
        self.local_mesh.start().await?;
        
        let addr = format!("0.0.0.0:{}", self.port).parse().map_err(|e| runtime::core::error::Error::MeshError(format!("Invalid address: {}", e)))?;
        let service = GrpcMeshService::new(self.local_mesh.clone());
        
        println!("Starting DistributedMesh on port {}", self.port);
        
        tokio::spawn(async move {
            if let Err(e) = Server::builder()
                .add_service(MeshServiceServer::new(service))
                .serve(addr)
                .await {
                    eprintln!("gRPC server error: {}", e);
                }
        });
        
        Ok(())
    }

    async fn stop(&self) -> Result<()> {
        self.local_mesh.stop().await
    }

    async fn add_agent(&self, agent: Box<dyn Agent + 'static>) -> Result<()> {
        let name = agent.name();
        self.local_mesh.add_agent(agent).await?;
        
        // Register in the registry
        let metadata = AgentMetadata {
            id: name.clone(),
            name: name,
            address: format!("http://127.0.0.1:{}", self.port),
            capabilities: vec![], // TODO: Extract capabilities from agent
            health_status: HealthStatus::Healthy,
            last_heartbeat: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_secs(),
        };
        
        self.registry.register(metadata).await?;
        Ok(())
    }

    async fn send(&self, message: Message, target: &str) -> Result<()> {
        // Check if target is local
        // We don't have a direct way to check if agent is local in LocalMesh public API easily 
        // without trying to send or checking registry.
        // But LocalMesh.send will fail if agent not found.
        
        // Let's check our peers map first.
        let peer_url = {
            let peers = self.peers.read().await;
            if let Some(url) = peers.get(target) {
                Some(url.clone())
            } else {
                // Check registry
                if let Ok(Some(metadata)) = self.registry.get_agent(target).await {
                    Some(metadata.address)
                } else {
                    None
                }
            }
        };

        if let Some(url) = peer_url {
            // It's a remote agent
            // TODO: Cache clients
            let mut client = MeshServiceClient::connect(url).await
                .map_err(|e| runtime::core::error::Error::MeshError(format!("Failed to connect to peer: {}", e)))?;
            
            let proto_msg: crate::ceylon::Message = message.into();
            let envelope = Envelope {
                message: Some(proto_msg),
                target_agent: Some(target.to_string()),
                target_node: None,
            };
            
            let _ = client.send(tonic::Request::new(envelope)).await
                .map_err(|e| runtime::core::error::Error::MeshError(format!("Failed to send to peer: {}", e)))?;
                
            Ok(())
        } else {
            // Try local
            self.local_mesh.send(message, target).await
        }
    }
}
