"""
Base collector class for the stock storage framework.
"""

import abc
from typing import Any, Dict, List, Optional
from datetime import date, datetime
import pandas as pd

from ..models import BatchStockData, CollectorConfig


class BaseCollector(abc.ABC):
    """Base class for all collectors."""
    
    def __init__(self, config: CollectorConfig):
        """
        Initialize collector with configuration.
        
        Args:
            config: Collector configuration
        """
        self.config = config
        self.name = config.name
        self.type = config.type
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate collector configuration."""
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
    async def collect(self, **kwargs) -> Any:
        """
        Collect stock data for given symbols and date range.
        
        Args:
            **kwargs: Dynamic parameters from workflow config
            
        Returns:
            Raw collected data (e.g., pandas DataFrame, dict, list, etc.)
        """
        pass
    
    def collect_sync(self, **kwargs) -> Any:
        """
        Synchronous version of collect method.
        
        Args:
            **kwargs: Dynamic parameters from workflow config
            
        Returns:
            Raw collected data (e.g., pandas DataFrame, dict, list, etc.)
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.collect(**kwargs))
    
    def test_connection(self) -> bool:
        """
        Test connection to data source.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to collect a small amount of test data
            test_symbols = ["000001"]  # Default test symbol
            today = date.today()
            yesterday = date(today.year, today.month, today.day - 1)
            
            # Adjust if yesterday is weekend/holiday
            if yesterday.weekday() >= 5:  # Saturday or Sunday
                yesterday = date(today.year, today.month, today.day - 3)
            
            result = self.collect_sync(
                symbols=test_symbols,
                start_date=yesterday,
                end_date=yesterday,
                frequency="daily"
            )
            
            # Check if result is not empty
            if hasattr(result, 'empty'):
                # pandas DataFrame
                return not result.empty
            elif hasattr(result, '__len__'):
                # List, dict, or other collection
                return len(result) > 0
            else:
                # Other types
                return result is not None
        except Exception as e:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get collector metadata.
        
        Returns:
            Dictionary containing metadata
        """
        return {
            "name": self.name,
            "type": self.type.value,
            "config": self.config.config,
            "required_fields": self.get_required_config_fields(),
        }
