"""
Custom collector for executing user-defined scripts.
"""

import asyncio
import importlib.util
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import date, datetime
import pandas as pd

from .base import BaseCollector
from ..models import CollectorConfig, BatchStockData


class CustomCollector(BaseCollector):
    """Custom collector that executes user-defined scripts."""
    
    def __init__(self, config: CollectorConfig):
        """
        Initialize custom collector.
        
        Args:
            config: Collector configuration
        """
        super().__init__(config)
        self.script_path = config.script
        self.module_name = config.module
        self.function_name = config.function
        self._validate_custom_config()
        
    def _validate_custom_config(self) -> None:
        """Validate custom collector configuration."""
        if not (self.script_path or self.module_name):
            raise ValueError("Custom collector requires either 'script' or 'module' field")
        
        if self.script_path and self.module_name:
            raise ValueError("Custom collector cannot have both 'script' and 'module' fields")
        
        if self.module_name and not self.function_name:
            raise ValueError("Custom collector with module requires 'function' field")
    
    def get_required_config_fields(self) -> List[str]:
        """
        Get list of required configuration fields.
        
        Returns:
            List of required field names
        """
        # Custom collector doesn't have fixed required fields
        # It requires either script or module+function
        return []
    
    def _load_custom_function(self, script_path):
        """
        Load custom function from script or module.
        
        Returns:
            Callable function
        """
        if script_path:
            # Load from script file
            script_path = Path(script_path)
            if not script_path.exists():
                raise FileNotFoundError(f"Script file not found: {self.script_path}")
            
            # Create a module name from the script path
            module_name = f"custom_collector_{script_path.stem}"
            
            # Load the module from file
            spec = importlib.util.spec_from_file_location(module_name, script_path)
            if spec is None:
                raise ImportError(f"Failed to load script: {script_path}")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                raise ImportError(f"Failed to execute script {self.script_path}: {str(e)}")
            
            # Look for a collect function in the module
            if hasattr(module, "collect"):
                return module.collect
            elif hasattr(module, "main"):
                return module.main
            else:
                # Try to find any function that might be the collector
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and not attr_name.startswith("_"):
                        return attr
                
                raise ValueError(f"No suitable function found in script: {self.script_path}")
        
        elif self.module_name:
            # Load from module
            try:
                module = importlib.import_module(self.module_name)
            except ImportError as e:
                raise ImportError(f"Failed to import module {self.module_name}: {str(e)}")
            
            if not self.function_name:
                raise ValueError("Function name is required when using module")
            
            if not hasattr(module, self.function_name):
                raise AttributeError(f"Module {self.module_name} has no function '{self.function_name}'")
            
            return getattr(module, self.function_name)
        
        else:
            raise ValueError("Custom collector requires either script or module configuration")
    
    async def collect(self, **kwargs) -> Any:
        """
        Collect data using custom script or module.
        
        Args:
            **kwargs: Dynamic parameters from workflow config
            
        Returns:
            Raw collected data
        """
        # Load the custom function
        script_path = kwargs.get("script", self.script_path)
        custom_func = self._load_custom_function(script_path)
        
        # Remove script parameter from kwargs before passing to script
        custom_kwargs = kwargs.copy()
        custom_kwargs.pop("script", None)

        # Prepare arguments for the custom function
        # Include collector config and any additional kwargs
        # The custom function can decide which parameters to use
        func_args = {
            "config": self.config.config,
            **custom_kwargs
        }
        
        # Execute the custom function
        try:
            if asyncio.iscoroutinefunction(custom_func):
                # Async function
                result = await custom_func(**func_args)
            else:
                # Sync function - run in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, 
                    lambda: custom_func(**func_args)
                )
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Custom collector failed: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test custom collector by trying to load the function.
        
        Returns:
            True if function can be loaded, False otherwise
        """
        try:
            self._load_custom_function()
            return True
        except Exception:
            return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get collector metadata.
        
        Returns:
            Dictionary containing metadata
        """
        metadata = super().get_metadata()
        metadata.update({
            "script": self.script_path,
            "module": self.module_name,
            "function": self.function_name,
            "custom": True,
        })
        return metadata


# Convenience function for creating custom collectors
def create_custom_collector(
    name: str,
    script: Optional[str] = None,
    module: Optional[str] = None,
    function: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> CustomCollector:
    """
    Create a custom collector instance.
    
    Args:
        name: Collector name
        script: Path to custom script
        module: Python module name
        function: Function name in module
        config: Additional configuration
        
    Returns:
        CustomCollector instance
    """
    from ..models import CollectorConfig, CollectorType
    
    collector_config = CollectorConfig(
        name=name,
        type=CollectorType.CUSTOM,
        script=script,
        module=module,
        function=function,
        config=config or {}
    )
    
    return CustomCollector(collector_config)
