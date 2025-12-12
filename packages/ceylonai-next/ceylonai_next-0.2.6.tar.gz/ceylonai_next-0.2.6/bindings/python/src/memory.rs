use async_trait::async_trait;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use runtime::core::memory::{Memory, MemoryEntry, MemoryQuery};
use runtime::memory::{InMemoryBackend, RedisBackend};
use serde_json::Value;
use std::sync::Arc;
use crate::runtime::RUNTIME;

/// Python wrapper for MemoryEntry
#[pyclass(subclass)]
#[derive(Clone)]
pub struct PyMemoryEntry {
    pub inner: MemoryEntry,
}

#[pymethods]
impl PyMemoryEntry {
    #[new]
    fn new(content: String) -> Self {
        PyMemoryEntry {
            inner: MemoryEntry::new(content),
        }
    }

    #[getter]
    fn id(&self) -> String {
        self.inner.id.clone()
    }

    #[getter]
    fn content(&self) -> String {
        self.inner.content.clone()
    }

    #[getter]
    fn metadata(&self, py: Python) -> PyResult<Py<PyDict>> {
        let dict = PyDict::new(py);
        for (key, value) in &self.inner.metadata {
            let json_str = serde_json::to_string(&value)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
            let json = py.import("json")?;
            let py_value = json.call_method1("loads", (json_str,))?;
            dict.set_item(key, py_value)?;
        }
        Ok(dict.unbind())
    }

    #[getter]
    fn created_at(&self) -> String {
        self.inner.created_at.to_rfc3339()
    }

    #[getter]
    fn expires_at(&self) -> Option<String> {
        self.inner.expires_at.map(|dt| dt.to_rfc3339())
    }

    fn with_metadata(
        mut slf: PyRefMut<'_, Self>,
        key: String,
        value: Py<PyAny>,
    ) -> PyResult<PyRefMut<'_, Self>> {
        Python::with_gil(|py| {
            let val = value.bind(py);
            let json = py.import("json")?;
            let json_str: String = json.call_method1("dumps", (val,))?.extract()?;
            let json_value: Value = serde_json::from_str(&json_str)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;

            slf.inner = slf.inner.clone().with_metadata(key, json_value);
            Ok(slf)
        })
    }

    fn with_ttl_seconds(mut slf: PyRefMut<'_, Self>, seconds: i64) -> PyResult<PyRefMut<'_, Self>> {
        slf.inner = slf.inner.clone().with_ttl_seconds(seconds);
        Ok(slf)
    }

    fn is_expired(&self) -> bool {
        self.inner.is_expired()
    }

    fn __repr__(&self) -> String {
        format!(
            "MemoryEntry(id='{}', content='{}', metadata={:?})",
            self.inner.id, self.inner.content, self.inner.metadata
        )
    }
}

/// Python wrapper for MemoryQuery
#[pyclass(subclass)]
#[derive(Clone)]
pub struct PyMemoryQuery {
    pub inner: MemoryQuery,
}

#[pymethods]
impl PyMemoryQuery {
    #[new]
    fn new() -> Self {
        PyMemoryQuery {
            inner: MemoryQuery::new(),
        }
    }

    fn with_filter(
        mut slf: PyRefMut<'_, Self>,
        key: String,
        value: Py<PyAny>,
    ) -> PyResult<PyRefMut<'_, Self>> {
        Python::with_gil(|py| {
            let val = value.bind(py);
            let json = py.import("json")?;
            let json_str: String = json.call_method1("dumps", (val,))?.extract()?;
            let json_value: Value = serde_json::from_str(&json_str)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;

            slf.inner = slf.inner.clone().with_filter(key, json_value);
            Ok(slf)
        })
    }

    fn with_limit(mut slf: PyRefMut<'_, Self>, limit: usize) -> PyResult<PyRefMut<'_, Self>> {
        slf.inner = slf.inner.clone().with_limit(limit);
        Ok(slf)
    }

    fn __repr__(&self) -> String {
        format!(
            "MemoryQuery(filters={:?}, limit={:?})",
            self.inner.filters, self.inner.limit
        )
    }
}

/// Wrapper to adapt Python Memory to Rust Memory trait
pub struct PythonMemoryWrapper {
    pub memory: Py<PyAny>,
}

