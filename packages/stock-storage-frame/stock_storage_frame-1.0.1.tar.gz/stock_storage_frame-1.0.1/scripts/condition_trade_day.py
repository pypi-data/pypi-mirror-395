"""
Example condition script that returns True or False based on configuration.
"""

import asyncio
import datetime
import chinese_calendar as calendar

async def check() -> bool:
    """
    Example condition that checks if current hour is before threshold.
    
    Args:
        threshold: Hour threshold (0-23)
        
    Returns:
        True if current hour < threshold, False otherwise
    """
    """
    判断A股交易日
    规则：非节假日且非周六日
    """
    print(f"判断是否A股交易日")
    today = datetime.date.today()
    print(f"Today is {today}")
    # 判断是否为节假日
    if calendar.is_holiday(today):
        return False
    
    # 判断是否为周六日
    weekday = today.weekday()  # 0-4是周一到周五，5-6是周六日
    if weekday >= 5:
        return False
    
    return True


if __name__ == "__main__":
    # Test the condition
    result = asyncio.run(check())
    print(f"Condition result: {result}")
