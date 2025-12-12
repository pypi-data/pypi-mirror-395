"""Pipeline executor for running FlowMind task workflows."""

import time
from typing import List, Optional
from datetime import datetime

from flowmind.core.task import BaseTask, TaskResult, TaskStatus
from flowmind.core.context import Context
from flowmind.utils.logger import Logger


class Pipeline:
    """Task execution pipeline.
    
    Manages the execution of a sequence of tasks with shared context.
    
    Attributes:
        name: Pipeline name
        tasks: List of tasks to execute
        context: Shared execution context
        logger: Logger instance
    """
    
    def __init__(self, name: str = "default", logger: Optional[Logger] = None):
        self.name = name
        self.tasks: List[BaseTask] = []
        self.context = Context()
        self.logger = logger or Logger(name)
        self.results: List[TaskResult] = []
    
    def add_task(self, task: BaseTask):
        """Add a task to the pipeline.
        
        Args:
            task: Task to add
        """
        self.tasks.append(task)
        self.logger.info(f"Added task: {task.name} ({task.task_type})")
    
    def run(self, stop_on_error: bool = True) -> List[TaskResult]:
        """Execute all tasks in the pipeline.
        
        Args:
            stop_on_error: Whether to stop on first error
            
        Returns:
            List of task results
        """
        self.logger.info(f"Starting pipeline '{self.name}' with {len(self.tasks)} tasks")
        self.results = []
        start_time = time.time()
        
        for i, task in enumerate(self.tasks, 1):
            self.logger.info(f"[{i}/{len(self.tasks)}] Executing task: {task.name}")
            
            # Check if task should execute
            if not task.should_execute(self.context):
                self.logger.info(f"Skipping task '{task.name}' (condition not met)")
                result = TaskResult(
                    status=TaskStatus.SKIPPED,
                    metadata={"reason": "Condition not met"}
                )
                task.result = result
                self.results.append(result)
                continue
            
            # Validate task configuration
            if not task.validate():
                self.logger.error(f"Task '{task.name}' validation failed")
                result = TaskResult(
                    status=TaskStatus.FAILED,
                    error="Task validation failed"
                )
                task.result = result
                self.results.append(result)
                
                if stop_on_error:
                    break
                continue
            
            # Execute task
            task_start = time.time()
            try:
                result = task.execute(self.context)
                result.duration = time.time() - task_start
                
                # Store result in context
                self.context.set_task_result(task.name, result.output)
                
                if result.is_success():
                    self.logger.info(f"Task '{task.name}' completed successfully in {result.duration:.2f}s")
                else:
                    self.logger.error(f"Task '{task.name}' failed: {result.error}")
                
            except Exception as e:
                result = TaskResult(
                    status=TaskStatus.FAILED,
                    error=str(e),
                    duration=time.time() - task_start
                )
                self.logger.error(f"Task '{task.name}' raised exception: {e}")
            
            task.result = result
            self.results.append(result)
            
            # Stop on error if configured
            if stop_on_error and result.is_failed():
                self.logger.error(f"Stopping pipeline due to task failure")
                break
        
        # Pipeline summary
        duration = time.time() - start_time
        success_count = sum(1 for r in self.results if r.is_success())
        failed_count = sum(1 for r in self.results if r.is_failed())
        skipped_count = sum(1 for r in self.results if r.status == TaskStatus.SKIPPED)
        
        self.logger.info(
            f"Pipeline '{self.name}' completed in {duration:.2f}s: "
            f"{success_count} succeeded, {failed_count} failed, {skipped_count} skipped"
        )
        
        return self.results
    
    def get_result(self, task_name: str) -> Optional[TaskResult]:
        """Get result for a specific task.
        
        Args:
            task_name: Name of the task
            
        Returns:
            Task result or None
        """
        for task in self.tasks:
            if task.name == task_name:
                return task.result
        return None
    
    def clear(self):
        """Clear all tasks and context."""
        self.tasks.clear()
        self.results.clear()
        self.context.clear()
        self.logger.info("Pipeline cleared")
    
    def __repr__(self) -> str:
        return f"Pipeline(name='{self.name}', tasks={len(self.tasks)})"
