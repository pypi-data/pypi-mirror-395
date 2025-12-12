# Async Best Practices

This guide covers practical patterns and best practices for writing robust, efficient asynchronous code with Ceylon AI.

## Architecture Patterns

### Pattern 1: Agent Pool

Reuse agents efficiently across many requests:

```python
import asyncio
from ceylonai_next import LlmAgent
from typing import List

class AgentPool:
    """Manage a pool of agents for concurrent requests."""

    def __init__(self, model: str, pool_size: int = 5):
        self.agents: List[LlmAgent] = []
        self.available = asyncio.Queue()

        # Create agents
        for i in range(pool_size):
            agent = LlmAgent(f"agent_{i}", model)
            agent.with_system_prompt("You are helpful.")
            agent.build()
            self.agents.append(agent)
            self.available.put_nowait(agent)

    async def query(self, message: str) -> str:
        """Query using an available agent."""
        # Get agent from pool
        agent = await self.available.get()

        try:
            # Use agent
            response = await agent.send_message_async(message)
            return response
        finally:
            # Return agent to pool
            await self.available.put(agent)

    async def batch_query(self, messages: list) -> list:
        """Query multiple messages concurrently."""
        tasks = [
            self.query(msg)
            for msg in messages
        ]
        return await asyncio.gather(*tasks)

# Usage
async def main():
    pool = AgentPool("ollama::llama3.2:latest", pool_size=3)

    messages = [f"Query {i}" for i in range(10)]
    responses = await pool.batch_query(messages)

    print(f"Processed {len(responses)} messages")

asyncio.run(main())
```

**Benefits:**
- Reuses agent instances efficiently
- Controls concurrency automatically
- Better resource management

### Pattern 2: Request Queue

Process requests from a queue with async workers:

```python
import asyncio
from ceylonai_next import LlmAgent
from dataclasses import dataclass

@dataclass
class Request:
    """Represent a request to process."""
    id: str
    message: str
    future: asyncio.Future = None

class AsyncWorker:
    """Process requests from a queue."""

    def __init__(self, agent_model: str, num_workers: int = 3):
        self.queue = asyncio.Queue()
        self.agent_model = agent_model
        self.num_workers = num_workers
        self.results = {}

    async def worker(self, worker_id: int):
        """Worker coroutine."""
        agent = LlmAgent(f"worker_{worker_id}", self.agent_model)
        agent.build()

        while True:
            request = await self.queue.get()

            try:
                response = await agent.send_message_async(request.message)
                self.results[request.id] = response
                request.future.set_result(response)
            except Exception as e:
                request.future.set_exception(e)
            finally:
                self.queue.task_done()

    async def start(self):
        """Start worker tasks."""
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.num_workers)
        ]

    async def submit(self, request_id: str, message: str) -> str:
        """Submit a request and wait for response."""
        future = asyncio.Future()
        request = Request(id=request_id, message=message, future=future)
        await self.queue.put(request)
        return await future

    async def shutdown(self):
        """Shutdown workers."""
        await self.queue.join()
        for worker in self.workers:
            worker.cancel()

# Usage
async def main():
    system = AsyncWorker("ollama::llama3.2:latest", num_workers=3)
    await system.start()

    # Submit requests
    tasks = [
        system.submit(f"req_{i}", f"Process {i}")
        for i in range(20)
    ]

    results = await asyncio.gather(*tasks)
    await system.shutdown()

    print(f"Completed {len(results)} requests")

asyncio.run(main())
```

**Benefits:**
- Decouples request submission from processing
- Handles backpressure automatically
- Scales to many requests

### Pattern 3: Pipeline Processing

Chain multiple async stages:

```python
import asyncio
from ceylonai_next import LlmAgent

class Pipeline:
    """Process data through multiple stages."""

    def __init__(self):
        self.validator = LlmAgent("validator", "ollama::llama3.2:latest")
        self.validator.with_system_prompt("Validate input format")
        self.validator.build()

        self.processor = LlmAgent("processor", "ollama::llama3.2:latest")
        self.processor.with_system_prompt("Process and analyze data")
        self.processor.build()

        self.analyzer = LlmAgent("analyzer", "ollama::llama3.2:latest")
        self.analyzer.with_system_prompt("Generate insights")
        self.analyzer.build()

    async def process(self, data: str) -> dict:
        """Process data through pipeline."""
        # Stage 1: Validate
        validation = await self.validator.send_message_async(
            f"Validate: {data}"
        )

        # Stage 2: Process
        processing = await self.processor.send_message_async(
            f"Process: {data}"
        )

        # Stage 3: Analyze
        analysis = await self.analyzer.send_message_async(
            f"Analyze: {processing}"
        )

        return {
            "validation": validation,
            "processing": processing,
            "analysis": analysis
        }

# Usage
async def main():
    pipeline = Pipeline()

    results = await asyncio.gather(*[
        pipeline.process(f"Data {i}")
        for i in range(10)
    ])

    print(f"Processed {len(results)} items through pipeline")

asyncio.run(main())
```

