"""
Example condition script that returns True or False based on configuration.
"""

import asyncio
from datetime import datetime


async def check(threshold: int = 18) -> bool:
    """
    Example condition that checks if current hour is before threshold.
    
    Args:
        threshold: Hour threshold (0-23)
        
    Returns:
        True if current hour < threshold, False otherwise
    """
    current_hour = datetime.now().hour
    print(f"Current hour: {current_hour}, threshold: {threshold}")
    return current_hour < threshold


if __name__ == "__main__":
    # Test the condition
    result = asyncio.run(check(18))
    print(f"Condition result: {result}")
