"""Shell command execution task."""

import subprocess
from typing import Any, Dict

from flowmind.core.task import BaseTask, TaskResult, TaskStatus, TaskFactory
from flowmind.core.context import Context


class ShellTask(BaseTask):
    """Task for executing shell commands.
    
    Operations:
    - run: Execute a shell command
    
    Example:
        >>> task = ShellTask(
        ...     name="list_files",
        ...     command="ls -la"
        ... )
    """
    
    def __init__(self, name: str, **config):
        super().__init__(name, "Shell command task", **config)
    
    def execute(self, context: Context) -> TaskResult:
        """Execute the shell command."""
        try:
            command = context.resolve_variables(self.config.get("command"))
            cwd = self.config.get("cwd")
            timeout = self.config.get("timeout", 30)
            shell = self.config.get("shell", True)
            
            result = subprocess.run(
                command,
                shell=shell,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "command": command,
                "success": result.returncode == 0
            }
            
            if result.returncode != 0:
                return TaskResult(
                    status=TaskStatus.FAILED,
                    output=output,
                    error=f"Command failed with code {result.returncode}"
                )
            
            return TaskResult(status=TaskStatus.SUCCESS, output=output)
            
        except subprocess.TimeoutExpired:
            return TaskResult(
                status=TaskStatus.FAILED,
                error=f"Command timed out after {timeout} seconds"
            )
        except Exception as e:
            return TaskResult(status=TaskStatus.FAILED, error=str(e))


# Register task type
TaskFactory.register("shell", ShellTask)
TaskFactory.register("command", ShellTask)
TaskFactory.register("run", ShellTask)
