use pyo3::prelude::*;
use distributed::registry::{AgentMetadata, HealthStatus, InMemoryRegistry, Registry};
use std::sync::Arc;
use crate::runtime::RUNTIME;

/// Python wrapper for AgentMetadata
#[pyclass]
#[derive(Clone)]
pub struct PyAgentMetadata {
    pub inner: AgentMetadata,
}

#[pymethods]
impl PyAgentMetadata {
    #[new]
    fn new(id: String, name: String, address: String) -> Self {
        PyAgentMetadata {
            inner: AgentMetadata {
                id,
                name,
                address,
                capabilities: vec![],
                health_status: HealthStatus::Healthy,
                last_heartbeat: 0,
            },
        }
    }

    #[getter]
    fn id(&self) -> String {
        self.inner.id.clone()
    }

    #[getter]
    fn name(&self) -> String {
        self.inner.name.clone()
    }

    #[getter]
    fn address(&self) -> String {
        self.inner.address.clone()
    }
}

/// Python wrapper for InMemoryRegistry
#[pyclass]
#[derive(Clone)]
pub struct PyInMemoryRegistry {
    pub inner: Arc<InMemoryRegistry>,
}

#[pymethods]
impl PyInMemoryRegistry {
    #[new]
    fn new() -> Self {
        PyInMemoryRegistry {
            inner: Arc::new(InMemoryRegistry::new()),
        }
    }

    fn register(&self, metadata: PyAgentMetadata) -> PyResult<()> {
        let registry = self.inner.clone();
        let meta = metadata.inner;
        RUNTIME.block_on(async move {
            registry.register(meta).await.map_err(|e| {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string())
            })
        })
    }

    fn get_agent(&self, agent_id: String) -> PyResult<Option<PyAgentMetadata>> {
        let registry = self.inner.clone();
        RUNTIME.block_on(async move {
            match registry.get_agent(&agent_id).await {
                Ok(Some(meta)) => Ok(Some(PyAgentMetadata { inner: meta })),
                Ok(None) => Ok(None),
                Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                    e.to_string(),
                )),
            }
        })
    }
}
