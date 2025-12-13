"""
Stock Storage Frame - A configuration-driven stock data storage framework.
"""

__version__ = "1.0.1"
__author__ = "Pan Huachao"
__email__ = "tzzjchao@126.com"

from .models import (
    WorkflowConfig,
    CollectorConfig,
    ProcessorConfig,
    StorageConfig,
    AppConfig,
    CollectorType,
    StorageType,
)
from .engine import WorkflowEngine
from .factories import CollectorFactory, ProcessorFactory, StorageFactory
from .scheduler import WorkflowScheduler

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "WorkflowConfig",
    "CollectorConfig",
    "ProcessorConfig",
    "StorageConfig",
    "AppConfig",
    "CollectorType",
    "StorageType",
    "WorkflowEngine",
    "CollectorFactory",
    "ProcessorFactory",
    "StorageFactory",
    "WorkflowScheduler",
]
