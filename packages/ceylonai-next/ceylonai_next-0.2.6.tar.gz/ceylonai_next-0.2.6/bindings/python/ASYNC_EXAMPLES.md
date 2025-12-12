# Ceylon Async Examples

This document describes the async examples available in the Ceylon Python bindings.

## Overview

Ceylon provides async functionality for LLM operations through the `send_message_async()` method on `LlmAgent`. This allows you to process multiple LLM queries concurrently, improving performance for batch operations.

## Available Examples

### 1. `examples/demo_async_llm.py` - Concurrent LLM Operations

**Purpose**: Demonstrates working async functionality with concurrent LLM message processing.

**What it covers**:
- ✅ Concurrent queries with `asyncio.gather()`
- ✅ Streaming responses with `asyncio.as_completed()`
- ✅ Batch processing with concurrency control
- ✅ Error handling in async contexts

**How to run**:
```bash
cd bindings/python
python examples/demo_async_llm.py
```

**Requirements**:
- Ollama must be running locally
- The `gemma3:latest` model must be available (or change the model in the script)

**Key demonstrations**:

#### Demo 1: Concurrent Queries
Sends multiple questions to the LLM simultaneously and waits for all responses using `asyncio.gather()`.

```python
tasks = [agent.send_message_async(q) for q in questions]
responses = await asyncio.gather(*tasks)
```

#### Demo 2: Streaming Responses
Processes LLM responses as they complete using `asyncio.as_completed()`, useful for displaying results progressively.

```python
for coro in asyncio.as_completed(tasks.keys()):
    response = await coro
    # Display response immediately
```

#### Demo 3: Batch Processing
Shows how to process large numbers of queries with concurrency limits to avoid overwhelming the LLM.

```python
for i in range(0, len(queries), batch_size):
    batch = queries[i:i + batch_size]
    results = await asyncio.gather(*[agent.send_message_async(q) for q in batch])
```

#### Demo 4: Error Handling
Demonstrates proper error handling in async contexts.

```python
try:
    response = await agent.send_message_async(query)
except Exception as e:
    # Handle errors gracefully
```

---

### 2. `examples/demo_async_agent.py` - Async Agent Message Handling

**Purpose**: Demonstrates async message handlers and actions on custom agents.

**Status**: ⚠️ Currently has event loop compatibility issues between Tokio (Rust) and asyncio (Python).

**What it attempts to cover**:
- Async `on_message()` handlers
- Async action execution
- Async message processing

**Note**: This example may encounter "no running event loop" errors due to event loop incompatibility. Refer to `ASYNC_STATUS.md` for details.

---

## Working vs. Non-Working Async Features

### ✅ What Works (Reliable)

1. **`send_message_async()` on `LlmAgent`**
   - Fully functional and production-ready
   - Supports concurrent execution with asyncio
   - Proper error propagation
   - Example: `examples/demo_async_llm.py`

2. **Basic async infrastructure**
   - Can use asyncio patterns in your code
   - Python-side async works as expected

### ⚠️ What Doesn't Work Yet

1. **Async `on_message()` handlers**
   - Event loop compatibility issue
   - Root cause: Tokio (Rust) vs asyncio (Python) incompatibility
   - Workaround: Use synchronous handlers

2. **Async actions with mesh integration**
   - Limited support
   - May work in some contexts but not well-integrated

For full details, see `ASYNC_STATUS.md`.

---

## Best Practices

### 1. Use `send_message_async()` for LLM operations

```python
# ✅ Good - works reliably
agent = ceylon.LlmAgent("agent", "ollama::model")
agent.build()
response = await agent.send_message_async("query")
```

### 2. Leverage `asyncio.gather()` for concurrent operations

```python
# ✅ Good - process multiple queries concurrently
tasks = [agent.send_message_async(q) for q in queries]
results = await asyncio.gather(*tasks)
```

### 3. Use synchronous handlers for custom agents

```python
# ✅ Good - use sync handler (works)
class MyAgent(Agent):
    def on_message(self, message, context=None):
        # Synchronous processing
        return "response"

# ❌ Avoid - async handler has event loop issues
class MyAgent(Agent):
    async def on_message(self, message, context=None):
        # May cause "no running event loop" error
        return "response"
```

### 4. Handle errors with `return_exceptions=True`

```python
# ✅ Good - graceful error handling
results = await asyncio.gather(*tasks, return_exceptions=True)
for result in results:
    if isinstance(result, Exception):
        print(f"Error: {result}")
    else:
        print(f"Success: {result}")
```

### 5. Control concurrency for large batches

```python
# ✅ Good - process in batches to avoid overwhelming the LLM
batch_size = 5
for i in range(0, len(queries), batch_size):
    batch = queries[i:i + batch_size]
    results = await asyncio.gather(*[agent.send_message_async(q) for q in batch])
```

---

## Performance Tips

1. **Concurrent queries** can significantly improve throughput:
   - Sequential: `n * avg_time`
   - Concurrent: `~avg_time` (limited by LLM backend)

2. **Batch size** should match your LLM backend capacity:
   - Too small: underutilized
   - Too large: may overwhelm the backend or hit rate limits

3. **Use `as_completed()`** for progressive results:
   - Better user experience with streaming output
   - Can start processing results while others are pending

---

## Troubleshooting

### "No running event loop" error

**Cause**: Tokio (Rust) and asyncio (Python) event loop incompatibility.

**Solution**: Use `send_message_async()` on LlmAgent instead of async message handlers.

### "Connection refused" when running examples

**Cause**: Ollama is not running.

**Solution**:
```bash
# Start Ollama
ollama serve

# Pull the model
ollama pull gemma3:latest
```

### Slow performance with concurrent queries

**Cause**: LLM backend may be processing queries sequentially.

**Solution**: Check your LLM backend configuration. Some backends have concurrency limits.

---

## Contributing

When adding new async examples:

1. Focus on the **working** async APIs (`send_message_async()`)
2. Include clear error handling
3. Document any limitations or known issues
4. Add performance measurements where relevant
5. Follow the existing example structure and style

---

## Related Documentation

- `ASYNC_STATUS.md` - Detailed status of async features
- `demo_conversation.py` - Synchronous LLM conversation example
- `demo_simple_agent.py` - Synchronous agent example
- Ceylon docs: `/home/user/next-processor/docs/`
