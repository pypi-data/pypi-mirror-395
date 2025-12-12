"""Shared context for task execution and data passing."""

import re
from typing import Any, Dict, Optional
from datetime import datetime


class Context:
    """Shared execution context for FlowMind tasks.
    
    The context stores task outputs and allows tasks to reference
    each other's results using variable syntax like ${task_name.output}.
    
    Attributes:
        data: Shared data dictionary
        metadata: Additional metadata
        start_time: Workflow start time
    """
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.start_time = datetime.now()
        self._task_results: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any):
        """Set a context variable.
        
        Args:
            key: Variable name
            value: Variable value
        """
        self.data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a context variable.
        
        Args:
            key: Variable name
            default: Default value if not found
            
        Returns:
            Variable value or default
        """
        return self.data.get(key, default)
    
    def set_task_result(self, task_name: str, result: Any):
        """Store a task's result.
        
        Args:
            task_name: Name of the task
            result: Task result
        """
        self._task_results[task_name] = result
    
    def get_task_result(self, task_name: str) -> Optional[Any]:
        """Get a task's result.
        
        Args:
            task_name: Name of the task
            
        Returns:
            Task result or None
        """
        return self._task_results.get(task_name)
    
    def resolve_variables(self, value: Any) -> Any:
        """Resolve variable references in a value.
        
        Supports syntax like:
        - ${task_name.output}
        - ${task_name.result.field}
        - ${context_var}
        
        Args:
            value: Value potentially containing variable references
            
        Returns:
            Resolved value
        """
        if not isinstance(value, str):
            return value
        
        # Pattern to match ${variable} syntax
        pattern = r'\$\{([^}]+)\}'
        
        def replace_var(match):
            var_path = match.group(1)
            return str(self._resolve_path(var_path))
        
        # Replace all variable references
        resolved = re.sub(pattern, replace_var, value)
        
        # If the entire string was a variable, return the actual value
        if value.startswith('${') and value.endswith('}'):
            var_path = value[2:-1]
            return self._resolve_path(var_path)
        
        return resolved
    
    def _resolve_path(self, path: str) -> Any:
        """Resolve a dotted path to a value.
        
        Args:
            path: Dotted path (e.g., "task_name.output.field")
            
        Returns:
            Resolved value
        """
        parts = path.split('.')
        
        # Check if it's a task result reference
        if parts[0] in self._task_results:
            value = self._task_results[parts[0]]
            
            # Navigate through nested attributes
            for part in parts[1:]:
                if isinstance(value, dict):
                    value = value.get(part)
                elif hasattr(value, part):
                    value = getattr(value, part)
                else:
                    return None
            
            return value
        
        # Check if it's a context variable
        if parts[0] in self.data:
            value = self.data[parts[0]]
            
            for part in parts[1:]:
                if isinstance(value, dict):
                    value = value.get(part)
                elif hasattr(value, part):
                    value = getattr(value, part)
                else:
                    return None
            
            return value
        
        return None
    
    def clear(self):
        """Clear all context data."""
        self.data.clear()
        self._task_results.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "data": self.data,
            "metadata": self.metadata,
            "task_results": self._task_results,
            "start_time": self.start_time.isoformat(),
        }
    
    def __repr__(self) -> str:
        return f"Context(tasks={len(self._task_results)}, vars={len(self.data)})"
