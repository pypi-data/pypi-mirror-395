use pyo3::prelude::*;
use pyo3_async_runtimes::tokio::future_into_py;
use runtime::core::action::ActionMetadata;
use runtime::core::agent::Agent;  // Add this import to use trait methods
use runtime::llm::LLMConfig;
use serde_json::Value;
use std::sync::Arc;
use crate::runtime::RUNTIME;
use crate::action::{PyAction, PythonActionWrapper};
use crate::memory::{PyInMemoryBackend, PythonMemoryWrapper};
use crate::react::{PyReActConfig, PyReActResult};

/// Python wrapper for LLMConfig
#[pyclass(subclass)]
#[derive(Clone)]
pub struct PyLlmConfig {
    pub inner: LLMConfig,
}

#[pymethods]
impl PyLlmConfig {
    #[staticmethod]
    fn builder() -> Self {
        PyLlmConfig {
            inner: LLMConfig::default(),
        }
    }

    fn provider(mut slf: PyRefMut<'_, Self>, provider: String) -> PyResult<PyRefMut<'_, Self>> {
        // In the Rust config, model is "provider::model".
        // We'll store provider temporarily or just prepend it if model is set?
        // Actually, let's just assume model() will be called with the model name,
        // and we combine them. Or we can store them separately in a builder state if we were building from scratch.
        // But here we are wrapping LLMConfig.
        // Let's assume the user calls provider() then model().
        // If model is already set, we might need to handle it.
        // For simplicity, let's just store it in the model string if it's empty, or prepend it.
        // But a cleaner way is to just let the user pass "provider::model" to model().
        // However, the Python example uses .provider("ollama").model("llama3.2:latest").

        // Let's try to handle this by checking if model already has "::".
        let current_model = slf.inner.model.clone();
        if current_model.contains("::") {
            let parts: Vec<&str> = current_model.split("::").collect();
            slf.inner.model = format!("{}::{}", provider, parts[1]);
        } else {
            slf.inner.model = format!("{}::{}", provider, current_model);
        }
        Ok(slf)
    }

    fn model(mut slf: PyRefMut<'_, Self>, model: String) -> PyResult<PyRefMut<'_, Self>> {
        let current_model = slf.inner.model.clone();
        if current_model.contains("::") {
            let parts: Vec<&str> = current_model.split("::").collect();
            slf.inner.model = format!("{}::{}", parts[0], model);
        } else {
            // If provider was set (e.g. "ollama::"), append model.
            // If not, just set model.
            if current_model.ends_with("::") {
                slf.inner.model = format!("{}{}", current_model, model);
            } else {
                slf.inner.model = model;
            }
        }
        Ok(slf)
    }

    fn base_url(mut slf: PyRefMut<'_, Self>, base_url: String) -> PyResult<PyRefMut<'_, Self>> {
        slf.inner.base_url = Some(base_url);
        Ok(slf)
    }

    fn temperature(mut slf: PyRefMut<'_, Self>, temperature: f32) -> PyResult<PyRefMut<'_, Self>> {
        slf.inner.temperature = Some(temperature);
        Ok(slf)
    }

    fn max_tokens(mut slf: PyRefMut<'_, Self>, max_tokens: u32) -> PyResult<PyRefMut<'_, Self>> {
        slf.inner.max_tokens = Some(max_tokens);
        Ok(slf)
    }

    fn build(slf: PyRefMut<'_, Self>) -> PyResult<PyRefMut<'_, Self>> {
        Ok(slf)
    }
}

/// Python wrapper for LlmAgent with builder pattern
#[pyclass]
pub struct PyLlmAgent {
    pub inner: Option<Arc<tokio::sync::Mutex<runtime::llm::LlmAgent>>>,
    // Builder state (used before build() is called)
    name: String,
    model: String,
    api_key: Option<String>,
    system_prompt: Option<String>,
    temperature: Option<f32>,
    max_tokens: Option<u32>,
    config: Option<LLMConfig>,
    memory: Option<Py<PyAny>>,
    actions: Vec<Py<PyAction>>,
}

#[pymethods]
impl PyLlmAgent {
    #[new]
    fn new(name: String, model: String) -> Self {
        PyLlmAgent {
            inner: None,
            name,
            model,
            api_key: None,
            system_prompt: None,
            temperature: None,
            max_tokens: None,
            config: None,
            memory: None,
            actions: Vec::new(),
        }
    }

    #[staticmethod]
    fn with_config(name: String, config: PyLlmConfig) -> Self {
        PyLlmAgent {
            inner: None,
            name,
            model: config.inner.model.clone(),
            api_key: None,
            system_prompt: None,
            temperature: None,
            max_tokens: None,

            config: Some(config.inner),
            memory: None,
            actions: Vec::new(),
        }
    }

    fn with_api_key(mut slf: PyRefMut<'_, Self>, api_key: String) -> PyResult<PyRefMut<'_, Self>> {
        slf.api_key = Some(api_key);
        Ok(slf)
    }

    fn with_system_prompt(
        mut slf: PyRefMut<'_, Self>,
        prompt: String,
    ) -> PyResult<PyRefMut<'_, Self>> {
        slf.system_prompt = Some(prompt);
        Ok(slf)
    }

    fn with_temperature(
        mut slf: PyRefMut<'_, Self>,
        temperature: f32,
    ) -> PyResult<PyRefMut<'_, Self>> {
        slf.temperature = Some(temperature);
        Ok(slf)
    }

    fn with_max_tokens(
        mut slf: PyRefMut<'_, Self>,
        max_tokens: u32,
    ) -> PyResult<PyRefMut<'_, Self>> {
        slf.max_tokens = Some(max_tokens);
        Ok(slf)
    }

    fn with_memory(mut slf: PyRefMut<'_, Self>, memory: Py<PyAny>) -> PyResult<PyRefMut<'_, Self>> {
        slf.memory = Some(memory);
        Ok(slf)
    }

    fn add_action(mut slf: PyRefMut<'_, Self>, action: Py<PyAction>) -> PyResult<PyRefMut<'_, Self>> {
        // If agent is already built, register directly
        if let Some(ref inner) = slf.inner {
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

            let agent_arc = inner.clone();
            RUNTIME.block_on(async move {
                let mut agent = agent_arc.lock().await;
                if let Some(invoker) = agent.tool_invoker_mut() {
                    invoker.register(Box::new(action_wrapper));
                }
            });
        } else {
            // Otherwise store for later
            slf.actions.push(action);
        }
        Ok(slf)
    }

    fn add_tool(slf: PyRefMut<'_, Self>, action: Py<PyAction>) -> PyResult<PyRefMut<'_, Self>> {
        Self::add_action(slf, action)
    }

    fn build(mut slf: PyRefMut<'_, Self>) -> PyResult<PyRefMut<'_, Self>> {
        // Helper function to convert Python memory to Rust Memory
        fn convert_python_memory(py_memory: &Py<PyAny>) -> PyResult<Arc<dyn runtime::core::memory::Memory>> {
            Python::with_gil(|py| {
                let bound = py_memory.bind(py);

                // Try to extract as PyInMemoryBackend first
                if let Ok(backend) = bound.extract::<PyInMemoryBackend>() {
                    let rust_memory: Arc<dyn runtime::core::memory::Memory> = backend.inner;
                    return Ok(rust_memory);
                }

                // Otherwise, wrap it as a custom Python Memory implementation
                let wrapper = PythonMemoryWrapper {
                    memory: py_memory.clone_ref(py),
                };
                Ok(Arc::new(wrapper) as Arc<dyn runtime::core::memory::Memory>)
            })
        }
        
        // Build the Rust LlmAgent using the builder pattern
        let mut builder = runtime::llm::LlmAgent::builder(&slf.name, &slf.model);

        // If config is present, use it as base (though LlmAgent::builder doesn't take config directly,
        // we might need to use new_with_config if we want to use the full config)
        if let Some(ref config) = slf.config {
            // If we have a full config, we should use LlmAgent::new_with_config
            // But we need to handle the system prompt which might be separate
            let system_prompt = slf
                .system_prompt
                .clone()
                .unwrap_or_else(|| "You are a helpful AI assistant.".to_string());


            // If memory is set, we might need to manually inject it or warn that it's not supported with full config yet
            // unless we update new_with_config to take memory. 
            // I updated new_with_config in Rust to take memory.
            // So I should update the call above.
            
            // Re-do the call with memory
            let memory = if let Some(ref py_mem) = slf.memory {
                Some(convert_python_memory(py_mem)?)
            } else {
                None
            };
            
            let agent =
                runtime::llm::LlmAgent::new_with_config(&slf.name, config.clone(), system_prompt, memory)
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

            // Register actions
            let mut agent_guard = agent;
            if let Some(invoker) = agent_guard.tool_invoker_mut() {
                for action in &slf.actions {
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
                    invoker.register(Box::new(action_wrapper));
                }
            }
            
            slf.inner = Some(Arc::new(tokio::sync::Mutex::new(agent_guard)));
            return Ok(slf);
        }

        let mut builder = runtime::llm::LlmAgent::builder(&slf.name, &slf.model);

        if let Some(ref api_key) = slf.api_key {
            builder = builder.with_api_key(api_key);
        }

        if let Some(ref prompt) = slf.system_prompt {
            builder = builder.with_system_prompt(prompt);
        }

        if let Some(temp) = slf.temperature {
            builder = builder.with_temperature(temp);
        }

        if let Some(tokens) = slf.max_tokens {
            builder = builder.with_max_tokens(tokens);
        }

        if let Some(ref py_mem) = slf.memory {
            let memory = convert_python_memory(py_mem)?;
            builder = builder.with_memory(memory);
        }

        let mut agent = builder
            .build()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        // Register actions
        if let Some(invoker) = agent.tool_invoker_mut() {
            for action in &slf.actions {
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
                invoker.register(Box::new(action_wrapper));
            }
        }

        slf.inner = Some(Arc::new(tokio::sync::Mutex::new(agent)));
        Ok(slf)
    }

    fn send_message(&self, message: String) -> PyResult<String> {
        let agent = self.inner.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Agent not built. Call build() first.",
            )
        })?;

        let agent_clone = agent.clone();

        RUNTIME.block_on(async move {
            let mut agent_guard = agent_clone.lock().await;
            let mut ctx = runtime::core::agent::AgentContext::new("python".to_string());

            // Use the new send_message_and_get_response method
            let response = agent_guard
                .send_message_and_get_response(message, &mut ctx)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

            Ok(response)
        })
    }

    fn send_message_async<'py>(
        &self,
        py: Python<'py>,
        message: String,
    ) -> PyResult<Bound<'py, PyAny>> {
        let agent = self.inner.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Agent not built. Call build() first.",
            )
        })?;

        let agent_clone = agent.clone();

        future_into_py(py, async move {
            let mut agent_guard = agent_clone.lock().await;
            let mut ctx = runtime::core::agent::AgentContext::new("python".to_string());

            let response = agent_guard
                .send_message_and_get_response(message, &mut ctx)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

            Ok(response)
        })
    }

