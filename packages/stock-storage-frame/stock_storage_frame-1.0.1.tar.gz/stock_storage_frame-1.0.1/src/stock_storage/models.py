"""
Data models for the stock storage framework.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing_extensions import Literal


class CollectorType(str, Enum):
    """Supported collector types."""
    AKSHAKE = "akshare"
    TUSHARE = "tushare"
    CUSTOM = "custom"


class StorageType(str, Enum):
    """Supported storage types."""
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    CSV = "csv"
    PARQUET = "parquet"
    CUSTOM = "custom"


class AppConfig(BaseModel):
    """Application configuration."""
    name: str = Field(default="stock-data-pipeline")
    version: str = Field(default="1.0.0")
    log_level: str = Field(default="INFO")
    log_dir: str = Field(default="./logs")


class CollectorConfig(BaseModel):
    """Collector configuration."""
    name: str
    type: CollectorType
    method: Optional[str] = None
    script: Optional[str] = None  # Path to custom collector script
    module: Optional[str] = None  # Python module for custom collector
    function: Optional[str] = None  # Function name in module
    config: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator("script", "module", "function")
    @classmethod
    def validate_custom_fields(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validate custom collector fields."""
        if v is not None:
            # Get the type field value from the model instance
            data = info.data
            if data and data.get("type") != CollectorType.CUSTOM:
                field_name = info.field_name
                raise ValueError(f"{field_name} can only be used with custom collector type")
        return v
    
    @field_validator("script")
    @classmethod
    def validate_script_path(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validate script path exists."""
        if v is not None:
            # Get the type field value from the model instance
            data = info.data
            if data and data.get("type") == CollectorType.CUSTOM:
                import os
                if not os.path.exists(v):
                    raise ValueError(f"Script file not found: {v}")
        return v


class StorageConfig(BaseModel):
    """Storage configuration."""
    name: str
    type: StorageType
    config: Dict[str, Any] = Field(default_factory=dict)


class ProcessorConfig(BaseModel):
    """Processor configuration."""
    script: Optional[str] = None
    module: Optional[str] = None
    function: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)


class ConditionConfig(BaseModel):
    """Condition configuration for schedule execution."""
    script: Optional[str] = None
    module: Optional[str] = None
    function: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator("script")
    @classmethod
    def validate_script_path(cls, v: Optional[str]) -> Optional[str]:
        """Validate script path exists."""
        if v is not None:
            import os
            if not os.path.exists(v):
                raise ValueError(f"Condition script file not found: {v}")
        return v


class WorkflowConfig(BaseModel):
    """Workflow configuration."""
    name: str
    description: Optional[str] = None
    schedule: Optional[str] = None  # cron expression
    
    collector: CollectorConfig
    processor: Optional[ProcessorConfig] = None
    condition: Optional[ConditionConfig] = None
    storage: StorageConfig
    
    @field_validator("schedule")
    @classmethod
    def validate_schedule(cls, v: Optional[str]) -> Optional[str]:
        """Validate cron expression format."""
        if v is None:
            return v
        
        # Basic cron validation - should have 5 parts
        parts = v.strip().split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron expression: {v}. Expected 5 parts.")
        
        # Try to parse with croniter for more detailed validation
        try:
            import croniter
            from datetime import datetime
            croniter.croniter(v, datetime.now())
        except ImportError:
            # croniter not installed, skip detailed validation
            pass
        except Exception as e:
            raise ValueError(f"Invalid cron expression '{v}': {str(e)}")
        
        return v


class ExecutionResult(BaseModel):
    """Execution result model."""
    workflow_name: str
    success: bool
    start_time: datetime
    end_time: datetime
    records_processed: int = 0
    error_message: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def duration(self) -> float:
        """Get execution duration in seconds."""
        return (self.end_time - self.start_time).total_seconds()


class StockData(BaseModel):
    """Stock data model."""
    symbol: str
    date: date
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None
    amount: Optional[float] = None
    adj_close: Optional[float] = None
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }


class BatchStockData(BaseModel):
    """Batch stock data model."""
    data: List[StockData]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def to_dataframe(self):
        """Convert to pandas DataFrame."""
        import pandas as pd
        data_dicts = [item.dict() for item in self.data]
        return pd.DataFrame(data_dicts)
    
    @classmethod
    def from_dataframe(cls, df):
        """Create from pandas DataFrame."""
        data = []
        for _, row in df.iterrows():
            data.append(StockData(**row.to_dict()))
        return cls(data=data)
