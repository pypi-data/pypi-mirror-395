use crate::ceylon::mesh_service_server::MeshService;
use crate::ceylon::{Envelope, Ack, AgentInfo, RegistrationResponse, AgentQuery, AgentList};
use runtime::LocalMesh;
use runtime::Mesh;
use runtime::Message;
use tonic::{Request, Response, Status};
use std::sync::Arc;

pub struct GrpcMeshService {
    local_mesh: Arc<LocalMesh>,
}

impl GrpcMeshService {
    pub fn new(local_mesh: Arc<LocalMesh>) -> Self {
        Self { local_mesh }
    }
}

#[tonic::async_trait]
impl MeshService for GrpcMeshService {
    async fn send(&self, request: Request<Envelope>) -> Result<Response<Ack>, Status> {
        let envelope = request.into_inner();
        
        if let Some(msg) = envelope.message {
             let runtime_msg: Message = msg.into();
             // Determine target
             let target = envelope.target_agent.ok_or(Status::invalid_argument("Missing target agent"))?;
             
             match self.local_mesh.send(runtime_msg, &target).await {
                 Ok(_) => Ok(Response::new(Ack { success: true, error: "".to_string() })),
                 Err(e) => Ok(Response::new(Ack { success: false, error: e.to_string() })),
             }
        } else {
             Err(Status::invalid_argument("Missing message"))
        }
    }

    async fn register(&self, _request: Request<AgentInfo>) -> Result<Response<RegistrationResponse>, Status> {
        // Registration logic (TODO)
        Ok(Response::new(RegistrationResponse { success: true, error: "".to_string() }))
    }

    async fn discover(&self, _request: Request<AgentQuery>) -> Result<Response<AgentList>, Status> {
        // Discovery logic (TODO)
        Ok(Response::new(AgentList { agents: vec![] }))
    }
}
