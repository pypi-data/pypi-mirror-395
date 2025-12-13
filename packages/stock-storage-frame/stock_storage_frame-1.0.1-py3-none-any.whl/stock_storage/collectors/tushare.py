"""
Tushare collector implementation.
"""

import asyncio
from datetime import date, datetime
from typing import List, Dict, Any
import pandas as pd

from .base import BaseCollector
from ..models import BatchStockData, StockData, CollectorConfig, CollectorType


class TushareCollector(BaseCollector):
    """Collector for Tushare data source."""
    
    def __init__(self, config: CollectorConfig):
        super().__init__(config)
        self.token = config.config.get("token", "")
        self.retry_times = config.config.get("retry_times", 3)
        self.timeout = config.config.get("timeout", 30)
        self.method = config.method

        if not self.token:
            raise ValueError("Tushare token is required in configuration")
        
        # Initialize tushare pro
        self._init_tushare()
    
    def _init_tushare(self):
        """Initialize Tushare Pro."""
        try:
            import tushare as ts
            ts.set_token(self.token)
            self.pro = ts.pro_api()
        except ImportError:
            raise ImportError(
                "Tushare is not installed. Please install it with: "
                "pip install tushare or pip install stock-storage-frame[tushare]"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Tushare: {str(e)}")
    
    def get_required_config_fields(self) -> List[str]:
        """Get required configuration fields."""
        return ["token"]
    
    async def collect(self, **kwargs) -> pd.DataFrame:
        """
        Collect stock data using Tushare.
        
        Args:
            **kwargs: Dynamic parameters from workflow config
            
        Returns:
            pandas DataFrame containing collected data
        """
        try:
            import tushare as ts
        except ImportError:
            raise ImportError("Tushare is not installed.")
        
        # Get method from kwargs or instance config
        method_name = kwargs.get("method", self.method)
        
        # Ensure method_name is a string
        if not method_name or not isinstance(method_name, str):
            raise ValueError(f"Method name must be a string, got: {method_name}")
        
        # Check if method exists in tushare
        if not hasattr(self.pro, method_name):
            raise AttributeError(
                f"Tushare has no method named '{method_name}'. "
                f"Available methods: {[m for m in dir(self.pro) if not m.startswith('_')][:10]}..."
            )
        
        method = getattr(self.pro, method_name)
        result_df = pd.DataFrame()
        
        # Remove method from kwargs before passing to tushare method
        tushare_kwargs = kwargs.copy()
        tushare_kwargs.pop("method", None)
        
        for attempt in range(self.retry_times):
            try:
                # Call the method
                result_df = await asyncio.to_thread(method, **tushare_kwargs)
                break  # Success, break out of retry loop
            except Exception as e:
                if attempt == self.retry_times - 1:
                    raise RuntimeError(
                        f"Failed to collect data "
                        f"after {self.retry_times} attempts: {str(e)}"
                    )
                await asyncio.sleep(1)  # Wait before retry
        
        return result_df
