use pyo3::prelude::*;
use runtime::logging::{init_logging, LoggingConfig, LoggingGuards};
use std::path::PathBuf;

/// Python wrapper for LoggingConfig
#[pyclass(subclass)]
#[derive(Clone)]
pub struct PyLoggingConfig {
    pub inner: LoggingConfig,
}

#[pymethods]
impl PyLoggingConfig {
    #[new]
    fn new(log_level: String, log_file_path: Option<String>, json_output: bool) -> Self {
        PyLoggingConfig {
            inner: LoggingConfig {
                log_level,
                log_file_path: log_file_path.map(PathBuf::from),
                json_output,
            },
        }
    }
}

/// Python wrapper for LoggingGuards to keep file appenders alive
#[pyclass(subclass)]
pub struct PyLoggingHandle {
    _inner: LoggingGuards,
}

/// Initialize logging from Python
#[pyfunction]
pub fn init_logging_py(config: PyLoggingConfig) -> PyLoggingHandle {
    let guards = init_logging(&config.inner);
    PyLoggingHandle { _inner: guards }
}
