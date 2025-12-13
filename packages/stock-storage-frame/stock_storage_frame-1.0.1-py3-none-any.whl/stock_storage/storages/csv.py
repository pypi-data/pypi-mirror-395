"""
CSV storage implementation.
"""

import asyncio
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import date, datetime
import pandas as pd

from .base import BaseStorage
from ..models import BatchStockData, StockData, StorageConfig, StorageType


class CSVStorage(BaseStorage):
    """Storage implementation for CSV files."""
    
    def __init__(self, config: StorageConfig):
        super().__init__(config)
        self.directory = config.config.get("directory", "./data/csv")
        self.encoding = config.config.get("encoding", "utf-8")
        
        # Ensure directory exists
        Path(self.directory).mkdir(parents=True, exist_ok=True)
    
    def get_required_config_fields(self) -> List[str]:
        """Get required configuration fields."""
        return ["directory"]
    
    async def connect(self) -> None:
        """Connect to CSV storage (no-op for CSV)."""
        pass
    
    async def disconnect(self) -> None:
        """Disconnect from CSV storage (no-op for CSV)."""
        pass
    
    def _get_file_path(self, table_name: str) -> Path:
        """Get file path for a table."""
        return Path(self.directory) / f"{table_name}.csv"
    
    async def save(self, data: pd.DataFrame, table_name: str, **kwargs) -> int:
        """
        Save stock data to CSV file.
        
        Args:
            data: pandas DataFrame containing stock data
            table_name: Name of the table to save to
            **kwargs: Additional parameters
            
        Returns:
            Number of records saved
        """
        file_path = self._get_file_path(table_name)
        
        if data.empty:
            return 0
        
        # Check if file exists
        if file_path.exists():
            # Load existing data
            existing_df = pd.read_csv(file_path)
            
            # Remove duplicates (keep new data)
            combined_df = pd.concat([existing_df, data])
            combined_df = combined_df.drop_duplicates(
                subset=["symbol", "date"],
                keep="last"
            )
        else:
            combined_df = data
        
        # Save to CSV
        combined_df.to_csv(file_path, index=False, encoding=self.encoding)
        
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
        Load stock data from CSV file.
        
        Args:
            table_name: Name of the table to load from
            symbols: List of stock symbols to filter by
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional parameters
            
        Returns:
            Loaded pandas DataFrame
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            return pd.DataFrame()
        
        # Load CSV file
        df = pd.read_csv(file_path, encoding=self.encoding)
        
        if df.empty:
            return df
        
        # Apply filters
        if symbols:
            df = df[df["symbol"].isin(symbols)]
        
        if start_date:
            df = df[pd.to_datetime(df["date"]) >= pd.Timestamp(start_date)]
        
        if end_date:
            df = df[pd.to_datetime(df["date"]) <= pd.Timestamp(end_date)]
        
        # Convert date column from string to date object if present
        if 'date' in df.columns and df['date'].dtype == 'object':
            try:
                df['date'] = pd.to_datetime(df['date']).dt.date
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
        Delete stock data from CSV file.
        
        Args:
            table_name: Name of the table to delete from
            symbols: List of stock symbols to filter by
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional parameters
            
        Returns:
            Number of records deleted
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            return 0
        
        # Load existing data
        df = pd.read_csv(file_path, encoding=self.encoding)
        
        if df.empty:
            return 0
        
        # Create filter mask
        mask = pd.Series([True] * len(df))
        
        if symbols:
            mask = mask & df["symbol"].isin(symbols)
        
        if start_date:
            mask = mask & (pd.to_datetime(df["date"]) >= pd.Timestamp(start_date))
        
        if end_date:
            mask = mask & (pd.to_datetime(df["date"]) <= pd.Timestamp(end_date))
        
        # Count records to delete
        delete_count = mask.sum()
        
        if delete_count > 0:
            # Keep records that don't match the filter
            df = df[~mask]
            
            # Save updated data
            if not df.empty:
                df.to_csv(file_path, index=False, encoding=self.encoding)
            else:
                # Delete file if empty
                file_path.unlink()
        
        return delete_count
    
    async def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get information about a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing table information
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            return {
                "table_name": table_name,
                "exists": False,
                "file_path": str(file_path),
            }
        
        # Load CSV file
        df = pd.read_csv(file_path, encoding=self.encoding)
        
        if df.empty:
            return {
                "table_name": table_name,
                "exists": True,
                "file_path": str(file_path),
                "row_count": 0,
                "columns": [],
                "date_range": {"min": None, "max": None},
                "symbol_count": 0,
            }
        
        # Get date range
        if "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            min_date = dates.min().date()
            max_date = dates.max().date()
        else:
            min_date = max_date = None
        
        # Get unique symbols
        symbol_count = df["symbol"].nunique() if "symbol" in df.columns else 0
        
        return {
            "table_name": table_name,
            "exists": True,
            "file_path": str(file_path),
            "row_count": len(df),
            "columns": df.columns.tolist(),
            "date_range": {
                "min": min_date.isoformat() if min_date else None,
                "max": max_date.isoformat() if max_date else None,
            },
            "symbol_count": symbol_count,
            "file_size": file_path.stat().st_size,
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
        }
    
    
    async def drop_table(self, table_name: str) -> None:
        """
        Drop a table.
        
        Args:
            table_name: Name of the table to drop
        """
        file_path = self._get_file_path(table_name)
        
        if file_path.exists():
            file_path.unlink()
    
    async def list_tables(self) -> List[str]:
        """
        List all tables in the directory.
        
        Returns:
            List of table names
        """
        directory = Path(self.directory)
        
        if not directory.exists():
            return []
        
        tables = []
        for file_path in directory.glob("*.csv"):
            table_name = file_path.stem
            tables.append(table_name)
        
        return tables
    
    async def export_to_excel(self, table_name: str, excel_path: str) -> None:
        """
        Export CSV table to Excel file.
        
        Args:
            table_name: Name of the table to export
            excel_path: Path to save the Excel file
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Table {table_name} not found")
        
        df = pd.read_csv(file_path, encoding=self.encoding)
        df.to_excel(excel_path, index=False)
    
    async def import_from_excel(self, table_name: str, excel_path: str) -> int:
        """
        Import data from Excel file to CSV table.
        
        Args:
            table_name: Name of the table to import to
            excel_path: Path to the Excel file
            
        Returns:
            Number of records imported
        """
        if not Path(excel_path).exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
        
        df = pd.read_excel(excel_path)
        
        if df.empty:
            return 0
        
        # Save to CSV
        file_path = self._get_file_path(table_name)
        df.to_csv(file_path, index=False, encoding=self.encoding)
        
        return len(df)
    
    async def merge_tables(self, source_table: str, target_table: str) -> int:
        """
        Merge data from source table to target table.
        
        Args:
            source_table: Source table name
            target_table: Target table name
            
        Returns:
            Number of records merged
        """
        source_path = self._get_file_path(source_table)
        target_path = self._get_file_path(target_table)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source table {source_table} not found")
        
        # Load source data
        source_df = pd.read_csv(source_path, encoding=self.encoding)
        
        if source_df.empty:
            return 0
        
        if target_path.exists():
            # Load target data
            target_df = pd.read_csv(target_path, encoding=self.encoding)
            
            # Merge data
            combined_df = pd.concat([target_df, source_df])
            combined_df = combined_df.drop_duplicates(
                subset=["symbol", "date"],
                keep="last"
            )
        else:
            combined_df = source_df
        
        # Save merged data
        combined_df.to_csv(target_path, index=False, encoding=self.encoding)
        
        return len(source_df)
