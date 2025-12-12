import ceylonai_next
import json
import sys

def test_decorator():
    print("Testing @agent.action() decorator...")
    
    # Define Agent class (this will be moved to library later)
    # For now, we expect ceylon.Agent to exist after our changes
    # But since we haven't implemented it yet, we will define a mock or just use the test to drive implementation
    
    # We need to import Agent from ceylonai_next package once implemented
    from ceylonai_next import Agent
    
    agent = Agent("decorator_agent")
    
    @agent.action(description="A decorated action")
    def simple_action(context, msg: str, count: int):
        print(f"Executing simple_action with msg: {msg}, count: {count}")
        print(f"Context mesh_name: {context.mesh_name}")
        return json.dumps({"status": "success", "repeated": msg * count})
        
    # Verify action registration
    # We need to access the underlying tool invoker to check if action is registered
    # Since we can't easily inspect the Rust map, we will just try to invoke it
    
    print("Action defined. Invoking...")
    
    # Mock tool_invoker for now as we did in previous test, 
    # BUT the decorator should have registered the action with the agent's tool invoker.
    # The Agent class should handle creating the tool invoker.
    
    # Let's assume Agent creates a PyToolInvoker internally.
    
    inputs = json.dumps({"msg": "hello", "count": 2})
    try:
        # We need to manually invoke it via the tool invoker exposed on the agent
        # or via agent.act if we implemented that (which we did!)
        
        # Note: In a real scenario, the context would be passed by the runtime.
        # Here, we are invoking via agent.act which delegates to tool_invoker.invoke.
        # The tool_invoker.invoke (Rust) calls PythonActionWrapper.execute (Rust).
        # PythonActionWrapper.execute needs to create the context and pass it to Python.
        
        result = agent.act("simple_action", {"msg": "hello", "count": 2})
        print(f"Result: {result}")
        
        result_json = json.loads(result)
        if result_json["repeated"] != "hellohello":
            print("Error: Unexpected result")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error invoking action: {e}")
        sys.exit(1)
        
    print("Decorator verification successful!")

if __name__ == "__main__":
    test_decorator()
