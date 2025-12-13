"""
Base processor class for the stock storage framework.
"""

import abc
from typing import Any, Dict, Optional
import pandas as pd

from ..models import ProcessorConfig


class BaseProcessor(abc.ABC):
    """Base class for all processors."""
    
    def __init__(self, config: Optional[ProcessorConfig] = None):
        """
        Initialize processor with configuration.
        
        Args:
            config: Processor configuration
        """
        self.config = config or ProcessorConfig()
    
    @abc.abstractmethod
    async def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process stock data.
        
        Args:
            data: Input pandas DataFrame
            
        Returns:
            Processed pandas DataFrame
        """
        pass
    
    def process_sync(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Synchronous version of process method.
        
        Args:
            data: Input pandas DataFrame
            
        Returns:
            Processed pandas DataFrame
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.process(data))
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get processor metadata.
        
        Returns:
            Dictionary containing metadata
        """
        return {
            "config": self.config.dict() if self.config else {},
        }
