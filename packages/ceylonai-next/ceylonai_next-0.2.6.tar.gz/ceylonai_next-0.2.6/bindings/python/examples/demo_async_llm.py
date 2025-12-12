#!/usr/bin/env python3
"""
Async LLM Demo - demonstrates concurrent LLM operations using send_message_async()

This example showcases the working async functionality in Ceylon:
- Concurrent LLM message processing
- Batch query processing with asyncio.gather()
- Streaming responses with asyncio.as_completed()
- Error handling in async contexts

Note: send_message_async() is the primary working async API in Ceylon.
"""
import asyncio
import time
from typing import List, Tuple
import ceylonai_next


async def demo_concurrent_queries():
    """Demo 1: Send multiple queries concurrently and wait for all"""
    print("=" * 60)

    # Create and configure LLM agent
    print("\n1. Creating LLM agent with gemma3:latest...")
    agent = ceylon.LlmAgent("concurrent_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("You are a helpful assistant. Be very concise.")
    agent.with_temperature(0.7)
    agent.with_max_tokens(50)
    agent.build()
    print("[OK] Agent created and built")

    # Prepare multiple questions
    questions = [
        "What is 2+2?",
        "What is the capital of France?",
        "What color is the sky?",
        "Who wrote Romeo and Juliet?",
        "What is the speed of light?",
    ]

    print(f"\n2. Sending {len(questions)} queries concurrently...\n")

    # Send all queries concurrently using gather()
    start_time = time.time()

    tasks = [agent.send_message_async(q) for q in questions]
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    elapsed = time.time() - start_time

    # Display results
    print("Results:")
    print("-" * 60)
    for i, (question, response) in enumerate(zip(questions, responses), 1):
        if isinstance(response, Exception):
            print(f"{i}. Q: {question}")
            print(f"   A: ERROR - {response}\n")
        else:
            print(f"{i}. Q: {question}")
            print(f"   A: {response}\n")

    print(f"✅ Processed {len(questions)} queries in {elapsed:.2f}s")
    print(f"   Average: {elapsed/len(questions):.2f}s per query")
    print()


async def demo_streaming_responses():
    """Demo 2: Process queries as they complete (streaming style)"""
    print("=" * 60)
    print("Demo 2: Streaming Responses with asyncio.as_completed()")
    print("=" * 60)

    # Create LLM agent
    print("\n1. Creating LLM agent...")
    agent = ceylon.LlmAgent("streaming_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("Answer in one short sentence.")
    agent.with_temperature(0.7)
    agent.with_max_tokens(30)
    agent.build()
    print("[OK] Agent ready")

    # Prepare questions with varying complexity
    questions = [
        ("Quick", "What is 1+1?"),
        ("Medium", "Explain photosynthesis briefly"),
        ("Long", "What is the theory of relativity?"),
    ]

    print(f"\n2. Sending {len(questions)} queries and displaying as they complete...\n")

    # Create tasks with labels attached
    tasks = []
    for label, question in questions:
        task = asyncio.create_task(agent.send_message_async(question))
        task.label = label  # Attach metadata to task
        task.question = question
        tasks.append(task)

    # Process as they complete using asyncio.wait
    start_time = time.time()
    completed_count = 0
    pending = set(tasks)

    while pending:
        # Wait for the first task to complete
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        
        for task in done:
            try:
                response = await task
                completed_count += 1
                elapsed = time.time() - start_time

                print(f"[{completed_count}/{len(questions)}] {task.label} query completed ({elapsed:.2f}s)")
                print(f"  Q: {task.question}")
                print(f"  A: {response}\n")

            except Exception as e:
                print(f"  ERROR: {e}\n")

    total_time = time.time() - start_time
    print(f"✅ All queries completed in {total_time:.2f}s")
    print()


async def demo_batch_processing():
    """Demo 3: Batch processing with concurrency control"""
    print("=" * 60)
    print("Demo 3: Batch Processing with Concurrency Limit")
    print("=" * 60)

    # Create LLM agent
    print("\n1. Creating LLM agent...")
    agent = ceylon.LlmAgent("batch_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("Provide a one-word answer.")
    agent.with_temperature(0.5)
    agent.with_max_tokens(10)
    agent.build()
    print("[OK] Agent ready")

    # Large batch of simple queries
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

    # Process in batches of 3
    batch_size = 3
    print(f"\n2. Processing {len(queries)} queries in batches of {batch_size}...\n")

    start_time = time.time()
    all_results = []

    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        batch_num = i // batch_size + 1

        print(f"Batch {batch_num}: Processing {len(batch)} queries...")

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

    print(f"✅ Batch processing complete!")
    print(f"   Total: {len(queries)} queries")
    print(f"   Successful: {successful}")
    print(f"   Failed: {len(queries) - successful}")
    print(f"   Time: {elapsed:.2f}s")
    print()


async def demo_error_handling():
    """Demo 4: Error handling in async contexts"""
    print("=" * 60)
    print("Demo 4: Error Handling with Async Operations")
    print("=" * 60)

    # Create LLM agent
    print("\n1. Creating LLM agent...")
    agent = ceylon.LlmAgent("error_agent", "ollama::gemma3:latest")
    agent.with_system_prompt("Be helpful.")
    agent.with_max_tokens(30)
    agent.build()
    print("[OK] Agent ready")

    # Mix of valid and potentially problematic queries
    test_cases = [
        ("Valid query", "What is 2+2?"),
        ("Empty query", ""),
        ("Very long query", "a" * 10000),
        ("Another valid", "What is Python?"),
    ]

    print(f"\n2. Testing error handling with {len(test_cases)} different cases...\n")

    results = []
    for label, query in test_cases:
        print(f"Testing: {label}")
        try:
            response = await agent.send_message_async(query)
            print(f"  ✓ Success: {response[:50]}...")
            results.append((label, "success", response))
        except Exception as e:
            print(f"  ✗ Error: {type(e).__name__}: {e}")
            results.append((label, "error", str(e)))
        print()

    # Summary
    successes = sum(1 for _, status, _ in results if status == "success")
    errors = sum(1 for _, status, _ in results if status == "error")

    print(f"✅ Error handling test complete!")
    print(f"   Successful: {successes}")
    print(f"   Errors caught: {errors}")
    print()


async def main():
    """Main entry point - run all demos"""
    print("\n" + "=" * 60)
    print("🚀 Ceylon Async LLM Demo")
    print("=" * 60)
    print("\nThis demo showcases Ceylon's working async functionality:")
    print("- Concurrent LLM queries using send_message_async()")
    print("- Different async patterns with asyncio")
    print("- Error handling in async contexts")
    print("\n" + "=" * 60 + "\n")

    try:
        # Run all demos
        await demo_concurrent_queries()
        await demo_streaming_responses()
        await demo_batch_processing()
        await demo_error_handling()

        print("=" * 60)
        print("✅ All demos completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    # Run the async demo
    exit_code = asyncio.run(main())
    exit(exit_code)
