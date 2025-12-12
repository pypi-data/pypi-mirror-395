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
