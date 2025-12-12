import asyncio
import time
from ceylonai_next import DistributedMesh, Agent

class EchoAgent(Agent):
    def on_message(self, message, context=None):
        print(f"[EchoAgent] Received: {message}")
        return f"Echo: {message}"

async def main():
    # 1. Start Server Node
    server_mesh = DistributedMesh("server_node", 50051)
    
    agent = EchoAgent("echo_agent")
    server_mesh.add_agent(agent)
    
    print("Starting server...")
    server_mesh.start()
    
    # Give it a moment to start
    await asyncio.sleep(1)
    
    # 2. Start Client Node
    client_mesh = DistributedMesh("client_node", 50052)
    client_mesh.start()
    
    # 3. Connect Client to Server Peer
    # We tell the client mesh that "echo_agent" is located at the server's URL
    print("Connecting to peer...")
    client_mesh.connect_peer("echo_agent", "http://127.0.0.1:50051")
    
    print("Sending message from client to server...")
    client_mesh.send_to("echo_agent", "Hello from Python Distributed Mesh!")
    
    # Wait for response (EchoAgent prints to stdout)
    await asyncio.sleep(2)
    
    print("Shutting down...")
    server_mesh.stop()
    client_mesh.stop()

if __name__ == "__main__":
    asyncio.run(main())
