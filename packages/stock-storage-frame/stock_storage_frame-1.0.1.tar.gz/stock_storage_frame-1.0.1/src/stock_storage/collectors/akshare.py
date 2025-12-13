"""
Akshare collector implementation.
"""

import asyncio
from datetime import date, datetime
from typing import List, Dict, Any
import pandas as pd

from .base import BaseCollector
from ..models import BatchStockData, StockData, CollectorConfig, CollectorType


class AkshareCollector(BaseCollector):
    """Collector for Akshare data source."""
    
    def __init__(self, config: CollectorConfig):
        super().__init__(config)
        self.timeout = config.config.get("timeout", 30)
        self.retry_times = config.config.get("retry_times", 3)
        self.method = config.method or "stock_zh_a_hist"  # Default method
    
    def get_required_config_fields(self) -> List[str]:
        """Get required configuration fields."""
        return []  # Akshare doesn't require specific config fields
    
    async def collect(self, **kwargs) -> pd.DataFrame:
        """
        Collect stock data using Akshare.
        
        Args:
            **kwargs: Dynamic parameters from workflow config
            
        Returns:
            pandas DataFrame containing collected data
        """
        try:
            import akshare as ak
        except ImportError:
            raise ImportError(
                "Akshare is not installed. Please install it with: "
                "pip install akshare or pip install stock-storage-frame[akshare]"
            )
        
         # Get method from kwargs or instance config
        method_name = kwargs.get("method", self.method)
        
        # Check if method exists in akshare
        if not hasattr(ak, method_name):
            raise AttributeError(
                f"Akshare has no method named '{method_name}'. "
                f"Available methods: {[m for m in dir(ak) if not m.startswith('_')][:10]}..."
            )
        
        method = getattr(ak, method_name)
        result_df = pd.DataFrame()
        
        # Remove method parameter from kwargs before passing to akshare method
        akshare_kwargs = kwargs.copy()
        akshare_kwargs.pop("method", None)
        
        for attempt in range(self.retry_times):
            try:
                # Call the method
                result_df = await asyncio.to_thread(method, **akshare_kwargs)
                break  # Success, break out of retry loop
            except Exception as e:
                if attempt == self.retry_times - 1:
                    raise RuntimeError(
                        f"Failed to collect data "
                        f"after {self.retry_times} attempts: {str(e)}"
                    )
                await asyncio.sleep(1)  # Wait before retry
        
        return result_df
