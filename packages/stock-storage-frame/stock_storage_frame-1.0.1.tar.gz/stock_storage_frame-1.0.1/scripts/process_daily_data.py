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
    
    # 确保数据按日期排序
    df = df.sort_values(["symbol", "date"])
    
    # 计算移动平均线
    df['ma5'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(5).mean())
    df['ma10'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(10).mean())
    df['ma20'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(20).mean())
    
    # 计算价格变化
    df['price_change'] = df.groupby('symbol')['close'].pct_change()
    
    # 计算波动率（20日标准差）
    df['volatility_20d'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(20).std())
    
    # 计算相对强弱指标（RSI）
    def calculate_rsi(series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    df['rsi_14'] = df.groupby('symbol')['close'].transform(calculate_rsi)
    
    # 计算布林带
    df['bb_middle'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(20).mean())
    df['bb_std'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(20).std())
    df['bb_upper'] = df['bb_middle'] + (df['bb_std'] * 2)
    df['bb_lower'] = df['bb_middle'] - (df['bb_std'] * 2)
    
    # 计算成交量移动平均
    df['volume_ma5'] = df.groupby('symbol')['volume'].transform(lambda x: x.rolling(5).mean())
    df['volume_ma10'] = df.groupby('symbol')['volume'].transform(lambda x: x.rolling(10).mean())
    
    # 添加技术信号
    df['ma_cross'] = (df['ma5'] > df['ma10']).astype(int)
    df['price_above_ma20'] = (df['close'] > df['ma20']).astype(int)
    df['bb_signal'] = pd.cut(
        df['close'],
        bins=[-float('inf'), df['bb_lower'], df['bb_upper'], float('inf')],
        labels=['below_lower', 'middle', 'above_upper']
    )
    
    # 添加日期相关特征
    df['year'] = pd.to_datetime(df['date']).dt.year
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['day'] = pd.to_datetime(df['date']).dt.day
    df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
    df['is_month_end'] = pd.to_datetime(df['date']).dt.is_month_end.astype(int)
    df['is_month_start'] = pd.to_datetime(df['date']).dt.is_month_start.astype(int)
    
    # 处理缺失值
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].fillna(method='ffill').fillna(method='bfill')
    
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
