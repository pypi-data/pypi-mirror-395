"""
Pandas-based processor implementation.
"""

import asyncio
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np

from .base import BaseProcessor
from ..models import BatchStockData, ProcessorConfig


class PandasProcessor(BaseProcessor):
    """Processor using pandas for data manipulation."""
    
    def __init__(self, config: Optional[ProcessorConfig] = None):
        super().__init__(config)
        self.operations = config.config.get("operations", []) if config else []
    
    async def process(self, data: BatchStockData) -> BatchStockData:
        """
        Process stock data using pandas operations.
        
        Args:
            data: Input stock data
            
        Returns:
            Processed stock data
        """
        # Convert to DataFrame
        df = data.to_dataframe()
        
        if df.empty:
            return data
        
        # Apply configured operations
        df = await self._apply_operations(df)
        
        # Convert back to BatchStockData
        processed_data = BatchStockData.from_dataframe(df)
        processed_data.metadata = {
            **data.metadata,
            "processor": "pandas",
            "operations_applied": self.operations,
            "original_records": len(data.data),
            "processed_records": len(processed_data.data),
        }
        
        return processed_data
    
    async def _apply_operations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply configured pandas operations."""
        if not self.operations:
            # Apply default operations if none specified
            df = await self._apply_default_operations(df)
        else:
            for operation in self.operations:
                df = await self._apply_single_operation(df, operation)
        
        return df
    
    async def _apply_default_operations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply default data cleaning operations."""
        # Remove duplicates
        df = df.drop_duplicates(subset=["symbol", "date"])
        
        # Sort by date
        df = df.sort_values(["symbol", "date"])
        
        # Handle missing values
        numeric_cols = ["open", "high", "low", "close", "volume", "amount"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Forward fill for missing values within each symbol
        df = df.groupby("symbol").apply(
            lambda x: x.ffill().bfill()
        ).reset_index(drop=True)
        
        return df
    
    async def _apply_single_operation(self, df: pd.DataFrame, operation: Dict[str, Any]) -> pd.DataFrame:
        """Apply a single pandas operation."""
        op_type = operation.get("type")
        params = operation.get("params", {})
        
        if op_type == "drop_duplicates":
            subset = params.get("subset", ["symbol", "date"])
            df = df.drop_duplicates(subset=subset)
            
        elif op_type == "sort":
            by = params.get("by", ["symbol", "date"])
            ascending = params.get("ascending", True)
            df = df.sort_values(by=by, ascending=ascending)
            
        elif op_type == "fillna":
            method = params.get("method", "ffill")
            if method == "ffill":
                df = df.ffill()
            elif method == "bfill":
                df = df.bfill()
            elif method == "value":
                value = params.get("value", 0)
                df = df.fillna(value)
            elif method == "mean":
                df = df.fillna(df.mean(numeric_only=True))
            elif method == "median":
                df = df.fillna(df.median(numeric_only=True))
                
        elif op_type == "dropna":
            subset = params.get("subset")
            if subset:
                df = df.dropna(subset=subset)
            else:
                df = df.dropna()
                
        elif op_type == "rename_columns":
            mapping = params.get("mapping", {})
            df = df.rename(columns=mapping)
            
        elif op_type == "add_column":
            column = params.get("column")
            value = params.get("value")
            expression = params.get("expression")
            
            if column:
                if value is not None:
                    df[column] = value
                elif expression:
                    # Simple expression evaluation (be careful with security!)
                    df[column] = df.eval(expression)
                    
        elif op_type == "remove_column":
            columns = params.get("columns", [])
            if isinstance(columns, str):
                columns = [columns]
            df = df.drop(columns=columns, errors="ignore")
            
        elif op_type == "filter":
            condition = params.get("condition")
            if condition:
                df = df.query(condition)
                
        elif op_type == "groupby_agg":
            groupby = params.get("groupby", ["symbol"])
            aggregations = params.get("aggregations", {})
            
            if aggregations:
                df = df.groupby(groupby).agg(aggregations).reset_index()
                
        elif op_type == "calculate_technical_indicators":
            df = await self._calculate_technical_indicators(df, params)
            
        elif op_type == "custom_function":
            module = params.get("module")
            function = params.get("function")
            
            if module and function:
                try:
                    import importlib
                    mod = importlib.import_module(module)
                    func = getattr(mod, function)
                    df = await asyncio.to_thread(func, df)
                except Exception as e:
                    raise RuntimeError(f"Failed to execute custom function: {str(e)}")
        
        return df
    
    async def _calculate_technical_indicators(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Calculate technical indicators."""
        if df.empty:
            return df
        
        # Group by symbol for calculation
        result_dfs = []
        
        for symbol, group in df.groupby("symbol"):
            symbol_df = group.copy()
            symbol_df = symbol_df.sort_values("date")
            
            # Calculate moving averages
            ma_periods = params.get("moving_averages", [5, 10, 20, 60])
            for period in ma_periods:
                if len(symbol_df) >= period:
                    symbol_df[f"ma{period}"] = symbol_df["close"].rolling(window=period).mean()
            
            # Calculate RSI
            rsi_period = params.get("rsi_period", 14)
            if len(symbol_df) >= rsi_period:
                delta = symbol_df["close"].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
                rs = gain / loss
                symbol_df["rsi"] = 100 - (100 / (1 + rs))
            
            # Calculate MACD
            if len(symbol_df) >= 26:
                exp1 = symbol_df["close"].ewm(span=12, adjust=False).mean()
                exp2 = symbol_df["close"].ewm(span=26, adjust=False).mean()
                symbol_df["macd"] = exp1 - exp2
                symbol_df["macd_signal"] = symbol_df["macd"].ewm(span=9, adjust=False).mean()
                symbol_df["macd_hist"] = symbol_df["macd"] - symbol_df["macd_signal"]
            
            # Calculate Bollinger Bands
            bb_period = params.get("bollinger_period", 20)
            bb_std = params.get("bollinger_std", 2)
            if len(symbol_df) >= bb_period:
                symbol_df["bb_middle"] = symbol_df["close"].rolling(window=bb_period).mean()
                symbol_df["bb_std"] = symbol_df["close"].rolling(window=bb_period).std()
                symbol_df["bb_upper"] = symbol_df["bb_middle"] + (symbol_df["bb_std"] * bb_std)
                symbol_df["bb_lower"] = symbol_df["bb_middle"] - (symbol_df["bb_std"] * bb_std)
            
            result_dfs.append(symbol_df)
        
        if result_dfs:
            return pd.concat(result_dfs, ignore_index=True)
        return df
    
    def get_available_operations(self) -> List[Dict[str, Any]]:
        """Get list of available pandas operations."""
        return [
            {
                "type": "drop_duplicates",
                "description": "Remove duplicate rows",
                "params": {
                    "subset": "List of column names to consider for duplicates"
                }
            },
            {
                "type": "sort",
                "description": "Sort DataFrame by columns",
                "params": {
                    "by": "Column or list of columns to sort by",
                    "ascending": "Sort ascending (True) or descending (False)"
                }
            },
            {
                "type": "fillna",
                "description": "Fill missing values",
                "params": {
                    "method": "Fill method: ffill, bfill, value, mean, median",
                    "value": "Value to fill (if method is 'value')"
                }
            },
            {
                "type": "dropna",
                "description": "Drop rows with missing values",
                "params": {
                    "subset": "List of columns to consider for missing values"
                }
            },
            {
                "type": "rename_columns",
                "description": "Rename DataFrame columns",
                "params": {
                    "mapping": "Dictionary mapping old column names to new ones"
                }
            },
            {
                "type": "add_column",
                "description": "Add new column to DataFrame",
                "params": {
                    "column": "New column name",
                    "value": "Constant value for the column",
                    "expression": "Pandas expression to calculate column values"
                }
            },
            {
                "type": "remove_column",
                "description": "Remove columns from DataFrame",
                "params": {
                    "columns": "List of column names to remove"
                }
            },
            {
                "type": "filter",
                "description": "Filter rows based on condition",
                "params": {
                    "condition": "Pandas query expression"
                }
            },
            {
                "type": "groupby_agg",
                "description": "Group by and aggregate data",
                "params": {
                    "groupby": "List of columns to group by",
                    "aggregations": "Dictionary of column-aggregation pairs"
                }
            },
            {
                "type": "calculate_technical_indicators",
                "description": "Calculate technical indicators",
                "params": {
                    "moving_averages": "List of periods for moving averages",
                    "rsi_period": "Period for RSI calculation",
                    "bollinger_period": "Period for Bollinger Bands",
                    "bollinger_std": "Standard deviation multiplier for Bollinger Bands"
                }
            },
            {
                "type": "custom_function",
                "description": "Apply custom Python function",
                "params": {
                    "module": "Python module containing the function",
                    "function": "Function name to apply"
                }
            }
        ]
