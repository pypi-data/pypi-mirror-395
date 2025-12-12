# Actions & Tools - Overview

Actions (also called tools) are one of Ceylon AI's most powerful features. They allow agents to perform specific tasks, interact with external systems, and extend their capabilities beyond text generation.

## What are Actions?

**Actions** are functions that agents can execute. They:

- Have clear names and descriptions
- Define input/output schemas
- Can be called by LLM agents automatically
- Are type-safe with automatic validation

## Quick Example

```python
from ceylonai_next import Agent

class WeatherAgent(Agent):
    @Agent.action(
        name="get_weather",
        description="Get current weather for a city"
    )
    def get_weather(self, city: str, units: str = "celsius") -> dict:
        """
        Fetch weather information for a specified city.

        Args:
            city: Name of the city
            units: Temperature units (celsius or fahrenheit)

        Returns:
            Dictionary with weather data
        """
        # In real implementation, call weather API
        return {
            "city": city,
            "temperature": 22,
            "units": units,
            "condition": "sunny"
        }
```

## Key Concepts

### 1. Action Decorator

The `@Agent.action()` decorator marks a method as an action:

```python
@Agent.action(
    name="action_name",           # Required: Unique identifier
    description="What it does"    # Required: For LLMs to understand
)
def my_action(self, param: str) -> str:
    return "result"
```

### 2. Automatic Schema Generation

Ceylon generates JSON schemas from type hints:

```python
def search(self, query: str, limit: int = 10, include_images: bool = False) -> list:
    """Search for items."""
    pass
```

Auto-generates:

```json
{
  "type": "object",
  "properties": {
    "query": {"type": "string"},
    "limit": {"type": "integer"},
    "include_images": {"type": "boolean"}
  },
  "required": ["query"]
}
```

### 3. Type Support

Supported Python types:

| Python Type | JSON Schema Type |
|-------------|------------------|
| `str` | `"string"` |
| `int` | `"integer"` |
| `float` | `"number"` |
| `bool` | `"boolean"` |
| `list` | `"array"` |
| `dict` | `"object"` |

## Action Registration

Actions are automatically registered when you use the decorator:

```python
class MyAgent(Agent):
    def __init__(self):
        super().__init__("my_agent")
        # Actions are registered during init

    @Agent.action(name="tool1", description="First tool")
    def tool1(self, param: str) -> str:
        return f"Tool1: {param}"

    @Agent.action(name="tool2", description="Second tool")
    def tool2(self, value: int) -> int:
        return value * 2

# Create agent - actions are automatically registered
agent = MyAgent()
```

## Using Actions with LLM Agents

### Method 1: Instance Decorator (Recommended)

The simplest way to add actions to an LLM agent is using the `@agent.action()` decorator:

```python
from ceylonai_next import LlmAgent

# Create LLM agent
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt(
    "You are a helpful assistant with access to tools. "
    "Use the available tools when appropriate to help users."
)

# Register actions using decorator
@agent.action(description="Get the current weather for a location")
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get weather information for a city."""
    # Mock weather data
    if "london" in location.lower():
        return f"Weather in {location}: Rainy, 15 degrees {unit}"
    elif "paris" in location.lower():
        return f"Weather in {location}: Sunny, 22 degrees {unit}"
    else:
        return f"Weather in {location}: Partly cloudy, 20 degrees {unit}"

@agent.action(description="Get information about the agent environment")
def get_agent_info(context) -> str:
    """Get information about the agent context."""
    return f"I am running on mesh: {context.mesh_name}"

# Build the agent
agent.build()

# LLM can now use the actions
response = agent.send_message("What's the weather in London?")
print(response)
```

**Key Features:**
- `name` parameter is optional (defaults to function name)
- `description` parameter is required for the LLM to understand the action
- Actions can optionally accept `context` as the first parameter
- Type hints are automatically converted to JSON schemas
- Actions are registered immediately when decorated

### Method 2: PyAction Class

For more complex actions, you can use the `PyAction` class:

```python
from ceylonai_next import LlmAgent, PyAction

# Create LLM agent
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt(
    "You are a helpful assistant with access to tools. "
    "Use the available tools when appropriate to help users."
)

# Register custom action
def get_time(context, inputs):
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

time_action = PyAction(
    "get_current_time",
    "Get the current time",
    '{"type": "object", "properties": {}}',
    None
)

agent.register_action(time_action)
agent.build()

# LLM can now use the action
response = agent.send_message("What time is it?")
print(response)
```

## Action Examples

### File Operations

```python
class FileAgent(Agent):
    @Agent.action(name="read_file", description="Read a text file")
    def read_file(self, filepath: str) -> str:
        """Read and return file contents."""
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"

    @Agent.action(name="write_file", description="Write to a text file")
    def write_file(self, filepath: str, content: str) -> str:
        """Write content to a file."""
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return f"Error: {e}"
```

