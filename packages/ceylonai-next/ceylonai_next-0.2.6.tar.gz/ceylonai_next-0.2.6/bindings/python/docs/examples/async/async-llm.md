# Async LLM Operations Example

## Overview

This example demonstrates **concurrent and asynchronous LLM operations** using Python's `asyncio` framework. You'll learn how to send multiple messages to language models simultaneously, process queries as they complete, and manage batch operations efficiently.

This is essential for building scalable applications that handle multiple requests without blocking.

## What You'll Learn

- **Async Programming Basics**: Understanding Python's asyncio event loop
- **Concurrent Queries**: Sending multiple LLM requests simultaneously
- **Gathering Results**: Using `asyncio.gather()` to wait for multiple operations
- **Streaming Responses**: Processing results as they complete with `asyncio.as_completed()`
- **Batch Processing**: Managing large numbers of queries efficiently
- **Error Handling**: Gracefully handling failures in async contexts

## Prerequisites

Before starting, make sure you have:

- Python 3.7+ (asyncio is built-in)
- Ceylon SDK with async support: `pip install ceylon`
- Ollama or other LLM provider set up
- Basic understanding of Python async/await syntax
- Familiarity with the synchronous LLM agent example

### Required Knowledge

If you're new to asyncio, here are the key concepts:

- **`async def`**: Defines an asynchronous function (coroutine)
- **`await`**: Waits for an async operation to complete
- **`asyncio.gather()`**: Run multiple coroutines concurrently
- **`asyncio.run()`**: Entry point for running async code
- **`asyncio.as_completed()`**: Process results as they arrive

## Step-by-Step Guide

### Step 1: Understand Async vs Sync

**Synchronous (Blocking)**:
```
Query 1 ────────────────────► Response 1 (5s)
Query 2 (blocked, waiting)
Query 2 ────────────────────► Response 2 (5s)
Query 3 (blocked, waiting)
Query 3 ────────────────────► Response 3 (5s)
Total time: 15 seconds
```

**Asynchronous (Concurrent)**:
```
Query 1 ────────────────────► Response 1 (5s)
Query 2 ────────────────────► Response 2 (5s)
Query 3 ────────────────────► Response 3 (5s)
Total time: 5 seconds (all run together!)
```

Async allows your program to do other things while waiting for I/O (like network calls).

### Step 2: Create an Async Function

```python
async def demo_concurrent_queries():
    """Demo showing concurrent LLM queries"""
    print("Running concurrent demo...")

    # Your async code here
    await some_async_operation()
```

Breaking it down:

- **`async def`**: Marks the function as asynchronous
- **`await`**: Pauses execution until an async operation completes
- Can only use `await` inside `async` functions

### Step 3: Create an LLM Agent

```python
agent = ceylon.LlmAgent("concurrent_agent", "ollama::gemma3:latest")
agent.with_system_prompt("You are a helpful assistant. Be very concise.")
agent.with_temperature(0.7)
agent.with_max_tokens(50)
agent.build()
```

This is the same as synchronous setup. The difference comes in how we call it.

### Step 4: Send Concurrent Messages

```python
questions = [
    "What is 2+2?",
    "What is the capital of France?",
    "What color is the sky?",
]

# Create async tasks for each question
tasks = [agent.send_message_async(q) for q in questions]

# Wait for all to complete and gather results
responses = await asyncio.gather(*tasks, return_exceptions=True)
```

What's happening:

- **`send_message_async(q)`**: Async version of `send_message()`
- **`[... for q in questions]`**: List comprehension creates tasks
- **`asyncio.gather(*tasks)`**: Wait for all tasks to complete
- **`return_exceptions=True`**: Return errors instead of raising them

### Step 5: Process Results As They Arrive

```python
# Create tasks with labels
tasks = []
for label, question in questions:
    task = asyncio.create_task(agent.send_message_async(question))
    task.label = label  # Attach metadata
    task.question = question
    tasks.append(task)

# Process as they complete
while pending:
    done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

    for task in done:
        response = await task
        print(f"✓ {task.label}: {response}")
```

