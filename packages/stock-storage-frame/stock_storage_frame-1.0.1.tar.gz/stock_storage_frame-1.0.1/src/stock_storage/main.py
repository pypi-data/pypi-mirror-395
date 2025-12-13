"""
Main entry point for the stock storage framework.
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import List, Optional
from loguru import logger

from .engine import WorkflowEngine
from .models import ExecutionResult


def setup_logging(log_level: str = "INFO", log_dir: Optional[str] = None) -> None:
    """
    Setup logging configuration.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR)
        log_dir: Directory for log files
    """
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )
    
    # Add file logger if log_dir is specified
    if log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_path / "stock_storage_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
            rotation="00:00",  # Rotate at midnight
            retention="30 days",  # Keep logs for 30 days
            compression="zip",
        )


def print_result(result: ExecutionResult) -> None:
    """
    Print execution result in a readable format.
    
    Args:
        result: Execution result
    """
    print("\n" + "=" * 60)
    print(f"Workflow: {result.workflow_name}")
    print(f"Status: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Duration: {result.duration:.2f} seconds")
    print(f"Records processed: {result.records_processed}")
    
    if result.success:
        print("\nDetails:")
        for key, value in result.details.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key}: {sub_value}")
            else:
                print(f"  {key}: {value}")
    else:
        print(f"\nError: {result.error_message}")
    
    print("=" * 60)


async def run_single_workflow(workflow_path: str, config_path: str = "config.yaml") -> ExecutionResult:
    """
    Run a single workflow.
    
    Args:
        workflow_path: Path to workflow configuration file
        config_path: Path to main configuration file
        
    Returns:
        Execution result
    """
    logger.info(f"Running workflow: {workflow_path}")
    
    try:
        engine = WorkflowEngine(config_path)
        result = await engine.execute_workflow_file(workflow_path)
        return result
    except Exception as e:
        logger.error(f"Failed to run workflow: {str(e)}")
        raise


async def run_all_workflows(workflows_dir: str = "workflows", config_path: str = "config.yaml") -> List[ExecutionResult]:
    """
    Run all workflows in a directory.
    
    Args:
        workflows_dir: Directory containing workflow configuration files
        config_path: Path to main configuration file
        
    Returns:
        List of execution results
    """
    logger.info(f"Running all workflows in: {workflows_dir}")
    
    try:
        engine = WorkflowEngine(config_path)
        results = await engine.execute_all_workflows(workflows_dir)
        return results
    except Exception as e:
        logger.error(f"Failed to run workflows: {str(e)}")
        raise


async def test_components(config_path: str = "config.yaml") -> dict:
    """
    Test all configured components.
    
    Args:
        config_path: Path to main configuration file
        
    Returns:
        Test results
    """
    logger.info("Testing all components")
    
    try:
        engine = WorkflowEngine(config_path)
        results = await engine.test_components()
        return results
    except Exception as e:
        logger.error(f"Failed to test components: {str(e)}")
        raise


async def validate_workflow(workflow_path: str, config_path: str = "config.yaml") -> dict:
    """
    Validate a workflow configuration.
    
    Args:
        workflow_path: Path to workflow configuration file
        config_path: Path to main configuration file
        
    Returns:
        Validation results
    """
    logger.info(f"Validating workflow: {workflow_path}")
    
    try:
        engine = WorkflowEngine(config_path)
        workflow_config = engine.load_workflow_config(workflow_path)
        validation_result = engine.validate_workflow(workflow_config)
        return validation_result
    except Exception as e:
        logger.error(f"Failed to validate workflow: {str(e)}")
        raise


async def run_scheduler(config_path: str = "config.yaml", workflows_dir: str = "workflows") -> None:
    """
    Run the workflow scheduler.
    
    Args:
        config_path: Path to main configuration file
        workflows_dir: Directory containing workflow configuration files
    """
    from .scheduler import run_scheduler as scheduler_main
    await scheduler_main(config_path, workflows_dir)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Stock Storage Framework - A configuration-driven stock data storage framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --workflow workflows/daily_stock_data.yaml
  %(prog)s --all
  %(prog)s --test
  %(prog)s --validate workflows/daily_stock_data.yaml
        """
    )
    
    parser.add_argument(
        "--workflow", "-w",
        type=str,
        help="Path to workflow configuration file"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all workflows in the workflows directory"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test all configured components"
    )
    
    parser.add_argument(
        "--validate",
        type=str,
        help="Validate a workflow configuration file"
    )
    
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Start the workflow scheduler"
    )
    
    parser.add_argument(
        "--scheduler-status",
        action="store_true",
        help="Show scheduler status"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config.yaml",
        help="Path to main configuration file (default: config.yaml)"
    )
    
    parser.add_argument(
        "--workflows-dir",
        type=str,
        default="workflows",
        help="Directory containing workflow configuration files (default: workflows)"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level (default: INFO)"
    )
    
    parser.add_argument(
        "--log-dir",
        type=str,
        help="Directory for log files"
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    
    args = parser.parse_args()
    
    # Show version
    if args.version:
        from . import __version__
        print(f"Stock Storage Framework v{__version__}")
        return
    
    # Setup logging
    setup_logging(args.log_level, args.log_dir)
    
    # Check if no action specified
    if not any([args.workflow, args.all, args.test, args.validate, args.schedule, args.scheduler_status]):
        # If only workflows_dir is specified (even if it's the default), execute all workflows in that directory
        if args.workflows_dir:
            # This means user wants to execute all workflows in the specified directory
            args.all = True
        else:
            parser.print_help()
            return
    
    try:
        # Handle workflow execution with or without schedule
        if args.workflow:
            if args.schedule:
                # Schedule a specific workflow
                logger.info(f"Scheduling workflow: {args.workflow}")
                from .scheduler import run_scheduler_for_specific_workflow
                
                # Start the scheduler with only this workflow
                try:
                    asyncio.run(run_scheduler_for_specific_workflow(args.workflow, args.config, args.workflows_dir))
                except KeyboardInterrupt:
                    logger.info("Scheduler stopped by user")
                except Exception as e:
                    logger.error(f"Failed to run scheduler: {str(e)}")
                    sys.exit(1)
            else:
                # Run a single workflow immediately
                result = asyncio.run(run_single_workflow(args.workflow, args.config))
                print_result(result)
        
        # Handle workflows directory execution with or without schedule
        elif args.schedule and not args.workflow:
            # Schedule all workflows in the directory
            logger.info(f"Starting workflow scheduler for directory: {args.workflows_dir}")
            try:
                asyncio.run(run_scheduler(args.config, args.workflows_dir))
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
            except Exception as e:
                logger.error(f"Failed to run scheduler: {str(e)}")
                sys.exit(1)
        
        # Handle --all flag (legacy support)
        elif args.all:
            results = asyncio.run(run_all_workflows("workflows", args.config))
            print(f"\nExecuted {len(results)} workflows:")
            for result in results:
                status = "✓" if result.success else "✗"
                print(f"  {status} {result.workflow_name}: {result.records_processed} records, {result.duration:.2f}s")
            
            success_count = sum(1 for r in results if r.success)
            print(f"\nSummary: {success_count}/{len(results)} successful")
        
        # Handle --workflows-dir without --schedule (execute all workflows in directory)
        elif args.workflows_dir and not args.schedule and not args.workflow and not args.all:
            results = asyncio.run(run_all_workflows(args.workflows_dir, args.config))
            print(f"\nExecuted {len(results)} workflows from {args.workflows_dir}:")
            for result in results:
                status = "✓" if result.success else "✗"
                print(f"  {status} {result.workflow_name}: {result.records_processed} records, {result.duration:.2f}s")
            
            success_count = sum(1 for r in results if r.success)
            print(f"\nSummary: {success_count}/{len(results)} successful")
            
        elif args.test:
            results = asyncio.run(test_components(args.config))
            
            print("\nComponent Test Results:")
            print("\nCollectors:")
            for name, test_result in results.get("collectors", {}).items():
                status = "✓" if test_result.get("success") else "✗"
                print(f"  {status} {name} ({test_result.get('type', 'unknown')})")
                if not test_result.get("success") and "error" in test_result:
                    print(f"    Error: {test_result['error']}")
            
            print("\nStorages:")
            for name, test_result in results.get("storages", {}).items():
                status = "✓" if test_result.get("success") else "✗"
                print(f"  {status} {name} ({test_result.get('type', 'unknown')})")
                if not test_result.get("success") and "error" in test_result:
                    print(f"    Error: {test_result['error']}")
            
        elif args.validate:
            validation_result = asyncio.run(validate_workflow(args.validate, args.config))
            
            print(f"\nWorkflow Validation: {validation_result['workflow_name']}")
            print(f"Valid: {'✓' if validation_result['valid'] else '✗'}")
            
            if validation_result['warnings']:
                print("\nWarnings:")
                for warning in validation_result['warnings']:
                    print(f"  ⚠ {warning}")
            
            if validation_result['errors']:
                print("\nErrors:")
                for error in validation_result['errors']:
                    print(f"  ✗ {error}")
            
            if validation_result['valid'] and not validation_result['warnings']:
                print("\n✓ Workflow configuration is valid and ready to run.")
        
        elif args.scheduler_status:
            from .scheduler import WorkflowScheduler
            scheduler = WorkflowScheduler(args.config, args.workflows_dir)
            status = scheduler.get_scheduler_status()
            
            print("\n" + "=" * 60)
            print("Workflow Scheduler Status")
            print("=" * 60)
            print(f"Running: {'Yes' if status['running'] else 'No'}")
            print(f"Active tasks: {status['active_tasks']}")
            print(f"Scheduled workflows: {len(status['scheduled_workflows'])}")
            
            if status['scheduled_workflows']:
                print("\nScheduled Workflows:")
                for i, workflow in enumerate(status['scheduled_workflows'], 1):
                    print(f"\n{i}. {workflow['name']}")
                    print(f"   Schedule: {workflow['schedule']}")
                    print(f"   Description: {workflow.get('description', 'N/A')}")
                    print(f"   File: {workflow['file_path']}")
                    
                    if 'next_run' in workflow:
                        from datetime import datetime
                        next_run = datetime.fromisoformat(workflow['next_run'])
                        now = datetime.now()
                        seconds_left = (next_run - now).total_seconds()
                        
                        if seconds_left > 0:
                            hours = int(seconds_left // 3600)
                            minutes = int((seconds_left % 3600) // 60)
                            seconds = int(seconds_left % 60)
                            print(f"   Next run: {next_run} (in {hours}h {minutes}m {seconds}s)")
                        else:
                            print(f"   Next run: {next_run} (overdue)")
                    elif 'next_run_error' in workflow:
                        print(f"   Next run: Error - {workflow['next_run_error']}")
            
            print("\n" + "=" * 60)
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
