use async_trait::async_trait;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use runtime::core::agent::{Agent, AgentContext};
use runtime::core::message::Message;

/// Base class for Python Agents
#[derive(Clone)]
#[pyclass(subclass)]
pub struct PyAgent {}

#[pymethods]
impl PyAgent {
    #[new]
    #[pyo3(signature = (_name = String::new()))]
    fn new(_name: String) -> Self {
        PyAgent {}
    }

    fn name(&self) -> String {
        "agent".to_string() // Default name, should be overridden by subclasses
    }

    fn act(self_: Py<Self>, action_name: String, inputs: Py<PyDict>) -> PyResult<Py<PyAny>> {
        Python::with_gil(|py| {
            let bound = self_.bind(py);
            if let Ok(tool_invoker) = bound.getattr("tool_invoker") {
                let json = py.import("json")?;
                let inputs_str: String = json.call_method1("dumps", (inputs,))?.extract()?;

                let result = tool_invoker.call_method1("invoke", (action_name, inputs_str))?;
                Ok(result.into())
            } else {
                Ok(py.None())
            }
        })
    }
}

/// Wrapper to adapt Python Agents to Rust Agent trait
pub struct PythonAgentWrapper {
    pub agent: Py<PyAgent>,
}

#[async_trait::async_trait]
impl Agent for PythonAgentWrapper {
    fn name(&self) -> String {
        Python::with_gil(|py| {
            let agent = self.agent.bind(py);
            // Try to call the name() method on the Python object
            if let Ok(name) = agent.call_method0("name") {
                name.extract().unwrap_or_else(|_| "unknown".to_string())
            } else {
                "unknown".to_string()
            }
        })
    }

    async fn on_start(&mut self, _ctx: &mut AgentContext) -> runtime::core::error::Result<()> {
        // Call on_start on the Python object if it exists
        Python::with_gil(|py| {
            let agent = self.agent.bind(py);
            if agent.hasattr("on_start")? {
                // TODO: Pass context to Python
                // We need to wrap AgentContext into a Python object to pass it here
                agent.call_method1("on_start", (py.None(),))?;
            }
            Ok(())
        })
        .map_err(|e: PyErr| runtime::core::error::Error::MeshError(e.to_string()))
    }

    async fn on_message(
        &mut self,
        msg: Message,
        _ctx: &mut AgentContext,
    ) -> runtime::core::error::Result<()> {
        let result = Python::with_gil(|py| {
            let agent = self.agent.bind(py);
            if agent.hasattr("on_message")? {
                // Pass proper message object and context
                // Convert bytes to string
                let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
                let result = agent.call_method1("on_message", (payload_str, py.None()))?;

                // Check if the result is awaitable (coroutine)
                let asyncio = py.import("asyncio")?;
                let is_coroutine = asyncio
                    .call_method1("iscoroutine", (result.clone(),))?
                    .extract::<bool>()?;

                if is_coroutine {
                    // Create a new event loop for this thread
                    let new_loop = asyncio.call_method0("new_event_loop")?;

                    // Get the current event loop (if any) to restore later
                    let old_loop = asyncio.call_method0("get_event_loop").ok();

                    // Temporarily set the new loop as the current loop for this thread
                    asyncio.call_method1("set_event_loop", (new_loop.clone(),))?;

                    // Run the coroutine on this thread-local event loop
                    let coro_result = new_loop.call_method1("run_until_complete", (result,));

                    // Restore the old event loop (or set to None)
                    if let Some(old) = old_loop {
                        asyncio.call_method1("set_event_loop", (old,))?;
                    } else {
                        asyncio.call_method1("set_event_loop", (py.None(),))?;
                    }

                    // Close the loop to clean up
                    new_loop.call_method0("close")?;

                    // Check if run_until_complete succeeded
                    coro_result?;

                    // Return None since we already executed the coroutine
                    Ok::<Option<Py<PyAny>>, PyErr>(None)
                } else {
                    Ok::<Option<Py<PyAny>>, PyErr>(None)
                }
            } else {
                Ok::<Option<Py<PyAny>>, PyErr>(None)
            }
        })
        .map_err(|e: PyErr| runtime::core::error::Error::MeshError(e.to_string()))?;

        Ok(())
    }

    async fn on_stop(&mut self, _ctx: &mut AgentContext) -> runtime::core::error::Result<()> {
        Python::with_gil(|py| {
            let agent = self.agent.bind(py);
            if agent.hasattr("on_stop")? {
                agent.call_method1("on_stop", (py.None(),))?;
            }
            Ok(())
        })
        .map_err(|e: PyErr| runtime::core::error::Error::MeshError(e.to_string()))
    }
}

/// Python wrapper for AgentContext
#[pyclass]
#[derive(Clone)]
pub struct PyAgentContext {
    #[pyo3(get)]
    pub mesh_name: String,
}

#[pymethods]
impl PyAgentContext {
    #[new]
    fn new(mesh_name: String) -> Self {
        PyAgentContext { mesh_name }
    }
}
