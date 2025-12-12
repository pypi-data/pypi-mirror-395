use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Get metrics snapshot from the runtime
#[pyfunction]
pub fn get_metrics() -> PyResult<Py<PyDict>> {
    let snapshot = runtime::metrics::metrics().snapshot();
    Python::with_gil(|py| {
        let dict = PyDict::new(py);
        dict.set_item("message_throughput", snapshot.message_throughput)?;
        dict.set_item("avg_message_latency_us", snapshot.avg_message_latency_us)?;
        dict.set_item(
            "avg_agent_execution_time_us",
            snapshot.avg_agent_execution_time_us,
        )?;
        dict.set_item("total_llm_tokens", snapshot.total_llm_tokens)?;
        dict.set_item("avg_llm_latency_us", snapshot.avg_llm_latency_us)?;
        dict.set_item("total_llm_cost_us", snapshot.total_llm_cost_us)?;
        dict.set_item("memory_hits", snapshot.memory_hits)?;
        dict.set_item("memory_misses", snapshot.memory_misses)?;
        dict.set_item("memory_writes", snapshot.memory_writes)?;

        let errors = PyDict::new(py);
        for (k, v) in snapshot.errors {
            errors.set_item(k, v)?;
        }
        dict.set_item("errors", errors)?;

        Ok(dict.into())
    })
}
