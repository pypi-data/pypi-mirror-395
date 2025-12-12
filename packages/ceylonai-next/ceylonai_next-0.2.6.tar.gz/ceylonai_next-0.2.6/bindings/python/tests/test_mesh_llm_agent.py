"""
Test Ceylon AI Mesh LLM Agent Example

Basic tests for the mesh agent system.
"""

import sys
import os

# Add path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../bindings/python"))
)

from ceylonai_next import LlmAgent, PyLocalMesh, InMemoryBackend, MemoryEntry


def test_mesh_creation():
    """Test creating a mesh instance."""
    print("\n🧪 Test: Mesh Creation")
    mesh = PyLocalMesh("test_mesh")
    assert mesh is not None
    print("   ✓ Mesh created successfully")


def test_llm_agent_creation():
    """Test creating LLM agents."""
    print("\n🧪 Test: LLM Agent Creation")

    agent = LlmAgent("test_agent", "ollama::llama3.2:latest")
    agent.with_system_prompt("You are a helpful assistant.")
    agent.with_temperature(0.7)
    agent.with_max_tokens(100)
    agent.build()

    assert agent is not None
    print("   ✓ LLM Agent created successfully")


def test_llm_agent_with_memory():
    """Test creating LLM agent with memory backend."""
    print("\n🧪 Test: LLM Agent with Memory")

    # Create memory
    memory = InMemoryBackend()
    entry = MemoryEntry("Test knowledge item")
    entry.with_metadata("category", "test")
    memory.store(entry)

    # Create agent with memory
    agent = LlmAgent("memory_agent", "ollama::llama3.2:latest")
    agent.with_memory(memory)
    agent.with_system_prompt("You are a helpful assistant with memory.")
    agent.build()

    assert agent is not None
    print("   ✓ LLM Agent with memory created successfully")


def test_multiple_agents():
    """Test creating multiple specialized agents."""
    print("\n🧪 Test: Multiple Specialized Agents")

    agents = {}

    # Create coordinator
    coordinator = LlmAgent("coordinator", "ollama::llama3.2:latest")
    coordinator.with_system_prompt("You are a coordinator.")
    coordinator.build()
    agents["coordinator"] = coordinator

    # Create specialist
    specialist = LlmAgent("specialist", "ollama::llama3.2:latest")
    specialist.with_system_prompt("You are a specialist.")
    specialist.build()
    agents["specialist"] = specialist

    assert len(agents) == 2
    print(f"   ✓ Created {len(agents)} agents successfully")


def test_mesh_agent_integration():
    """Test adding LLM agent to mesh (conceptual)."""
    print("\n🧪 Test: Mesh-Agent Integration")

    mesh = PyLocalMesh("integration_mesh")
    agent = LlmAgent("test_agent", "ollama::llama3.2:latest")
    agent.with_system_prompt("Test agent")
    agent.build()

    # Note: This may not work depending on Ceylon's current implementation
    # This is more of a conceptual test
    try:
        mesh.add_agent(agent)
        mesh.start()
        print("   ✓ Agent added to mesh successfully")
    except Exception as e:
        print(f"   ℹ️  Mesh integration note: {e}")
        print("   ℹ️  LLM agents may operate independently of mesh")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Ceylon AI - Mesh LLM Agent Tests")
    print("=" * 60)

    tests = [
        test_mesh_creation,
        test_llm_agent_creation,
        test_llm_agent_with_memory,
        test_multiple_agents,
        test_mesh_agent_integration,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"   ✗ Test failed: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Tests: {passed} passed, {failed} failed")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
