"""
SQLite storage implementation.
"""

import asyncio
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import date, datetime
import pandas as pd

from .base import BaseStorage
from ..models import BatchStockData, StockData, StorageConfig, StorageType


class SQLiteStorage(BaseStorage):
    """Storage implementation for SQLite database."""
    
    def __init__(self, config: StorageConfig):
        super().__init__(config)
        self.database = config.config.get("database", "./data/stock_data.db")
        self.connection = None
    
    def get_required_config_fields(self) -> List[str]:
        """Get required configuration fields."""
        return ["database"]
    
    async def connect(self) -> None:
        """Connect to SQLite database."""
        # Ensure directory exists
        db_path = Path(self.database)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create connection
        self.connection = sqlite3.connect(self.database)
        self.connection.row_factory = sqlite3.Row
    
    async def disconnect(self) -> None:
        """Disconnect from SQLite database."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    async def save(self, data: pd.DataFrame, table_name: str, **kwargs) -> int:
        """
        Save stock data to SQLite database.
        
        Args:
            data: pandas DataFrame containing stock data
            table_name: Name of the table to save to
            **kwargs: Additional parameters
            
        Returns:
            Number of records saved
        """
        if not self.connection:
            await self.connect()
        
        if data.empty:
            return 0
        
        # Simply use pandas to_sql with if_exists='replace' or 'append'
        # Let pandas handle table creation and schema
        if_exists = kwargs.get('if_exists', 'append')
        
        data.to_sql(
            table_name,
            self.connection,
            if_exists=if_exists,
            index=False,
            method="multi"
        )
        return len(data)
    
    
    async def load(
        self,
        table_name: str,
        symbols: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load stock data from SQLite database.
        
        Args:
            table_name: Name of the table to load from
            symbols: List of stock symbols to filter by
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional parameters
            
        Returns:
            Loaded pandas DataFrame
        """
        if not self.connection:
            await self.connect()
        
        # Build query - use simple approach, let pandas handle column names
        query = f"SELECT * FROM {table_name}"
        conditions = []
        params = []
        
        # Try to determine the best column names for filtering
        # We'll try common column names
        symbol_column = kwargs.get('symbol_column', 'symbol')
        date_column = kwargs.get('date_column', 'date')
        
        if symbols:
            placeholders = ", ".join(["?"] * len(symbols))
            conditions.append(f"{symbol_column} IN ({placeholders})")
            params.extend(symbols)
        
        if start_date:
            conditions.append(f"{date_column} >= ?")
            params.append(start_date.isoformat())
        
        if end_date:
            conditions.append(f"{date_column} <= ?")
            params.append(end_date.isoformat())
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Execute query and convert to DataFrame
        df = pd.read_sql_query(query, self.connection, params=params if params else None)
        
        # Convert date column from string to date object if present
        # Try common date column names
        for date_col in ['date', 'trade_date', 'timestamp']:
            if date_col in df.columns and df[date_col].dtype == 'object':
                try:
                    df[date_col] = pd.to_datetime(df[date_col]).dt.date
                except:
                    pass
        
        return df
    
    async def delete(
        self,
        table_name: str,
        symbols: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> int:
        """
        Delete stock data from SQLite database.
        
        Args:
            table_name: Name of the table to delete from
            symbols: List of stock symbols to filter by
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional parameters
            
        Returns:
            Number of records deleted
        """
        if not self.connection:
            await self.connect()
        
        # Build query
        query = f"DELETE FROM {table_name}"
        conditions = []
        params = []
        
        if symbols:
            placeholders = ", ".join(["?"] * len(symbols))
            conditions.append(f"symbol IN ({placeholders})")
            params.extend(symbols)
        
        if start_date:
            conditions.append("date >= ?")
            params.append(start_date.isoformat())
        
        if end_date:
            conditions.append("date <= ?")
            params.append(end_date.isoformat())
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Execute query
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        deleted_count = cursor.rowcount
        self.connection.commit()
        
        return deleted_count
    
    async def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get information about a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing table information
        """
        if not self.connection:
            await self.connect()
        
        # Get table schema
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        # Get date range
        cursor.execute(f"SELECT MIN(date), MAX(date) FROM {table_name}")
        min_date, max_date = cursor.fetchone()
        
        # Get unique symbols
        cursor.execute(f"SELECT COUNT(DISTINCT symbol) as symbol_count FROM {table_name}")
        symbol_count = cursor.fetchone()[0]
        
        return {
            "table_name": table_name,
            "columns": [dict(col) for col in columns],
            "row_count": row_count,
            "date_range": {
                "min": min_date,
                "max": max_date,
            },
            "symbol_count": symbol_count,
        }
    
    async def drop_table(self, table_name: str) -> None:
        """
        Drop a table.
        
        Args:
            table_name: Name of the table to drop
        """
        if not self.connection:
            await self.connect()
        
        cursor = self.connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.commit()
    
    async def list_tables(self) -> List[str]:
        """
        List all tables in the database.
        
        Returns:
            List of table names
        """
        if not self.connection:
            await self.connect()
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        return tables
    
    async def execute_query(self, query: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a custom SQL query.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            List of result rows as dictionaries
        """
        if not self.connection:
            await self.connect()
        
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    async def backup(self, backup_path: str) -> None:
        """
        Create a backup of the database.
        
        Args:
            backup_path: Path to save the backup
        """
        if not self.connection:
            await self.connect()
        
        backup_conn = sqlite3.connect(backup_path)
        self.connection.backup(backup_conn)
        backup_conn.close()
    
    
    async def vacuum(self) -> None:
        """Optimize database by vacuuming."""
        if not self.connection:
            await self.connect()
        
        cursor = self.connection.cursor()
        cursor.execute("VACUUM")
        self.connection.commit()