    fn register_action(&self, action: Py<PyAction>) -> PyResult<()> {
        let agent = self.inner.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Agent not built. Call build() first.",
            )
        })?;

        let (metadata, action_wrapper) = Python::with_gil(|py| {
            let bound_action = action.bind(py);
            let metadata_str: String = bound_action.call_method0("metadata")?.extract()?;
            let metadata: runtime::core::action::ActionMetadata =
                serde_json::from_str(&metadata_str)
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;

            let wrapper = PythonActionWrapper {
                action: action.clone_ref(py),
                metadata: metadata.clone(),
            };
            Ok::<(runtime::core::action::ActionMetadata, PythonActionWrapper), PyErr>((
                metadata, wrapper,
            ))
        })?;

        let mut agent_guard = agent.blocking_lock();
        if let Some(tool_invoker) = agent_guard.tool_invoker_mut() {
            tool_invoker.register(Box::new(action_wrapper));
        }

        Ok(())
    }
   
    fn with_react(&self, config: PyReActConfig) -> PyResult<()> {
        let agent = self.inner.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Agent not built. Call build() first.",
            )
        })?;
       
        let mut agent_guard = agent.blocking_lock();
        agent_guard.with_react(config.inner);
       
        Ok(())
    }
   
    fn send_message_react(&self, message: String) -> PyResult<PyReActResult> {
        let agent = self.inner.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Agent not built. Call build() first.",
            )
        })?;
       
        let agent_clone = agent.clone();
       
        RUNTIME.block_on(async move {
            let mut agent_guard = agent_clone.lock().await;
            let mut ctx = runtime::core::agent::AgentContext::new("python".to_string());
           
            let result = agent_guard
                .send_message_react(message, &mut ctx)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
           
            Ok(PyReActResult { inner: result })
        })
    }
}
