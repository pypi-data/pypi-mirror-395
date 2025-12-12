import sys


def test_llm_agent_creation():
    """Test creating an LlmAgent instance."""
    print("\nTesting LlmAgent creation...")
    from ceylonai_next import LlmAgent

    # Create agent with Ollama (no API key needed)
    # Using gemma3:latest which is available in Ollama
    agent = LlmAgent("test_agent", "ollama::gemma3:latest")
    print("✓ Successfully created LlmAgent instance")

    # Test builder pattern
    agent.with_system_prompt("You are a helpful assistant.")
    agent.with_temperature(0.7)
    agent.with_max_tokens(100)
    print("✓ Builder methods work correctly")

    # Build the agent
    agent.build()
    print("✓ Successfully built agent")
    assert agent is not None


def test_llm_agent_message():
    """Test sending a message to LlmAgent."""
    print("\nTesting LlmAgent message sending...")
    from ceylonai_next import LlmAgent

    # Create and build agent with gemma3:latest
    agent = LlmAgent("test_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("You are a helpful assistant. Respond briefly.")
    agent.with_temperature(0.7)
    agent.with_max_tokens(50)
    agent.build()

    # Send a message
    print("Sending message to agent...")
    response = agent.send_message("Hello! What's 2+2?")
    print(f"✓ Response: {response}")
    assert response is not None
    assert len(response) > 0


def main():
    print("Testing Ceylon LlmAgent Python Bindings")
    print("=" * 50)

    # Run tests
    tests = [
        test_llm_agent_import,
        test_llm_agent_creation,
        test_llm_agent_message,  # Now enabled to test actual Ollama calls
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    # Summary
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
