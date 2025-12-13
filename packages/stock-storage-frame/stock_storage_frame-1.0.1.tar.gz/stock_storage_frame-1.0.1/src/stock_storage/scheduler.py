"""
Scheduler module for executing workflows on schedule.
"""

import asyncio
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from loguru import logger
import croniter

from .engine import WorkflowEngine
from .models import WorkflowConfig, ExecutionResult


class WorkflowScheduler:
    """Scheduler for executing workflows on schedule."""
    
    def __init__(self, config_path: str = "config.yaml", workflows_dir: str = "workflows"):
        """
        Initialize workflow scheduler.
        
        Args:
            config_path: Path to main configuration file
            workflows_dir: Directory containing workflow configuration files
        """
        self.config_path = config_path
        self.workflows_dir = workflows_dir
        self.engine = WorkflowEngine(config_path)
        self.scheduled_tasks: Dict[str, asyncio.Task] = {}
        self.running = False
        self.shutdown_event = asyncio.Event()
        
    def load_scheduled_workflows(self) -> List[Dict[str, Any]]:
        """
        Load all workflows with schedule from workflows directory.
        
        Returns:
            List of workflow configurations with schedule
        """
        workflows_path = Path(self.workflows_dir)
        
        if not workflows_path.exists():
            logger.warning(f"Workflows directory not found: {self.workflows_dir}")
            return []
        
        # Find all YAML files in the directory
        workflow_files = list(workflows_path.glob("*.yaml")) + list(workflows_path.glob("*.yml"))
        
        scheduled_workflows = []
        
        for workflow_file in workflow_files:
            try:
                workflow_config = self.engine.load_workflow_config(str(workflow_file))
                
                if workflow_config.schedule:
                    scheduled_workflows.append({
                        "file_path": str(workflow_file),
                        "config": workflow_config,
                        "name": workflow_config.name,
                        "schedule": workflow_config.schedule,
                        "description": workflow_config.description,
                    })
                    logger.info(f"Loaded scheduled workflow: {workflow_config.name} ({workflow_config.schedule})")
                else:
                    logger.debug(f"Skipping workflow without schedule: {workflow_config.name}")
                    
            except Exception as e:
                logger.error(f"Failed to load workflow {workflow_file}: {str(e)}")
        
        return scheduled_workflows
    
    def load_specific_workflow(self, workflow_path: str) -> Optional[Dict[str, Any]]:
        """
        Load a specific workflow from file path.
        
        Args:
            workflow_path: Path to workflow configuration file
            
        Returns:
            Workflow configuration with schedule or None if not found/invalid
        """
        try:
            workflow_config = self.engine.load_workflow_config(workflow_path)
            
            if not workflow_config.schedule:
                logger.error(f"Workflow {workflow_path} does not have a schedule field")
                return None
            
            return {
                "file_path": workflow_path,
                "config": workflow_config,
                "name": workflow_config.name,
                "schedule": workflow_config.schedule,
                "description": workflow_config.description,
            }
            
        except Exception as e:
            logger.error(f"Failed to load workflow {workflow_path}: {str(e)}")
            return None
    
    async def check_condition(self, workflow_config: WorkflowConfig) -> bool:
        """
        Check if a workflow should be executed based on its condition.
        
        Args:
            workflow_config: Workflow configuration
            
        Returns:
            True if workflow should be executed, False otherwise
        """
        if not workflow_config.condition:
            # No condition configured, default to True
            return True
        
        condition_config = workflow_config.condition
        
        try:
            # Create condition processor using component manager
            from .factories import ComponentManager
            component_manager = ComponentManager()
            condition_processor = component_manager.create_condition(condition_config)
            
            # Execute condition check
            result = await condition_processor.check()
            
            logger.info(f"Condition check for workflow {workflow_config.name}: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to check condition for workflow {workflow_config.name}: {str(e)}")
            # If condition check fails, default to True to avoid blocking execution
            return True
    
    async def execute_workflow(self, workflow_info: Dict[str, Any]) -> ExecutionResult:
        """
        Execute a workflow and log the result.
        
        Args:
            workflow_info: Workflow information
            
        Returns:
            Execution result
        """
        workflow_name = workflow_info["name"]
        workflow_file = workflow_info["file_path"]
        
        logger.info(f"Executing scheduled workflow: {workflow_name}")
        
        try:
            result = await self.engine.execute_workflow_file(workflow_file)
            
            if result.success:
                logger.info(f"Scheduled workflow completed: {workflow_name} - {result.records_processed} records in {result.duration:.2f}s")
            else:
                logger.error(f"Scheduled workflow failed: {workflow_name} - {result.error_message}")
            
            return result
            
        except Exception as e:
            logger.error(f"Unexpected error executing scheduled workflow {workflow_name}: {str(e)}")
            raise
    
    def calculate_next_run(self, cron_expression: str, reference_time: datetime = None) -> datetime:
        """
        Calculate next run time based on cron expression.
        
        Args:
            cron_expression: Cron expression string
            reference_time: Reference time for calculation (default: now)
            
        Returns:
            Next run time
        """
        if reference_time is None:
            reference_time = datetime.now()
        
        try:
            cron = croniter.croniter(cron_expression, reference_time)
            next_run = cron.get_next(datetime)
            return next_run
        except Exception as e:
            logger.error(f"Failed to calculate next run for cron '{cron_expression}': {str(e)}")
            # Fallback: run in 1 hour
            return reference_time.replace(hour=reference_time.hour + 1)
    
    async def schedule_workflow(self, workflow_info: Dict[str, Any]) -> None:
        """
        Schedule a workflow for execution based on its cron expression.
        
        Args:
            workflow_info: Workflow information
        """
        workflow_name = workflow_info["name"]
        cron_expression = workflow_info["schedule"]
        
        logger.info(f"Scheduling workflow: {workflow_name} ({cron_expression})")
        
        while self.running and not self.shutdown_event.is_set():
            try:
                # Calculate next run time
                next_run = self.calculate_next_run(cron_expression)
                wait_seconds = (next_run - datetime.now()).total_seconds()
                
                if wait_seconds < 0:
                    # If next run is in the past, recalculate from now
                    next_run = self.calculate_next_run(cron_expression, datetime.now())
                    wait_seconds = (next_run - datetime.now()).total_seconds()
                
                logger.info(f"Next run for {workflow_name}: {next_run} (in {wait_seconds:.0f} seconds)")
                
                # Wait until next run time or shutdown
                try:
                    await asyncio.wait_for(
                        self.shutdown_event.wait(),
                        timeout=wait_seconds
                    )
                    # If we get here, shutdown was requested
                    break
                except asyncio.TimeoutError:
                    # Timeout means it's time to execute
                    pass
                
                # Execute the workflow
                if self.running and not self.shutdown_event.is_set():
                    # Check condition before execution
                    workflow_config = workflow_info["config"]
                    should_execute = await self.check_condition(workflow_config)
                    
                    if should_execute:
                        await self.execute_workflow(workflow_info)
                    else:
                        logger.info(f"Skipping workflow {workflow_name} due to condition check returning False")
                    
            except asyncio.CancelledError:
                logger.info(f"Scheduler task for {workflow_name} cancelled")
                break
            except Exception as e:
                logger.error(f"Error in scheduler for {workflow_name}: {str(e)}")
                # Wait a bit before retrying
                await asyncio.sleep(60)
    
    async def start(self) -> None:
        """Start the scheduler."""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        logger.info("Starting workflow scheduler")
        self.running = True
        self.shutdown_event.clear()
        
        # Load scheduled workflows
        scheduled_workflows = self.load_scheduled_workflows()
        
        if not scheduled_workflows:
            logger.warning("No scheduled workflows found")
            return
        
        logger.info(f"Found {len(scheduled_workflows)} scheduled workflows")
        
        # Create tasks for each scheduled workflow
        for workflow_info in scheduled_workflows:
            task = asyncio.create_task(self.schedule_workflow(workflow_info))
            self.scheduled_tasks[workflow_info["name"]] = task
            logger.debug(f"Created scheduler task for: {workflow_info['name']}")
        
        # Wait for shutdown signal
        try:
            await self.shutdown_event.wait()
        except asyncio.CancelledError:
            logger.info("Scheduler received cancellation signal")
        finally:
            await self.stop()
    
    async def start_with_specific_workflow(self, workflow_path: str) -> None:
        """
        Start the scheduler with a specific workflow.
        
        Args:
            workflow_path: Path to workflow configuration file
        """
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        logger.info(f"Starting workflow scheduler for specific workflow: {workflow_path}")
        self.running = True
        self.shutdown_event.clear()
        
        # Load the specific workflow
        workflow_info = self.load_specific_workflow(workflow_path)
        if not workflow_info:
            logger.error(f"Failed to load workflow {workflow_path} or it doesn't have a schedule")
            return
        
        logger.info(f"Found scheduled workflow: {workflow_info['name']} ({workflow_info['schedule']})")
        
        # Create task for this workflow
        task = asyncio.create_task(self.schedule_workflow(workflow_info))
        self.scheduled_tasks[workflow_info["name"]] = task
        logger.debug(f"Created scheduler task for: {workflow_info['name']}")
        
        # Wait for shutdown signal
        try:
            await self.shutdown_event.wait()
        except asyncio.CancelledError:
            logger.info("Scheduler received cancellation signal")
        finally:
            await self.stop()
    
    async def stop(self) -> None:
        """Stop the scheduler."""
        if not self.running:
            return
        
        logger.info("Stopping workflow scheduler")
        self.running = False
        self.shutdown_event.set()
        
        # Cancel all scheduled tasks
        for workflow_name, task in self.scheduled_tasks.items():
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                logger.debug(f"Cancelled scheduler task for: {workflow_name}")
        
        self.scheduled_tasks.clear()
        logger.info("Workflow scheduler stopped")
    
    def get_scheduler_status(self) -> Dict[str, Any]:
        """
        Get current scheduler status.
        
        Returns:
            Scheduler status information
        """
        status = {
            "running": self.running,
            "scheduled_workflows": [],
            "active_tasks": len(self.scheduled_tasks),
        }
        
        # Add information about each scheduled workflow
        scheduled_workflows = self.load_scheduled_workflows()
        for workflow_info in scheduled_workflows:
            workflow_status = {
                "name": workflow_info["name"],
                "schedule": workflow_info["schedule"],
                "description": workflow_info["description"],
                "file_path": workflow_info["file_path"],
            }
            
            # Calculate next run time
            try:
                next_run = self.calculate_next_run(workflow_info["schedule"])
                workflow_status["next_run"] = next_run.isoformat()
                workflow_status["next_run_in_seconds"] = (next_run - datetime.now()).total_seconds()
            except Exception as e:
                workflow_status["next_run_error"] = str(e)
            
            status["scheduled_workflows"].append(workflow_status)
        
        return status


