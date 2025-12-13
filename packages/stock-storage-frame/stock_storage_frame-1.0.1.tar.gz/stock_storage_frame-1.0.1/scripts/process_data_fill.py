"""
示例处理脚本：处理每日股票数据
"""

import pandas as pd


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
    
    # 处理缺失值
    # numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    # df[numeric_cols] = df[numeric_cols].fillna(method='ffill').fillna(method='bfill')
    
    return df


if __name__ == "__main__":
    # 测试代码
    test_data = pd.DataFrame({
        'symbol': ['000001', '000001', '000001', '000002', '000002'],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-01', '2024-01-02'],
        'open': [10.0, 10.5, 10.2, 20.0, 21.0],
        'high': [10.5, 11.0, 10.8, 21.0, 22.0],
        'low': [9.8, 10.3, 10.0, 19.5, 20.5],
        'close': [10.2, 10.8, 10.5, 20.5, 21.5],
        'volume': [1000000, 1200000, 1100000, 500000, 600000],
        'amount': [10200000, 12960000, 11550000, 10250000, 12900000]
    })
    
    result = process(test_data)
    print("处理后的数据形状:", result.shape)
    print("新增列:", [col for col in result.columns if col not in test_data.columns])
    print("\n前几行数据:")
    print(result.head())
