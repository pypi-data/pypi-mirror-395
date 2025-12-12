// Python bindings for the Ceylon AI framework
// This module coordinates all the Python bindings across different components

use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::wrap_pyfunction;

// Module declarations
mod action;
mod agent;
mod llm;
mod logging;
mod memory;
mod mesh;
mod metrics;
mod react;
mod registry;
mod runtime;

// Re-exports for easy access
pub use action::{PyAction, PyToolInvoker};
pub use agent::{PyAgent, PyAgentContext};
pub use llm::{PyLlmAgent, PyLlmConfig};
pub use logging::{init_logging_py, PyLoggingConfig, PyLoggingHandle};
pub use memory::{PyInMemoryBackend, PyMemoryEntry, PyMemoryQuery, PyRedisBackend};
pub use mesh::{PyDistributedMesh, PyLocalMesh};
pub use metrics::get_metrics;
pub use react::{PyReActConfig, PyReActResult, PyReActStep};
pub use registry::{PyAgentMetadata, PyInMemoryRegistry};

/// Ceylon AI Python module
#[pymodule]
fn ceylonai_next(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Mesh components
    m.add_class::<PyLocalMesh>()?;
    m.add_class::<PyDistributedMesh>()?;

    // Agent components
    m.add_class::<PyAgent>()?;
    m.add_class::<PyAgentContext>()?;

    // Action/Tool components
    m.add_class::<PyAction>()?;
    m.add_class::<PyToolInvoker>()?;

    // LLM components
    m.add_class::<PyLlmAgent>()?;
    m.add_class::<PyLlmConfig>()?;

    // Memory components
    m.add_class::<PyMemoryEntry>()?;
    m.add_class::<PyMemoryQuery>()?;
    m.add_class::<PyInMemoryBackend>()?;
    m.add_class::<PyRedisBackend>()?;

    // ReAct framework components
    m.add_class::<PyReActConfig>()?;
    m.add_class::<PyReActStep>()?;
    m.add_class::<PyReActResult>()?;

    // Registry components
    m.add_class::<PyAgentMetadata>()?;
    m.add_class::<PyInMemoryRegistry>()?;

    // Logging components
    m.add_class::<PyLoggingConfig>()?;
    m.add_class::<PyLoggingHandle>()?;
    m.add_function(wrap_pyfunction!(init_logging_py, m)?)?;

    // Metrics
    m.add_function(wrap_pyfunction!(get_metrics, m)?)?;

    Ok(())
}
