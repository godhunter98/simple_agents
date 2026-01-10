"""
Formatting utilities for agent outputs.
This module provides optional formatting functions that can be used
to enhance the appearance of agent responses.
"""

def format_security_data(
    symbol: str,
    price: float,
    percent_change: float,
    pe_ratio: float,
    industry: str,
    debug: bool = False
) -> str:
    """
    Format security data as a simple one-liner.
    
    Args:
        symbol: Stock symbol (e.g., "INFY")
        price: Current price
        percent_change: Percentage change
        pe_ratio: Price-to-earnings ratio
        industry: Industry sector
        debug: If True, use lightweight format
        
    Returns:
        Formatted string
    """
    if debug:
        return f"DEBUG: {symbol.upper()} - ₹{price:.2f} ({percent_change:+.2f}%) | P/E: {pe_ratio:.2f} | {industry}"
    
    return f"Price: ₹{price:.2f}, Change: {percent_change:+.2f}%, P/E: {pe_ratio:.2f}, Industry: {industry}"


def format_final_response(content: str, use_formatting: bool = True) -> str:
    """
    Format the final assistant response.
    
    Args:
        content: The response content
        use_formatting: If True, add visual formatting
        
    Returns:
        Formatted string
    """
    if not use_formatting:
        return content
    
    header = "=" * 60
    return f"\n{header}\nASSISTANT RESPONSE\n{header}\n{content}\n{header}"
