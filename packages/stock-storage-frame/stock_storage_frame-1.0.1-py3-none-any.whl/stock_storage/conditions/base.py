"""
Base condition class for workflow execution conditions.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import asyncio

from ..models import ConditionConfig


class BaseCondition(ABC):
    """Base class for workflow execution conditions."""
    
    def __init__(self, config: ConditionConfig):
        """
        Initialize condition.
        
        Args:
            config: Condition configuration
        """
        self.config = config
        self.name = config.__class__.__name__
    
    @abstractmethod
    async def check(self) -> bool:
        """
        Check if condition is satisfied.
        
        Returns:
            True if condition is satisfied (workflow should execute),
            False otherwise (workflow should be skipped)
        """
        pass
    
    async def test_connection(self) -> bool:
        """
        Test connection/configuration for the condition.
        
        Returns:
            True if test passes, False otherwise
        """
        try:
            result = await self.check()
            return isinstance(result, bool)
        except Exception:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this condition.
        
        Returns:
            Dictionary with metadata
        """
        return {
            "name": self.name,
            "config": self.config.dict() if hasattr(self.config, "dict") else {},
        }
