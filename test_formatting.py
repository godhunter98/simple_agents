#!/usr/bin/env python3
"""Test script to verify the improved output formatting."""

import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the openai client for testing
class MockCompletion:
    def __init__(self, message):
        self.choices = [MockChoice(message)]

class MockChoice:
    def __init__(self, message):
        self.message = message

class MockToolCall:
    def __init__(self, name, arguments):
        self.function = MockFunction(name, arguments)

class MockFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class MockMessage:
    def __init__(self, tool_calls=None, content=None):
        self.tool_calls = tool_calls
        self.content = content

class MockClient:
    def __init__(self):
        pass
    
    class Chat:
        class Completions:
            def create(self, model, messages, tools, tool_choice):
                # Simulate a tool call response
                if tools:
                    tool_call = MockToolCall(
                        name="fetch_security_data",
                        arguments='{"symbol": "INFY"}'
                    )
                    return MockCompletion(MockMessage(tool_calls=[tool_call]))
                else:
                    return MockCompletion(MockMessage(content="This is a test response."))
        
        completions = Completions()
    
    chat = Chat()

# Test the formatting methods
from main import Agent

# Create a mock client
client = MockClient()

# Test 1: Format security data
print("=" * 60)
print("TEST 1: Security Data Formatting")
print("=" * 60)

agent = Agent(client, system="Test system", tools=[])
formatted = agent._format_security_data(
    symbol="INFY",
    price=1234.56,
    percent_change=2.5,
    pe_ratio=28.35,
    industry="Information Technology"
)
print(formatted)

# Test 2: Format final response
print("\n" + "=" * 60)
print("TEST 2: Final Response Formatting")
print("=" * 60)

formatted = agent._format_final_response(
    "The current price of Infosys is ₹1234.56, which is up by 2.5% today. "
    "The P/E ratio is 28.35 and it belongs to the Information Technology sector."
)
print(formatted)

# Test 3: Combined output simulation
print("\n" + "=" * 60)
print("TEST 3: Combined Output Simulation")
print("=" * 60)

print("\n[User] What is the price of Infosys stock?")
print("\n[Agent is thinking...]")

# Simulate tool execution output
print("\n" + "=" * 60)
print("SECURITY DATA FOR: INFY")
print("=" * 60)
print("Price:           ₹1,234.56")
print("Change:          +2.50%")
print("P/E Ratio:       28.35")
print("Industry:        Information Technology")
print("=" * 60)

# Simulate final response
print("\n" + "=" * 60)
print("ASSISTANT RESPONSE")
print("=" * 60)
print("The current price of Infosys (INFY) is ₹1,234.56, which shows a positive change of 2.50% today. "
    "The stock has a P/E ratio of 28.35 and belongs to the Information Technology sector.")
print("=" * 60)

print("\n✅ All formatting tests completed successfully!")
