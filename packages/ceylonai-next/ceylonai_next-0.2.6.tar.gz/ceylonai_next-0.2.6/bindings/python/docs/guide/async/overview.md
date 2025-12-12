# Async Operations - Overview

Ceylon AI provides comprehensive async/await support for building high-performance, concurrent applications. This guide covers async patterns, best practices, and what works in the current implementation.

## What is Async?

**Asynchronous programming** allows you to:

- Process multiple operations concurrently
- Avoid blocking on I/O or slow operations
- Build responsive, high-throughput applications
- Efficiently use system resources

```python
import asyncio
from ceylonai_next import LlmAgent

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    # Non-blocking message
    response = await agent.send_message_async("What is Python?")
    print(response)

asyncio.run(main())
```

## Async with LLM Agents

### Single Async Query

```python
import asyncio
from ceylonai_next import LlmAgent

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.with_system_prompt("You are helpful.")
    agent.build()

    # Send message asynchronously
    response = await agent.send_message_async("Explain Python")
    print(response)

asyncio.run(main())
```

### Concurrent Queries

Send multiple messages concurrently using `asyncio.gather()`:

```python
import asyncio
from ceylonai_next import LlmAgent

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.with_system_prompt("You are helpful.")
    agent.build()

    questions = [
        "What is Python?",
        "What is Rust?",
        "What is AI?"
    ]

    # Send all questions concurrently
    tasks = [
        agent.send_message_async(q)
        for q in questions
    ]

    responses = await asyncio.gather(*tasks)

    # Display results
    for q, r in zip(questions, responses):
        print(f"Q: {q}")
        print(f"A: {r}\n")

asyncio.run(main())
```

**Performance benefit:** All questions sent simultaneously, not sequentially.

## Async Patterns

### Pattern 1: Batch Processing

Process large numbers of items with concurrency control:

```python
import asyncio
from ceylonai_next import LlmAgent

async def batch_process(agent: LlmAgent, items: list, batch_size: int = 5):
    """Process items in batches."""
    results = []

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1}...")

        # Process batch concurrently
        tasks = [
            agent.send_message_async(item)
            for item in batch
        ]

        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)

    return results

async def main():
    agent = LlmAgent("processor", "ollama::llama3.2:latest")
    agent.build()

    items = [f"Process item {i}" for i in range(100)]

    results = await batch_process(agent, items, batch_size=10)
    print(f"Processed {len(results)} items")

asyncio.run(main())
```

### Pattern 2: Progress Tracking

Monitor progress as tasks complete:

```python
import asyncio
from ceylonai_next import LlmAgent

async def process_with_progress(agent: LlmAgent, items: list):
    """Process items and track progress."""
    tasks = {
        asyncio.create_task(agent.send_message_async(item)): item
        for item in items
    }

    results = []

    # Process tasks as they complete
    for future in asyncio.as_completed(tasks):
        item = tasks[future]
        try:
            result = await future
            results.append(result)
            print(f"✓ Completed: {item[:50]}...")
        except Exception as e:
            print(f"✗ Failed: {item[:50]}... - {e}")

    return results

async def main():
    agent = LlmAgent("processor", "ollama::llama3.2:latest")
    agent.build()

    items = [f"Process {i}" for i in range(10)]

    results = await process_with_progress(agent, items)
    print(f"Completed {len(results)} items")

asyncio.run(main())
```

### Pattern 3: Error Handling

Handle errors gracefully in async operations:

```python
import asyncio
from ceylonai_next import LlmAgent

async def robust_query(agent: LlmAgent, message: str, retries: int = 3):
    """Query with automatic retry on failure."""
    for attempt in range(retries):
        try:
            response = await agent.send_message_async(message)
            return response
        except Exception as e:
            if attempt == retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed, retrying...")
            await asyncio.sleep(0.1 * (attempt + 1))  # Exponential backoff

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    try:
        response = await robust_query(agent, "Hello", retries=3)
        print(response)
    except Exception as e:
        print(f"Failed after retries: {e}")

asyncio.run(main())
```

### Pattern 4: Timeout Handling

Add timeouts to prevent hanging:

```python
import asyncio
from ceylonai_next import LlmAgent

async def query_with_timeout(agent: LlmAgent, message: str, timeout: float = 10.0):
    """Send message with timeout."""
    try:
        response = await asyncio.wait_for(
            agent.send_message_async(message),
            timeout=timeout
        )
        return response
    except asyncio.TimeoutError:
        return "Request timed out after {timeout}s"

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    response = await query_with_timeout(agent, "Hello", timeout=5.0)
    print(response)

asyncio.run(main())
```

