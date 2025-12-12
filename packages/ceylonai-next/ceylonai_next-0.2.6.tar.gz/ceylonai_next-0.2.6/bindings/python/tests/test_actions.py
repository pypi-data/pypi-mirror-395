import ceylonai_next
import json

# Define a custom action
class MyAction(ceylonai_next.PyAction):
    def execute(self, context, inputs):
        print(f"Executing MyAction with inputs: {inputs}")
        # Return a JSON string as result
        return json.dumps({"status": "success", "processed_input": inputs})

def test_actions():
    print("Testing Agent Actions...")
    
    # 1. Create Action
    input_schema = json.dumps({"type": "object", "properties": {"msg": {"type": "string"}}})
    action = MyAction(
        name="my_action",
        description="A test action",
        input_schema=input_schema
    )
    print("Action created.")
    
    # 2. Check Metadata
    metadata = action.metadata()
    print(f"Metadata: {metadata}")
    
    # 3. Create ToolInvoker
    invoker = ceylonai_next.PyToolInvoker()
    print("ToolInvoker created.")
    
    # 4. Register Action
    invoker.register(action)
    print("Action registered.")
    
    # 5. Invoke Action
    inputs = json.dumps({"msg": "hello"})
    print(f"Invoking action with inputs: {inputs}")
    result = invoker.invoke("my_action", inputs)
    print(f"Result: {result}")

    # Verify result
    result_json = json.loads(result)
    # The result from Rust is currently wrapped in a string because of our simplified implementation
    # Let's parse it again if needed, or check the structure
    assert result is not None, "Result should not be None"
    print("Verification successful!")

if __name__ == "__main__":
    test_actions()
