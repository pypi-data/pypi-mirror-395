"""
Custom processor implementation for executing user-defined Python scripts.
"""

import asyncio
import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, Optional
import pandas as pd

from .base import BaseProcessor
from ..models import BatchStockData, ProcessorConfig


class CustomProcessor(BaseProcessor):
    """Processor for executing custom Python scripts."""
    
    def __init__(self, config: Optional[ProcessorConfig] = None):
        super().__init__(config)
        self.script_path = config.script if config else None
        self.module_name = config.module if config else None
        self.function_name = config.function if config else None
        
        if not self.script_path and not self.module_name:
            raise ValueError("Either script path or module name must be provided")
        
        if self.module_name and not self.function_name:
            raise ValueError("Function name must be provided when using module")
    
    async def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process stock data using custom Python script or module.
        
        Args:
            data: Input pandas DataFrame
            
        Returns:
            Processed pandas DataFrame
        """
        if self.script_path:
            return await self._process_with_script(data)
        else:
            return await self._process_with_module(data)
    
    async def _process_with_script(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data using a Python script file."""
        script_path = Path(self.script_path)
        
        if not script_path.exists():
            raise FileNotFoundError(f"Script file not found: {self.script_path}")
        
        # Load the script as a module
        module_name = f"custom_processor_{hash(str(script_path))}"
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        
        if spec is None or spec.loader is None:
            raise ImportError(f"Failed to load script: {self.script_path}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise RuntimeError(f"Failed to execute script {self.script_path}: {str(e)}")
        
        # Look for a process function
        if hasattr(module, "process"):
            process_func = module.process
        else:
            # Try to find any function that takes a DataFrame and returns a DataFrame
            process_func = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and not attr_name.startswith("_"):
                    # Check if it might be a processing function
                    try:
                        # Test with a small sample
                        test_df = data.head(1) if not data.empty else pd.DataFrame()
                        result = attr(test_df)
                        if isinstance(result, pd.DataFrame):
                            process_func = attr
                            break
                    except:
                        continue
            
            if process_func is None:
                raise RuntimeError(
                    f"No suitable process function found in script {self.script_path}. "
                    "The script should define a function named 'process' that takes a "
                    "DataFrame and returns a DataFrame."
                )
        
        # Execute the process function
        try:
            processed_df = await asyncio.to_thread(process_func, data)
            
            if not isinstance(processed_df, pd.DataFrame):
                raise TypeError(
                    f"Process function should return a DataFrame, got {type(processed_df)}"
                )
            
            return processed_df
            
        except Exception as e:
            raise RuntimeError(f"Failed to process data with custom script: {str(e)}")
    
    async def _process_with_module(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data using a Python module and function."""
        try:
            module = importlib.import_module(self.module_name)
        except ImportError as e:
            raise ImportError(f"Failed to import module {self.module_name}: {str(e)}")
        
        if not hasattr(module, self.function_name):
            raise AttributeError(
                f"Module {self.module_name} has no function named {self.function_name}"
            )
        
        process_func = getattr(module, self.function_name)
        
        if not callable(process_func):
            raise TypeError(
                f"{self.function_name} in module {self.module_name} is not callable"
            )
        
        # Execute the process function
        try:
            processed_df = await asyncio.to_thread(process_func, data)
            
            if not isinstance(processed_df, pd.DataFrame):
                raise TypeError(
                    f"Process function should return a DataFrame, got {type(processed_df)}"
                )
            
            return processed_df
            
        except Exception as e:
            raise RuntimeError(f"Failed to process data with custom module: {str(e)}")
    
    def validate_script(self) -> bool:
        """
        Validate the custom script/module without executing it.
        
        Returns:
            True if validation successful, False otherwise
        """
        try:
            if self.script_path:
                script_path = Path(self.script_path)
                if not script_path.exists():
                    return False
                
                # Try to load the module
                module_name = f"custom_processor_{hash(str(script_path))}"
                spec = importlib.util.spec_from_file_location(module_name, script_path)
                return spec is not None and spec.loader is not None
            else:
                # Try to import the module
                importlib.import_module(self.module_name)
                return True
        except:
            return False
    
    def get_script_info(self) -> Dict[str, Any]:
        """
        Get information about the custom script/module.
        
        Returns:
            Dictionary containing script information
        """
        info = {
            "type": "script" if self.script_path else "module",
            "config": self.config.dict() if self.config else {},
        }
        
        if self.script_path:
            script_path = Path(self.script_path)
            info.update({
                "script_path": str(self.script_path),
                "exists": script_path.exists(),
                "size": script_path.stat().st_size if script_path.exists() else 0,
                "modified": script_path.stat().st_mtime if script_path.exists() else 0,
            })
        else:
            info.update({
                "module": self.module_name,
                "function": self.function_name,
            })
        
        return info
