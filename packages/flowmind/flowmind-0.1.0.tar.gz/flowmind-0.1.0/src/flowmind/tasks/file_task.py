"""File operations task for reading, writing, and processing files."""

import os
import json
from pathlib import Path
from typing import Any, Dict

from flowmind.core.task import BaseTask, TaskResult, TaskStatus
from flowmind.core.context import Context
from flowmind.utils.validator import Validator


class FileTask(BaseTask):
    """Task for file operations (read, write, copy, move, delete).
    
    Operations:
    - read: Read file contents
    - write: Write content to file
    - copy: Copy file
    - move: Move/rename file
    - delete: Delete file
    - exists: Check if file exists
    - list: List files in directory
    
    Example:
        >>> task = FileTask(
        ...     name="read_data",
        ...     operation="read",
        ...     file_path="data.json"
        ... )
    """
    
    def __init__(self, name: str, **config):
        super().__init__(name, "File operations task", **config)
    
    def validate(self) -> bool:
        """Validate task configuration."""
        try:
            Validator.require_fields(self.config, "operation")
            Validator.validate_choice(
                self.config["operation"],
                ["read", "write", "copy", "move", "delete", "exists", "list"],
                "operation"
            )
            return True
        except (ValueError, TypeError) as e:
            return False
    
    def execute(self, context: Context) -> TaskResult:
        """Execute the file operation."""
        operation = self.config["operation"]
        
        try:
            if operation == "read":
                result = self._read_file(context)
            elif operation == "write":
                result = self._write_file(context)
            elif operation == "copy":
                result = self._copy_file(context)
            elif operation == "move":
                result = self._move_file(context)
            elif operation == "delete":
                result = self._delete_file(context)
            elif operation == "exists":
                result = self._file_exists(context)
            elif operation == "list":
                result = self._list_files(context)
            else:
                return TaskResult(
                    status=TaskStatus.FAILED,
                    error=f"Unknown operation: {operation}"
                )
            
            return TaskResult(status=TaskStatus.SUCCESS, output=result)
            
        except Exception as e:
            return TaskResult(status=TaskStatus.FAILED, error=str(e))
    
    def _read_file(self, context: Context) -> str:
        """Read file contents."""
        file_path = context.resolve_variables(self.config.get("file_path"))
        encoding = self.config.get("encoding", "utf-8")
        
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        
        # Parse JSON if requested
        if self.config.get("parse_json", False):
            content = json.loads(content)
        
        return content
    
    def _write_file(self, context: Context) -> Dict[str, Any]:
        """Write content to file."""
        file_path = context.resolve_variables(self.config.get("file_path"))
        content = context.resolve_variables(self.config.get("content", ""))
        encoding = self.config.get("encoding", "utf-8")
        
        # Create parent directories if needed
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert dict to JSON if needed
        if isinstance(content, dict) and self.config.get("as_json", False):
            content = json.dumps(content, indent=2)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(str(content))
        
        return {"file_path": file_path, "size": os.path.getsize(file_path)}
    
    def _copy_file(self, context: Context) -> Dict[str, str]:
        """Copy file."""
        import shutil
        
        source = context.resolve_variables(self.config.get("source"))
        dest = context.resolve_variables(self.config.get("destination"))
        
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        
        return {"source": source, "destination": dest}
    
    def _move_file(self, context: Context) -> Dict[str, str]:
        """Move/rename file."""
        import shutil
        
        source = context.resolve_variables(self.config.get("source"))
        dest = context.resolve_variables(self.config.get("destination"))
        
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(source, dest)
        
        return {"source": source, "destination": dest}
    
    def _delete_file(self, context: Context) -> Dict[str, bool]:
        """Delete file."""
        file_path = context.resolve_variables(self.config.get("file_path"))
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"deleted": True, "file_path": file_path}
        else:
            return {"deleted": False, "file_path": file_path, "reason": "File not found"}
    
    def _file_exists(self, context: Context) -> Dict[str, bool]:
        """Check if file exists."""
        file_path = context.resolve_variables(self.config.get("file_path"))
        exists = os.path.exists(file_path)
        
        result = {"exists": exists, "file_path": file_path}
        if exists:
            result["size"] = os.path.getsize(file_path)
        
        return result
    
    def _list_files(self, context: Context) -> list:
        """List files in directory."""
        directory = context.resolve_variables(self.config.get("directory", "."))
        pattern = self.config.get("pattern", "*")
        
        path = Path(directory)
        files = list(path.glob(pattern))
        
        return [str(f) for f in files]


# Register task type
from flowmind.core.task import TaskFactory
TaskFactory.register("file", FileTask)
