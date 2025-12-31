#!/usr/bin/env python3
"""
Demonstration of improved output formatting for Agent+Tool responses.

This script shows how the structured output makes it easier to read
and understand the agent's responses and tool outputs.
"""

from main import Agent

# Create a sample agent instance
class MockClient:
    pass

client = MockClient()
agent = Agent(client, system="You are a helpful financial assistant.", tools=[])

print("=" * 70)
print("DEMONSTRATION: Improved Agent Output Formatting")
print("=" * 70)

print("\n" + "=" * 70)
print("SCENARIO 1: Single Tool Call with Security Data")
print("=" * 70)

print("\n📝 User Query: 'What is the current price of Reliance Industries?'")
print("\n🔧 Agent Actions:")

# Simulate tool output
security_data = agent._format_security_data(
    symbol="RELIANCE",
    price=2987.50,
    percent_change=-1.25,
    pe_ratio=32.80,
    industry="Oil & Gas"
)
print(security_data)

# Simulate final response
final_response = agent._format_final_response(
    "Reliance Industries (RELIANCE) is currently trading at ₹2,987.50, "
    "showing a slight decline of 1.25% today. The stock has a P/E ratio of 32.80 "
    "and operates in the Oil & Gas sector."
)
print(final_response)

print("\n" + "=" * 70)
print("SCENARIO 2: Multiple Security Comparisons")
print("=" * 70)

print("\n📝 User Query: 'Compare Infosys and TCS stock prices'")
print("\n🔧 Agent Actions:")

# First stock
print(agent._format_security_data(
    symbol="INFY",
    price=1234.56,
    percent_change=2.50,
    pe_ratio=28.35,
    industry="Information Technology"
))

# Second stock
print(agent._format_security_data(
    symbol="TCS",
    price=3456.78,
    percent_change=1.80,
    pe_ratio=30.15,
    industry="Information Technology"
))

# Final comparison response
print(agent._format_final_response(
    "Here's a comparison of Infosys and TCS:\n\n"
    "• Infosys (INFY): ₹1,234.56 (+2.50%) with P/E of 28.35\n"
    "• TCS (TCS): ₹3,456.78 (+1.80%) with P/E of 30.15\n\n"
    "Both stocks are in the Information Technology sector. Infosys shows a higher "
    "percentage gain today, while TCS has a higher absolute price and P/E ratio."
))

print("\n" + "=" * 70)
print("SCENARIO 3: Error Handling with Clear Output")
print("=" * 70)

print("\n📝 User Query: 'What is the price of XYZ company?'")
print("\n⚠️  Error: Symbol 'XYZ' not found in NSE data")
print("\n💡 Assistant Response:")

print(agent._format_final_response(
    "I'm sorry, I couldn't find data for 'XYZ' company. Please check the "
    "ticker symbol and try again. For example, you can use symbols like INFY, "
    "RELIANCE, TCS, etc."
))

print("\n" + "=" * 70)
print("BENEFITS OF STRUCTURED OUTPUT:")
print("=" * 70)
print("""
✅ Clear visual separation between tool data and final response
✅ Easy-to-read formatted tables for security information
✅ Consistent structure for all outputs
✅ Better user experience with proper spacing and headers
✅ Professional appearance with aligned columns
✅ Error messages are clearly distinguishable
✅ Multiple data points can be compared easily
""")

print("=" * 70)
print("DEMONSTRATION COMPLETE")
print("=" * 70)