**Benefits:**
- Clear separation of concerns
- Easy to test each stage
- Can add/remove stages easily

## Error Handling Patterns

### Pattern 1: Retry with Exponential Backoff

```python
import asyncio
from ceylonai_next import LlmAgent

async def retry_with_backoff(
    agent: LlmAgent,
    message: str,
    max_retries: int = 3,
    initial_delay: float = 0.1
) -> str:
    """Retry operation with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await agent.send_message_async(message)
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff
            delay = initial_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
            await asyncio.sleep(delay)

# Usage
async def main():
    agent = LlmAgent("resilient", "ollama::llama3.2:latest")
    agent.build()

    try:
        response = await retry_with_backoff(agent, "Hello", max_retries=3)
        print(response)
    except Exception as e:
        print(f"Failed: {e}")

asyncio.run(main())
```

### Pattern 2: Fallback Strategy

```python
import asyncio
from ceylonai_next import LlmAgent

class FallbackAgent:
    """Try primary agent, fallback to secondary if needed."""

    def __init__(self, primary_model: str, secondary_model: str):
        self.primary = LlmAgent("primary", primary_model)
        self.primary.build()

        self.secondary = LlmAgent("secondary", secondary_model)
        self.secondary.build()

    async def query(self, message: str) -> str:
        """Query with fallback."""
        try:
            return await asyncio.wait_for(
                self.primary.send_message_async(message),
                timeout=5.0
            )
        except (asyncio.TimeoutError, Exception) as e:
            print(f"Primary failed: {e}, using secondary")
            try:
                return await self.secondary.send_message_async(message)
            except Exception as e2:
                return f"Both agents failed: {e2}"

# Usage
async def main():
    agent = FallbackAgent(
        "openai::gpt-4",
        "ollama::llama3.2:latest"
    )

    response = await agent.query("Explain AI")
    print(response)

asyncio.run(main())
```

### Pattern 3: Graceful Degradation

```python
import asyncio
from ceylonai_next import LlmAgent

async def process_with_fallback(
    agent: LlmAgent,
    message: str
) -> str:
    """Process with graceful fallback."""
    try:
        # Try full processing with timeout
        response = await asyncio.wait_for(
            agent.send_message_async(message),
            timeout=5.0
        )
        return response

    except asyncio.TimeoutError:
        # Timeout - return cached or default response
        return f"[Cached Response] Processing {message}"

    except Exception as e:
        # Other error - return fallback
        return f"[Fallback Response] Request failed: {e}"

# Usage
async def main():
    agent = LlmAgent("app", "ollama::llama3.2:latest")
    agent.build()

    responses = await asyncio.gather(*[
        process_with_fallback(agent, f"Query {i}")
        for i in range(10)
    ])

    print(f"Got {len(responses)} responses")

asyncio.run(main())
```

## Performance Optimization

### Pattern 1: Adaptive Concurrency

```python
import asyncio
import time
from ceylonai_next import LlmAgent

class AdaptiveConcurrency:
    """Automatically adjust concurrency based on performance."""

    def __init__(self, agent: LlmAgent):
        self.agent = agent
        self.current_concurrency = 2
        self.max_concurrency = 10
        self.min_concurrency = 1

    async def process_batch(self, messages: list) -> list:
        """Process with adaptive concurrency."""
        results = []

        for i in range(0, len(messages), self.current_concurrency):
            batch = messages[i:i + self.current_concurrency]

            start = time.time()

            # Process batch
            responses = await asyncio.gather(*[
                self.agent.send_message_async(msg)
                for msg in batch
            ])

            elapsed = time.time() - start

            # Adjust concurrency based on performance
            avg_time = elapsed / len(batch)

            if avg_time < 0.5:  # Fast - increase concurrency
                self.current_concurrency = min(
                    self.current_concurrency + 1,
                    self.max_concurrency
                )
            elif avg_time > 2.0:  # Slow - decrease concurrency
                self.current_concurrency = max(
                    self.current_concurrency - 1,
                    self.min_concurrency
                )

            results.extend(responses)

        return results

# Usage
async def main():
    agent = LlmAgent("adaptive", "ollama::llama3.2:latest")
    agent.build()

    adaptive = AdaptiveConcurrency(agent)

    messages = [f"Message {i}" for i in range(100)]
    results = await adaptive.process_batch(messages)

    print(f"Processed {len(results)} messages")

asyncio.run(main())
```