This shows results immediately as they're ready, without waiting for all to complete.

### Step 6: Batch Processing

```python
batch_size = 3
for i in range(0, len(queries), batch_size):
    batch = queries[i:i + batch_size]

    # Process batch concurrently
    tasks = [agent.send_message_async(q) for q in batch]
    results = await asyncio.gather(*tasks, return_exceptions=True)
```

Useful for:
- Limiting concurrent requests to avoid overwhelming the server
- Processing large datasets in chunks
- Rate limiting

### Step 7: Run Async Code

```python
if __name__ == "__main__":
    exit_code = asyncio.run(demo_concurrent_queries())
    exit(exit_code)
```

`asyncio.run()` is the entry point - it:
- Creates an event loop
- Runs your async function
- Cleans up the loop

## Complete Code with Inline Comments

```python
#!/usr/bin/env python3
"""
Async LLM Demo - demonstrates concurrent LLM operations using send_message_async()

This example showcases key async functionality:
- Concurrent LLM message processing using asyncio.gather()
- Batch query processing with concurrency control
- Streaming responses with asyncio.as_completed()
- Error handling in async contexts
"""
import asyncio
import time
from typing import List, Tuple
import ceylon


async def demo_concurrent_queries():
    """
    Demo 1: Send multiple queries concurrently and wait for all.

    This is the most common async pattern - fire off multiple tasks
    and wait for all to complete before continuing.
    """
    print("=" * 60)
    print("Demo 1: Concurrent LLM Queries with asyncio.gather()")
    print("=" * 60)

    # Step 1: Create and configure LLM agent
    print("\n1. Creating LLM agent with gemma3:latest...")
    agent = ceylon.LlmAgent("concurrent_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("You are a helpful assistant. Be very concise.")
    agent.with_temperature(0.7)
    agent.with_max_tokens(50)
    agent.build()
    print("[OK] Agent created and built")

    # Step 2: Prepare multiple questions
    questions = [
        "What is 2+2?",
        "What is the capital of France?",
        "What color is the sky?",
        "Who wrote Romeo and Juliet?",
        "What is the speed of light?",
    ]

    print(f"\n2. Sending {len(questions)} queries concurrently...\n")

    # Step 3: Send all queries at the same time
    start_time = time.time()

    # Create async tasks (doesn't execute yet, just schedules them)
    tasks = [agent.send_message_async(q) for q in questions]

    # await asyncio.gather() waits for all tasks to complete
    # return_exceptions=True means errors are returned, not raised
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    elapsed = time.time() - start_time

    # Step 4: Display results
    print("Results:")
    print("-" * 60)
    for i, (question, response) in enumerate(zip(questions, responses), 1):
        if isinstance(response, Exception):
            # Error occurred
            print(f"{i}. Q: {question}")
            print(f"   A: ERROR - {response}\n")
        else:
            # Successful response
            print(f"{i}. Q: {question}")
            print(f"   A: {response}\n")

    # Step 5: Performance statistics
    print(f"✅ Processed {len(questions)} queries in {elapsed:.2f}s")
    print(f"   Average: {elapsed/len(questions):.2f}s per query")
    print()


async def demo_streaming_responses():
    """
    Demo 2: Process queries as they complete (streaming style).

    Instead of waiting for all to finish, display results as they arrive.
    This is useful when you want to show progress to users.
    """
    print("=" * 60)
    print("Demo 2: Streaming Responses with asyncio.as_completed()")
    print("=" * 60)

    # Step 1: Create LLM agent
    print("\n1. Creating LLM agent...")
    agent = ceylon.LlmAgent("streaming_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("Answer in one short sentence.")
    agent.with_temperature(0.7)
    agent.with_max_tokens(30)
    agent.build()
    print("[OK] Agent ready")

    # Step 2: Prepare questions with varying complexity
    # Different questions take different amounts of time
    questions = [
        ("Quick", "What is 1+1?"),
        ("Medium", "Explain photosynthesis briefly"),
        ("Long", "What is the theory of relativity?"),
    ]

    print(f"\n2. Sending {len(questions)} queries and displaying as they complete...\n")

    # Step 3: Create tasks and attach metadata
    tasks = []
    for label, question in questions:
        # Create the async task
        task = asyncio.create_task(agent.send_message_async(question))
        # Attach metadata so we can identify which task completed
        task.label = label
        task.question = question
        tasks.append(task)

    # Step 4: Wait for tasks one at a time as they complete
    start_time = time.time()
    completed_count = 0
    pending = set(tasks)

    # Loop until no tasks are pending
    while pending:
        # Wait for the first task to complete
        done, pending = await asyncio.wait(
            pending,
            return_when=asyncio.FIRST_COMPLETED  # Return after ONE completes
        )

        # Process each newly completed task
        for task in done:
            try:
                response = await task
                completed_count += 1
                elapsed = time.time() - start_time

                # Display result immediately
                print(f"[{completed_count}/{len(questions)}] {task.label} query completed ({elapsed:.2f}s)")
                print(f"  Q: {task.question}")
                print(f"  A: {response}\n")

            except Exception as e:
                print(f"  ERROR: {e}\n")

    total_time = time.time() - start_time
    print(f"✅ All queries completed in {total_time:.2f}s")
    print()


async def demo_batch_processing():
    """
    Demo 3: Batch processing with concurrency control.

    Instead of sending all queries at once, process them in batches.
    Useful for:
    - Rate limiting
    - Memory management
    - Server load management
    """
    print("=" * 60)
    print("Demo 3: Batch Processing with Concurrency Limit")
    print("=" * 60)

    # Step 1: Create LLM agent
    print("\n1. Creating LLM agent...")
    agent = ceylon.LlmAgent("batch_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("Provide a one-word answer.")
    agent.with_temperature(0.5)
    agent.with_max_tokens(10)
    agent.build()
    print("[OK] Agent ready")

    # Step 2: Create a large batch of simple queries
    queries = [
        "What is 2+2?",
        "What is 3+3?",
        "What is 5+5?",
        "What is 7+7?",
        "What is 9+9?",
        "What is 11+11?",
        "What is 13+13?",
        "What is 15+15?",
    ]

    # Step 3: Process in batches of 3
    batch_size = 3
    print(f"\n2. Processing {len(queries)} queries in batches of {batch_size}...\n")

    start_time = time.time()
    all_results = []

    # Process each batch
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        batch_num = i // batch_size + 1

        print(f"Batch {batch_num}: Processing {len(batch)} queries...")

        # Send all queries in this batch concurrently
        tasks = [agent.send_message_async(q) for q in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_results.extend(results)

        # Display batch results
        for query, result in zip(batch, results):
            if isinstance(result, Exception):
                print(f"  ✗ {query} -> ERROR: {result}")
            else:
                print(f"  ✓ {query} -> {result}")
        print()

    elapsed = time.time() - start_time
    successful = sum(1 for r in all_results if not isinstance(r, Exception))

    # Step 4: Summary
    print(f"✅ Batch processing complete!")
    print(f"   Total: {len(queries)} queries")
    print(f"   Successful: {successful}")
    print(f"   Failed: {len(queries) - successful}")
    print(f"   Time: {elapsed:.2f}s")
    print()


async def demo_error_handling():
    """
    Demo 4: Error handling in async contexts.

    Demonstrates gracefully handling errors when queries fail.
    Important because network operations can always fail.
    """
    print("=" * 60)
    print("Demo 4: Error Handling with Async Operations")
    print("=" * 60)

    # Step 1: Create LLM agent
    print("\n1. Creating LLM agent...")
    agent = ceylon.LlmAgent("error_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("Be helpful.")
    agent.with_max_tokens(30)
    agent.build()
    print("[OK] Agent ready")

    # Step 2: Create test cases (some valid, some problematic)
    test_cases = [
        ("Valid query", "What is 2+2?"),
        ("Empty query", ""),
        ("Very long query", "a" * 10000),
        ("Another valid", "What is Python?"),
    ]

    print(f"\n2. Testing error handling with {len(test_cases)} different cases...\n")

    # Step 3: Test each case
    results = []
    for label, query in test_cases:
        print(f"Testing: {label}")
        try:
            # Send async message
            response = await agent.send_message_async(query)
            # Show success
            preview = response[:50] + "..." if len(response) > 50 else response
            print(f"  ✓ Success: {preview}")
            results.append((label, "success", response))
        except Exception as e:
            # Handle the error gracefully
            error_type = type(e).__name__
            error_msg = str(e)[:50]  # First 50 chars of error
            print(f"  ✗ Error: {error_type}: {error_msg}")
            results.append((label, "error", str(e)))
        print()

    # Step 4: Summary
    successes = sum(1 for _, status, _ in results if status == "success")
    errors = sum(1 for _, status, _ in results if status == "error")

    print(f"✅ Error handling test complete!")
    print(f"   Successful: {successes}")
    print(f"   Errors caught: {errors}")
    print()


async def main():
    """
    Main entry point - run all async demos.

    This is an async function that calls other async functions.
    """
    print("\n" + "=" * 60)
    print("🚀 Ceylon Async LLM Demo")
    print("=" * 60)
    print("\nThis demo showcases Ceylon's async functionality:")
    print("- Concurrent LLM queries using send_message_async()")
    print("- Different async patterns with asyncio")
    print("- Error handling in async contexts")
    print("\n" + "=" * 60 + "\n")

    try:
        # Run all demos sequentially (one after another)
        await demo_concurrent_queries()
        await demo_streaming_responses()
        await demo_batch_processing()
        await demo_error_handling()

        # All complete!
        print("=" * 60)
        print("✅ All demos completed successfully!")
        print("=" * 60)

    except Exception as e:
        # Handle any unexpected errors
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    # Run the async demo using asyncio.run()
    exit_code = asyncio.run(main())
    exit(exit_code)
```

