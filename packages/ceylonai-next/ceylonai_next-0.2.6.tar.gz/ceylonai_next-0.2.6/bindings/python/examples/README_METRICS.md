# Ceylon AI Metrics Examples

This directory contains examples demonstrating the metrics collection features in Ceylon AI.

## Prerequisites

Before running these examples, make sure Ceylon AI is installed:

```bash
# From the bindings/python directory
maturin develop --release

# Or if you want to install it in editable mode
pip install -e .
```

## Available Examples

### 📊 `metrics_quickstart.py`

A minimal example showing the basics of retrieving metrics.

**Run it:**

```bash
python metrics_quickstart.py
```

**What it shows:**

- Creating agents and sending messages
- Retrieving metrics with `get_metrics()`
- Basic metrics display

---

### 📈 `metrics_demo.py`

A comprehensive demo showing all aspects of metrics collection.

**Run it:**

```bash
python metrics_demo.py
```

**What it shows:**

- **Message Metrics**: Throughput, latency, and agent execution time
- **Memory Metrics**: Hits, misses, writes, and hit rate calculation
- **Continuous Monitoring**: Real-time metrics snapshots
- **Error Tracking**: How errors are recorded in metrics

---

### 🔢 `metrics_token_counter.py`

Simple OpenAI token counting example.

**Run it:**

```bash
export OPENAI_API_KEY="your-key"
python metrics_token_counter.py
```

**What it shows:**

- Tracking OpenAI token usage
- Calculating tokens per query
- Estimating API costs

---

### 🤖 `metrics_openai_tokens.py`

Comprehensive OpenAI token tracking with multiple scenarios.

**Run it:**

```bash
export OPENAI_API_KEY="your-key"
python metrics_openai_tokens.py
```

**What it shows:**

- Single query token tracking
- Concurrent queries
- Token budgeting
- Cost tracking across models

---

## Metrics API Reference

### Getting Metrics

```python
import ceylonai_next as ceylon

metrics = ceylon.get_metrics()
```

### Available Metrics

```python
{
    # Message metrics
    "message_throughput": int,           # Total messages processed
    "avg_message_latency_us": float,     # Average message latency (microseconds)
    "avg_agent_execution_time_us": float, # Average agent execution time (microseconds)

    # Memory metrics
    "memory_hits": int,                  # Memory cache hits
    "memory_misses": int,                # Memory cache misses
    "memory_writes": int,                # Memory write operations

    # LLM metrics (when using LLM agents)
    "total_llm_tokens": int,             # Total tokens used
    "avg_llm_latency_us": float,         # Average LLM API latency
    "total_llm_cost_us": int,            # Total cost (micro-dollars)

    # Error tracking
    "errors": {                          # Dictionary of error types and counts
        "error_type_1": count,
        "error_type_2": count,
        ...
    }
}
```

## Use Cases

### 1. Performance Monitoring

```python
import ceylonai_next as ceylon

# Run your workload
# ...

metrics = ceylon.get_metrics()
print(f"Throughput: {metrics['message_throughput']} msg/s")
print(f"Latency: {metrics['avg_message_latency_us']/1000:.2f} ms")
```

### 2. Memory Optimization

```python
metrics = ceylon.get_metrics()
total_ops = metrics['memory_hits'] + metrics['memory_misses']
if total_ops > 0:
    hit_rate = metrics['memory_hits'] / total_ops * 100
    print(f"Cache hit rate: {hit_rate:.1f}%")

    if hit_rate < 80:
        print("⚠️  Consider increasing cache size")
```

### 3. Cost Tracking

```python
metrics = ceylon.get_metrics()
cost_dollars = metrics['total_llm_cost_us'] / 1_000_000
print(f"Total LLM cost: ${cost_dollars:.4f}")
print(f"Tokens used: {metrics['total_llm_tokens']}")
```

### 4. Error Rate Monitoring

```python
metrics = ceylon.get_metrics()
total_messages = metrics['message_throughput']

if metrics['errors']:
    total_errors = sum(metrics['errors'].values())
    error_rate = (total_errors / total_messages) * 100
    print(f"Error rate: {error_rate:.2f}%")

    for error_type, count in metrics['errors'].items():
        print(f"  {error_type}: {count}")
```

## Notes

- **Thread-safe**: Metrics are collected using atomic operations and are safe to access from multiple threads
- **Global**: Metrics are collected globally across all meshes and agents
- **Cumulative**: Metrics accumulate over the lifetime of the process
- **Low overhead**: Metrics collection uses efficient atomic operations with minimal performance impact

## Next Steps

- Check out the [full documentation](../docs/) for more details
- See other examples for LLM agents, memory backends, and distributed meshes
- Explore metric exporters (coming soon: Prometheus, StatsD)
