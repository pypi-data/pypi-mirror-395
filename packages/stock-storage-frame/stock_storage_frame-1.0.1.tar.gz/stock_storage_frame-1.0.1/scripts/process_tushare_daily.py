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
    
    df['ts_code'] = df['ts_code'].str.split('.').str[0]
    df['trade_date'] = pd.to_datetime(df['trade_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df = df.rename(columns={
        'ts_code': '股票代码',
        'trade_date': '日期',
        'name': '股票名称',
        'pre_close': '昨收价',
        'high': '最高价',
        'open': '开盘价',
        'low': '最低价',
        'close': '收盘价',
        'change': '涨跌额',
        'pct_chg': '涨跌幅',
        'vol': '成交量 （手）',
        'amount': '成交额 （千元）'
    })
    return df
