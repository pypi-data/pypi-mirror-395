"""
Factory classes for creating collectors, processors, and storages.
"""

from typing import Dict, Any, Type, Optional
import importlib

from .models import (
    CollectorConfig,
    ProcessorConfig,
    StorageConfig,
    ConditionConfig,
    CollectorType,
    StorageType,
)
from .collectors import BaseCollector, AkshareCollector, TushareCollector, CustomCollector
from .processors import BaseProcessor, PandasProcessor, CustomProcessor
from .storages import BaseStorage, SQLiteStorage, MySQLStorage, CSVStorage
from .conditions import BaseCondition, CustomCondition


class CollectorFactory:
    """Factory for creating collector instances."""
    
    _registry: Dict[CollectorType, Type[BaseCollector]] = {
        CollectorType.AKSHAKE: AkshareCollector,
        CollectorType.TUSHARE: TushareCollector,
        CollectorType.CUSTOM: CustomCollector,
    }
    
    @classmethod
    def register_collector(cls, collector_type: CollectorType, collector_class: Type[BaseCollector]) -> None:
        """
        Register a new collector type.
        
        Args:
            collector_type: Type of collector
            collector_class: Collector class
        """
        cls._registry[collector_type] = collector_class
    
    @classmethod
    def create(cls, config: CollectorConfig) -> BaseCollector:
        """
        Create a collector instance.
        
        Args:
            config: Collector configuration
            
        Returns:
            Collector instance
            
        Raises:
            ValueError: If collector type is not supported
        """
        collector_class = cls._registry.get(config.type)
        
        if collector_class is None:
            raise ValueError(f"Unsupported collector type: {config.type}")
        
        return collector_class(config)
    
    @classmethod
    def get_supported_types(cls) -> Dict[CollectorType, str]:
        """
        Get supported collector types and their descriptions.
        
        Returns:
            Dictionary of collector types and descriptions
        """
        return {
            CollectorType.AKSHAKE: "Akshare data collector for Chinese stock market",
            CollectorType.TUSHARE: "Tushare data collector for Chinese stock market",
            CollectorType.CUSTOM: "Custom collector (requires registration)",
        }
    
    @classmethod
    def create_from_dict(cls, config_dict: Dict[str, Any]) -> BaseCollector:
        """
        Create collector from dictionary configuration.
        
        Args:
            config_dict: Collector configuration dictionary
            
        Returns:
            Collector instance
        """
        config = CollectorConfig(**config_dict)
        return cls.create(config)


class ProcessorFactory:
    """Factory for creating processor instances."""
    
    _registry: Dict[str, Type[BaseProcessor]] = {
        "pandas": PandasProcessor,
        "custom": CustomProcessor,
    }
    
    @classmethod
    def register_processor(cls, processor_type: str, processor_class: Type[BaseProcessor]) -> None:
        """
        Register a new processor type.
        
        Args:
            processor_type: Type of processor
            processor_class: Processor class
        """
        cls._registry[processor_type] = processor_class
    
    @classmethod
    def create(cls, config: Optional[ProcessorConfig] = None) -> BaseProcessor:
        """
        Create a processor instance.
        
        Args:
            config: Processor configuration
            
        Returns:
            Processor instance
        """
        if config is None:
            # Default to pandas processor
            return PandasProcessor()
        
        # Determine processor type based on configuration
        if config.script or config.module:
            processor_type = "custom"
        else:
            processor_type = "pandas"
        
        processor_class = cls._registry.get(processor_type)
        
        if processor_class is None:
            raise ValueError(f"Unsupported processor type: {processor_type}")
        
        return processor_class(config)
    
    @classmethod
    def get_supported_types(cls) -> Dict[str, str]:
        """
        Get supported processor types and their descriptions.
        
        Returns:
            Dictionary of processor types and descriptions
        """
        return {
            "pandas": "Pandas-based data processing with built-in operations",
            "custom": "Custom Python script or module for data processing",
        }
    
    @classmethod
    def create_from_dict(cls, config_dict: Optional[Dict[str, Any]] = None) -> BaseProcessor:
        """
        Create processor from dictionary configuration.
        
        Args:
            config_dict: Processor configuration dictionary
            
        Returns:
            Processor instance
        """
        config = ProcessorConfig(**config_dict) if config_dict else None
        return cls.create(config)


