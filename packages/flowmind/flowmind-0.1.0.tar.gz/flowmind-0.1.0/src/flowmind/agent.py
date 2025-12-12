"""Main FlowAgent class - the entry point for FlowMind automation."""

from typing import Any, Dict, List, Optional

from flowmind.core.task import BaseTask, TaskResult, TaskFactory
from flowmind.core.pipeline import Pipeline
from flowmind.core.context import Context
from flowmind.core.scheduler import Scheduler
from flowmind.utils.logger import Logger


class FlowAgent:
    """Main automation agent for building and executing workflows.
    
    FlowAgent provides a simple API for creating task-based automation workflows
    without the complexity of traditional agent frameworks.
    
    Example:
        >>> agent = FlowAgent("my_workflow")
        >>> agent.add_task("download", url="https://api.example.com/data.json")
        >>> agent.add_task("transform", operation="filter")
        >>> agent.run()
    
    Attributes:
        name: Agent name
        pipeline: Task execution pipeline
        scheduler: Task scheduler
        logger: Logger instance
    """
    
    def __init__(self, name: str = "default", verbose: bool = True):
        """Initialize FlowAgent.
        
        Args:
            name: Agent name
            verbose: Enable verbose logging
        """
        self.name = name
        self.pipeline = Pipeline(name)
        self.scheduler = Scheduler()
        self.logger = Logger(name)
        self._scheduled_callback: Optional[callable] = None
        
        if not verbose:
            import logging
            self.logger.set_level(logging.WARNING)
    
    def add_task(
        self,
        task_type: str,
        name: Optional[str] = None,
        **config
    ) -> "FlowAgent":
        """Add a task to the workflow.
        
        Args:
            task_type: Type of task (e.g., "download", "transform")
            name: Optional task name (auto-generated if not provided)
            **config: Task configuration parameters
            
        Returns:
            Self for method chaining
            
        Example:
            >>> agent.add_task("download", url="https://example.com/data.json", output="data.json")
            >>> agent.add_task("transform", input="${download.output}", operation="filter")
        """
        # Auto-generate name if not provided
        if name is None:
            name = f"{task_type}_{len(self.pipeline.tasks)}"
        
        # Create task instance
        try:
            task = TaskFactory.create(task_type, name, **config)
            self.pipeline.add_task(task)
        except ValueError as e:
            self.logger.error(f"Failed to create task: {e}")
            raise
        
        return self
    
    def run(self, stop_on_error: bool = True) -> List[TaskResult]:
        """Execute the workflow.
        
        Args:
            stop_on_error: Whether to stop on first error
            
        Returns:
            List of task results
            
        Example:
            >>> results = agent.run()
            >>> for result in results:
            ...     print(result.status, result.output)
        """
        return self.pipeline.run(stop_on_error=stop_on_error)
    
    def schedule(self, every: str):
        """Schedule the workflow to run periodically.
        
        Args:
            every: Interval string (e.g., "5m", "1h", "30s")
            
        Example:
            >>> agent.schedule(every="5m")  # Run every 5 minutes
            >>> agent.start()  # Start the scheduler
        """
        self._scheduled_callback = lambda: self.run()
        self.scheduler.every(every, self._scheduled_callback)
        self.logger.info(f"Scheduled workflow to run every {every}")
    
    def start(self):
        """Start the scheduler (if workflow is scheduled)."""
        if not self._scheduled_callback:
            raise RuntimeError("No scheduled workflow. Call schedule() first.")
        
        self.logger.info(f"Starting scheduler for workflow '{self.name}'")
        self.scheduler.start()
    
    def stop(self):
        """Stop the scheduler."""
        self.scheduler.stop()
        self.logger.info(f"Stopped scheduler for workflow '{self.name}'")
    
    def get_context(self) -> Context:
        """Get the execution context.
        
        Returns:
            Shared execution context
        """
        return self.pipeline.context
    
    def get_result(self, task_name: str) -> Optional[TaskResult]:
        """Get result for a specific task.
        
        Args:
            task_name: Name of the task
            
        Returns:
            Task result or None
        """
        return self.pipeline.get_result(task_name)
    
    def clear(self):
        """Clear all tasks and context."""
        self.pipeline.clear()
        self.logger.info("Agent cleared")
    
    @property
    def task_count(self) -> int:
        """Get number of tasks in the workflow."""
        return len(self.pipeline.tasks)
    
    @property
    def results(self) -> List[TaskResult]:
        """Get all task results."""
        return self.pipeline.results
    
    def __repr__(self) -> str:
        return f"FlowAgent(name='{self.name}', tasks={self.task_count})"
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False
