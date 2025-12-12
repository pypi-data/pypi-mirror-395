"""
Test script for Ceylon Mesh Python bindings.
"""
import ceylonai_next

class SampleAgent(ceylonai_next.PyAgent):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self.messages_received = []

    def name(self):
        return self._name

    def on_start(self, ctx):
        print(f"Agent {self.name()} started")

    def on_message(self, payload, ctx):
        msg = bytes(payload).decode('utf-8')
        print(f"Agent {self.name()} received: {msg}")
        self.messages_received.append(msg)

    def on_stop(self, ctx):
        print(f"Agent {self.name()} stopped")

def test_mesh():
    # Create a mesh
    mesh = ceylonai_next.PyLocalMesh("test_mesh")

    # Create an agent
    agent = SampleAgent("test_agent")
    
    # Add agent to mesh
    mesh.add_agent(agent)

    # Start the mesh
    mesh.start()

    # Send a message
    mesh.send_to("test_agent", "Hello from Python!")

    print("Test completed successfully!")
    assert mesh is not None
    assert agent is not None

if __name__ == "__main__":
    test_mesh()
