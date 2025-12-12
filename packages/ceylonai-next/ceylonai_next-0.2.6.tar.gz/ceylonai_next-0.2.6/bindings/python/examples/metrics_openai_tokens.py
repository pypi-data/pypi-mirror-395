"""
OpenAI Token Counting with Ceylon AI Metrics
=============================================

This example demonstrates how to use Ceylon AI with OpenAI
to track token usage and costs through the metrics system.

Requirements:
    pip install openai
    export OPENAI_API_KEY="your-api-key"
"""

import ceylonai_next as ceylon
import asyncio
import os
import json


def print_token_metrics():
    """Print current token and cost metrics."""
    metrics = ceylon.get_metrics()
    
    print("\n" + "="*60)
    print("  📊 OpenAI Token Metrics")
    print("="*60)
    
    # LLM metrics
    print(f"\n🤖 LLM Usage:")
    print(f"  Total tokens:         {metrics['total_llm_tokens']:,}")
    print(f"  Average latency:      {metrics['avg_llm_latency_us']/1000:.2f} ms")
    print(f"  Total API calls:      {metrics['message_throughput']}")
    
    # Cost (micro-dollars)
    if metrics['total_llm_cost_us'] > 0:
        cost_dollars = metrics['total_llm_cost_us'] / 1_000_000
        print(f"  Total cost:           ${cost_dollars:.4f}")
        
        if metrics['total_llm_tokens'] > 0:
            cost_per_token = cost_dollars / metrics['total_llm_tokens']
            print(f"  Cost per token:       ${cost_per_token:.6f}")
    
    print("="*60 + "\n")


async def example_single_query():
    """Single query example with token tracking."""
    print("\n🔹 Example 1: Single Query")
    print("-" * 60)
    
    # Create LLM agent with OpenAI
    agent = ceylon.LlmAgent("openai_agent", "openai::gpt-3.5-turbo")
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set. Using default configuration.")
    else:
        agent.with_api_key(api_key)
    
    agent.with_temperature(0.7)
    agent.with_max_tokens(100)
    agent.build()
    
    # Send a query
    print("\nSending query to OpenAI...")
    question = "What is the capital of France?"
    response = await agent.send_message_async(question)
    
    print(f"\nQuestion: {question}")
    print(f"Response: {response}")
    
    # Show token metrics
    print_token_metrics()


async def example_multiple_queries():
    """Multiple queries to demonstrate cumulative token tracking."""
    print("\n🔹 Example 2: Multiple Queries (Concurrent)")
    print("-" * 60)
    
    # Create agent
    agent = ceylon.LlmAgent("openai_batch", "openai::gpt-3.5-turbo")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        agent.with_api_key(api_key)
    
    agent.with_temperature(0.5)
    agent.with_max_tokens(50)
    agent.build()
    
    # Multiple questions
    questions = [
        "What is 15 + 27?",
        "What is the largest planet?",
        "Who wrote Romeo and Juliet?",
        "What is the speed of light?",
        "Name a programming language starting with P."
    ]
    
    print(f"\nSending {len(questions)} concurrent queries...")
    
    # Send all queries concurrently
    tasks = [agent.send_message_async(q) for q in questions]
    responses = await asyncio.gather(*tasks)
    
    # Display results
    print("\nResults:")
    for i, (q, r) in enumerate(zip(questions, responses), 1):
        print(f"\n{i}. Q: {q}")
        print(f"   A: {r}")
    
    # Show cumulative metrics
    print_token_metrics()


