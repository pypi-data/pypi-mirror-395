import os
import sys

# Add the bindings directory to path to ensure we can import ceylon if running from source
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from ceylonai_next import LlmAgent, LlmConfig, ReActConfig

def main():
    """
    Demonstrates the ReAct (Reason + Act) framework.
    
    Note: Currently, the ReAct engine is in "Reasoning Only" mode.
    It will generate thoughts and propose actions, but tool execution 
    integration is pending in the Rust core. You will see the agent 
    attempt to act and receive a system message about missing tool invoker.
    """
    
    # 1. Check API Key (Not needed for Ollama)
    # if "OPENAI_API_KEY" not in os.environ:
    #     print("Please set OPENAI_API_KEY environment variable.")
    #     return

    print("🤖 Initializing ReAct Agent with Ollama (gemma3:latest)...")

    # 2. Configure LLM
    config = LlmConfig.builder() \
        .provider("ollama") \
        .model("gemma3:latest") \
        .temperature(0.0) \
        .build()

    # 3. Create Agent
    agent = LlmAgent("reasoner", config)
    
    # 4. Configure ReAct Mode
    react_config = ReActConfig() \
        .with_max_iterations(5) \
        .with_thought_prefix("Thought:") \
        .with_action_prefix("Action:")
        
    agent.build()
    agent.with_react(react_config)

    # 5. Define a query that requires multi-step reasoning
    query = "Compare the population of Paris and London. Which one is larger and by how much?"
    
    print(f"\n👤 User: {query}")
    print("-" * 60)
    
    try:
        # 6. Execute with ReAct
        # This will block until the reasoning loop completes
        result = agent.send_message_react(query)
        
        # 7. Print the full trace
        result.print_trace()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