### Pattern 5: Rate Limiting

Control request rate to avoid overwhelming services:

```python
import asyncio
from ceylonai_next import LlmAgent

async def rate_limited_queries(agent: LlmAgent, messages: list, max_concurrent: int = 3):
    """Process messages with rate limiting."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_query(msg):
        async with semaphore:
            return await agent.send_message_async(msg)

    tasks = [limited_query(msg) for msg in messages]
    return await asyncio.gather(*tasks)

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    messages = [f"Message {i}" for i in range(10)]

    # Only 3 concurrent requests
    responses = await rate_limited_queries(agent, messages, max_concurrent=3)
    print(f"Got {len(responses)} responses")

asyncio.run(main())
```

### Pattern 6: Concurrent Agent Communication

```python
import asyncio
from ceylonai_next import LlmAgent

async def multi_agent_query():
    """Query multiple agents concurrently."""
    # Create agents
    python_expert = LlmAgent("python_expert", "ollama::llama3.2:latest")
    python_expert.with_system_prompt("You are a Python expert.")
    python_expert.build()

    rust_expert = LlmAgent("rust_expert", "ollama::llama3.2:latest")
    rust_expert.with_system_prompt("You are a Rust expert.")
    rust_expert.build()

    js_expert = LlmAgent("js_expert", "ollama::llama3.2:latest")
    js_expert.with_system_prompt("You are a JavaScript expert.")
    js_expert.build()

    # Query all concurrently
    responses = await asyncio.gather(
        python_expert.send_message_async("Explain decorators"),
        rust_expert.send_message_async("Explain ownership"),
        js_expert.send_message_async("Explain closures")
    )

    return responses

asyncio.run(multi_agent_query())
```

## Async Context Managers

Use async context managers for resource management:

```python
import asyncio
from ceylonai_next import LlmAgent

class AsyncAgent:
    def __init__(self, name: str, model: str):
        self.agent = LlmAgent(name, model)
        self.agent.build()

    async def __aenter__(self):
        """Setup on entry."""
        print(f"Initializing {self.agent.name()}")
        return self.agent

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup on exit."""
        print(f"Cleaning up {self.agent.name()}")
        # Perform cleanup
        return False

async def main():
    async with AsyncAgent("assistant", "ollama::llama3.2:latest") as agent:
        response = await agent.send_message_async("Hello")
        print(response)

asyncio.run(main())
```

## Performance Considerations

### Concurrency vs Sequential

```python
import asyncio
import time
from ceylonai_next import LlmAgent

async def sequential():
    """Process messages one at a time."""
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    questions = ["Q1", "Q2", "Q3"]

    start = time.time()
    for q in questions:
        await agent.send_message_async(q)
    elapsed = time.time() - start

    print(f"Sequential: {elapsed:.2f}s")

async def concurrent():
    """Process messages concurrently."""
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    questions = ["Q1", "Q2", "Q3"]

    start = time.time()
    await asyncio.gather(*[
        agent.send_message_async(q)
        for q in questions
    ])
    elapsed = time.time() - start

    print(f"Concurrent: {elapsed:.2f}s")

# Run both
asyncio.run(sequential())    # Takes 3 * response_time
asyncio.run(concurrent())    # Takes ~1 * response_time
```

**Result:** Concurrent processing is much faster for multiple independent operations.

## Known Limitations and Workarounds

### Async Message Handlers

**Status:** Limited support

The `on_message_async()` method has event loop compatibility issues between Tokio (Rust) and asyncio (Python).

**Workaround:** Use synchronous handlers:

```python
from ceylonai_next import Agent

class MyAgent(Agent):
    # Good: Synchronous handler (works reliably)
    def on_message(self, message: str, context=None) -> str:
        return f"Handled: {message}"

    # Problematic: Async handler may cause issues
    # async def on_message_async(self, message: str, context=None) -> str:
    #     return f"Handled: {message}"
```

### Async Actions

**Status:** Limited support in mesh contexts

Async actions work for `LlmAgent.send_message_async()` but have limitations with mesh integration.

**Workaround:** Use synchronous actions or move async logic to the handler:

```python
from ceylonai_next import Agent

class MyAgent(Agent):
    # Good: Synchronous action
    @Agent.action(name="get_data", description="Get data")
    def get_data(self, key: str) -> str:
        return "data"

    # Avoid in mesh: Async action
    # @Agent.action(name="async_get", description="Get async")
    # async def async_get(self, key: str) -> str:
    #     return "data"
```