unsafe impl Send for PythonMemoryWrapper {}
unsafe impl Sync for PythonMemoryWrapper {}

#[async_trait]
impl runtime::core::memory::Memory for PythonMemoryWrapper {
    async fn store(&self, entry: runtime::core::memory::MemoryEntry) -> runtime::core::error::Result<String> {
        // Clone the reference within the GIL context before moving to spawn_blocking
        let memory = Python::with_gil(|py| self.memory.clone_ref(py));

        tokio::task::spawn_blocking(move || {
            Python::with_gil(|py| {
                let py_entry = PyMemoryEntry { inner: entry };
                let id = memory.bind(py).call_method1("store", (py_entry,))
                    .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?;
                id.extract::<String>()
                    .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))
            })
        })
        .await
        .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?
    }

    async fn get(&self, id: &str) -> runtime::core::error::Result<Option<runtime::core::memory::MemoryEntry>> {
        let id_owned = id.to_string();
        let memory = Python::with_gil(|py| self.memory.clone_ref(py));

        tokio::task::spawn_blocking(move || {
            Python::with_gil(|py| {
                let obj = memory.bind(py).call_method1("get", (id_owned,))
                    .map_err(|e: PyErr| runtime::core::error::Error::MeshError(e.to_string()))?;

                if obj.is_none() {
                    return Ok(None);
                }

                // Try to extract as PyMemoryEntry
                match obj.extract::<PyMemoryEntry>() {
                    Ok(py_entry) => Ok(Some(py_entry.inner)),
                    Err(e) => Err(runtime::core::error::Error::MeshError(e.to_string()))
                }
            })
        })
        .await
        .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?
    }

    async fn search(&self, query: runtime::core::memory::MemoryQuery) -> runtime::core::error::Result<Vec<runtime::core::memory::MemoryEntry>> {
        let memory = Python::with_gil(|py| self.memory.clone_ref(py));

        tokio::task::spawn_blocking(move || {
            Python::with_gil(|py| {
                let py_query = PyMemoryQuery { inner: query };
                let list = memory.bind(py).call_method1("search", (py_query,))
                    .map_err(|e: PyErr| runtime::core::error::Error::MeshError(e.to_string()))?;

                let entries: Vec<PyMemoryEntry> = list.extract()
                    .map_err(|e: PyErr| runtime::core::error::Error::MeshError(e.to_string()))?;
                Ok(entries.into_iter().map(|e| e.inner).collect())
            })
        })
        .await
        .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?
    }

    async fn delete(&self, id: &str) -> runtime::core::error::Result<bool> {
        let id_owned = id.to_string();
        let memory = Python::with_gil(|py| self.memory.clone_ref(py));

        tokio::task::spawn_blocking(move || {
            Python::with_gil(|py| {
                let deleted = memory.bind(py).call_method1("delete", (id_owned,))
                    .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?;
                deleted.extract::<bool>()
                    .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))
            })
        })
        .await
        .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?
    }

    async fn clear(&self) -> runtime::core::error::Result<()> {
        let memory = Python::with_gil(|py| self.memory.clone_ref(py));

        tokio::task::spawn_blocking(move || {
            Python::with_gil(|py| {
                memory.bind(py).call_method0("clear")
                    .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?;
                Ok(())
            })
        })
        .await
        .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?
    }

    async fn count(&self) -> runtime::core::error::Result<usize> {
        let memory = Python::with_gil(|py| self.memory.clone_ref(py));

        tokio::task::spawn_blocking(move || {
            Python::with_gil(|py| {
                let count = memory.bind(py).call_method0("count")
                    .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?;
                count.extract::<usize>()
                    .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))
            })
        })
        .await
        .map_err(|e| runtime::core::error::Error::MeshError(e.to_string()))?
    }
}


/// Python wrapper for InMemoryBackend
#[pyclass(subclass)]
#[derive(Clone)]
pub struct PyInMemoryBackend {
    pub inner: Arc<InMemoryBackend>,
}

#[pymethods]
impl PyInMemoryBackend {
    #[new]
    fn new() -> Self {
        PyInMemoryBackend {
            inner: Arc::new(InMemoryBackend::new()),
        }
    }

    #[staticmethod]
    fn with_max_entries(max: usize) -> Self {
        PyInMemoryBackend {
            inner: Arc::new(InMemoryBackend::new().with_max_entries(max)),
        }
    }