async def run_scheduler(config_path: str = "config.yaml", workflows_dir: str = "workflows") -> None:
    """
    Run the workflow scheduler.
    
    Args:
        config_path: Path to main configuration file
        workflows_dir: Directory containing workflow configuration files
    """
    scheduler = WorkflowScheduler(config_path, workflows_dir)
    
    # Setup signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    
    def signal_handler():
        logger.info("Received shutdown signal, shutting down...")
        stop_event.set()
    
    # Add signal handlers to the event loop
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        # Start the scheduler
        scheduler_task = asyncio.create_task(scheduler.start())
        
        # Wait for stop event
        await stop_event.wait()
        
        # Stop the scheduler
        await scheduler.stop()
        await scheduler_task
    except asyncio.CancelledError:
        logger.info("Scheduler cancelled")
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")
        raise
    finally:
        # Clean up signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)
        await scheduler.stop()


async def run_scheduler_for_specific_workflow(workflow_path: str, config_path: str = "config.yaml", workflows_dir: str = "workflows") -> None:
    """
    Run the workflow scheduler for a specific workflow.
    
    Args:
        workflow_path: Path to workflow configuration file
        config_path: Path to main configuration file
        workflows_dir: Directory containing workflow configuration files
    """
    scheduler = WorkflowScheduler(config_path, workflows_dir)
    
    # Setup signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    
    def signal_handler():
        logger.info("Received shutdown signal, shutting down...")
        stop_event.set()
    
    # Add signal handlers to the event loop
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        # Start the scheduler with specific workflow
        scheduler_task = asyncio.create_task(scheduler.start_with_specific_workflow(workflow_path))
        
        # Wait for stop event
        await stop_event.wait()
        
        # Stop the scheduler
        await scheduler.stop()
        await scheduler_task
    except asyncio.CancelledError:
        logger.info("Scheduler cancelled")
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")
        raise
    finally:
        # Clean up signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)
        await scheduler.stop()


def main() -> None:
    """Main entry point for scheduler CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Workflow Scheduler - Schedule and execute workflows based on cron expressions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config.yaml",
        help="Path to main configuration file (default: config.yaml)"
    )
    
    parser.add_argument(
        "--workflows-dir", "-w",
        type=str,
        default="workflows",
        help="Directory containing workflow configuration files (default: workflows)"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show scheduler status and exit"
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
    
    args = parser.parse_args()
    
    # Setup logging
    from .main import setup_logging
    setup_logging(args.log_level, args.log_dir)
    
    if args.status:
        # Show scheduler status
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
        return
    
    # Run the scheduler
    try:
        asyncio.run(run_scheduler(args.config, args.workflows_dir))
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Failed to run scheduler: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
