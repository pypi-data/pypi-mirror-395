use pyo3::prelude::*;

// ============================================================================
// ReAct Framework Python Bindings
// ============================================================================

/// Python wrapper for ReActConfig
#[pyclass]
#[derive(Clone)]
pub struct PyReActConfig {
    pub inner: runtime::llm::ReActConfig,
}

#[pymethods]
impl PyReActConfig {
    #[new]
    fn new() -> Self {
        PyReActConfig {
            inner: runtime::llm::ReActConfig::default(),
        }
    }

    fn with_max_iterations(
        mut slf: PyRefMut<'_, Self>,
        max_iterations: usize,
    ) -> PyResult<PyRefMut<'_, Self>> {
        slf.inner.max_iterations = max_iterations;
        Ok(slf)
    }

    fn with_thought_prefix(
        mut slf: PyRefMut<'_, Self>,
        prefix: String,
    ) -> PyResult<PyRefMut<'_, Self>> {
        slf.inner.thought_prefix = prefix;
        Ok(slf)
    }

    fn with_action_prefix(
        mut slf: PyRefMut<'_, Self>,
        prefix: String,
    ) -> PyResult<PyRefMut<'_, Self>> {
        slf.inner.action_prefix = prefix;
        Ok(slf)
    }
}

/// Python wrapper for ReActStep
#[pyclass]
#[derive(Clone)]
pub struct PyReActStep {
    pub inner: runtime::llm::ReActStep,
}

#[pymethods]
impl PyReActStep {
    #[getter]
    fn iteration(&self) -> usize {
        self.inner.iteration
    }

    #[getter]
    fn thought(&self) -> String {
        self.inner.thought.clone()
    }

    #[getter]
    fn action(&self) -> Option<String> {
        self.inner.action.clone()
    }

    #[getter]
    fn action_input(&self) -> Option<String> {
        self.inner.action_input.clone()
    }

    #[getter]
    fn observation(&self) -> Option<String> {
        self.inner.observation.clone()
    }

    fn __repr__(&self) -> String {
        format!(
            "ReActStep(iteration={}, thought='{}...')",
            self.inner.iteration,
            &self.inner.thought.chars().take(50).collect::<String>()
        )
    }
}

/// Python wrapper for ReActResult
#[pyclass]
pub struct PyReActResult {
    pub inner: runtime::llm::ReActResult,
}

#[pymethods]
impl PyReActResult {
    #[getter]
    fn answer(&self) -> String {
        self.inner.answer.clone()
    }

    #[getter]
    fn iterations(&self) -> usize {
        self.inner.iterations
    }

    #[getter]
    fn finish_reason(&self) -> String {
        format!("{:?}", self.inner.finish_reason)
    }

    fn get_steps(&self) -> Vec<PyReActStep> {
        self.inner
            .steps
            .iter()
            .map(|s| PyReActStep { inner: s.clone() })
            .collect()
    }

    fn __repr__(&self) -> String {
        format!(
            "ReActResult(answer='...', iterations={})",
            self.inner.iterations
        )
    }
}
