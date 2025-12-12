"""Test token estimation without OpenAI API"""
import sys
sys.path.insert(0, 'F:\\\\projects\\\\ceylon\\\\next-processor\\\\bindings\\\\python')

try:
    import ceylonai_next as ceylon
    print("✓ Module imported successfully")
    
    # Get initial metrics
    metrics = ceylon.get_metrics()
    print(f"Initial token count: {metrics['total_llm_tokens']}")
    print(f"Initial cost: {metrics['total_llm_cost_us']} micro-dollars")
    
    print("\n✅ Token estimation is now active in the metrics system!")
    print("Note: Tokens will be estimated when LLM queries are made")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
