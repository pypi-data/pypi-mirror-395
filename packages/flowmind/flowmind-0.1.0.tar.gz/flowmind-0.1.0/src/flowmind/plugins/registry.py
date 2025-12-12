"""Task registry for FlowMind plugins."""

from typing import Dict, Type, List
from flowmind.core.task import BaseTask, TaskFactory


_custom_tasks: Dict[str, Type[BaseTask]] = {}


def register_task(task_type: str):
    """Decorator to register a custom task type.
    
    Example:
        >>> @register_task("my_custom_task")
        ... class MyTask(BaseTask):
        ...     def execute(self, context):
        ...         return TaskResult(status=TaskStatus.SUCCESS)
    """
    def decorator(cls: Type[BaseTask]):
        _custom_tasks[task_type] = cls
        TaskFactory.register(task_type, cls)
        return cls
    return decorator


def get_task(task_type: str) -> Type[BaseTask]:
    """Get a registered task class.
    
    Args:
        task_type: Task type identifier
        
    Returns:
        Task class
        
    Raises:
        KeyError: If task type not found
    """
    if task_type in _custom_tasks:
        return _custom_tasks[task_type]
    raise KeyError(f"Task type not found: {task_type}")


def list_tasks() -> List[str]:
    """List all registered custom tasks.
    
    Returns:
        List of task type names
    """
    return list(_custom_tasks.keys())