### Pattern 2: Caching with TTL

```python
import asyncio
import time
from ceylonai_next import LlmAgent
from typing import Optional

class CachedAgent:
    """Agent with TTL-based caching."""

    def __init__(self, agent: LlmAgent, ttl: float = 300.0):
        self.agent = agent
        self.ttl = ttl
        self.cache = {}
        self.timestamps = {}

    async def query(self, message: str) -> str:
        """Query with caching."""
        # Check cache
        if message in self.cache:
            timestamp = self.timestamps[message]
            if time.time() - timestamp < self.ttl:
                return self.cache[message]
            else:
                # Expired
                del self.cache[message]
                del self.timestamps[message]

        # Call agent
        response = await self.agent.send_message_async(message)

        # Cache result
        self.cache[message] = response
        self.timestamps[message] = time.time()

        return response

    def clear_cache(self):
        """Clear all cache."""
        self.cache.clear()
        self.timestamps.clear()

# Usage
async def main():
    agent = LlmAgent("cached", "ollama::llama3.2:latest")
    agent.build()

    cached = CachedAgent(agent, ttl=60.0)

    # Same query twice - second from cache
    response1 = await cached.query("What is Python?")
    response2 = await cached.query("What is Python?")  # From cache

    print("Responses identical:", response1 == response2)

asyncio.run(main())
```

## Monitoring and Observability

### Pattern 1: Metrics Collection

```python
import asyncio
import time
from ceylonai_next import LlmAgent
from dataclasses import dataclass
from typing import Dict

@dataclass
class Metrics:
    """Collect performance metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0

class MonitoredAgent:
    """Agent with metrics collection."""

    def __init__(self, agent: LlmAgent):
        self.agent = agent
        self.metrics = Metrics()

    async def query(self, message: str) -> str:
        """Query with metrics."""
        start = time.time()
        self.metrics.total_requests += 1

        try:
            response = await self.agent.send_message_async(message)
            self.metrics.successful_requests += 1
            return response

        except Exception as e:
            self.metrics.failed_requests += 1
            raise

        finally:
            elapsed = time.time() - start
            self.metrics.total_time += elapsed
            self.metrics.min_time = min(self.metrics.min_time, elapsed)
            self.metrics.max_time = max(self.metrics.max_time, elapsed)

    def get_stats(self) -> dict:
        """Get performance statistics."""
        avg_time = (
            self.metrics.total_time / self.metrics.total_requests
            if self.metrics.total_requests > 0
            else 0
        )

        return {
            "total_requests": self.metrics.total_requests,
            "successful": self.metrics.successful_requests,
            "failed": self.metrics.failed_requests,
            "avg_time": avg_time,
            "min_time": self.metrics.min_time,
            "max_time": self.metrics.max_time
        }

# Usage
async def main():
    agent = LlmAgent("monitored", "ollama::llama3.2:latest")
    agent.build()

    monitored = MonitoredAgent(agent)

    # Process messages
    for i in range(10):
        await monitored.query(f"Query {i}")

    stats = monitored.get_stats()
    print(f"Stats: {stats}")

asyncio.run(main())
```

## Testing Patterns

### Pattern 1: Mock Agent for Testing

```python
import asyncio
from unittest.mock import AsyncMock

class MockAgent:
    """Mock agent for testing."""

    def __init__(self, responses: dict = None):
        self.responses = responses or {}
        self.call_count = 0

    async def send_message_async(self, message: str) -> str:
        """Return predefined response."""
        self.call_count += 1
        return self.responses.get(message, "Default response")

# Test
async def test_with_mock():
    mock = MockAgent({
        "What is AI?": "AI is artificial intelligence",
        "What is ML?": "ML is machine learning"
    })

    response = await mock.send_message_async("What is AI?")
    assert response == "AI is artificial intelligence"
    assert mock.call_count == 1

asyncio.run(test_with_mock())
```

