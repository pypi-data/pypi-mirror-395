use dashmap::DashMap;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;

pub struct Metrics {
    // Message metrics
    pub message_count: AtomicU64,
    pub message_latency_sum_us: AtomicU64,
    pub message_latency_count: AtomicU64,

    // Agent execution metrics
    pub agent_execution_time_sum_us: AtomicU64,
    pub agent_execution_time_count: AtomicU64,

    // LLM metrics
    pub llm_tokens_total: AtomicU64,
    pub llm_latency_sum_us: AtomicU64,
    pub llm_latency_count: AtomicU64,
    pub llm_cost_total_us: AtomicU64, // Micro-cents or similar unit? Let's say micro-dollars for now, or just raw value

    // Memory metrics
    pub memory_hits: AtomicU64,
    pub memory_misses: AtomicU64,
    pub memory_writes: AtomicU64,

    // Errors
    pub errors: DashMap<String, AtomicU64>,
}

impl Metrics {
    pub fn new() -> Self {
        Self {
            message_count: AtomicU64::new(0),
            message_latency_sum_us: AtomicU64::new(0),
            message_latency_count: AtomicU64::new(0),
            agent_execution_time_sum_us: AtomicU64::new(0),
            agent_execution_time_count: AtomicU64::new(0),
            llm_tokens_total: AtomicU64::new(0),
            llm_latency_sum_us: AtomicU64::new(0),
            llm_latency_count: AtomicU64::new(0),
            llm_cost_total_us: AtomicU64::new(0),
            memory_hits: AtomicU64::new(0),
            memory_misses: AtomicU64::new(0),
            memory_writes: AtomicU64::new(0),
            errors: DashMap::new(),
        }
    }

    pub fn record_message(&self, latency_us: u64) {
        self.message_count.fetch_add(1, Ordering::Relaxed);
        self.message_latency_sum_us
            .fetch_add(latency_us, Ordering::Relaxed);
        self.message_latency_count.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_agent_execution(&self, duration_us: u64) {
        self.agent_execution_time_sum_us
            .fetch_add(duration_us, Ordering::Relaxed);
        self.agent_execution_time_count
            .fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_llm_call(&self, duration_us: u64, tokens: u64, cost_us: u64) {
        self.llm_latency_sum_us
            .fetch_add(duration_us, Ordering::Relaxed);
        self.llm_latency_count.fetch_add(1, Ordering::Relaxed);
        self.llm_tokens_total.fetch_add(tokens, Ordering::Relaxed);
        self.llm_cost_total_us.fetch_add(cost_us, Ordering::Relaxed);
    }

    pub fn record_memory_hit(&self) {
        self.memory_hits.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_memory_miss(&self) {
        self.memory_misses.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_memory_write(&self) {
        self.memory_writes.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_error(&self, error_type: &str) {
        self.errors
            .entry(error_type.to_string())
            .and_modify(|c| {
                c.fetch_add(1, Ordering::Relaxed);
            })
            .or_insert(AtomicU64::new(1));
    }

    pub fn snapshot(&self) -> MetricsSnapshot {
        MetricsSnapshot {
            message_throughput: self.message_count.load(Ordering::Relaxed),
            avg_message_latency_us: self.avg(
                self.message_latency_sum_us.load(Ordering::Relaxed),
                self.message_latency_count.load(Ordering::Relaxed),
            ),
            avg_agent_execution_time_us: self.avg(
                self.agent_execution_time_sum_us.load(Ordering::Relaxed),
                self.agent_execution_time_count.load(Ordering::Relaxed),
            ),
            total_llm_tokens: self.llm_tokens_total.load(Ordering::Relaxed),
            avg_llm_latency_us: self.avg(
                self.llm_latency_sum_us.load(Ordering::Relaxed),
                self.llm_latency_count.load(Ordering::Relaxed),
            ),
            total_llm_cost_us: self.llm_cost_total_us.load(Ordering::Relaxed),
            memory_hits: self.memory_hits.load(Ordering::Relaxed),
            memory_misses: self.memory_misses.load(Ordering::Relaxed),
            memory_writes: self.memory_writes.load(Ordering::Relaxed),
            errors: self
                .errors
                .iter()
                .map(|r| (r.key().clone(), r.value().load(Ordering::Relaxed)))
                .collect(),
        }
    }

    fn avg(&self, sum: u64, count: u64) -> f64 {
        if count == 0 {
            0.0
        } else {
            sum as f64 / count as f64
        }
    }
}

#[derive(Debug, Clone, serde::Serialize)]
pub struct MetricsSnapshot {
    pub message_throughput: u64,
    pub avg_message_latency_us: f64,
    pub avg_agent_execution_time_us: f64,
    pub total_llm_tokens: u64,
    pub avg_llm_latency_us: f64,
    pub total_llm_cost_us: u64,
    pub memory_hits: u64,
    pub memory_misses: u64,
    pub memory_writes: u64,
    pub errors: std::collections::HashMap<String, u64>,
}

// Global metrics instance
use std::sync::OnceLock;

pub static GLOBAL_METRICS: OnceLock<Arc<Metrics>> = OnceLock::new();

pub fn metrics() -> &'static Arc<Metrics> {
    GLOBAL_METRICS.get_or_init(|| Arc::new(Metrics::new()))
}
