"""Data transformation task for processing and manipulating data."""

import json
from typing import Any, Dict, List

from flowmind.core.task import BaseTask, TaskResult, TaskStatus, TaskFactory
from flowmind.core.context import Context


class DataTask(BaseTask):
    """Task for data transformation and processing.
    
    Operations:
    - filter: Filter data by condition
    - transform: Apply transformation
    - aggregate: Aggregate data
    - merge: Merge datasets
    - sort: Sort data
    
    Example:
        >>> task = DataTask(
        ...     name="filter_data",
        ...     operation="filter",
        ...     condition="value > 100"
        ... )
    """
    
    def __init__(self, name: str, **config):
        super().__init__(name, "Data transformation task", **config)
    
    def execute(self, context: Context) -> TaskResult:
        """Execute the data operation."""
        operation = self.config.get("operation", "transform")
        input_data = context.resolve_variables(self.config.get("input"))
        
        try:
            if operation == "filter":
                result = self._filter_data(input_data, context)
            elif operation == "transform":
                result = self._transform_data(input_data, context)
            elif operation == "aggregate":
                result = self._aggregate_data(input_data, context)
            elif operation == "merge":
                result = self._merge_data(input_data, context)
            elif operation == "sort":
                result = self._sort_data(input_data, context)
            else:
                result = input_data
            
            return TaskResult(status=TaskStatus.SUCCESS, output=result)
            
        except Exception as e:
            return TaskResult(status=TaskStatus.FAILED, error=str(e))
    
    def _filter_data(self, data: Any, context: Context) -> Any:
        """Filter data by condition."""
        condition = self.config.get("condition")
        
        if isinstance(data, list):
            # Filter list of dicts
            if condition:
                filtered = []
                for item in data:
                    # Simple condition evaluation
                    if self._eval_condition(condition, item):
                        filtered.append(item)
                return filtered
        
        return data
    
    def _eval_condition(self, condition: str, item: Dict) -> bool:
        """Evaluate condition on item."""
        try:
            # Very basic evaluation - for production, use safer approach
            return eval(condition, {"__builtins__": {}}, item)
        except:
            return False
    
    def _transform_data(self, data: Any, context: Context) -> Any:
        """Transform data."""
        transform_func = self.config.get("transform")
        
        if transform_func == "to_json" and not isinstance(data, str):
            return json.dumps(data, indent=2)
        elif transform_func == "from_json" and isinstance(data, str):
            return json.loads(data)
        elif transform_func == "to_upper" and isinstance(data, str):
            return data.upper()
        elif transform_func == "to_lower" and isinstance(data, str):
            return data.lower()
        
        return data
    
    def _aggregate_data(self, data: List[Dict], context: Context) -> Dict:
        """Aggregate data."""
        if not isinstance(data, list):
            return {}
        
        agg_type = self.config.get("agg_type", "count")
        field = self.config.get("field")
        
        if agg_type == "count":
            return {"count": len(data)}
        elif agg_type == "sum" and field:
            total = sum(item.get(field, 0) for item in data if isinstance(item, dict))
            return {"sum": total, "field": field}
        elif agg_type == "avg" and field:
            values = [item.get(field, 0) for item in data if isinstance(item, dict)]
            avg = sum(values) / len(values) if values else 0
            return {"avg": avg, "field": field}
        
        return {"count": len(data)}
    
    def _merge_data(self, data1: Any, context: Context) -> Any:
        """Merge two datasets."""
        data2 = context.resolve_variables(self.config.get("merge_with"))
        
        if isinstance(data1, list) and isinstance(data2, list):
            return data1 + data2
        elif isinstance(data1, dict) and isinstance(data2, dict):
            merged = data1.copy()
            merged.update(data2)
            return merged
        
        return data1
    
    def _sort_data(self, data: List, context: Context) -> List:
        """Sort data."""
        if not isinstance(data, list):
            return data
        
        key = self.config.get("key")
        reverse = self.config.get("reverse", False)
        
        if key and all(isinstance(item, dict) for item in data):
            return sorted(data, key=lambda x: x.get(key, 0), reverse=reverse)
        else:
            return sorted(data, reverse=reverse)


# Register task type
TaskFactory.register("data", DataTask)
TaskFactory.register("transform", DataTask)
TaskFactory.register("filter", DataTask)
