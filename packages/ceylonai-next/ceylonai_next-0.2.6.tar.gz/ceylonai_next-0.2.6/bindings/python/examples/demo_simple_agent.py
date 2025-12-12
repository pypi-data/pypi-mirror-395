#!/usr/bin/env python3
"""
Simple synchronous agent demo - verifies basic functionality
"""
import time
from ceylonai_next import Agent, PyLocalMesh


class SimpleAgent(Agent):
    """Agent with synchronous message handler"""
    
    def __init__(self, name):
        super().__init__(name)
        self.received = []

    def on_message(self, message, context=None):
        """Synchronous message handler"""
        print(f"[{self.name()}] Received: {message}")
        self.received.append(message)
        print(f"[{self.name()}] Processed: {message}")
        return f"Processed: {message}"


def main():
    """Main entry point"""
    print("\n🚀 Ceylon Simple Agent Demo\n")
    print("=" * 60)
    
    # Create agent and mesh
    agent = SimpleAgent("simple_agent")
    mesh = PyLocalMesh("demo_mesh")
    mesh.add_agent(agent)
    
    print(f"Created mesh with agent '{agent.name()}'")
    
    # Send messages
    messages = ["Hello", "World", "Test"]
    for msg in messages:
        print(f"\nSending: {msg}")
        mesh.send_to("simple_agent", msg)
        time.sleep(0.1)  # Give time for processing
    
    # Check results
    time.sleep(0.5)  # Wait for all messages to process
    print(f"\n✅ Agent received {len(agent.received)} messages: {agent.received}")
    
    if len(agent.received) == len(messages):
        print("✅ All messages processed successfully!")
    else:
        print(f"⚠️  Expected {len(messages)} messages, got {len(agent.received)}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
