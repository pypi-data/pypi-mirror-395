#!/usr/bin/env python3
"""Test Agent class with message sending and responses."""

from ceylonai_next import Agent

# Create a custom agent that responds to messages
class MyAgent(Agent):
    def __init__(self, name="my_agent"):
        super().__init__(name)
        self.message_count = 0
    
    def on_message(self, message, context=None):
        """Process incoming messages and return a response."""
        self.message_count += 1
        
        # Simple response logic
        if "hello" in message.lower():
            return f"Hello! This is message #{self.message_count}"
        elif "count" in message.lower():
            return f"I have received {self.message_count} messages"
        else:
            return f"You said: {message}"

# Test the agent
print("Testing Agent with send_message...")
print("=" * 50)

agent = MyAgent("test_agent")

# Send messages and get responses
messages = [
    "Hello there!",
    "How are you?",
    "What's the count?",
]

for msg in messages:
    print(f"\nSending: {msg}")
    response = agent.send_message(msg)
    print(f"Response: {response}")

print("\n" + "=" * 50)
print(f"Last response: {agent.last_response()}")
print("Test complete!")
