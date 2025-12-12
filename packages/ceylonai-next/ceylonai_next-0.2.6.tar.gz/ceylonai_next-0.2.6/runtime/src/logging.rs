use std::fmt::Debug;
use std::path::PathBuf;
use tracing::info;
use tracing_subscriber::{fmt, prelude::*, EnvFilter};
use uuid::Uuid;

/// Configuration for the logging system
#[derive(Debug, Clone)]
pub struct LoggingConfig {
    pub log_level: String,
    pub log_file_path: Option<PathBuf>,
    pub json_output: bool,
}

impl Default for LoggingConfig {
    fn default() -> Self {
        Self {
            log_level: "info".to_string(),
            log_file_path: None,
            json_output: false,
        }
    }
}

/// Guards to keep file appenders alive
pub struct LoggingGuards {
    pub _file_guard: Option<tracing_appender::non_blocking::WorkerGuard>,
}

/// Initialize the logging system
pub fn init_logging(config: &LoggingConfig) -> LoggingGuards {
    let env_filter =
        EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new(&config.log_level));

    let registry = tracing_subscriber::registry().with(env_filter);

    let mut file_guard = None;
    let file_writer = if let Some(path) = &config.log_file_path {
        let file_appender = tracing_appender::rolling::daily(
            path.parent().unwrap_or(&PathBuf::from(".")),
            path.file_name().unwrap_or("ceylon.log".as_ref()),
        );
        let (non_blocking, guard) = tracing_appender::non_blocking(file_appender);
        file_guard = Some(guard);
        Some(non_blocking)
    } else {
        None
    };

    let fmt_layer = fmt::layer()
        .with_target(true)
        .with_thread_ids(true)
        .with_level(true);

    if config.json_output {
        let stdout_layer = fmt_layer.json();
        if let Some(writer) = file_writer {
            let file_layer = fmt::layer().with_ansi(false).with_writer(writer).json();
            if let Err(e) = registry.with(stdout_layer).with(file_layer).try_init() {
                eprintln!("Global logging already initialized: {}", e);
            }
        } else {
            if let Err(e) = registry.with(stdout_layer).try_init() {
                eprintln!("Global logging already initialized: {}", e);
            }
        }
    } else {
        let stdout_layer = fmt_layer.compact();
        if let Some(writer) = file_writer {
            let file_layer = fmt::layer().with_ansi(false).with_writer(writer).json();
            if let Err(e) = registry.with(stdout_layer).with(file_layer).try_init() {
                eprintln!("Global logging already initialized: {}", e);
            }
        } else {
            if let Err(e) = registry.with(stdout_layer).try_init() {
                eprintln!("Global logging already initialized: {}", e);
            }
        }
    }

    info!("Logging initialized");

    LoggingGuards {
        _file_guard: file_guard,
    }
}

/// Correlation ID for tracking requests across boundaries
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct CorrelationId(String);

impl CorrelationId {
    pub fn new() -> Self {
        Self(Uuid::new_v4().to_string())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl Default for CorrelationId {
    fn default() -> Self {
        Self::new()
    }
}

impl std::fmt::Display for CorrelationId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}