## Async with Web Frameworks

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from ceylonai_next import LlmAgent
import asyncio

app = FastAPI()

# Create agent (shared across requests)
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are helpful.")
agent.build()

@app.post("/chat")
async def chat(message: str):
    """Chat endpoint."""
    try:
        response = await agent.send_message_async(message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch")
async def batch_chat(messages: list):
    """Process multiple messages."""
    try:
        responses = await asyncio.gather(*[
            agent.send_message_async(msg)
            for msg in messages
        ])
        return {"responses": responses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Aiohttp Integration

```python
import asyncio
from aiohttp import web
from ceylonai_next import LlmAgent

async def init_app():
    app = web.Application()

    # Initialize agent
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()
    app['agent'] = agent

    # Routes
    app.router.add_post('/chat', chat_handler)

    return app

async def chat_handler(request):
    """Handle chat requests."""
    agent = request.app['agent']

    try:
        data = await request.json()
        message = data.get('message')

        response = await agent.send_message_async(message)

        return web.json_response({'response': response})
    except Exception as e:
        return web.json_response(
            {'error': str(e)},
            status=500
        )

if __name__ == '__main__':
    app = asyncio.run(init_app())
    web.run_app(app, port=8080)
```

## Testing Async Code

### Unit Testing with pytest

```python
import pytest
import asyncio
from ceylonai_next import LlmAgent

@pytest.mark.asyncio
async def test_async_message():
    agent = LlmAgent("test", "ollama::llama3.2:latest")
    agent.build()

    response = await agent.send_message_async("test")
    assert response is not None

@pytest.mark.asyncio
async def test_concurrent_messages():
    agent = LlmAgent("test", "ollama::llama3.2:latest")
    agent.build()

    responses = await asyncio.gather(*[
        agent.send_message_async(f"msg{i}")
        for i in range(3)
    ])

    assert len(responses) == 3
```

## Best Practices

### 1. Use Async for I/O-Bound Operations

```python
# Good: Multiple I/O operations concurrently
async def get_multiple_responses(agent, queries):
    return await asyncio.gather(*[
        agent.send_message_async(q) for q in queries
    ])

# Avoid: Sequential I/O
for query in queries:
    response = agent.send_message(query)  # Blocks
```

### 2. Reuse Agent Instances

```python
# Good: Create once, use multiple times
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.build()

responses = await asyncio.gather(*[
    agent.send_message_async(q) for q in queries
])

# Avoid: Creating new agent for each query
```

### 3. Handle Exceptions Properly

```python
# Good: Handle exceptions in gather
responses = await asyncio.gather(
    *[agent.send_message_async(q) for q in queries],
    return_exceptions=True  # Returns exceptions instead of raising
)

# Process results, some may be exceptions
for i, response in enumerate(responses):
    if isinstance(response, Exception):
        print(f"Query {i} failed: {response}")
    else:
        print(f"Query {i}: {response}")
```

### 4. Use Appropriate Concurrency

```python
# Good: Limit concurrency to avoid overwhelming system
semaphore = asyncio.Semaphore(5)

async def limited_query(agent, msg):
    async with semaphore:
        return await agent.send_message_async(msg)

responses = await asyncio.gather(*[
    limited_query(agent, msg) for msg in messages
])
```

### 5. Set Timeouts

```python
# Good: Always set timeouts on potentially slow operations
try:
    response = await asyncio.wait_for(
        agent.send_message_async(message),
        timeout=10.0
    )
except asyncio.TimeoutError:
    print("Operation timed out")
```

## Debugging Async Code

### Enable Debug Logging

```python
import logging
import asyncio

# Enable asyncio debug mode
logging.basicConfig(level=logging.DEBUG)

# Run with debug
asyncio.run(main(), debug=True)
```

### Track Task Status

```python
import asyncio
from ceylonai_next import LlmAgent

async def debug_concurrent():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    queries = ["Q1", "Q2", "Q3"]

    # Create tasks
    tasks = [
        asyncio.create_task(agent.send_message_async(q))
        for q in queries
    ]

    # Monitor completion
    for future in asyncio.as_completed(tasks):
        try:
            result = await future
            print(f"Completed: {result[:50]}...")
        except Exception as e:
            print(f"Failed: {e}")
```

## Next Steps

- [Async Best Practices](best-practices.md) - Deep dive into async patterns
- [LLM Agents](../agents/llm-agents.md) - Agent configuration
- [Agents](../agents/overview.md) - Agent fundamentals
- [Mesh](../mesh/overview.md) - Multi-agent systems
