"""
股票数据增加当天日期，用于记录
"""

import pandas as pd
from datetime import datetime

def process(df: pd.DataFrame) -> pd.DataFrame:
    """
    处理股票数据，计算技术指标。
    
    Args:
        df: 输入的股票数据DataFrame
        
    Returns:
        处理后的DataFrame
    """
    if df.empty:
        return df
    
    df['日期'] = datetime.now().strftime("%Y-%m-%d") # 添加日期

    return df
