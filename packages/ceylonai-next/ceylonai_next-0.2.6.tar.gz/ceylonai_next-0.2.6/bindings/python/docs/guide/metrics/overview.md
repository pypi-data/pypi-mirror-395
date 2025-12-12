# Metrics & Monitoring

Ceylon provides built-in metrics collection to help you monitor the performance, costs, and health of your agent systems.

## Overview

Metrics are automatically collected throughout your application's lifecycle and can be accessed at any time using the `get_metrics()` function. All metrics are thread-safe and collected using efficient atomic operations with minimal performance impact.

## Getting Metrics

```python
import ceylonai_next as ceylon

# Run your agent system
# ... your code ...

# Get current metrics snapshot
metrics = ceylon.get_metrics()
```

## Available Metrics

### Message Metrics

Track agent communication and performance:

- **`message_throughput`** (int): Total number of messages processed across all agents
- **`avg_message_latency_us`** (float): Average time taken to deliver a message (microseconds)
- **`avg_agent_execution_time_us`** (float): Average time agents spend processing messages (microseconds)

### LLM Metrics

Monitor LLM usage and costs:

- **`total_llm_tokens`** (int): Total tokens consumed across all LLM calls
- **`avg_llm_latency_us`** (float): Average LLM API response time (microseconds)
- **`total_llm_cost_us`** (int): Total cost in micro-dollars (μ$)
  - Note: $1.00 = 1,000,000 μ$

### Memory Metrics

Track memory system efficiency:

- **`memory_hits`** (int): Number of successful memory cache hits
- **`memory_misses`** (int): Number of cache misses
- **`memory_writes`** (int): Number of memory write operations

### Error Tracking

Monitor system health:

- **`errors`** (dict): Dictionary mapping error types to occurrence counts

## Common Use Cases

### Performance Monitoring

```python
metrics = ceylon.get_metrics()

# Convert to milliseconds for readability
latency_ms = metrics['avg_message_latency_us'] / 1000
exec_time_ms = metrics['avg_agent_execution_time_us'] / 1000

print(f"📊 Performance Metrics:")
print(f"  Throughput: {metrics['message_throughput']} messages")
print(f"  Avg Latency: {latency_ms:.2f} ms")
print(f"  Avg Execution Time: {exec_time_ms:.2f} ms")
```

### Cost Tracking

```python
metrics = ceylon.get_metrics()

# Convert micro-dollars to dollars
total_cost = metrics['total_llm_cost_us'] / 1_000_000
tokens_used = metrics['total_llm_tokens']

print(f"💰 LLM Usage:")
print(f"  Total Tokens: {tokens_used:,}")
print(f"  Total Cost: ${total_cost:.4f}")

if tokens_used > 0:
    cost_per_1k_tokens = (total_cost / tokens_used) * 1000
    print(f"  Cost per 1K tokens: ${cost_per_1k_tokens:.4f}")
```

### Memory Optimization

```python
metrics = ceylon.get_metrics()

hits = metrics['memory_hits']
misses = metrics['memory_misses']
total_ops = hits + misses

if total_ops > 0:
    hit_rate = (hits / total_ops) * 100

    print(f"🧠 Memory Performance:")
    print(f"  Cache Hits: {hits}")
    print(f"  Cache Misses: {misses}")
    print(f"  Hit Rate: {hit_rate:.1f}%")

    if hit_rate < 80:
        print("  ⚠️  Consider increasing cache size")
    else:
        print("  ✅ Cache performing well")
```

### Error Rate Monitoring

```python
metrics = ceylon.get_metrics()

if metrics['errors']:
    total_errors = sum(metrics['errors'].values())
    total_messages = metrics['message_throughput']

    if total_messages > 0:
        error_rate = (total_errors / total_messages) * 100

        print(f"⚠️  Error Rate: {error_rate:.2f}%")
        print(f"Error Breakdown:")
        for error_type, count in metrics['errors'].items():
            print(f"  - {error_type}: {count}")
else:
    print("✅ No errors recorded")
```

## Continuous Monitoring

For long-running applications, you can set up periodic monitoring:

```python
import asyncio
import ceylonai_next as ceylon

async def monitor_metrics(interval_seconds=10):
    """Monitor metrics every N seconds"""
    while True:
        await asyncio.sleep(interval_seconds)

        metrics = ceylon.get_metrics()

        print(f"\n📊 Metrics Update (every {interval_seconds}s):")
        print(f"  Messages: {metrics['message_throughput']}")
        print(f"  Latency: {metrics['avg_message_latency_us']/1000:.2f} ms")
        print(f"  LLM Tokens: {metrics['total_llm_tokens']}")
        print(f"  LLM Cost: ${metrics['total_llm_cost_us']/1_000_000:.4f}")

# Run monitoring in the background
asyncio.create_task(monitor_metrics(10))
```

## Best Practices

### 1. Regular Snapshots

Take periodic snapshots to track trends over time:

```python
import time

metrics_history = []

for i in range(10):
    metrics = ceylon.get_metrics()
    metrics_history.append({
        'timestamp': time.time(),
        'throughput': metrics['message_throughput'],
        'latency': metrics['avg_message_latency_us']
    })
    time.sleep(60)  # Every minute
```

### 2. Set Alerts

Define thresholds and alert when exceeded:

```python
def check_metrics_health(metrics):
    """Check if metrics are within acceptable ranges"""
    warnings = []

    # Check latency
    latency_ms = metrics['avg_message_latency_us'] / 1000
    if latency_ms > 100:
        warnings.append(f"High latency: {latency_ms:.2f}ms")

    # Check error rate
    if metrics['errors']:
        total_errors = sum(metrics['errors'].values())
        if total_errors > 10:
            warnings.append(f"High error count: {total_errors}")

    # Check memory efficiency
    total_mem_ops = metrics['memory_hits'] + metrics['memory_misses']
    if total_mem_ops > 0:
        hit_rate = metrics['memory_hits'] / total_mem_ops
        if hit_rate < 0.7:
            warnings.append(f"Low cache hit rate: {hit_rate*100:.1f}%")

    return warnings

# Usage
metrics = ceylon.get_metrics()
warnings = check_metrics_health(metrics)

if warnings:
    print("⚠️  Warnings:")
    for warning in warnings:
        print(f"  - {warning}")
```

### 3. Export for Analysis

Export metrics to external monitoring systems:

```python
import json

def export_metrics_json(metrics, filename='metrics.json'):
    """Export metrics to JSON for external analysis"""
    with open(filename, 'w') as f:
        json.dump(metrics, f, indent=2)

# Export current state
metrics = ceylon.get_metrics()
export_metrics_json(metrics)
```

## Technical Details

- **Thread Safety**: All metrics use atomic operations and are safe to access from multiple threads
- **Scope**: Metrics are global and persist for the lifetime of the process
- **Accumulation**: Metrics are cumulative and never reset automatically
- **Performance**: Metrics collection has minimal overhead (~nanoseconds per operation)

## Next Steps

- See [Metrics Examples](../../examples/metrics/quickstart.md) for complete working examples
- Check [examples/README_METRICS.md](../../examples/README_METRICS.md) for detailed examples
- View [API Reference](../../api/reference/index.md) for complete API documentation
