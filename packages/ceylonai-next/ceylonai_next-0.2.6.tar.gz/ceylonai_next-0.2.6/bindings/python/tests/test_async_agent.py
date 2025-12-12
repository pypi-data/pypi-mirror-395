import pytest
import asyncio
import json
from ceylonai_next import Agent, PyLocalMesh

class AsyncAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.received = []

    async def on_message(self, message, context=None):
        await asyncio.sleep(0.01)
        self.received.append(message)
        return f"Processed: {message}"

@pytest.mark.asyncio
async def test_async_agent_on_message():
    agent = AsyncAgent("async_agent")
    mesh = PyLocalMesh("test_mesh")
    mesh.add_agent(agent)
    
    # Run blocking send_to in executor to avoid blocking the event loop
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: mesh.send_to("async_agent", "hello"))
    
    await asyncio.sleep(0.1)
    print(agent.received)
    assert "hello" in agent.received

@pytest.mark.asyncio
async def test_async_action():
    agent = AsyncAgent("action_agent")
    
    @agent.action(name="async_job")
    async def my_job(data: str):
        await asyncio.sleep(0.01)
        return f"Job done: {data}"
        
    mesh = PyLocalMesh("mesh2")
    mesh.add_agent(agent)
    
    loop = asyncio.get_running_loop()
    # Invoke action via tool_invoker (blocking)
    result = await loop.run_in_executor(None, lambda: agent.tool_invoker.invoke("async_job", json.dumps({"data": "test"})))
    
    print(result)
    # Result is a JSON string
    assert "Job done: test" in result
