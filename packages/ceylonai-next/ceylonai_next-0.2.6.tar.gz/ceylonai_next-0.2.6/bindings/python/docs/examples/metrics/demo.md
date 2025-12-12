# Metrics Demo

A comprehensive demonstration of Ceylon AI's metrics collection capabilities.

## Overview

This example demonstrates:

- Message throughput and latency tracking
- Memory hit rate monitoring
- Continuous metrics monitoring
- Error tracking and reporting

## Prerequisites

```bash
pip install ceylonai-next
```

## Complete Code

The complete code for this example can be found in [`examples/metrics_demo.py`](../../examples/metrics_demo.py).

## Core Concepts

### 1. Message Metrics

Track agent communication performance:

```python
import ceylonai_next as ceylon
import asyncio

class WorkerAgent(ceylon.Agent):
    def name(self):
        return "worker"

    async def on_message(self, message, ctx):
        # Simulate work
        await asyncio.sleep(0.01)
        return f"Processed: {message}"

async def demo_message_metrics():
    mesh = ceylon.LocalMesh("metrics_demo")
    agent = WorkerAgent()
    mesh.add_agent(agent)
    mesh.start()

    # Send multiple messages
    for i in range(100):
        mesh.send_to("worker", f"task_{i}")

    await asyncio.sleep(2.0)

    # Get metrics
    metrics = ceylon.get_metrics()

    print(f"📊 Message Metrics:")
    print(f"  Throughput: {metrics['message_throughput']} messages")
    print(f"  Avg Latency: {metrics['avg_message_latency_us']/1000:.2f} ms")
    print(f"  Avg Execution Time: {metrics['avg_agent_execution_time_us']/1000:.2f} ms")
```

### 2. Memory Monitoring

Track memory system efficiency:

```python
from ceylonai_next import InMemoryBackend, MemoryEntry

def demo_memory_metrics():
    # Create memory backend
    memory = InMemoryBackend()

    # Perform operations
    for i in range(50):
        entry = MemoryEntry(
            content=f"data_{i}",
            metadata={"index": i}
        )
        memory.store(f"key_{i}", entry)

    # Simulate cache hits and misses
    for i in range(100):
        key = f"key_{i % 60}"  # Some keys won't exist
        memory.get(key)

    # Check metrics
    metrics = ceylon.get_metrics()

    total_ops = metrics['memory_hits'] + metrics['memory_misses']
    if total_ops > 0:
        hit_rate = (metrics['memory_hits'] / total_ops) * 100

        print(f"\n🧠 Memory Metrics:")
        print(f"  Hits: {metrics['memory_hits']}")
        print(f"  Misses: {metrics['memory_misses']}")
        print(f"  Writes: {metrics['memory_writes']}")
        print(f"  Hit Rate: {hit_rate:.1f}%")
```

### 3. Continuous Monitoring

Monitor metrics over time:

```python
async def continuous_monitoring(interval=5, duration=30):
    """Monitor metrics every `interval` seconds for `duration` seconds"""
    start_time = asyncio.get_event_loop().time()

    print(f"\n🔄 Starting continuous monitoring (every {interval}s)")
    print("=" * 60)

    while (asyncio.get_event_loop().time() - start_time) < duration:
        metrics = ceylon.get_metrics()

        print(f"\n📊 Snapshot at T+{int(asyncio.get_event_loop().time() - start_time)}s:")
        print(f"  Messages: {metrics['message_throughput']}")
        print(f"  Latency: {metrics['avg_message_latency_us']/1000:.2f} ms")
        print(f"  Memory Hit Rate: ", end="")

        total_ops = metrics['memory_hits'] + metrics['memory_misses']
        if total_ops > 0:
            hit_rate = (metrics['memory_hits'] / total_ops) * 100
            print(f"{hit_rate:.1f}%")
        else:
            print("N/A")

        await asyncio.sleep(interval)
```

### 4. Error Tracking

