# PyAction

The `PyAction` class provides a foundation for defining actions that agents can execute. Actions encapsulate reusable functionality with input/output schemas, metadata, and context-aware execution.

## Class Signature

```python
class PyAction(_PyAction):
    def __new__(
        cls,
        name: str,
        description: str,
        input_schema: str | None = None,
        output_schema: str | None = None
    ) -> PyAction:
        ...

    @abstractmethod
    def execute(
        self,
        context: PyAgentContext,
        inputs: Dict[str, Any]
    ) -> str:
        ...
```

## Description

`PyAction` is a Python wrapper around `_PyAction` that represents a discrete action that an agent can perform. Each action has a name, description, and JSON schemas describing its inputs and outputs. The class uses automatic schema generation from function signatures and provides a simple interface for action execution.

## Constructor

### `__new__(name: str, description: str, input_schema: str | None = None, output_schema: str | None = None)`

Creates a new action instance.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | Required | Unique action identifier |
| `description` | `str` | Required | Human-readable action description |
| `input_schema` | `str \| None` | `None` | JSON schema for inputs (auto-generated if None) |
| `output_schema` | `str \| None` | `None` | JSON schema for outputs |

**Returns:** PyAction instance

**Notes:**
- `name` should be unique within an agent
- `description` helps the LLM decide when to use the action
- If `input_schema` is None, it's automatically generated from the `execute()` method signature
- Schemas should be valid JSON strings

**Example:**
```python
import json
from ceylonai_next import PyAction

class MyCustomAction(PyAction):
    def __init__(self):
        input_schema = json.dumps({
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer"}
            },
            "required": ["query"]
        })
        super().__init__(
            name="search",
            description="Search for information",
            input_schema=input_schema
        )

    def execute(self, context, inputs):
        query = inputs.get("query", "")
        limit = inputs.get("limit", 10)
        # Perform search
        return json.dumps({"results": []})
```

## Abstract Methods

### `execute(context: PyAgentContext, inputs: Dict[str, Any]) -> str`

Execute the action with the given inputs and context.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `PyAgentContext` | Agent execution context |
| `inputs` | `Dict[str, Any]` | Input parameters matching the schema |

**Returns:** `str` - JSON-formatted result

**Notes:**
- Must be implemented by subclasses
- Should return JSON-serializable string
- Has access to agent context for state/information
- Execution is typically synchronous

**Example:**
```python
import json
from ceylonai_next import PyAction

class CalculatorAction(PyAction):
    def __init__(self):
        super().__init__(
            name="calculate",
            description="Perform arithmetic operations"
        )

    def execute(self, context, inputs):
        operation = inputs.get("op", "add")
        a = inputs.get("a", 0)
        b = inputs.get("b", 0)

        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            result = a / b if b != 0 else None
        else:
            result = None

        return json.dumps({
            "operation": operation,
            "result": result,
            "error": result is None
        })
```

## Methods

### `metadata() -> Dict[str, Any]`

Get the action's metadata (name, description, schemas).

**Parameters:** None

**Returns:** `Dict[str, Any]` - Metadata dictionary

**Example:**
```python
class InfoAction(PyAction):
    def __init__(self):
        super().__init__(
            name="get_info",
            description="Get system information"
        )

    def execute(self, context, inputs):
        return json.dumps({"status": "ok"})

action = InfoAction()
metadata = action.metadata()
print(f"Name: {metadata['name']}")
print(f"Description: {metadata['description']}")
```

## Related Classes

### `FunctionalAction`

A convenience subclass that wraps a function as an action:

```python
from ceylonai_next import FunctionalAction

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

action = FunctionalAction(
    multiply,
    name="multiply_numbers",
    description="Multiply two integers"
)
```

## Complete Examples

### Example 1: Simple Custom Action

```python
import json
from ceylonai_next import PyAction, Agent

class GreetingAction(PyAction):
    """Action that generates greetings"""

    def __init__(self):
        super().__init__(
            name="greet",
            description="Generate a personalized greeting"
        )

    def execute(self, context, inputs):
        name = inputs.get("name", "Friend")
        formal = inputs.get("formal", False)

        if formal:
            greeting = f"Good day, {name}. I hope you are well."
        else:
            greeting = f"Hey {name}! How's it going?"

        return json.dumps({
            "greeting": greeting,
            "recipient": name,
            "formal": formal
        })

class GreetingAgent(Agent):
    def __init__(self):
        super().__init__("greeter")
        self.tool_invoker.register(GreetingAction())

# Usage
agent = GreetingAgent()
# The agent can now use the greet action
```

### Example 2: Action with Validation

```python
import json
from ceylonai_next import PyAction

class ValidatedMathAction(PyAction):
    """Math action with input validation"""

    def __init__(self):
        schema = json.dumps({
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"]
                },
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        })
        super().__init__(
            name="math",
            description="Perform mathematical operations",
            input_schema=schema
        )

    def execute(self, context, inputs):
        operation = inputs.get("operation")
        a = inputs.get("a")
        b = inputs.get("b")

        # Validation
        if operation not in ["add", "subtract", "multiply", "divide"]:
            return json.dumps({"error": "Invalid operation"})

        if operation == "divide" and b == 0:
            return json.dumps({"error": "Division by zero"})

        # Execution
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        else:
            result = a / b

        return json.dumps({
            "operation": operation,
            "operands": {"a": a, "b": b},
            "result": result
        })
```

### Example 3: Context-Aware Action

