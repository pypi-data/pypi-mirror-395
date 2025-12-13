"""
Custom condition implementation.
"""

import importlib
import inspect
from pathlib import Path
from typing import Any, Dict
import asyncio

from .base import BaseCondition
from ..models import ConditionConfig


class CustomCondition(BaseCondition):
    """Custom condition defined by a Python script or module."""
    
    def __init__(self, config: ConditionConfig):
        """
        Initialize custom condition.
        
        Args:
            config: Condition configuration
        """
        super().__init__(config)
        self.script = config.script
        self.module = config.module
        self.function = config.function or "check"
        self.custom_config = config.config or {}
        
        # Load the custom condition function
        self._condition_func = self._load_condition_function()
    
    def _load_condition_function(self):
        """Load the condition function from script or module."""
        if self.script:
            # Load from script file
            script_path = Path(self.script)
            if not script_path.exists():
                raise FileNotFoundError(f"Condition script not found: {self.script}")
            
            # Create a module from the script
            import sys
            import importlib.util
            
            spec = importlib.util.spec_from_file_location(
                f"custom_condition_{script_path.stem}", 
                script_path
            )
            if spec is None:
                raise ImportError(f"Failed to load condition script: {self.script}")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                raise ImportError(f"Failed to execute condition script {self.script}: {str(e)}")
            
            # Get the condition function
            if hasattr(module, self.function):
                return getattr(module, self.function)
            else:
                # Try to find any async function named check
                for name, obj in inspect.getmembers(module):
                    if (inspect.iscoroutinefunction(obj) or inspect.isfunction(obj)) and name == self.function:
                        return obj
                
                raise AttributeError(
                    f"Condition function '{self.function}' not found in script {self.script}"
                )
        
        elif self.module:
            # Load from module
            try:
                module = importlib.import_module(self.module)
            except ImportError as e:
                raise ImportError(f"Failed to import condition module {self.module}: {str(e)}")
            
            # Get the condition function
            if hasattr(module, self.function):
                return getattr(module, self.function)
            else:
                # Try to find any async function named check
                for name, obj in inspect.getmembers(module):
                    if (inspect.iscoroutinefunction(obj) or inspect.isfunction(obj)) and name == self.function:
                        return obj
                
                raise AttributeError(
                    f"Condition function '{self.function}' not found in module {self.module}"
                )
        
        else:
            raise ValueError("Either script or module must be specified for custom condition")
    
    async def check(self) -> bool:
        """
        Execute the custom condition function.
        
        Returns:
            Result of the condition function (should be bool)
        """
        try:
            # Call the condition function with config
            result = self._condition_func(**self.custom_config)
            
            # Handle async functions
            if inspect.iscoroutine(result):
                result = await result
            
            # Convert to bool
            if isinstance(result, bool):
                return result
            else:
                # Try to convert to bool
                return bool(result)
                
        except Exception as e:
            raise RuntimeError(f"Custom condition execution failed: {str(e)}")
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about this condition."""
        metadata = super().get_metadata()
        metadata.update({
            "type": "custom",
            "script": self.script,
            "module": self.module,
            "function": self.function,
        })
        return metadata