Monitor and report errors:

```python
class ErrorProneAgent(ceylon.Agent):
    def __init__(self):
        super().__init__("error_agent")
        self.call_count = 0

    async def on_message(self, message, ctx):
        self.call_count += 1

        # Simulate occasional errors
        if self.call_count % 10 == 0:
            raise ValueError("Simulated error")

        return f"OK: {message}"

async def demo_error_tracking():
    mesh = ceylon.LocalMesh("error_demo")
    agent = ErrorProneAgent()
    mesh.add_agent(agent)
    mesh.start()

    # Send messages (some will error)
    for i in range(50):
        try:
            mesh.send_to("error_agent", f"task_{i}")
        except:
            pass

    await asyncio.sleep(1.0)

    # Check error metrics
    metrics = ceylon.get_metrics()

    if metrics['errors']:
        total_errors = sum(metrics['errors'].values())
        error_rate = (total_errors / metrics['message_throughput']) * 100

        print(f"\n⚠️  Error Metrics:")
        print(f"  Total Errors: {total_errors}")
        print(f"  Error Rate: {error_rate:.2f}%")
        print(f"  Error Breakdown:")
        for error_type, count in metrics['errors'].items():
            print(f"    - {error_type}: {count}")
    else:
        print("\n✅ No errors detected")
```

## Running the Example

```bash
cd bindings/python
python examples/metrics_demo.py
```

## Expected Output

```
📊 Message Metrics:
  Throughput: 100 messages
  Avg Latency: 0.12 ms
  Avg Execution Time: 10.23 ms

🧠 Memory Metrics:
  Hits: 83
  Misses: 17
  Writes: 50
  Hit Rate: 83.0%

🔄 Starting continuous monitoring (every 5s)
============================================================

📊 Snapshot at T+0s:
  Messages: 100
  Latency: 0.12 ms
  Memory Hit Rate: 83.0%

📊 Snapshot at T+5s:
  Messages: 150
  Latency: 0.15 ms
  Memory Hit Rate: 85.2%

⚠️  Error Metrics:
  Total Errors: 5
  Error Rate: 3.33%
  Error Breakdown:
    - ValueError: 5
```

## Key Takeaways

1. **Comprehensive Tracking**: All aspects of your system are automatically monitored
2. **Real-time Updates**: Metrics update in real-time as your system runs
3. **Performance Insights**: Identify bottlenecks through latency and throughput metrics
4. **Health Monitoring**: Track errors and memory efficiency
5. **Zero Configuration**: No setup required - just call `get_metrics()`

## Best Practices

### Setting Up Periodic Monitoring

```python
import asyncio

async def periodic_metrics_logger(interval=60):
    """Log metrics every minute"""
    while True:
        await asyncio.sleep(interval)
        metrics = ceylon.get_metrics()

        # Log to file or monitoring system
        with open('metrics.log', 'a') as f:
            f.write(f"{time.time()},{metrics['message_throughput']},{metrics['avg_message_latency_us']}\n")
```

### Alerting on Thresholds

```python
def check_health(metrics):
    """Alert if metrics exceed thresholds"""
    alerts = []

    if metrics['avg_message_latency_us'] > 1000000:  # >1 second
        alerts.append("HIGH_LATENCY")

    total_ops = metrics['memory_hits'] + metrics['memory_misses']
    if total_ops > 0:
        hit_rate = metrics['memory_hits'] / total_ops
        if hit_rate < 0.8:
            alerts.append("LOW_CACHE_HIT_RATE")

    if alerts:
        send_alert(alerts)  # Your alerting logic
```

## Next Steps

- Review [Metrics Guide](../../guide/metrics/overview.md) for detailed documentation
- See [Metrics Quickstart](./quickstart.md) for a simpler introduction
- Check [examples/README_METRICS.md](../../examples/README_METRICS.md) for more examples
- Explore LLM token tracking examples in `examples/metrics_openai_tokens.py`
