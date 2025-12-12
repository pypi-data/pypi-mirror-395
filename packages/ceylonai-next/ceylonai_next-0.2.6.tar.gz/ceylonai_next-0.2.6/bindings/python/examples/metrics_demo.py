"""
Ceylon AI Metrics Demo
======================

This example demonstrates how to use the built-in metrics collection
in Ceylon AI to monitor your agents, memory backends, and LLM usage.

Metrics tracked:
- Message throughput and latency
- Agent execution time
- Memory operations (hits, misses, writes)
- LLM API calls (tokens, cost, latency)
- Error rates by type
"""

import ceylonai_next as ceylon
import asyncio
import json
import time


class WorkerAgent(ceylon.Agent):
    """Example agent that performs some work and tracks metrics."""
    
    def __init__(self, name: str):
        self._name = name
        self.work_duration = 0.1  # Default work duration
        self.messages_processed = 0
    
    def set_work_duration(self, duration: float):
        """Set the work duration after initialization."""
        self.work_duration = duration
        return self
    
    def name(self):
        return self._name
    
    async def on_message(self, message, ctx):
        """Process messages with simulated work."""
        self.messages_processed += 1
        print(f"[{self._name}] Processing message #{self.messages_processed}: {message}")
        
        # Simulate some work
        await asyncio.sleep(self.work_duration)
        
        print(f"[{self._name}] Completed message #{self.messages_processed}")


def print_metrics(title: str):
    """Pretty print the current metrics."""
    metrics = ceylon.get_metrics()
    
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    
    # Message metrics
    print("\n📨 Message Metrics:")
    print(f"  Total messages:        {metrics['message_throughput']}")
    print(f"  Avg latency:          {metrics['avg_message_latency_us']:.2f} μs")
    print(f"  Avg execution time:   {metrics['avg_agent_execution_time_us']:.2f} μs")
    
    # Memory metrics
    print("\n💾 Memory Metrics:")
    print(f"  Memory hits:          {metrics['memory_hits']}")
    print(f"  Memory misses:        {metrics['memory_misses']}")
    print(f"  Memory writes:        {metrics['memory_writes']}")
    
    if metrics['memory_hits'] + metrics['memory_misses'] > 0:
        hit_rate = metrics['memory_hits'] / (metrics['memory_hits'] + metrics['memory_misses']) * 100
        print(f"  Hit rate:             {hit_rate:.1f}%")
    
    # LLM metrics
    print("\n🤖 LLM Metrics:")
    print(f"  Total tokens:         {metrics['total_llm_tokens']}")
    print(f"  Avg LLM latency:      {metrics['avg_llm_latency_us']:.2f} μs")
    print(f"  Total LLM cost:       {metrics['total_llm_cost_us']} μ$")
    
    # Error metrics
    if metrics['errors']:
        print("\n⚠️  Errors:")
        for error_type, count in metrics['errors'].items():
            print(f"  {error_type}: {count}")
    else:
        print("\n✅ No errors recorded")
    
    print(f"{'='*60}\n")


async def demo_message_metrics():
    """Demonstrate message and agent execution metrics."""
    print("\n🚀 Demo 1: Message Metrics")
    print("-" * 60)
    
    # Create mesh and agents
    mesh = ceylon.LocalMesh("metrics_demo")
    
    # Add agents with different work durations
    fast_agent = WorkerAgent("fast_worker").set_work_duration(0.05)
    slow_agent = WorkerAgent("slow_worker").set_work_duration(0.15)
    
    mesh.add_agent(fast_agent)
    mesh.add_agent(slow_agent)
    mesh.start()
    
    # Send messages
    print("\nSending messages to agents...")
    for i in range(5):
        mesh.send_to("fast_worker", f"fast_task_{i}")
        mesh.send_to("slow_worker", f"slow_task_{i}")
        await asyncio.sleep(0.02)  # Small delay between sends
    
    # Wait for processing
    print("\nWaiting for processing to complete...")
    await asyncio.sleep(1.5)
    
    print_metrics("After Processing 10 Messages")


