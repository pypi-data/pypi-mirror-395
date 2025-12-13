"""
Workflow engine for executing data processing workflows.
"""

import asyncio
import yaml
import json
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from loguru import logger
import pandas as pd

from .models import (
    WorkflowConfig,
    CollectorConfig,
    ProcessorConfig,
    StorageConfig,
    ConditionConfig,
    ExecutionResult,
)
from .factories import ComponentManager


class WorkflowEngine:
    """Engine for executing data processing workflows."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize workflow engine.
        
        Args:
            config_path: Path to main configuration file
        """
        self.config_path = Path(config_path)
        
        # Load environment variables from .env file
        self._load_env_file()
        
        self.config = self._load_config()
        self.component_manager = ComponentManager()
        self.collectors: Dict[str, Any] = {}
        self.storages: Dict[str, Any] = {}
        
        # Initialize components from config
        self._initialize_components()
    
    def _load_env_file(self) -> None:
        """Load environment variables from .env file."""
        env_path = Path(".env")
        if env_path.exists():
            try:
                import os
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            # Parse key=value
                            if "=" in line:
                                key, value = line.split("=", 1)
                                key = key.strip()
                                value = value.strip()
                                
                                # Remove quotes if present
                                if (value.startswith('"') and value.endswith('"')) or \
                                   (value.startswith("'") and value.endswith("'")):
                                    value = value[1:-1]
                                
                                os.environ[key] = value
                                logger.debug(f"Loaded env variable: {key}")
            except Exception as e:
                logger.warning(f"Failed to load .env file: {str(e)}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load main configuration file."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return {}
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        # Process template variables (including environment variables)
        if config:
            config = self._process_template_variables(config)
        
        return config or {}
    
    def _initialize_components(self) -> None:
        """Initialize collectors and storages from configuration."""
        # Initialize collectors
        collectors_config = self.config.get("collectors", {})
        for name, collector_config in collectors_config.items():
            try:
                collector = self.component_manager.create_collector(
                    CollectorConfig(
                        name=name,
                        type=collector_config["type"],
                        script=collector_config.get("script"),
                        method=collector_config.get("method"),
                        config=collector_config.get("config", {})
                    )
                )
                self.collectors[name] = collector
                logger.info(f"Initialized collector: {name}")
            except Exception as e:
                logger.error(f"Failed to initialize collector {name}: {str(e)}")
        
        # Initialize storages
        storages_config = self.config.get("storages", {})
        for name, storage_config in storages_config.items():
            try:
                storage = self.component_manager.create_storage(
                    StorageConfig(
                        name=name,
                        type=storage_config["type"],
                        config=storage_config.get("config", {})
                    )
                )
                self.storages[name] = storage
                logger.info(f"Initialized storage: {name}")
            except Exception as e:
                logger.error(f"Failed to initialize storage {name}: {str(e)}")
    
    def load_workflow_config(self, workflow_path: str) -> WorkflowConfig:
        """
        Load workflow configuration from YAML file.
        
        Args:
            workflow_path: Path to workflow configuration file
            
        Returns:
            Workflow configuration
        """
        workflow_file = Path(workflow_path)
        
        if not workflow_file.exists():
            raise FileNotFoundError(f"Workflow file not found: {workflow_path}")
        
        with open(workflow_file, "r", encoding="utf-8") as f:
            workflow_data = yaml.safe_load(f)
        
        # Process template variables
        workflow_data = self._process_template_variables(workflow_data)
        
        # Create workflow config
        collector_data = workflow_data["collector"]
        workflow_config = WorkflowConfig(
            name=workflow_data["name"],
            description=workflow_data.get("description"),
            schedule=workflow_data.get("schedule"),
            collector=CollectorConfig(
                name=collector_data["name"],
                type=collector_data["type"],
                method=collector_data.get("method"),
                script=collector_data.get("script"),  # 添加 script 字段
                module=collector_data.get("module"),  # 添加 module 字段
                function=collector_data.get("function"),  # 添加 function 字段
                config=collector_data.get("config", {})
            ),
            processor=ProcessorConfig(
                **workflow_data.get("processor", {})
            ) if workflow_data.get("processor") else None,
            condition=ConditionConfig(
                **workflow_data.get("condition", {})
            ) if workflow_data.get("condition") else None,
            storage=StorageConfig(
                name=workflow_data["storage"]["name"],
                type=workflow_data["storage"]["type"],
                config=workflow_data["storage"].get("config", {})
            )
        )
        
        return workflow_config
    
    def _process_template_variables(self, data: Any) -> Any:
        """
        Process template variables in configuration data.
        
        Args:
            data: Configuration data
            
        Returns:
            Processed data with template variables replaced
        """
        if isinstance(data, dict):
            return {k: self._process_template_variables(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._process_template_variables(item) for item in data]
        elif isinstance(data, str):
            return self._replace_template_variables(data)
        else:
            return data
    
    def _replace_template_variables(self, value: str) -> str:
        """
        Replace template variables in string.
        
        Args:
            value: String containing template variables
            
        Returns:
            String with template variables replaced
        """
        import os
        import re
        
        # Helper function to convert user-friendly format to strftime format
        def _convert_format(fmt: str) -> str:
            """Convert YYYYMMDD-like format to strftime format."""
            if not fmt:
                return fmt
            # Trim whitespace
            fmt = fmt.strip()
            # Common conversions
            replacements = {
                'YYYY': '%Y',
                'YY': '%y',
                'MM': '%m',
                'DD': '%d',
                'HH': '%H',
                'hh': '%I',
                'mm': '%M',
                'ss': '%S',
                'YYYYMMDD': '%Y%m%d',
                'YYYY-MM-DD': '%Y-%m-%d',
                'YYYY/MM/DD': '%Y/%m/%d',
                'YYYYMMDD_HHMMSS': '%Y%m%d_%H%M%S',
                'YYYY-MM-DD HH:MM:SS': '%Y-%m-%d %H:%M:%S',
            }
            # Apply known replacements
            for pattern, replacement in replacements.items():
                if pattern in fmt:
                    fmt = fmt.replace(pattern, replacement)
            # If no replacements were made, assume it's already a strftime format
            return fmt
        
        # Pattern for template variables: {{ variable:format }} or {{ variable }}
        template_pattern = r'\{\{\s*(\w+)(?::([^}]+))?\s*\}\}'
        
        def replace_match(match):
            var_name = match.group(1)
            fmt_raw = match.group(2)
            
            if var_name == "today":
                dt = date.today()
                if fmt_raw:
                    fmt = _convert_format(fmt_raw)
                    # Convert date to datetime for strftime compatibility
                    dt_datetime = datetime.combine(dt, datetime.min.time())
                    return dt_datetime.strftime(fmt)
                else:
                    return dt.isoformat()
            
            elif var_name == "yesterday":
                dt = date.today().replace(day=date.today().day - 1)
                if fmt_raw:
                    fmt = _convert_format(fmt_raw)
                    dt_datetime = datetime.combine(dt, datetime.min.time())
                    return dt_datetime.strftime(fmt)
                else:
                    return dt.isoformat()
            
            elif var_name == "now":
                dt = datetime.now()
                if fmt_raw:
                    fmt = _convert_format(fmt_raw)
                    return dt.strftime(fmt)
                else:
                    return dt.isoformat()
            
            else:
                # Unknown variable, keep original
                return match.group(0)
        
        # Replace template variables
        value = re.sub(template_pattern, replace_match, value)
        
        # Replace environment variables (legacy format: ${VAR})
        env_pattern = r"\$\{([^}]+)\}"
        matches = re.findall(env_pattern, value)
        
        for match in matches:
            env_value = os.getenv(match, "")
            value = value.replace(f"${{{match}}}", env_value)
        
        return value
    
    async def execute_workflow(self, workflow_config: WorkflowConfig) -> ExecutionResult:
        """
        Execute a workflow.
        
        Args:
            workflow_config: Workflow configuration
            
        Returns:
            Execution result
        """
        start_time = datetime.now()
        
        try:
            logger.info(f"Starting workflow: {workflow_config.name}")
            
            # Get collector
            collector_name = workflow_config.collector.name
            if collector_name not in self.collectors:
                raise ValueError(f"Collector not found: {collector_name}")
            
            collector = self.collectors[collector_name]
            
            # Get storage
            storage_name = workflow_config.storage.name
            if storage_name not in self.storages:
                raise ValueError(f"Storage not found: {storage_name}")
            
            storage = self.storages[storage_name]
            
            # Step 1: Collect data
            logger.info("Step 1: Collecting data")
            collector_config = workflow_config.collector.config
            
            # Process template variables in config
            processed_config = self._process_template_variables(collector_config)
            
            # Convert symbols to list if it's a string
            if "symbols" in processed_config and isinstance(processed_config["symbols"], str):
                processed_config["symbols"] = [processed_config["symbols"]]
            
            # Collect data - pass all config parameters to collector
            # Collector will handle the specific parameters it needs
            # Add method from workflow config if not already in processed_config
            if workflow_config.collector.method and "method" not in processed_config:
                processed_config["method"] = workflow_config.collector.method
            
            # 增加script到workflow中，否则只有基础配置config.yml的script
            if workflow_config.collector.script and "script" not in processed_config:
                processed_config["script"] = workflow_config.collector.script
            collected_raw_data = await collector.collect(**processed_config)
            
            # Log collection results
            if hasattr(collected_raw_data, 'shape'):
                # pandas DataFrame
                logger.info(f"Collected {len(collected_raw_data)} records")
            elif hasattr(collected_raw_data, '__len__'):
                # List, dict, or other collection
                logger.info(f"Collected {len(collected_raw_data)} items")
            else:
                logger.info("Collected data")
            
            # Step 2: Process data
            processed_data = collected_raw_data
            if workflow_config.processor:
                logger.info("Step 2: Processing data")
                processor = self.component_manager.create_processor(workflow_config.processor)
                
                # Process the data (processor should handle pandas DataFrame)
                processed_data = await processor.process(collected_raw_data)
                
                # Log processing results
                if hasattr(processed_data, 'shape'):
                    logger.info(f"Processed {len(processed_data)} records")
                elif hasattr(processed_data, '__len__'):
                    logger.info(f"Processed {len(processed_data)} items")
                else:
                    logger.info("Processed data")
            
            # Step 3: Store data
            logger.info("Step 3: Storing data")
            storage_config = workflow_config.storage.config
            table_name = storage_config.get("table_name", workflow_config.name)
            
            # Connect to storage
            await storage.connect()
            
            try:
                # Remove table_name from storage_config to avoid duplicate parameter
                save_kwargs = storage_config.copy()
                save_kwargs.pop("table_name", None)
                
                # Save data
                saved_count = await storage.save(
                    processed_data,
                    table_name=table_name,
                    **save_kwargs
                )
                
                logger.info(f"Saved {saved_count} records to {table_name}")
                
                # Get table info
                table_info = await storage.get_table_info(table_name)
                
            finally:
                # Disconnect from storage
                await storage.disconnect()
            
            # Step 4: Return result
            end_time = datetime.now()
            
            # Calculate records processed
            if hasattr(processed_data, 'shape'):
                records_processed = len(processed_data)
            elif hasattr(processed_data, '__len__'):
                records_processed = len(processed_data)
            else:
                records_processed = 0
            
            result = ExecutionResult(
                workflow_name=workflow_config.name,
                success=True,
                start_time=start_time,
                end_time=end_time,
                records_processed=records_processed,
                details={
                    "collected_records": records_processed,
                    "saved_records": saved_count,
                    "table_info": table_info,
                    "collector": collector_name,
                    "storage": storage_name,
                    "table": table_name,
                }
            )
            
            logger.info(f"Workflow completed successfully: {workflow_config.name}")
            return result
            
        except Exception as e:
            end_time = datetime.now()
            logger.error(f"Workflow failed: {str(e)}")
            
            result = ExecutionResult(
                workflow_name=workflow_config.name,
                success=False,
                start_time=start_time,
                end_time=end_time,
                error_message=str(e),
                details={
                    "error_type": type(e).__name__,
                }
            )
            
            return result
    
    async def execute_workflow_file(self, workflow_path: str) -> ExecutionResult:
        """
        Execute workflow from configuration file.
        
        Args:
            workflow_path: Path to workflow configuration file
            
        Returns:
            Execution result
        """
        workflow_config = self.load_workflow_config(workflow_path)
        return await self.execute_workflow(workflow_config)
    
    async def execute_all_workflows(self, workflows_dir: str = "workflows") -> List[ExecutionResult]:
        """
        Execute all workflows in a directory.
        
        Args:
            workflows_dir: Directory containing workflow configuration files
            
        Returns:
            List of execution results
        """
        workflows_path = Path(workflows_dir)
        
        if not workflows_path.exists():
            logger.warning(f"Workflows directory not found: {workflows_dir}")
            return []
        
        # Find all YAML files in the directory
        workflow_files = list(workflows_path.glob("*.yaml")) + list(workflows_path.glob("*.yml"))
        
        if not workflow_files:
            logger.warning(f"No workflow files found in: {workflows_dir}")
            return []
        
        results = []
        
        for workflow_file in workflow_files:
            try:
                logger.info(f"Executing workflow from: {workflow_file}")
                result = await self.execute_workflow_file(str(workflow_file))
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to execute workflow {workflow_file}: {str(e)}")
                results.append(
                    ExecutionResult(
                        workflow_name=workflow_file.stem,
                        success=False,
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        error_message=str(e),
                    )
                )
        
        return results
    
    def get_workflow_status(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a workflow.
        
        Args:
            workflow_name: Name of the workflow
            
        Returns:
            Workflow status information
        """
        # This would typically query a database or file for execution history
        # For now, return basic information
        return {
            "name": workflow_name,
            "last_execution": None,
            "next_execution": None,
            "status": "unknown",
        }
    
    def validate_workflow(self, workflow_config: WorkflowConfig) -> Dict[str, Any]:
        """
        Validate workflow configuration.
        
        Args:
            workflow_config: Workflow configuration
            
        Returns:
            Validation results
        """
        errors = []
        warnings = []
        
        # Validate collector
        collector_name = workflow_config.collector.name
        if collector_name not in self.collectors:
            errors.append(f"Collector not found: {collector_name}")
        
        # Validate storage
        storage_name = workflow_config.storage.name
        if storage_name not in self.storages:
            errors.append(f"Storage not found: {storage_name}")
        
        # Validate processor script if specified
        if workflow_config.processor and workflow_config.processor.script:
            script_path = Path(workflow_config.processor.script)
            if not script_path.exists():
                errors.append(f"Processor script not found: {workflow_config.processor.script}")
        
        # Validate schedule if specified
        if workflow_config.schedule:
            try:
                from croniter import croniter
                croniter(workflow_config.schedule)
            except ImportError:
                warnings.append("croniter not installed, schedule validation skipped")
            except Exception as e:
                errors.append(f"Invalid schedule format: {str(e)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "workflow_name": workflow_config.name,
        }
    
    async def test_components(self) -> Dict[str, Any]:
        """
        Test all configured components.
        
        Returns:
            Test results
        """
        results = {
            "collectors": {},
            "storages": {},
        }
        
        # Test collectors
        for name, collector in self.collectors.items():
            try:
                success = collector.test_connection()
                results["collectors"][name] = {
                    "success": success,
                    "type": collector.type.value,
                }
            except Exception as e:
                results["collectors"][name] = {
                    "success": False,
                    "error": str(e),
                    "type": collector.type.value,
                }
        
        # Test storages
        for name, storage in self.storages.items():
            try:
                success = storage.test_connection()
                results["storages"][name] = {
                    "success": success,
                    "type": storage.type.value,
                }
            except Exception as e:
                results["storages"][name] = {
                    "success": False,
                    "error": str(e),
                    "type": storage.type.value,
                }
        
        return results
    
    def export_configuration(self, export_path: str) -> None:
        """
        Export current configuration to file.
        
        Args:
            export_path: Path to export configuration to
        """
        export_data = {
            "config": self.config,
            "collectors": {name: collector.get_metadata() for name, collector in self.collectors.items()},
            "storages": {name: storage.get_metadata() for name, storage in self.storages.items()},
            "export_time": datetime.now().isoformat(),
        }
        
        export_file = Path(export_path)
        export_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Configuration exported to: {export_path}")