## Running the Example

### 1. Ensure Prerequisites

```bash
# Install Ceylon with async support
pip install ceylon

# Ensure Ollama is running (if using local LLM)
ollama serve

# In another terminal, optionally pull a model
ollama pull gemma3:latest
```

### 2. Run the Script

```bash
cd bindings/python/examples
python demo_async_llm.py
```

### 3. Expected Output

```
============================================================
🚀 Ceylon Async LLM Demo
============================================================

This demo showcases Ceylon's async functionality:
- Concurrent LLM queries using send_message_async()
- Different async patterns with asyncio
- Error handling in async contexts

============================================================

============================================================
Demo 1: Concurrent LLM Queries with asyncio.gather()
============================================================

1. Creating LLM agent with gemma3:latest...
[OK] Agent created and built

2. Sending 5 queries concurrently...

Results:
------------------------------------------------------------
1. Q: What is 2+2?
   A: 4

2. Q: What is the capital of France?
   A: Paris

3. Q: What color is the sky?
   A: Blue

4. Q: Who wrote Romeo and Juliet?
   A: William Shakespeare

5. Q: What is the speed of light?
   A: 299,792,458 meters per second

✅ Processed 5 queries in 5.23s
   Average: 1.05s per query
```

## Key Concepts Explained

### Async vs Sync Comparison

