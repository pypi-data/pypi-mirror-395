"""
Ceylon AI Multi-Agent System on Modal

This example demonstrates a multi-agent system using Ceylon AI on Modal.
Shows how multiple agents can communicate and coordinate via PyLocalMesh.

Use case: Customer service routing system with specialized agents

Prerequisites:
1. Install Modal: pip install modal
2. Setup Modal: modal setup

Run with: modal run multi_agent_modal.py
Deploy with: modal deploy multi_agent_modal.py
"""

import modal

# Create a Modal app
app = modal.App("ceylon-multi-agent")

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
    
    # Start Ollama server in the background
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
    
    # Check if model is available, pull if not
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
async def run_multi_agent_system(customer_query: str) -> dict:
    """
    Run a multi-agent customer service system.
    
    This demonstrates:
    - Multiple specialized agents
    - Agent coordination via PyLocalMesh
    - Routing logic based on query type
    """
    from ceylonai_next import LlmAgent, PyLocalMesh
    
    ensure_ollama_running()
    
    print(f"Customer query: {customer_query}")
    
    # Create mesh for agent communication
    mesh = PyLocalMesh("customer_service_mesh")
    
    # Create specialized agents
    print("\nInitializing agents...")
    
    # 1. Router agent - determines which specialist to use
    router = LlmAgent("router", "ollama::qwen2.5:0.5b")
    router.with_system_prompt(
        "You are a routing agent. Analyze customer queries and determine if they are about: "
        "'technical_support', 'billing', or 'general'. Respond with ONLY ONE of these three words."
    )
    router.build()
    
    # 2. Technical support agent
    tech_agent = LlmAgent("tech_support", "ollama::qwen2.5:0.5b")
    tech_agent.with_system_prompt(
        "You are a technical support specialist. Help customers with technical issues. "
        "Be concise and helpful."
    )
    tech_agent.build()
    
    # 3. Billing agent
    billing_agent = LlmAgent("billing", "ollama::qwen2.5:0.5b")
    billing_agent.with_system_prompt(
        "You are a billing specialist. Help customers with payment and invoice questions. "
        "Be clear and professional."
    )
    billing_agent.build()
    
    # 4. General agent
    general_agent = LlmAgent("general", "ollama::qwen2.5:0.5b")
    general_agent.with_system_prompt(
        "You are a general customer service representative. Handle general inquiries politely."
    )
    general_agent.build()
    
    print("✓ All agents initialized")
    
    # Route the query
    print("\nRouting query...")
    route_result = await router.send_message_async(customer_query)
    route = route_result.lower().strip()
    
    print(f"Routed to: {route}")
    
    # Select appropriate agent
    if "technical" in route:
        agent = tech_agent
        agent_name = "Technical Support"
    elif "billing" in route:
        agent = billing_agent
        agent_name = "Billing Department"
    else:
        agent = general_agent
        agent_name = "General Support"
    
    # Get response from specialist
    print(f"\nProcessing with {agent_name}...")
    response = await agent.send_message_async(customer_query)
    
    return {
        "query": customer_query,
        "routed_to": agent_name,
        "response": response,
        "status": "success"
    }


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
@modal.fastapi_endpoint(method="POST")
async def multi_agent_api(request: dict) -> dict:
    """
    Web API endpoint for multi-agent system.
    
    Deploy with: modal deploy multi_agent_modal.py
    
    Example request:
    curl -X POST <your-modal-url> \\
      -H "Content-Type: application/json" \\
      -d '{"query": "How do I reset my password?"}'
    """
    query = request.get("query", "")
    
    if not query:
        return {"error": "No query provided"}
    
    result = await run_multi_agent_system.remote.aio(query)
    return result


@app.local_entrypoint()
def main():
    """Test multi-agent system on Modal."""
    print("=" * 60)
    print("Ceylon AI Multi-Agent System on Modal")
    print("Customer Service Routing Example")
    print("=" * 60)
    
    # Test different query types
    test_queries = [
        ("How do I reset my password?", "technical"),
        ("Why was I charged twice?", "billing"),
        ("What are your business hours?", "general"),
    ]
    
    for query, expected_type in test_queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print(f"Expected route: {expected_type}")
        print("-" * 60)
        
        result = run_multi_agent_system.remote(query)
        
        print(f"Routed to: {result['routed_to']}")
        print(f"Response: {result['response']}")
        print(f"Status: {result['status']}")
    
    print("\n" + "=" * 60)
    print("Multi-Agent System Benefits:")
    print("=" * 60)
    print("""
    ✓ Specialized agents for different domains
    ✓ Intelligent query routing
    ✓ Scalable architecture
    ✓ Easy to add new agent types
    
    Deployment:
    1. Deploy as web API:
       modal deploy multi_agent_modal.py
    
    2. Send queries via HTTP:
       curl -X POST <url> -d '{"query": "your question"}'
    
    3. Monitor via Modal dashboard:
       https://modal.com/apps
    """)


if __name__ == "__main__":
    print("Run with: modal run multi_agent_modal.py")
    print("Deploy with: modal deploy multi_agent_modal.py")
