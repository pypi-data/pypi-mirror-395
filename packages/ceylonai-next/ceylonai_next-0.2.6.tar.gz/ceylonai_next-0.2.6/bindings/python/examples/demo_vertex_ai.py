#!/usr/bin/env python3
"""
Demo showing Vertex AI integration with Ceylon.

This example demonstrates:
1. Creating an LLM agent with Google Vertex AI
2. Configuring the agent with system prompt and parameters
3. Having a conversation with Vertex AI models
4. Handling errors gracefully

Prerequisites:
- Vertex AI API key
- Set VERTEX_API_KEY environment variable

Environment Variables:
- VERTEX_API_KEY: Your Vertex AI API key (required)
"""

import sys
import os

# Add parent directory to path to import ceylon
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ceylonai_next as ceylon

def main():
    """Main demo function"""
    # Print header
    print("=" * 60)
    print("Ceylon LlmAgent - Vertex AI Demo")
    print("=" * 60)

    # Check for Vertex AI API key
    api_key = os.getenv("VERTEX_API_KEY")
    
    if not api_key:
        print("\n⚠️  VERTEX_API_KEY environment variable not set.")
        print("Please set your Vertex AI API key:")
        print("  export VERTEX_API_KEY='your-api-key'")
        print("\nOr on Windows PowerShell:")
        print("  $env:VERTEX_API_KEY='your-api-key'")
        sys.exit(1)

    print(f"\n📋 Configuration:")
    print(f"   API Key: {api_key[:10]}...{api_key[-4:]}")
    
    # STEP 1: Create an LLM agent with Vertex AI
    # Using Gemini 2.0 Flash model via Vertex AI
    print("\n1. Creating LLM agent with Vertex AI (gemini-2-flash)...")
    
    try:
        agent = ceylon.LlmAgent("vertex_agent", "google::gemini-2-flash")
        
        # STEP 2: Configure the system prompt
        agent.with_system_prompt("You are a helpful assistant. Be concise and accurate.")
        
        # STEP 3: Configure temperature
        # 0.7 is a good balance between creativity and consistency
        agent.with_temperature(0.7)
        
        # STEP 4: Set maximum token limit
        agent.with_max_tokens(150)
        
        # STEP 5: Build the agent
        agent.build()
        print("[OK] Agent created and built successfully")
        
    except Exception as e:
        print(f"\n❌ Error creating agent: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Vertex AI API is enabled in your GCP project")
        print("2. Check authentication: gcloud auth application-default login")
        print("3. Verify your project ID is correct")
        sys.exit(1)

    # STEP 6: Start conversation
    print("\n2. Starting conversation with Vertex AI...\n")

    # Define some test questions
    questions = [
        "What is 2+2?",
        "What is the capital of France?",
        "Write a haiku about Python programming",
        "Explain what Google Vertex AI is in one sentence",
    ]

    # Ask each question and get responses
    successful = 0
    for i, question in enumerate(questions, 1):
        print(f"Q{i}: {question}")
        try:
            # Send message to Vertex AI and get response
            response = agent.send_message(question)
            print(f"A{i}: {response}\n")
            successful += 1
        except Exception as e:
            # Handle any errors gracefully
            print(f"❌ Error: {e}\n")

    # Print summary
    print("=" * 60)
    print(f"Demo complete! ({successful}/{len(questions)} successful)")
    print("=" * 60)
    
    if successful == len(questions):
        print("\n✅ All queries successful! Vertex AI is working correctly.")
    else:
        print(f"\n⚠️  Some queries failed. Check your Vertex AI configuration.")


if __name__ == "__main__":
    main()
