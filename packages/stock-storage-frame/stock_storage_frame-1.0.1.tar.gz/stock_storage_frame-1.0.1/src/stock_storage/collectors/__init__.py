"""
Collector implementations for the stock storage framework.
"""

from .base import BaseCollector
from .akshare import AkshareCollector
from .tushare import TushareCollector
from .custom import CustomCollector

__all__ = [
    "BaseCollector",
    "AkshareCollector",
    "TushareCollector",
    "CustomCollector",
]