### API Calls

```python
import requests

class APIAgent(Agent):
    @Agent.action(name="fetch_url", description="Fetch content from a URL")
    def fetch_url(self, url: str) -> dict:
        """
        Fetch content from a URL.

        Args:
            url: The URL to fetch

        Returns:
            Dictionary with status and content
        """
        try:
            response = requests.get(url, timeout=10)
            return {
                "status": response.status_code,
                "content": response.text[:1000],  # Limit size
                "success": response.ok
            }
        except Exception as e:
            return {
                "status": 0,
                "error": str(e),
                "success": False
            }
```

### Database Operations

```python
import sqlite3

class DatabaseAgent(Agent):
    def __init__(self, db_path):
        super().__init__("db_agent")
        self.db_path = db_path

    @Agent.action(name="query", description="Execute a SELECT query")
    def query(self, sql: str) -> list:
        """
        Execute a SELECT query and return results.

        Args:
            sql: The SQL SELECT query

        Returns:
            List of rows as dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            results = [dict(row) for row in cursor.fetchall()]
            return results
        finally:
            conn.close()
```

### Calculations

```python
class CalculatorAgent(Agent):
    @Agent.action(name="calculate", description="Evaluate a math expression")
    def calculate(self, expression: str) -> float:
        """
        Safely evaluate a mathematical expression.

        Args:
            expression: Math expression like "2 + 2" or "sin(3.14)"

        Returns:
            Result of the calculation
        """
        import ast
        import operator as op
        import math

        # Safe operators
        operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
        }

        def eval_expr(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                return operators[type(node.op)](
                    eval_expr(node.left),
                    eval_expr(node.right)
                )
            else:
                raise ValueError(f"Unsupported operation: {node}")

        try:
            node = ast.parse(expression, mode='eval')
            return eval_expr(node.body)
        except Exception as e:
            return f"Error: {e}"
```

## Best Practices

### 1. Clear Descriptions

```python
# Good
@Agent.action(
    name="search_products",
    description="Search for products in the catalog by name or category"
)

# Bad
@Agent.action(name="search", description="search")
```

### 2. Type Annotations

```python
# Good - enables automatic schema generation
def search(self, query: str, limit: int = 10) -> list:
    pass

# Bad - requires manual schema
def search(self, query, limit=10):
    pass
```

### 3. Error Handling

```python
@Agent.action(name="api_call", description="Call external API")
def api_call(self, endpoint: str) -> dict:
    try:
        result = call_api(endpoint)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### 4. Documentation

```python
@Agent.action(name="process", description="Process data")
def process(self, data: str, mode: str = "fast") -> dict:
    """
    Process input data with specified mode.

    Args:
        data: Input data to process
        mode: Processing mode - "fast" or "thorough"

    Returns:
        Dictionary with processed results

    Raises:
        ValueError: If mode is invalid
    """
    if mode not in ["fast", "thorough"]:
        raise ValueError(f"Invalid mode: {mode}")

    # Process data...
    return {"result": "processed"}
```

### 5. Idempotency

Actions should be idempotent when possible:

```python
@Agent.action(name="set_value", description="Set a configuration value")
def set_value(self, key: str, value: str) -> str:
    """Set a value - can be called multiple times safely."""
    self.config[key] = value  # Same result every time
    return f"Set {key} = {value}"
```

## Next Steps

- [LLM Agents](../agents/llm-agents.md) - Use actions with AI agents
- [Basic Agents](../agents/basic-agents.md) - Implement custom agent logic
- [Agents Overview](../agents/overview.md) - Agent fundamentals
- [Memory System](../memory/overview.md) - Add memory capabilities
- [Examples](../../examples/index.md) - Browse complete examples

## Common Patterns

### Action with Context

```python
@Agent.action(name="contexta action", description="Uses context")
def context_action(self, context, param: str) -> str:
    """Actions can access context if needed."""
    sender = context.sender if context else "unknown"
    return f"Received '{param}' from {sender}"
```

### Action with State

```python
class StatefulAgent(Agent):
    def __init__(self):
        super().__init__("stateful")
        self.counter = 0

    @Agent.action(name="increment", description="Increment counter")
    def increment(self, amount: int = 1) -> int:
        """Increment internal counter."""
        self.counter += amount
        return self.counter
```

### Async Actions

```python
import asyncio

class AsyncAgent(Agent):
    @Agent.action(name="async_task", description="Async operation")
    async def async_task(self, duration: int) -> str:
        """Perform an async operation."""
        await asyncio.sleep(duration)
        return f"Completed after {duration} seconds"
```