```python
# Synchronous (blocking) - waits for each response
def sync_queries(agent, questions):
    for question in questions:
        response = agent.send_message(question)  # Blocks here
        print(response)

# Asynchronous (concurrent) - sends all at once
async def async_queries(agent, questions):
    tasks = [agent.send_message_async(q) for q in questions]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response)
```

**Time Comparison**:
- Sync (5 queries × 1s each): 5 seconds
- Async (5 queries): ~1 second total

### Event Loop

The event loop is the core of asyncio:

```
Event Loop:
1. Check all tasks
2. Run task A until it awaits
3. Run task B until it awaits
4. Run task C until it awaits
5. Go back to step 1 until all complete
```

This allows pseudoparallelism on a single thread.

### Common Async Patterns

**Pattern 1: Wait for All (gather)**
```python
tasks = [agent.send_message_async(q) for q in questions]
results = await asyncio.gather(*tasks)  # Wait for all
```

**Pattern 2: Process As Ready (as_completed)**
```python
tasks = [asyncio.create_task(agent.send_message_async(q)) for q in questions]
for coro in asyncio.as_completed(tasks):
    result = await coro  # Process as ready
```

**Pattern 3: Batch Processing**
```python
for i in range(0, len(items), batch_size):
    batch = items[i:i + batch_size]
    results = await asyncio.gather(*[process(item) for item in batch])
```

