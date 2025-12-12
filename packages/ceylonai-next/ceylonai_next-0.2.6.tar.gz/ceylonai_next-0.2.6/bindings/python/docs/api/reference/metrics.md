# Metrics API Reference

## `get_metrics()`

Get a snapshot of all collected metrics from the Ceylon runtime.

### Signature

```python
def get_metrics() -> dict
```

### Returns

**Type**: `dict`

A dictionary containing all current metric values:

```python
{
    "message_throughput": int,
    "avg_message_latency_us": float,
    "avg_agent_execution_time_us": float,
    "total_llm_tokens": int,
    "avg_llm_latency_us": float,
    "total_llm_cost_us": int,
    "memory_hits": int,
    "memory_misses": int,
    "memory_writes": int,
    "errors": dict[str, int]
}
```

### Metric Descriptions

#### Message Metrics

- **`message_throughput`** (`int`): Total number of messages processed across all agents since the process started.

- **`avg_message_latency_us`** (`float`): Average time in microseconds from when a message is sent to when it's delivered to the target agent.

- **`avg_agent_execution_time_us`** (`float`): Average time in microseconds that agents spend executing their `on_message()` handlers.

#### LLM Metrics

- **`total_llm_tokens`** (`int`): Cumulative token count across all LLM API calls (input + output tokens).

- **`avg_llm_latency_us`** (`float`): Average response time in microseconds for LLM API calls.

- **`total_llm_cost_us`** (`int`): Total cost in micro-dollars (μ$) for all LLM API calls.
  - **Conversion**: $1.00 = 1,000,000 μ$
  - **Example**: 5000 μ$ = $0.005

#### Memory Metrics

- **`memory_hits`** (`int`): Number of times a memory query found the requested data in cache.

- **`memory_misses`** (`int`): Number of times a memory query did not find the requested data in cache.

- **`memory_writes`** (`int`): Number of memory write/store operations performed.

#### Error Metrics

- **`errors`** (`dict[str, int]`): Dictionary mapping error type names to their occurrence counts.
  - Keys are error type strings (e.g., "ValueError", "TimeoutError")
  - Values are integer counts of how many times each error occurred

### Example Usage

#### Basic Usage

```python
import ceylonai_next as ceylon

# ... run your agents ...

metrics = ceylon.get_metrics()
print(f"Processed {metrics['message_throughput']} messages")
```

#### Formatted Output

```python
import ceylonai_next as ceylon
import json

metrics = ceylon.get_metrics()

# Pretty print all metrics
print(json.dumps(metrics, indent=2))
```

#### Calculating Derived Metrics

```python
import ceylonai_next as ceylon

metrics = ceylon.get_metrics()

# Calculate memory hit rate
total_memory_ops = metrics['memory_hits'] + metrics['memory_misses']
if total_memory_ops > 0:
    hit_rate = (metrics['memory_hits'] / total_memory_ops) * 100
    print(f"Memory hit rate: {hit_rate:.1f}%")

# Convert costs to dollars
cost_dollars = metrics['total_llm_cost_us'] / 1_000_000
print(f"LLM cost: ${cost_dollars:.4f}")

# Calculate error rate
if metrics['message_throughput'] > 0 and metrics['errors']:
    total_errors = sum(metrics['errors'].values())
    error_rate = (total_errors / metrics['message_throughput']) * 100
    print(f"Error rate: {error_rate:.2f}%")
```

#### Monitoring Over Time

```python
import ceylonai_next as ceylon
import asyncio

async def monitor_metrics():
    """Print metrics every 10 seconds"""
    while True:
        await asyncio.sleep(10)

        metrics = ceylon.get_metrics()
        print(f"\n📊 Metrics Update:")
        print(f"  Throughput: {metrics['message_throughput']}")
        print(f"  Latency: {metrics['avg_message_latency_us']/1000:.2f} ms")
        print(f"  Tokens: {metrics['total_llm_tokens']}")

# Start monitoring
asyncio.create_task(monitor_metrics())
```

## Notes

### Thread Safety

All metrics are collected using atomic operations and are safe to access from multiple threads simultaneously. You can call `get_metrics()` from any thread without synchronization.

### Global Scope

Metrics are global across the entire process. They accumulate data from:

- All meshes (local and distributed)
- All agents
- All LLM calls
- All memory operations

### Cumulative Nature

Metrics are cumulative and never reset automatically. They accumulate from process start until process termination.

### Performance Impact

Metrics collection uses efficient atomic operations with minimal performance overhead (typically nanoseconds per metric update).

## See Also

- [Metrics Guide](../../guide/metrics/overview.md) - Comprehensive guide to using metrics
- [Metrics Examples](../../examples/metrics/quickstart.md) - Working examples
- [examples/README_METRICS.md](../../examples/README_METRICS.md) - Detailed metrics documentation