async def demo_memory_metrics():
    """Demonstrate memory backend metrics."""
    print("\n🚀 Demo 2: Memory Metrics")
    print("-" * 60)
    
    # Create memory backend
    memory = ceylon.InMemoryBackend()
    
    print("\nStoring 10 entries...")
    stored_ids = []
    for i in range(10):
        entry = ceylon.MemoryEntry(f"Content for entry {i}")
        entry_id = memory.store(entry)
        stored_ids.append(entry_id)
        print(f"  Stored entry {i}: {entry_id[:8]}...")
    
    print("\nRetrieving 5 existing entries (hits)...")
    for i in range(5):
        result = memory.get(stored_ids[i])
        if result:
            print(f"  ✓ Found entry {i}")
    
    print("\nAttempting to retrieve 3 non-existent entries (misses)...")
    for i in range(3):
        result = memory.get(f"fake_id_{i}")
        if not result:
            print(f"  ✗ Entry fake_id_{i} not found (miss)")
    
    print_metrics("After Memory Operations")


async def demo_continuous_monitoring():
    """Demonstrate continuous metrics monitoring."""
    print("\n🚀 Demo 3: Continuous Monitoring")
    print("-" * 60)
    
    mesh = ceylon.LocalMesh("monitor_demo")
    agent = WorkerAgent("monitored_agent").set_work_duration(0.1)
    mesh.add_agent(agent)
    mesh.start()
    
    memory = ceylon.InMemoryBackend()
    
    print("\nRunning workload for 3 seconds with periodic metrics snapshots...")
    print("(Sending messages and doing memory operations)\n")
    
    start_time = time.time()
    snapshot_count = 0
    
    while time.time() - start_time < 3.0:
        # Send a message
        mesh.send_to("monitored_agent", f"task_{int(time.time() * 1000)}")
        
        # Do some memory operations
        entry = ceylon.MemoryEntry(f"data_{int(time.time() * 1000)}")
        entry_id = memory.store(entry)
        memory.get(entry_id)
        
        # Take a snapshot every second
        if int(time.time() - start_time) > snapshot_count:
            snapshot_count += 1
            metrics = ceylon.get_metrics()
            print(f"[T+{snapshot_count}s] Messages: {metrics['message_throughput']}, "
                  f"Memory: {metrics['memory_writes']}W/{metrics['memory_hits']}H")
        
        await asyncio.sleep(0.2)
    
    await asyncio.sleep(0.5)  # Let final messages process
    print_metrics("Final Metrics After 3 Seconds")


async def demo_error_tracking():
    """Demonstrate error tracking in metrics."""
    print("\n🚀 Demo 4: Error Tracking")
    print("-" * 60)
    
    class FaultyAgent(ceylon.Agent):
        """Agent that sometimes raises errors."""
        
        def __init__(self):
            self.count = 0
        
        def name(self):
            return "faulty_agent"
        
        async def on_message(self, message, ctx):
            self.count += 1
            if self.count % 3 == 0:
                print(f"[faulty_agent] ⚠️  Raising error on message {self.count}")
                raise ValueError(f"Simulated error on message {self.count}")
            else:
                print(f"[faulty_agent] ✓ Processed message {self.count}")
                await asyncio.sleep(0.05)
    
    mesh = ceylon.LocalMesh("error_demo")
    agent = FaultyAgent()
    mesh.add_agent(agent)
    mesh.start()
    
    print("\nSending 10 messages (every 3rd will error)...")
    for i in range(10):
        try:
            mesh.send_to("faulty_agent", f"message_{i}")
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"  Caught: {e}")
    
    await asyncio.sleep(0.5)
    print_metrics("Metrics Showing Error Tracking")


async def main():
    """Run all demos."""
    print("""
╔══════════════════════════════════════════════════════════╗
║         Ceylon AI Metrics Collection Demo               ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Show initial state
    print_metrics("Initial State (Should be all zeros)")
    
    # Run demos
    await demo_message_metrics()
    await demo_memory_metrics()
    await demo_continuous_monitoring()
    await demo_error_tracking()
    
    print("\n✨ Demo complete! Metrics are automatically collected for:")
    print("   • Message throughput and latency")
    print("   • Agent execution times")
    print("   • Memory backend operations")
    print("   • LLM API usage (when using LLM agents)")
    print("   • Error rates and types")
    print("\nUse ceylon.get_metrics() anytime to retrieve current metrics.\n")


if __name__ == "__main__":
    asyncio.run(main())
