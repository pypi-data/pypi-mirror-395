#!/usr/bin/env python3
"""
Async Agent Demo - demonstrates async message handling without pytest
"""
import asyncio
import json
from ceylonai_next import Agent, PyLocalMesh


class AsyncAgent(Agent):
    """Agent with async message handler"""
    
    def __init__(self, name):
        super().__init__(name)
        self.received = []

    async def on_message(self, message, context=None):
        """Async message handler - simulates async processing"""
        print(f"[{self.name()}] Received: {message}")
        await asyncio.sleep(0.01)  # Simulate async work
        self.received.append(message)
        print(f"[{self.name()}] Processed: {message}")
        return f"Processed: {message}"


async def demo_async_messaging():
    """Demo 1: Async message handling"""
    print("=" * 60)
    print("Demo 1: Async Message Handling")
    print("=" * 60)
    
    # Create agent and mesh
    agent = AsyncAgent("async_agent")
    mesh = PyLocalMesh("demo_mesh")
    mesh.add_agent(agent)
    
    print(f"Created mesh with agent '{agent.name()}'")
    
    # Send messages in executor (since send_to is blocking)
    loop = asyncio.get_running_loop()
    
    messages = ["Hello", "World", "Async", "Test"]
    for msg in messages:
        print(f"\nSending: {msg}")
        await loop.run_in_executor(None, lambda m=msg: mesh.send_to("async_agent", m))
        await asyncio.sleep(0.05)  # Give time for processing
    
    # Check results
    await asyncio.sleep(0.2)  # Wait for all messages to process
    print(f"\n✅ Agent received {len(agent.received)} messages: {agent.received}")
    
    if len(agent.received) == len(messages):
        print("✅ All messages processed successfully!")
    else:
        print(f"⚠️  Expected {len(messages)} messages, got {len(agent.received)}")


async def demo_async_action():
    """Demo 2: Async action execution"""
    print("\n" + "=" * 60)
    print("Demo 2: Async Action Execution")
    print("=" * 60)
    
    # Create agent with async action
    agent = AsyncAgent("action_agent")
    
    @agent.action(name="async_job")
    async def my_job(data: str):
        """Async action that processes data"""
        print(f"[Action] Processing: {data}")
        await asyncio.sleep(0.01)  # Simulate async work
        result = f"Job done: {data}"
        print(f"[Action] Result: {result}")
        return result
    
    # Add to mesh
    mesh = PyLocalMesh("action_mesh")
    mesh.add_agent(agent)
    
    print(f"Created agent with async action 'async_job'")
    
    # Invoke action in executor
    loop = asyncio.get_running_loop()
    test_data = {"data": "test_value"}
    
    print(f"\nInvoking action with: {test_data}")
    result = await loop.run_in_executor(
        None, 
        lambda: agent.tool_invoker.invoke("async_job", json.dumps(test_data))
    )
    
    print(f"\n✅ Action result: {result}")
    
    if "Job done: test_value" in result:
        print("✅ Async action executed successfully!")
    else:
        print(f"⚠️  Unexpected result: {result}")


async def main():
    """Main entry point"""
    print("\n🚀 Ceylon Async Agent Demo\n")
    
    try:
        # Run demo 1: Async messaging
        await demo_async_messaging()
        
        # Run demo 2: Async actions
        await demo_async_action()
        
        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the async demo
    asyncio.run(main())