    #[staticmethod]
    fn with_ttl_seconds(seconds: i64) -> Self {
        PyInMemoryBackend {
            inner: Arc::new(InMemoryBackend::new().with_ttl_seconds(seconds)),
        }
    }

    fn store(&self, entry: PyMemoryEntry) -> PyResult<String> {
        let backend = self.inner.clone();
        let entry_inner = entry.inner.clone();

        RUNTIME.block_on(async move {
            backend
                .store(entry_inner)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn get(&self, id: String) -> PyResult<Option<PyMemoryEntry>> {
        let backend = self.inner.clone();

        RUNTIME.block_on(async move {
            let result = backend
                .get(&id)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

            Ok(result.map(|entry| PyMemoryEntry { inner: entry }))
        })
    }

    fn search(&self, query: PyMemoryQuery) -> PyResult<Vec<PyMemoryEntry>> {
        let backend = self.inner.clone();
        let query_inner = query.inner.clone();

        RUNTIME.block_on(async move {
            let results = backend
                .search(query_inner)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

            Ok(results
                .into_iter()
                .map(|entry| PyMemoryEntry { inner: entry })
                .collect())
        })
    }

    fn delete(&self, id: String) -> PyResult<bool> {
        let backend = self.inner.clone();

        RUNTIME.block_on(async move {
            backend
                .delete(&id)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn clear(&self) -> PyResult<()> {
        let backend = self.inner.clone();

        RUNTIME.block_on(async move {
            backend
                .clear()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn count(&self) -> PyResult<usize> {
        let backend = self.inner.clone();

        RUNTIME.block_on(async move {
            backend
                .count()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn __repr__(&self) -> String {
        "InMemoryBackend()".to_string()
    }
}

// ============================================================================
// Redis Backend Python Bindings
// ============================================================================

#[pyclass(subclass)]
#[derive(Clone)]
pub struct PyRedisBackend {
    pub inner: Arc<RedisBackend>,
}

#[pymethods]
impl PyRedisBackend {
    #[new]
    fn new(redis_url: String) -> PyResult<Self> {
        RUNTIME.block_on(async move {
            let backend = RedisBackend::new(redis_url)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
            Ok(PyRedisBackend {
                inner: Arc::new(backend),
            })
        })
    }

    fn with_prefix(&self, prefix: String) -> Self {
        let backend = (*self.inner).clone().with_prefix(prefix);
        PyRedisBackend {
            inner: Arc::new(backend),
        }
    }

    fn with_ttl_seconds(&self, seconds: i64) -> Self {
        let backend = (*self.inner).clone().with_ttl_seconds(seconds);
        PyRedisBackend {
            inner: Arc::new(backend),
        }
    }

    fn store(&self, entry: PyMemoryEntry) -> PyResult<String> {
        let backend = self.inner.clone();
        let entry_inner = entry.inner.clone();

        RUNTIME.block_on(async move {
            backend
                .store(entry_inner)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn get(&self, id: String) -> PyResult<Option<PyMemoryEntry>> {
        let backend = self.inner.clone();

        RUNTIME.block_on(async move {
            let result = backend
                .get(&id)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

            Ok(result.map(|entry| PyMemoryEntry { inner: entry }))
        })
    }

    fn search(&self, query: PyMemoryQuery) -> PyResult<Vec<PyMemoryEntry>> {
        let backend = self.inner.clone();
        let query_inner = query.inner.clone();

        RUNTIME.block_on(async move {
            let results = backend
                .search(query_inner)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

            Ok(results
                .into_iter()
                .map(|entry| PyMemoryEntry { inner: entry })
                .collect())
        })
    }

    fn delete(&self, id: String) -> PyResult<bool> {
        let backend = self.inner.clone();

        RUNTIME.block_on(async move {
            backend
                .delete(&id)
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn clear(&self) -> PyResult<()> {
        let backend = self.inner.clone();

        RUNTIME.block_on(async move {
            backend
                .clear()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn count(&self) -> PyResult<usize> {
        let backend = self.inner.clone();

        RUNTIME.block_on(async move {
            backend
                .count()
                .await
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
        })
    }

    fn __repr__(&self) -> String {
        "RedisBackend()".to_string()
    }
}
