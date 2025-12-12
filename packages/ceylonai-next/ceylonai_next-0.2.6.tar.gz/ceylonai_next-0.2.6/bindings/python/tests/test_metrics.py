import pytest
import asyncio
import json
import time
from ceylonai_next import (
    LocalMesh, 
    Agent, 
    get_metrics, 
    InMemoryBackend, 
    MemoryEntry
)

class MetricsTestAgent(Agent):
    def __init__(self, name="metrics_agent"):
        super().__init__(name)
        self._name = name

    def name(self):
        return self._name

    async def on_message(self, message, ctx):
        # Simulate some work to ensure execution time is measurable
        await asyncio.sleep(0.01)

@pytest.mark.asyncio
async def test_message_metrics():
    """Test that message throughput and latency are recorded."""
    mesh = LocalMesh("metrics_mesh")
    agent = MetricsTestAgent("metrics_agent")
    mesh.add_agent(agent)
    mesh.start()

    # Send a few messages
    for i in range(5):
        mesh.send_to("metrics_agent", f"message_{i}")
        # Small delay to ensure they are processed sequentially
        await asyncio.sleep(0.05)
    
    # Wait a bit for processing to complete
    await asyncio.sleep(0.2)

    metrics = get_metrics()
    print(f"Metrics: {json.dumps(metrics, indent=2)}")

    # Verify throughput
    assert metrics["message_throughput"] >= 5, "Message throughput should be at least 5"
    
    # Verify latency
    # Note: Latency might be 0 if it's extremely fast, but with sleep(0.01) in agent it should be > 0
    assert metrics["avg_agent_execution_time_us"] > 0, "Agent execution time should be recorded"
    assert metrics["avg_message_latency_us"] > 0, "Message latency should be recorded"

@pytest.mark.asyncio
async def test_memory_metrics():
    """Test that memory operations are recorded."""
    backend = InMemoryBackend()
    
    # 1. Test Write
    entry = MemoryEntry("test content")
    backend.store(entry)
    
    metrics_after_write = get_metrics()
    assert metrics_after_write["memory_writes"] >= 1, "Memory write should be recorded"

    # 2. Test Hit
    backend.get(entry.id)
    
    metrics_after_hit = get_metrics()
    assert metrics_after_hit["memory_hits"] >= 1, "Memory hit should be recorded"

    # 3. Test Miss
    backend.get("non_existent_id")
    
    metrics_after_miss = get_metrics()
    assert metrics_after_miss["memory_misses"] >= 1, "Memory miss should be recorded"
