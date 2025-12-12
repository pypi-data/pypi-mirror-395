import asyncio
import os
from ceylonai_next import LlmAgent

async def main():
    print("Demo: LLM Agent with Custom Actions")
    print("=" * 40)
    
    # Create an agent using Ollama
    # Note: You need Ollama running with the specified model
    agent = LlmAgent("weather_agent", "ollama::gemma3:latest")
    
    # Configure the agent
    agent.with_system_prompt("You are a helpful assistant that can check the weather.")
    
    # Define a custom action using the decorator
    @agent.action(description="Get the current weather for a location")
    def get_weather(location: str, unit: str = "celsius"):
        print(f"  [Action] Checking weather for {location} in {unit}...")
        # Mock weather data
        if "london" in location.lower():
            return f"Weather in {location}: Rainy, 15 degrees {unit}"
        elif "paris" in location.lower():
            return f"Weather in {location}: Sunny, 22 degrees {unit}"
        else:
            return f"Weather in {location}: Partly cloudy, 20 degrees {unit}"
            
    # Define an action that uses the agent context
    @agent.action(description="Get information about the agent environment")
    def get_agent_info(context):
        print(f"  [Action] Accessing agent context...")
        return f"I am running on mesh: {context.mesh_name}"
            
    # Build the agent
    print("Building agent...")
    agent.build()
    
    # Send a message that triggers the action
    print("\nUser: What's the weather in London?")
    response = await agent.send_message_async("What's the weather in London?")
    print(f"Agent: {response}")
    
    print("\nUser: How about Paris?")
    response = await agent.send_message_async("How about Paris?")
    print(f"Agent: {response}")

    print("\nUser: What environment are you running in?")
    response = await agent.send_message_async("What environment are you running in?")
    print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
