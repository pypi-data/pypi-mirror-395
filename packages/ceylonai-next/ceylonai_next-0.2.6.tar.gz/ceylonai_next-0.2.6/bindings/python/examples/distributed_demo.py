import asyncio
import ceylonai_next as ceylon

class EchoAgent(ceylon.PyAgent):
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def on_message(self, message, ctx):
        print(f"[{self._name}] Received: {message}")
        return None

async def main():
    # Create a shared registry
    registry = ceylon.PyInMemoryRegistry()

    # Node 1
    print("Starting Node 1...")
    mesh1 = ceylon.PyDistributedMesh.with_registry("node1", 50091, registry)
    mesh1.start()
    
    agent1 = EchoAgent("agent1")
    mesh1.add_agent(agent1)

    # Node 2
    print("Starting Node 2...")
    mesh2 = ceylon.PyDistributedMesh.with_registry("node2", 50092, registry)
    mesh2.start()

    agent2 = EchoAgent("agent2")
    mesh2.add_agent(agent2)

    # Give time for startup and registration
    await asyncio.sleep(1)

    # Send message from agent1 to agent2
    print("Sending message from agent1 to agent2...")
    mesh1.send_to("agent2", "Hello from Python Agent 1")

    # Wait for delivery
    await asyncio.sleep(1)

    print("Stopping nodes...")
    mesh1.stop()
    mesh2.stop()

if __name__ == "__main__":
    asyncio.run(main())