async def example_token_budgeting():
    """Demonstrate monitoring token usage against a budget."""
    print("\n🔹 Example 3: Token Budgeting")
    print("-" * 60)
    
    TOKEN_BUDGET = 500  # Maximum tokens to use
    
    agent = ceylon.LlmAgent("budget_agent", "openai::gpt-3.5-turbo")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        agent.with_api_key(api_key)
    
    agent.with_max_tokens(30)  # Limit tokens per response
    agent.build()
    
    print(f"\nToken Budget: {TOKEN_BUDGET} tokens")
    print("Sending queries until budget is reached...\n")
    
    initial_metrics = ceylon.get_metrics()
    initial_tokens = initial_metrics['total_llm_tokens']
    
    questions = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?",
        "What is Go?",
        "What is Java?",
    ]
    
    for i, question in enumerate(questions, 1):
        # Check current token usage
        current_metrics = ceylon.get_metrics()
        tokens_used = current_metrics['total_llm_tokens'] - initial_tokens
        
        if tokens_used >= TOKEN_BUDGET:
            print(f"\n⚠️  Token budget reached! Used {tokens_used}/{TOKEN_BUDGET} tokens")
            print(f"   Stopped after {i-1} queries")
            break
        
        # Send query
        print(f"{i}. Asking: {question}")
        response = await agent.send_message_async(question)
        
        # Update tokens
        new_metrics = ceylon.get_metrics()
        new_tokens_used = new_metrics['total_llm_tokens'] - initial_tokens
        tokens_this_query = new_tokens_used - tokens_used
        
        print(f"   Response: {response[:100]}...")
        print(f"   Tokens this query: ~{tokens_this_query}")
        print(f"   Total tokens used: {new_tokens_used}/{TOKEN_BUDGET}")
    
    # Final metrics
    print_token_metrics()


async def example_cost_tracking():
    """Demonstrate cost tracking for different models."""
    print("\n🔹 Example 4: Cost Tracking")
    print("-" * 60)
    
    models = [
        ("openai::gpt-3.5-turbo", "GPT-3.5 Turbo"),
        # ("openai::gpt-4", "GPT-4"),  # Uncomment if you have access
    ]
    
    question = "Explain quantum computing in one sentence."
    
    for model_name, display_name in models:
        print(f"\nTesting {display_name}...")
        
        # Get baseline metrics
        before_metrics = ceylon.get_metrics()
        before_tokens = before_metrics['total_llm_tokens']
        before_cost = before_metrics['total_llm_cost_us']
        
        # Create and query agent
        agent = ceylon.LlmAgent(f"cost_{model_name}", model_name)
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            agent.with_api_key(api_key)
        
        agent.with_max_tokens(50)
        agent.build()
        
        response = await agent.send_message_async(question)
        
        # Calculate metrics for this query
        after_metrics = ceylon.get_metrics()
        tokens_used = after_metrics['total_llm_tokens'] - before_tokens
        cost_us = after_metrics['total_llm_cost_us'] - before_cost
        cost_dollars = cost_us / 1_000_000
        
        print(f"  Response: {response}")
        print(f"  Tokens: {tokens_used}")
        print(f"  Cost: ${cost_dollars:.4f}")
    
    # Final summary
    print_token_metrics()


async def main():
    """Run all examples."""
    print("""
╔══════════════════════════════════════════════════════════╗
║     Ceylon AI - OpenAI Token Tracking Demo              ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY environment variable not set!")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print("\n   The examples will run but may fail without a valid API key.\n")
        
        # Ask user if they want to continue
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    # Show initial state
    print_token_metrics()
    
    # Run examples
    try:
        await example_single_query()
        await asyncio.sleep(0.5)
        
        await example_multiple_queries()
        await asyncio.sleep(0.5)
        
        await example_token_budgeting()
        await asyncio.sleep(0.5)
        
        await example_cost_tracking()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. OPENAI_API_KEY is set correctly")
        print("  2. You have sufficient OpenAI API credits")
        print("  3. The openai Python package is installed: pip install openai")
    
    # Final summary
    final_metrics = ceylon.get_metrics()
    print("\n" + "="*60)
    print("  ✨ Demo Complete!")
    print("="*60)
    print(f"\nTotal tokens used: {final_metrics['total_llm_tokens']:,}")
    print(f"Total API calls: {final_metrics['message_throughput']}")
    
    if final_metrics['total_llm_cost_us'] > 0:
        cost = final_metrics['total_llm_cost_us'] / 1_000_000
        print(f"Total cost: ${cost:.4f}")
    
    print("\n💡 Use ceylon.get_metrics() anytime to track your LLM usage!\n")


if __name__ == "__main__":
    asyncio.run(main())