## Troubleshooting

### Issue: "RuntimeError: no running event loop"

**Symptoms**: Error when trying to use async inside non-async function

**Solution**:
```python
# ❌ Wrong - can't await outside async function
agent.send_message_async(question)

# ✅ Correct - must be in async function
async def my_function():
    result = await agent.send_message_async(question)
```

### Issue: Tasks don't seem to run concurrently

**Symptoms**: Total time is sum of individual times (not faster)

**Solutions**:
1. Verify you're using `send_message_async()` not `send_message()`
2. Ensure you're actually awaiting: `await asyncio.gather(*tasks)`
3. Check that all tasks are created before gathering

### Issue: "TypeError: object is not iterable"

**Symptoms**: Error with `*tasks` unpacking

**Solution**:
```python
# ❌ Wrong - forgot the * unpacking
responses = await asyncio.gather(tasks)

# ✅ Correct - unpack the list
responses = await asyncio.gather(*tasks)
```

### Issue: Exceptions are silently ignored

**Symptoms**: Errors happen but you don't see them

**Solution**:
```python
# ✅ Correct - return_exceptions=True to see errors
responses = await asyncio.gather(*tasks, return_exceptions=True)

# Check for errors
for response in responses:
    if isinstance(response, Exception):
        print(f"Error: {response}")
```

## Advanced Patterns

### Semaphore (Limiting Concurrency)

```python
async def limited_concurrent_queries(agent, questions, max_concurrent=3):
    """Limit concurrent queries to avoid overwhelming server"""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_query(question):
        async with semaphore:
            return await agent.send_message_async(question)

    tasks = [limited_query(q) for q in questions]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

### Timeout Handling

```python
async def query_with_timeout(agent, question, timeout=5):
    """Query with maximum time limit"""
    try:
        return await asyncio.wait_for(
            agent.send_message_async(question),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return f"Query timed out after {timeout}s"
```

### Progress Tracking

```python
async def queries_with_progress(agent, questions):
    """Show progress as queries complete"""
    tasks = {
        asyncio.create_task(agent.send_message_async(q)): q
        for q in questions
    }

    completed = 0
    for coro in asyncio.as_completed(tasks):
        result = await coro
        completed += 1
        print(f"Progress: {completed}/{len(questions)}")
        yield result
```

## Performance Tips

1. **Use async for I/O operations**: Network calls benefit greatly
2. **Avoid blocking in async**: No sleep-loops, use asyncio.sleep()
3. **Gather vs As Completed**: Use gather for simple cases, as_completed for streaming
4. **Batch size matters**: Too small = overhead, too large = memory issues
5. **Handle errors**: Always use `return_exceptions=True` or try/except

## Next Steps

Now that you understand async operations:

1. **Memory System** (`../memory/basic-memory.md`): Store and retrieve information
2. **RAG System** (`../rag/markdown-rag.md`): Build knowledge-based Q&A systems
3. **Production Patterns**: Learn deployment and monitoring strategies
4. **Integration**: Combine async with web frameworks (FastAPI, etc.)

## Summary

The async LLM example demonstrates:
- ✅ Using `send_message_async()` for concurrent operations
- ✅ Running multiple queries simultaneously with `asyncio.gather()`
- ✅ Processing results as they arrive with streaming patterns
- ✅ Batch processing with concurrency control
- ✅ Comprehensive error handling in async contexts

Async programming is crucial for scalable, high-performance LLM applications.
