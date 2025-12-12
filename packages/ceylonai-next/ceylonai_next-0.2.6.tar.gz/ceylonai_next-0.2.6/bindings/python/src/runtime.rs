use tokio::runtime::Runtime;

// Create a static Tokio runtime for async execution
lazy_static::lazy_static! {
    pub static ref RUNTIME: Runtime = Runtime::new().unwrap();
}
