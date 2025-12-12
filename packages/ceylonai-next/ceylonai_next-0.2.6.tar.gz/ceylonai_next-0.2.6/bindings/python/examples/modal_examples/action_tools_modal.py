"""
Ceylon AI Action Tools on Modal

This example demonstrates how to create agents with custom actions (tools).
Agents can call Python functions to extend their capabilities.

Use case: Agent with real-time data access and calculation abilities

Prerequisites:
1. Install Modal: pip install modal
2. Setup Modal: modal setup

Run with: modal run action_tools_modal.py
Deploy with: modal deploy action_tools_modal.py
"""

import modal

# Create a Modal app
app = modal.App("ceylon-action-tools")

# Create a persistent volume for Ollama models
ollama_volume = modal.Volume.from_name("ollama-models", create_if_missing=True)

# Define image with Ceylon AI and dependencies
image = (
    modal.Image.from_registry("ubuntu:24.04", add_python="3.12")
    .apt_install("curl")
    .run_commands(
        "curl -fsSL https://ollama.ai/install.sh | sh",
    )
    .pip_install(
        "ceylonai-next>=0.2.5",
        "fastapi[standard]"
    )
)


def ensure_ollama_running():
    """Ensure Ollama server is running and model is available."""
    import subprocess
    import time
    
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(3)
        print("✓ Ollama server started")
    except Exception as e:
        print(f"Note: Ollama server might already be running: {e}")
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "qwen2.5:0.5b" not in result.stdout:
            print("Pulling qwen2.5:0.5b model (first run only, ~397 MB)...")
            subprocess.run(
                ["ollama", "pull", "qwen2.5:0.5b"],
                check=True,
                timeout=600
            )
            print("✓ Model pulled successfully")
            ollama_volume.commit()
        else:
            print("✓ Model already available")
    except Exception as e:
        print(f"Warning: Error checking/pulling model: {e}")


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
async def run_agent_with_tools(query: str) -> dict:
    """
    Run an agent with custom action tools.
    
    This demonstrates:
    - Defining custom actions with @agent.action decorator
    - Agent automatic tool selection
    - Function calling with parameters
    """
    from ceylonai_next import LlmAgent
    import random
    from datetime import datetime
    
    ensure_ollama_running()
    
    print(f"Query: {query}")
    
    # Create agent
    agent = LlmAgent("tool_agent", "ollama::qwen2.5:0.5b")
    agent.with_system_prompt(
        "You are a helpful assistant with access to various tools. "
        "Use the available tools to answer questions accurately."
    )
    
    # Define custom actions (tools)
    
    @agent.action(description="Get the current time and date")
    def get_current_time() -> str:
        """Returns current date and time"""
        print("  [Tool] Getting current time...")
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @agent.action(description="Calculate a mathematical expression")
    def calculate(expression: str) -> str:
        """Safely evaluate a mathematical expression"""
        print(f"  [Tool] Calculating: {expression}")
        try:
            # Safe eval for basic math
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"
    
    @agent.action(description="Get weather information for a city")
    def get_weather(city: str) -> str:
        """Get mock weather data for a city"""
        print(f"  [Tool] Getting weather for {city}...")
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
        temp = random.randint(10, 30)
        condition = random.choice(weather_conditions)
        return f"Weather in {city}: {condition}, {temp}°C"
    
    @agent.action(description="Search for information in a knowledge base")
    def search_knowledge(topic: str) -> str:
        """Search mock knowledge base"""
        print(f"  [Tool] Searching for: {topic}")
        knowledge = {
            "python": "Python is a high-level programming language known for its simplicity and readability.",
            "ai": "Artificial Intelligence involves creating systems that can perform tasks requiring human intelligence.",
            "ceylon": "Ceylon AI is a framework for building multi-agent AI systems.",
        }
        for key, value in knowledge.items():
            if key in topic.lower():
                return value
        return f"No information found about {topic}"
    
    @agent.action(description="Convert temperature between Celsius and Fahrenheit")
    def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
        """Convert temperature between C and F"""
        print(f"  [Tool] Converting {value}°{from_unit} to °{to_unit}")
        if from_unit.lower() == "c" and to_unit.lower() == "f":
            result = (value * 9/5) + 32
            return f"{value}°C = {result:.1f}°F"
        elif from_unit.lower() == "f" and to_unit.lower() == "c":
            result = (value - 32) * 5/9
            return f"{value}°F = {result:.1f}°C"
        else:
            return "Invalid units. Use 'C' or 'F'"
    
    # Build agent with all tools
    agent.build()
    
    print("✓ Agent initialized with 5 tools")
    print("  - get_current_time")
    print("  - calculate")
    print("  - get_weather") 
    print("  - search_knowledge")
    print("  - convert_temperature")
    
    # Get response
    print(f"\nProcessing query...")
    response = await agent.send_message_async(query)
    
    return {
        "query": query,
        "response": response,
        "tools_available": 5,
        "status": "success"
    }


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
@modal.web_endpoint(method="POST")
async def tools_api(request: dict) -> dict:
    """
    Web API endpoint for agent with tools.
    
    Deploy with: modal deploy action_tools_modal.py
    
    Example request:
    curl -X POST <your-modal-url> \\
      -H "Content-Type: application/json" \\
      -d '{"query": "What is 42 * 17?"}'
    """
    query = request.get("query", "")
    
    if not query:
        return {"error": "No query provided"}
    
    result = await run_agent_with_tools.remote.aio(query)
    return result


@app.local_entrypoint()
def main():
    """Test agent with action tools on Modal."""
    print("=" * 60)
    print("Ceylon AI Action Tools on Modal")
    print("Agent with Custom Capabilities")
    print("=" * 60)
    
    # Test different tool usage scenarios
    test_queries = [
        "What time is it?",
        "Calculate 123 + 456",
        "What's the weather in Paris?",
        "Tell me about Python",
        "Convert 100 Fahrenheit to Celsius",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Test {i}: {query}")
        print("-" * 60)
        
        result = run_agent_with_tools.remote(query)
        
        print(f"Response: {result['response']}")
        print(f"Status: {result['status']}")
    
    print("\n" + "=" * 60)
    print("Action Tools Features:")
    print("=" * 60)
    print("""
    ✓ Custom function definitions with @agent.action
    ✓ Automatic tool selection by LLM
    ✓ Type-safe parameters
    ✓ Easy to extend
    
    Available Tools:
    1. get_current_time - Returns current date/time
    2. calculate - Evaluates math expressions
    3. get_weather - Gets weather for a city
    4. search_knowledge - Searches knowledge base
    5. convert_temperature - Converts C ↔ F
    
    Use Cases:
    - Data retrieval agents
    - Calculation assistants
    - API integration bots
    - Research assistants
    
    Deployment:
    modal deploy action_tools_modal.py
    """)


if __name__ == "__main__":
    print("Run with: modal run action_tools_modal.py")
    print("Deploy with: modal deploy action_tools_modal.py")
