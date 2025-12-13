"""
股票数据增加当天日期，用于记录
"""

import pandas as pd
from datetime import datetime

def convert_mixed_unit(value):
    """将带亿/万的字符串统一转换为亿单位"""
    if pd.isna(value):
        return np.nan
    
    value = str(value).strip()
    if value.endswith('亿'):
        return float(value[:-1])
    elif value.endswith('万'):
        return float(value[:-1]) / 10000
    else:
        return float(value)
    
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
    # 处理百分比列
    print('处理百分比列')
    for col in ['涨跌幅', '换手率']:
        df[col] = df[col].str.replace('%', '').astype(float)
        df = df.rename(columns={col: f'{col}(%)'})

    # 处理混合单位列
    print('处理混合单位列')
    for col in ['流入资金', '流出资金', '净额', '成交额']:
        df[col] = df[col].apply(convert_mixed_unit)
        df = df.rename(columns={col: f'{col}(亿)'})

    df['股票代码'] = df['股票代码'].astype(str).str.zfill(6)  # 确保6位，确保保留前缀0
    return df
