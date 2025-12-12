"""Base task abstraction for FlowMind automation framework."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class TaskResult:
    """Result of a task execution.
    
    Attributes:
        status: Execution status
        output: Task output data
        error: Error message if failed
        duration: Execution time in seconds
        metadata: Additional information
    """
    
    def __init__(
        self,
        status: TaskStatus,
        output: Any = None,
        error: Optional[str] = None,
        duration: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.status = status
        self.output = output
        self.error = error
        self.duration = duration
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
    
    def __repr__(self) -> str:
        return f"TaskResult(status={self.status.value}, output={self.output})"
    
    def is_success(self) -> bool:
        """Check if task succeeded."""
        return self.status == TaskStatus.SUCCESS
    
    def is_failed(self) -> bool:
        """Check if task failed."""
        return self.status == TaskStatus.FAILED


class BaseTask(ABC):
    """Base class for all FlowMind tasks.
    
    All custom tasks must inherit from this class and implement the execute method.
    
    Attributes:
        name: Unique task name
        description: Task description
        task_type: Type of task
        config: Task configuration
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        **config
    ):
        self.name = name
        self.description = description
        self.config = config
        self.task_type = self.__class__.__name__
        self.result: Optional[TaskResult] = None
    
    @abstractmethod
    def execute(self, context: "Context") -> TaskResult:
        """Execute the task.
        
        Args:
            context: Shared execution context
            
        Returns:
            TaskResult with execution outcome
        """
        pass
    
    def validate(self) -> bool:
        """Validate task configuration.
        
        Returns:
            True if configuration is valid
        """
        return True
    
    def should_execute(self, context: "Context") -> bool:
        """Determine if task should execute based on conditions.
        
        Args:
            context: Shared execution context
            
        Returns:
            True if task should execute
        """
        # Check if_condition parameter
        if "if_condition" in self.config:
            condition = self.config["if_condition"]
            return self._evaluate_condition(condition, context)
        return True
    
    def _evaluate_condition(self, condition: str, context: "Context") -> bool:
        """Evaluate a condition string.
        
        Args:
            condition: Condition to evaluate (e.g., "${check.failed}")
            context: Execution context
            
        Returns:
            True if condition is met
        """
        # Simple variable substitution and evaluation
        resolved = context.resolve_variables(condition)
        try:
            # Safe evaluation of boolean expressions
            return bool(eval(resolved, {"__builtins__": {}}, {}))
        except:
            return False
    
    def __repr__(self) -> str:
        return f"{self.task_type}(name='{self.name}')"


class TaskFactory:
    """Factory for creating task instances."""
    
    _tasks: Dict[str, type] = {}
    
    @classmethod
    def register(cls, task_type: str, task_class: type):
        """Register a task type.
        
        Args:
            task_type: Type identifier
            task_class: Task class
        """
        cls._tasks[task_type] = task_class
    
    @classmethod
    def create(cls, task_type: str, name: str, **config) -> BaseTask:
        """Create a task instance.
        
        Args:
            task_type: Type of task to create
            name: Task name
            **config: Task configuration
            
        Returns:
            Task instance
            
        Raises:
            ValueError: If task type not registered
        """
        if task_type not in cls._tasks:
            raise ValueError(f"Unknown task type: {task_type}")
        
        task_class = cls._tasks[task_type]
        return task_class(name=name, **config)
    
    @classmethod
    def list_tasks(cls) -> list:
        """List all registered task types.
        
        Returns:
            List of task type names
        """
        return list(cls._tasks.keys())
