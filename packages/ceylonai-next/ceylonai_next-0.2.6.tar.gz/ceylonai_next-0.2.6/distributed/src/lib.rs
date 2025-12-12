pub mod ceylon {
    tonic::include_proto!("ceylon");
}

pub mod conversion;
pub mod mesh;
pub mod service;
pub mod registry;

pub use ceylon::*;
pub use mesh::DistributedMesh;
