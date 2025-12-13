#!/usr/bin/env python3
"""
Example custom collector script for fetching data from web APIs.

This script demonstrates how to create a custom collector that can be used
with the stock storage framework. The script should define a function that
returns stock data in a format that can be processed by the framework.

Usage in workflow configuration:
  collector:
    name: "web_collector"
    type: "custom"
    script: "./scripts/collector_fetch_web.py"
    config:
      api_url: "https://api.example.com/stock-data"
      api_key: "your_api_key_here"
"""

import asyncio
import aiohttp
import pandas as pd
from datetime import date, datetime
from typing import Dict, List, Any, Optional
import json


async def collect(
    config: Optional[Dict[str, Any]] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Collect stock data from a web API.
    
    This is the main function that will be called by the custom collector.
    It receives all parameters from the workflow configuration.
    
    Args:
        config: Collector configuration from workflow (config.config)
        collector_config: Full collector configuration
        **kwargs: Additional parameters from workflow (e.g., symbols, start_date, etc.)
        
    Returns:
        pandas DataFrame with stock data
    """
    # Get configuration
    config = config or {}
    df = pd.DataFrame({
        'symbol': ['000001', '000001', '000001', '000002', '000002'],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-01', '2024-01-02'],
        'open': [10.0, 10.5, 10.2, 20.0, 21.0],
        'high': [10.5, 11.0, 10.8, 21.0, 22.0],
        'low': [9.8, 10.3, 10.0, 19.5, 20.5],
        'close': [10.2, 10.8, 10.5, 20.5, 21.5],
        'volume': [1000000, 1200000, 1100000, 500000, 600000],
        'amount': [10200000, 12960000, 11550000, 10250000, 12900000]
    })
    return df