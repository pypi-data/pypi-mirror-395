"""
Base storage class for the stock storage framework.
"""

import abc
from typing import Any, Dict, List, Optional
from datetime import date, datetime
import pandas as pd

from ..models import StorageConfig


class BaseStorage(abc.ABC):
    """Base class for all storage backends."""
    
    def __init__(self, config: StorageConfig):
        """
        Initialize storage with configuration.
        
        Args:
            config: Storage configuration
        """
        self.config = config
        self.name = config.name
        self.type = config.type
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate storage configuration."""
        required_fields = self.get_required_config_fields()
        for field in required_fields:
            if field not in self.config.config:
                raise ValueError(f"Missing required config field: {field}")
    
    @abc.abstractmethod
    def get_required_config_fields(self) -> List[str]:
        """
        Get list of required configuration fields.
        
        Returns:
            List of required field names
        """
        pass
    
    @abc.abstractmethod
    async def connect(self) -> None:
        """Connect to the storage backend."""
        pass
    
    @abc.abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the storage backend."""
        pass
    
    @abc.abstractmethod
    async def save(self, data: pd.DataFrame, table_name: str, **kwargs) -> int:
        """
        Save stock data to storage.
        
        Args:
            data: pandas DataFrame to save
            table_name: Name of the table to save to
            **kwargs: Additional parameters
            
        Returns:
            Number of records saved
        """
        pass
    
    @abc.abstractmethod
    async def load(
        self,
        table_name: str,
        symbols: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load stock data from storage.
        
        Args:
            table_name: Name of the table to load from
            symbols: List of stock symbols to filter by
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional parameters
            
        Returns:
            Loaded pandas DataFrame
        """
        pass
    
    @abc.abstractmethod
    async def delete(
        self,
        table_name: str,
        symbols: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> int:
        """
        Delete stock data from storage.
        
        Args:
            table_name: Name of the table to delete from
            symbols: List of stock symbols to filter by
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional parameters
            
        Returns:
            Number of records deleted
        """
        pass
    
    @abc.abstractmethod
    async def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get information about a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing table information
        """
        pass
    
    @abc.abstractmethod
    async def drop_table(self, table_name: str) -> None:
        """
        Drop a table.
        
        Args:
            table_name: Name of the table to drop
        """
        pass
    
    @abc.abstractmethod
    async def list_tables(self) -> List[str]:
        """
        List all tables in the storage.
        
        Returns:
            List of table names
        """
        pass
    
    def save_sync(self, data: pd.DataFrame, table_name: str, **kwargs) -> int:
        """
        Synchronous version of save method.
        
        Args:
            data: pandas DataFrame to save
            table_name: Name of the table to save to
            **kwargs: Additional parameters
            
        Returns:
            Number of records saved
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.save(data, table_name, **kwargs))
    
    def load_sync(
        self,
        table_name: str,
        symbols: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Synchronous version of load method.
        
        Args:
            table_name: Name of the table to load from
            symbols: List of stock symbols to filter by
            start_date: Start date for data range
            end_date: End date for data range
            **kwargs: Additional parameters
            
        Returns:
            Loaded pandas DataFrame
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(
            self.load(table_name, symbols, start_date, end_date, **kwargs)
        )
    
    def test_connection(self) -> bool:
        """
        Test connection to storage backend.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            import asyncio
            
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            loop.run_until_complete(self.connect())
            loop.run_until_complete(self.disconnect())
            return True
        except Exception as e:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get storage metadata.
        
        Returns:
            Dictionary containing metadata
        """
        return {
            "name": self.name,
            "type": self.type.value,
            "config": self.config.config,
            "required_fields": self.get_required_config_fields(),
        }
