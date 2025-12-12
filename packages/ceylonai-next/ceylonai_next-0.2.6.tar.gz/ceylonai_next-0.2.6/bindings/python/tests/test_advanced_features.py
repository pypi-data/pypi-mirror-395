import ceylonai_next
import json
import sys
from typing import TypedDict

# Define a custom action with type hints
class TypedAction(ceylonai_next.PyAction):
    def execute(self, msg: str, count: int) -> str:
        print(f"Executing TypedAction with msg: {msg}, count: {count}")
        return json.dumps({"status": "success", "repeated": msg * count})

def test_schema_generation():
    print("Testing Schema Generation...")
    
    # Create action without explicit schema
    action = TypedAction(
        name="typed_action",
        description="A typed action"
    )
    
    # Check Metadata
    metadata_str = action.metadata()
    metadata = json.loads(metadata_str)
    print(f"Generated Metadata: {json.dumps(metadata, indent=2)}")
    
    schema = metadata.get("input_schema")
    if not schema:
        print("Error: Schema was not generated.")
        sys.exit(1)
        
    props = schema.get("properties", {})
    if "msg" not in props or "count" not in props:
        print("Error: Schema missing expected properties.")
        sys.exit(1)
        
    if props["msg"]["type"] != "string" or props["count"]["type"] != "integer":
        print("Error: Schema types are incorrect.")
        sys.exit(1)
        
    print("Schema generation verification successful!")

def test_agent_act():
    print("\nTesting Agent self.act()...")
    
    class TestAgent(ceylonai_next.PyAgent):
        pass
        
    agent = TestAgent("test_agent")
    
    # Mock tool_invoker
    class MockInvoker:
        def invoke(self, name, inputs):
            print(f"MockInvoker invoked: {name} with {inputs}")
            return json.dumps({"mock": "result"})
            
    # Inject mock invoker
    agent.tool_invoker = MockInvoker()
    
    try:
        result = agent.act("some_action", {"param": "value"})
        print(f"Agent act result: {result}")
        
        if result != '{"mock": "result"}':
             print("Error: Unexpected result from agent.act")
             sys.exit(1)
             
    except Exception as e:
        print(f"Error calling agent.act: {e}")
        sys.exit(1)
        
    print("Agent act verification successful!")

if __name__ == "__main__":
    test_schema_generation()
    test_agent_act()