```python
import json
from ceylonai_next import PyAction, PyAgentContext

class ContextAwareAction(PyAction):
    """Action that uses agent context"""

    def __init__(self):
        super().__init__(
            name="context_info",
            description="Get information about the execution context"
        )

    def execute(self, context, inputs):
        # Access context information
        info = {
            "context_type": type(context).__name__,
            "has_context": context is not None,
            "request_type": getattr(context, "request_type", "unknown")
        }
        return json.dumps(info)
```

### Example 4: Data Processing Action

```python
import json
from ceylonai_next import PyAction

class DataProcessingAction(PyAction):
    """Action that processes and transforms data"""

    def __init__(self):
        input_schema = json.dumps({
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {"type": "number"}
                },
                "operation": {
                    "type": "string",
                    "enum": ["sum", "average", "max", "min"]
                }
            },
            "required": ["data", "operation"]
        })
        super().__init__(
            name="process_data",
            description="Process numerical data",
            input_schema=input_schema
        )

    def execute(self, context, inputs):
        data = inputs.get("data", [])
        operation = inputs.get("operation")

        if not data:
            return json.dumps({"error": "No data provided"})

        try:
            if operation == "sum":
                result = sum(data)
            elif operation == "average":
                result = sum(data) / len(data)
            elif operation == "max":
                result = max(data)
            elif operation == "min":
                result = min(data)
            else:
                result = None

            return json.dumps({
                "operation": operation,
                "result": result,
                "data_count": len(data)
            })
        except Exception as e:
            return json.dumps({"error": str(e)})
```

### Example 5: Action with State

```python
import json
from ceylonai_next import PyAction

class StatefulAction(PyAction):
    """Action that maintains state across calls"""

    def __init__(self):
        super().__init__(
            name="counter",
            description="Increment a counter"
        )
        self.counter = 0

    def execute(self, context, inputs):
        operation = inputs.get("operation", "increment")
        amount = inputs.get("amount", 1)

        if operation == "increment":
            self.counter += amount
        elif operation == "decrement":
            self.counter -= amount
        elif operation == "reset":
            self.counter = 0
        elif operation == "get":
            pass  # Just return current value

        return json.dumps({
            "counter": self.counter,
            "operation": operation
        })
```

### Example 6: Using FunctionalAction Decorator

```python
from ceylonai_next import Agent
import json

class SmartAgent(Agent):
    def __init__(self):
        super().__init__("smart")

    @Agent.action(name="add", description="Add two numbers")
    def add_numbers(self, a: int, b: int) -> int:
        return a + b

    @Agent.action(description="Multiply two numbers together")
    def multiply(self, x: float, y: float) -> float:
        return x * y

    @Agent.action(name="greet", description="Greet a person")
    def say_hello(self, name: str) -> str:
        return f"Hello, {name}!"

# Usage
agent = SmartAgent()
# Agent can now use these actions
```

### Example 7: Complex Action with Multiple Inputs

```python
import json
from ceylonai_next import PyAction

class WebSearchAction(PyAction):
    """Simulated web search action"""

    def __init__(self):
        schema = json.dumps({
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "num_results": {"type": "integer", "minimum": 1, "maximum": 10},
                "language": {"type": "string", "default": "en"},
                "include_sources": {"type": "boolean"}
            },
            "required": ["query"]
        })
        super().__init__(
            name="web_search",
            description="Search the web for information",
            input_schema=schema
        )

    def execute(self, context, inputs):
        query = inputs.get("query", "")
        num_results = inputs.get("num_results", 5)
        language = inputs.get("language", "en")
        include_sources = inputs.get("include_sources", True)

        # Simulate search results
        results = [
            {
                "title": f"Result {i+1}",
                "url": f"https://example.com/{i+1}",
                "snippet": f"Information about {query}...",
                "source": "example.com"
            }
            for i in range(min(num_results, 5))
        ]

        response = {
            "query": query,
            "language": language,
            "results": results if include_sources else [r["snippet"] for r in results],
            "result_count": len(results)
        }

        return json.dumps(response)
```

## Best Practices

1. **Clear Names and Descriptions**
   ```python
   # Good
   PyAction("user_search", "Search for users by name or email")

   # Avoid
   PyAction("a", "search thing")
   ```

2. **Proper Schema Definition**
   ```python
   # Define schemas clearly
   schema = json.dumps({
       "type": "object",
       "properties": {
           "email": {"type": "string", "format": "email"},
           "limit": {"type": "integer", "minimum": 1}
       },
       "required": ["email"]
   })
   ```

3. **Error Handling**
   ```python
   def execute(self, context, inputs):
       try:
           # Process inputs
           result = do_something(inputs)
           return json.dumps({"success": True, "data": result})
       except ValueError as e:
           return json.dumps({"success": False, "error": str(e)})
   ```

4. **Return JSON**
   ```python
   # Always return JSON strings
   return json.dumps({"status": "ok", "value": result})
   # Not: return {"status": "ok"}
   ```

## Related APIs

- **[Agent](../core/agent.md)** - Agent that executes actions
- **[LlmAgent](../core/llm-agent.md)** - LLM agent with action support
- **[PyToolInvoker](./tool-invoker.md)** - Action registry and invoker

## See Also

- [Actions Guide](../../guide/actions.md)
- [Creating Custom Actions](../../guide/custom-actions.md)
- [Action Patterns](../../guide/action-patterns.md)
- [Action Examples](../../examples/action-examples.md)
