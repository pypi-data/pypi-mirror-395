use async_trait::async_trait;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use runtime::core::action::{ActionInvoker, ActionMetadata, ToolInvoker};
use runtime::core::agent::AgentContext;
use serde_json::Value;
use std::sync::Arc;
use crate::runtime::RUNTIME;
use crate::agent::PyAgentContext;

/// Base class for Python Actions
#[pyclass(subclass, name = "_PyAction")]
pub struct PyAction {
    pub metadata: ActionMetadata,
}

#[pymethods]
impl PyAction {
    #[new]
    #[pyo3(signature = (name, description, input_schema, output_schema=None))]
    fn new(
        name: String,
        description: String,
        input_schema: String,
        output_schema: Option<String>,
    ) -> PyResult<Self> {
        let input_json: Value = serde_json::from_str(&input_schema)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;

        let output_json: Option<Value> = match output_schema {
            Some(s) => Some(
                serde_json::from_str(&s)
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?,
            ),
            None => None,
        };

        Ok(PyAction {
            metadata: ActionMetadata {
                name,
                description,
                input_schema: input_json,
                output_schema: output_json,
            },
        })
    }

    fn metadata(&self) -> PyResult<String> {
        serde_json::to_string(&self.metadata)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))
    }

    fn execute(&self, _context: Py<PyAgentContext>, _inputs: Py<PyDict>) -> PyResult<Py<PyAny>> {
        Python::with_gil(|py| Ok(py.None()))
    }
}

/// Wrapper to adapt Python Actions to Rust ActionInvoker trait
pub struct PythonActionWrapper {
    pub action: Py<PyAction>,
    pub metadata: ActionMetadata,
}

#[async_trait::async_trait]
impl ActionInvoker for PythonActionWrapper {
    async fn execute(
        &self,
        ctx: &mut AgentContext,
        inputs: Value,
    ) -> runtime::core::error::Result<Value> {
        let value_obj = Python::with_gil(|py| {
            let action = self.action.bind(py);
            let inputs_str = serde_json::to_string(&inputs).unwrap();
            let json = py.import("json")?;
            let py_inputs = json.call_method1("loads", (inputs_str,))?;
            let py_ctx = PyAgentContext {
                mesh_name: ctx.mesh_name.clone(),
            };
            let py_ctx_obj = py_ctx.into_pyobject(py)?;

            let result = action.call_method1("execute", (py_ctx_obj, py_inputs))?;

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
                let final_result = coro_result?;

                Ok(final_result.unbind())
            } else {
                Ok(result.unbind())
            }
        })
        .map_err(|e: PyErr| runtime::core::error::Error::ActionExecutionError(e.to_string()))?;

        // Convert value_obj to Value
        Python::with_gil(|py| {
            let val = value_obj.bind(py);
            if let Ok(result_str) = val.extract::<String>() {
                if let Ok(v) = serde_json::from_str::<Value>(&result_str) {
                    Ok(v)
                } else {
                    Ok(Value::String(result_str))
                }
            } else {
                let result_str = val.to_string();
                Ok(Value::String(result_str))
            }
        })
        .map_err(|e: PyErr| runtime::core::error::Error::ActionExecutionError(e.to_string()))
    }

    fn metadata(&self) -> &ActionMetadata {
        &self.metadata
    }
}

/// Python wrapper for ToolInvoker
#[pyclass]
pub struct PyToolInvoker {
    pub inner: Arc<std::sync::Mutex<ToolInvoker>>,
}

#[pymethods]
impl PyToolInvoker {
    #[new]
    fn new() -> Self {
        PyToolInvoker {
            inner: Arc::new(std::sync::Mutex::new(ToolInvoker::new())),
        }
    }

    fn register(&self, action: Py<PyAction>) -> PyResult<()> {
        let (metadata, action_wrapper) = Python::with_gil(|py| {
            let bound_action = action.bind(py);
            let metadata_str: String = bound_action.call_method0("metadata")?.extract()?;
            let metadata: ActionMetadata = serde_json::from_str(&metadata_str)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;

            let wrapper = PythonActionWrapper {
                action: action.clone_ref(py),
                metadata: metadata.clone(),
            };
            Ok::<(ActionMetadata, PythonActionWrapper), PyErr>((metadata, wrapper))
        })?;

        let mut invoker = self.inner.lock().unwrap();
        invoker.register(Box::new(action_wrapper));
        Ok(())
    }

    fn invoke(&self, name: String, inputs: String) -> PyResult<String> {
        let invoker = self.inner.clone();
        let inputs_json: Value = serde_json::from_str(&inputs)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;

        // We need a dummy context for now as we don't have one exposed to Python yet in this call
        // In a real app, this would come from the agent
        let mut ctx = AgentContext::new("system".to_string());

        let result = RUNTIME.block_on(async move {
            let invoker = invoker.lock().unwrap();
            invoker.invoke(&name, &mut ctx, inputs_json).await
        });

        match result {
            Ok(val) => serde_json::to_string(&val)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string())),
            Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                e.to_string(),
            )),
        }
    }
}