### Pattern 2: Fixture-Based Testing

```python
import pytest
import asyncio
from ceylonai_next import LlmAgent

@pytest.fixture
async def agent():
    """Create test agent."""
    agent = LlmAgent("test_agent", "ollama::llama3.2:latest")
    agent.build()
    yield agent
    # Cleanup
    del agent

@pytest.mark.asyncio
async def test_agent_response(agent):
    """Test agent response."""
    response = await agent.send_message_async("Hello")
    assert response is not None
    assert len(response) > 0

@pytest.mark.asyncio
async def test_concurrent_queries(agent):
    """Test concurrent queries."""
    responses = await asyncio.gather(*[
        agent.send_message_async(f"Query {i}")
        for i in range(5)
    ])
    assert len(responses) == 5
```

## Common Pitfalls and Solutions

### Pitfall 1: Not Awaiting Coroutines

```python
# Bad - coroutine is not awaited
async def bad():
    agent = LlmAgent("agent", "ollama::llama3.2:latest")
    agent.send_message_async("Hello")  # Not awaited!

# Good - coroutine is awaited
async def good():
    agent = LlmAgent("agent", "ollama::llama3.2:latest")
    response = await agent.send_message_async("Hello")
    return response
```

### Pitfall 2: Creating Multiple Event Loops

```python
# Bad - creates multiple event loops
for i in range(10):
    asyncio.run(agent.send_message_async("Message"))

# Good - single event loop
async def main():
    for i in range(10):
        await agent.send_message_async("Message")

asyncio.run(main())
```

### Pitfall 3: Blocking Operations in Async Code

```python
import asyncio
import time

# Bad - blocks event loop
async def bad():
    time.sleep(5)  # Blocks!
    return "Done"

# Good - non-blocking
async def good():
    await asyncio.sleep(5)  # Non-blocking
    return "Done"

asyncio.run(good())
```

### Pitfall 4: Uncaught Exceptions in Tasks

```python
# Bad - exception is lost
async def bad():
    task = asyncio.create_task(failing_coro())
    # Task might fail but we don't know

# Good - wait for task and handle exceptions
async def good():
    task = asyncio.create_task(failing_coro())
    try:
        result = await task
    except Exception as e:
        print(f"Task failed: {e}")
```

### Pitfall 5: Resource Leaks

```python
# Bad - agents not cleaned up
async def bad():
    agents = [
        LlmAgent(f"agent_{i}", "ollama::llama3.2:latest")
        for i in range(1000)
    ]
    # Memory leak!

# Good - proper resource management
async def good():
    agents = [
        LlmAgent(f"agent_{i}", "ollama::llama3.2:latest")
        for i in range(10)  # Reasonable number
    ]

    try:
        # Use agents
        pass
    finally:
        # Cleanup
        for agent in agents:
            del agent
```

## Debugging Async Code

### Enable Debug Logging

```python
import logging
import asyncio

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Run with debug
asyncio.run(main(), debug=True)
```

### Monitor Task Status

```python
import asyncio

async def monitor_tasks():
    """Monitor all running tasks."""
    while True:
        tasks = asyncio.all_tasks()
        print(f"Active tasks: {len(tasks)}")

        for task in tasks:
            print(f"  - {task.get_name()}: {task._state}")

        await asyncio.sleep(1)
```

## Best Practices Summary

1. **Always await coroutines** - Don't forget `await`
2. **Reuse agent instances** - Create once, use many times
3. **Set timeouts** - Prevent hanging indefinitely
4. **Handle exceptions** - Use try-except or `return_exceptions=True`
5. **Limit concurrency** - Don't overwhelm the system
6. **Use connection pooling** - For database/API access
7. **Monitor performance** - Track metrics and adjust
8. **Test async code** - Use `pytest-asyncio`
9. **Document assumptions** - Comment about async behavior
10. **Profile your code** - Find bottlenecks

## Next Steps

- [Async Overview](overview.md) - Async fundamentals
- [LLM Agents](../agents/llm-agents.md) - Agent configuration
- [Mesh](../mesh/overview.md) - Multi-agent systems
