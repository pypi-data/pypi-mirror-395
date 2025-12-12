# Metrics Quickstart

A minimal example demonstrating basic metrics collection in Ceylon AI.

## Overview

This example shows how to:

- Create a simple agent and mesh
- Send messages to agents
- Retrieve and display metrics using `get_metrics()`

## Prerequisites

```bash
# Install Ceylon AI
pip install ceylonai-next

# Or install from source
cd bindings/python
pip install -e .
```

## Code Example

```python
"""
Quick Start: Ceylon AI Metrics
===============================

A minimal example showing how to access metrics in Ceylon AI.
"""

import ceylonai_next as ceylon
import asyncio
import json


class SimpleAgent(ceylon.Agent):
    def name(self):
        return "simple_agent"

    async def on_message(self, message, ctx):
        print(f"Processing: {message}")
        await asyncio.sleep(0.1)  # Simulate work


async def main():
    # Create and start a mesh
    mesh = ceylon.LocalMesh("my_mesh")
    agent = SimpleAgent()
    mesh.add_agent(agent)
    mesh.start()

    # Send some messages
    for i in range(5):
        mesh.send_to("simple_agent", f"task_{i}")

    # Wait for processing
    await asyncio.sleep(1.0)

    # Get metrics
    metrics = ceylon.get_metrics()

    # Display metrics
    print("\n📊 Metrics Summary:")
    print(json.dumps(metrics, indent=2))

    print(f"\n✅ Processed {metrics['message_throughput']} messages")
    print(f"⏱️  Average latency: {metrics['avg_message_latency_us']:.0f} μs")


if __name__ == "__main__":
    asyncio.run(main())
```

## Running the Example

```bash
cd bindings/python
python examples/metrics_quickstart.py
```

## Expected Output

```
Processing: task_0
Processing: task_1
Processing: task_2
Processing: task_3
Processing: task_4

📊 Metrics Summary:
{
  "message_throughput": 5,
  "avg_message_latency_us": 123.45,
  "avg_agent_execution_time_us": 100234.56,
  "total_llm_tokens": 0,
  "avg_llm_latency_us": 0.0,
  "total_llm_cost_us": 0,
  "memory_hits": 0,
  "memory_misses": 0,
  "memory_writes": 0,
  "errors": {}
}

✅ Processed 5 messages
⏱️  Average latency: 123 μs
```

## Key Takeaways

1. **Simple Access**: Metrics are easily accessible via `ceylon.get_metrics()`
2. **Automatic Collection**: No configuration needed - metrics are collected automatically
3. **Complete Snapshot**: Returns all metrics in a single dictionary
4. **JSON Serializable**: Can be easily exported or logged

## Next Steps

- See [Metrics Demo](./demo.md) for more comprehensive examples
- Check [Metrics Guide](../../guide/metrics/overview.md) for detailed documentation
- View [examples/README_METRICS.md](../../examples/README_METRICS.md) for all metrics examples
