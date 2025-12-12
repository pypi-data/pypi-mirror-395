"""
Simple OpenAI Token Counter
============================

Quick example showing how to track OpenAI token usage
with Ceylon AI metrics.

Usage:
    export OPENAI_API_KEY="your-key"
    python metrics_token_counter.py
"""

import ceylonai_next as ceylon
import asyncio
import os


async def main():
    print("🔢 OpenAI Token Counter Demo\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable first!")
        return
    
    # Create OpenAI agent
    agent = ceylon.LlmAgent("counter", "openai::gpt-3.5-turbo")
    agent.with_api_key(os.getenv("OPENAI_API_KEY"))
    agent.with_max_tokens(100)
    agent.build()
    
    # Get baseline metrics
    print("📊 Initial metrics:")
    initial = ceylon.get_metrics()
    print(f"   Tokens: {initial['total_llm_tokens']}\n")
    
    # Send some queries
    queries = [
        "What is 2+2?",
        "What is the capital of France?",
        "What is Python?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"{i}. Query: {query}")
        response = await agent.send_message_async(query)
        print(f"   Response: {response}\n")
    
    # Show final token count
    final = ceylon.get_metrics()
    tokens_used = final['total_llm_tokens'] - initial['total_llm_tokens']
    
    print("="*60)
    print(f"✅ Total tokens used: {tokens_used}")
    print(f"   Average per query: {tokens_used / len(queries):.0f}")
    
    # Calculate approximate cost (GPT-3.5-turbo pricing)
    # Input: $0.0015 / 1K tokens, Output: $0.002 / 1K tokens
    # Using average of ~$0.00175 per 1K tokens
    estimated_cost = (tokens_used / 1000) * 0.00175
    print(f"   Estimated cost: ${estimated_cost:.4f}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