class StorageFactory:
    """Factory for creating storage instances."""
    
    _registry: Dict[StorageType, Type[BaseStorage]] = {
        StorageType.SQLITE: SQLiteStorage,
        StorageType.MYSQL: MySQLStorage,
        StorageType.CSV: CSVStorage,
    }
    
    @classmethod
    def register_storage(cls, storage_type: StorageType, storage_class: Type[BaseStorage]) -> None:
        """
        Register a new storage type.
        
        Args:
            storage_type: Type of storage
            storage_class: Storage class
        """
        cls._registry[storage_type] = storage_class
    
    @classmethod
    def create(cls, config: StorageConfig) -> BaseStorage:
        """
        Create a storage instance.
        
        Args:
            config: Storage configuration
            
        Returns:
            Storage instance
            
        Raises:
            ValueError: If storage type is not supported
        """
        storage_class = cls._registry.get(config.type)
        
        if storage_class is None:
            raise ValueError(f"Unsupported storage type: {config.type}")
        
        return storage_class(config)
    
    @classmethod
    def get_supported_types(cls) -> Dict[StorageType, str]:
        """
        Get supported storage types and their descriptions.
        
        Returns:
            Dictionary of storage types and descriptions
        """
        return {
            StorageType.SQLITE: "SQLite database (local file-based)",
            StorageType.MYSQL: "MySQL database",
            StorageType.POSTGRESQL: "PostgreSQL database (requires registration)",
            StorageType.CSV: "CSV file storage",
            StorageType.PARQUET: "Parquet file storage (requires registration)",
            StorageType.CUSTOM: "Custom storage (requires registration)",
        }
    
    @classmethod
    def create_from_dict(cls, config_dict: Dict[str, Any]) -> BaseStorage:
        """
        Create storage from dictionary configuration.
        
        Args:
            config_dict: Storage configuration dictionary
            
        Returns:
            Storage instance
        """
        config = StorageConfig(**config_dict)
        return cls.create(config)


class ConditionFactory:
    """Factory for creating condition instances."""
    
    _registry: Dict[str, Type[BaseCondition]] = {
        "custom": CustomCondition,
    }
    
    @classmethod
    def register_condition(cls, condition_type: str, condition_class: Type[BaseCondition]) -> None:
        """
        Register a new condition type.
        
        Args:
            condition_type: Type of condition
            condition_class: Condition class
        """
        cls._registry[condition_type] = condition_class
    
    @classmethod
    def create(cls, config: Optional[ConditionConfig] = None) -> BaseCondition:
        """
        Create a condition instance.
        
        Args:
            config: Condition configuration
            
        Returns:
            Condition instance
        """
        if config is None:
            # Default condition that always returns True
            from .conditions.base import BaseCondition as BaseConditionClass
            class DefaultCondition(BaseConditionClass):
                def __init__(self):
                    pass
                
                async def check(self) -> bool:
                    return True
            return DefaultCondition()
        
        # Determine condition type based on configuration
        if config.script or config.module:
            condition_type = "custom"
        else:
            # Default condition that always returns True
            from .conditions.base import BaseCondition as BaseConditionClass
            class DefaultCondition(BaseConditionClass):
                def __init__(self, config):
                    super().__init__(config)
                
                async def check(self) -> bool:
                    return True
            return DefaultCondition(config)
        
        condition_class = cls._registry.get(condition_type)
        
        if condition_class is None:
            raise ValueError(f"Unsupported condition type: {condition_type}")
        
        return condition_class(config)
    
    @classmethod
    def get_supported_types(cls) -> Dict[str, str]:
        """
        Get supported condition types and their descriptions.
        
        Returns:
            Dictionary of condition types and descriptions
        """
        return {
            "custom": "Custom Python script or module for condition checking",
        }
    
    @classmethod
    def create_from_dict(cls, config_dict: Optional[Dict[str, Any]] = None) -> BaseCondition:
        """
        Create condition from dictionary configuration.
        
        Args:
            config_dict: Condition configuration dictionary
            
        Returns:
            Condition instance
        """
        config = ConditionConfig(**config_dict) if config_dict else None
        return cls.create(config)


class ComponentManager:
    """Manager for creating and managing all components."""
    
    def __init__(self):
        self.collector_factory = CollectorFactory()
        self.processor_factory = ProcessorFactory()
        self.storage_factory = StorageFactory()
        self.condition_factory = ConditionFactory()
    
    def create_collector(self, config: CollectorConfig) -> BaseCollector:
        """Create a collector instance."""
        return self.collector_factory.create(config)
    
    def create_processor(self, config: Optional[ProcessorConfig] = None) -> BaseProcessor:
        """Create a processor instance."""
        return self.processor_factory.create(config)
    
    def create_storage(self, config: StorageConfig) -> BaseStorage:
        """Create a storage instance."""
        return self.storage_factory.create(config)
    
    def create_condition(self, config: Optional[ConditionConfig] = None) -> BaseCondition:
        """Create a condition instance."""
        return self.condition_factory.create(config)
    
    def get_component_info(self) -> Dict[str, Any]:
        """Get information about all supported components."""
        return {
            "collectors": self.collector_factory.get_supported_types(),
            "processors": self.processor_factory.get_supported_types(),
            "storages": self.storage_factory.get_supported_types(),
            "conditions": self.condition_factory.get_supported_types(),
        }
    
    @classmethod
    def load_plugin(cls, plugin_module: str) -> None:
        """
        Load a plugin module to register additional components.
        
        Args:
            plugin_module: Python module containing plugin definitions
        """
        try:
            module = importlib.import_module(plugin_module)
            
            # Register collectors
            if hasattr(module, "register_collectors"):
                module.register_collectors(CollectorFactory)
            
            # Register processors
            if hasattr(module, "register_processors"):
                module.register_processors(ProcessorFactory)
            
            # Register storages
            if hasattr(module, "register_storages"):
                module.register_storages(StorageFactory)
            
            # Register conditions
            if hasattr(module, "register_conditions"):
                module.register_conditions(ConditionFactory)
                
        except ImportError as e:
            raise ImportError(f"Failed to load plugin module {plugin_module}: {str(e)}")
