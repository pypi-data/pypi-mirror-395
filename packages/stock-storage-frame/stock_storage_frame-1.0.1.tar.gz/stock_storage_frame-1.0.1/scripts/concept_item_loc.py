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
    
    subset = df.loc[:, ['行业', '行业代码', '名称', '代码']] # 提取特定列
    # 如果原始是数值型，先转为字符串并补零到指定长度
    subset['代码'] = subset['代码'].astype(str).str.zfill(6)  # 确保6位，确保保留前缀0
    return subset
