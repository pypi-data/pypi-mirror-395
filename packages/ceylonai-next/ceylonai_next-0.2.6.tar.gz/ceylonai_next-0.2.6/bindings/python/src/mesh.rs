use pyo3::prelude::*;
use runtime::core::message::Message;
use runtime::core::mesh::Mesh;
use runtime::LocalMesh;
use distributed::DistributedMesh;
use std::sync::Arc;
use crate::runtime::RUNTIME;
use crate::agent::PythonAgentWrapper;
use crate::registry::PyInMemoryRegistry;

/// Python wrapper for LocalMesh
#[pyclass(subclass)]
pub struct PyLocalMesh {
    pub inner: Arc<LocalMesh>,
}

#[pymethods]
impl PyLocalMesh {
    #[new]
    fn new(name: String) -> Self {
        PyLocalMesh {
            inner: Arc::new(LocalMesh::new(name)),
        }
    }

    fn start(&self) -> PyResult<()> {
        let mesh = self.inner.clone();
        RUNTIME.block_on(async move {
            mesh.start()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn add_agent(&self, agent: Py<crate::agent::PyAgent>) -> PyResult<()> {
        let mesh = self.inner.clone();
        let agent_wrapper = Box::new(PythonAgentWrapper { agent });

        RUNTIME.block_on(async move {
            mesh.add_agent(agent_wrapper)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn send_to(&self, target: String, payload: String) -> PyResult<()> {
        let mesh = self.inner.clone();
        let msg = Message::new("system", payload.into_bytes(), target.clone());

        RUNTIME.block_on(async move {
            mesh.send(msg, &target)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }
}

/// Python wrapper for DistributedMesh
#[pyclass(subclass)]
pub struct PyDistributedMesh {
    pub inner: Arc<DistributedMesh>,
}

#[pymethods]
impl PyDistributedMesh {
    #[new]
    fn new(name: String, port: u16) -> Self {
        PyDistributedMesh {
            inner: Arc::new(DistributedMesh::new(name, port)),
        }
    }

    fn start(&self) -> PyResult<()> {
        let mesh = self.inner.clone();
        RUNTIME.block_on(async move {
            mesh.start()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn stop(&self) -> PyResult<()> {
        let mesh = self.inner.clone();
        RUNTIME.block_on(async move {
            mesh.stop()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn add_agent(&self, agent: Py<crate::agent::PyAgent>) -> PyResult<()> {
        let mesh = self.inner.clone();
        let agent_wrapper = Box::new(PythonAgentWrapper { agent });

        RUNTIME.block_on(async move {
            mesh.add_agent(agent_wrapper)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn connect_peer(&self, agent_name: String, url: String) -> PyResult<()> {
        let mesh = self.inner.clone();
        RUNTIME.block_on(async move {
            mesh.connect_peer(agent_name, url).await;
            Ok(())
        })
    }

    fn send_to(&self, target: String, payload: String) -> PyResult<()> {
        let mesh = self.inner.clone();
        let msg = Message::new("system", payload.into_bytes(), target.clone());

        RUNTIME.block_on(async move {
            mesh.send(msg, &target)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    #[staticmethod]
    fn with_registry(name: String, port: u16, registry: &PyInMemoryRegistry) -> Self {
        let reg = registry.inner.clone();
        PyDistributedMesh {
            inner: Arc::new(DistributedMesh::with_registry(name, port, reg)),
        }
    }
}
