"""
FlowMind - A Multi-Agent Automation Platform for Enterprise Tasks

A lightweight, native Python agent framework for building automation workflows
without the complexity of LangChain or enterprise tools.

Features:
- Native Python implementation
- Zero-dependency core
- Plugin architecture
- Offline-first design
- Built-in tasks for common operations
- Simple task-based API

Example:
    >>> from flowmind import FlowAgent
    >>> agent = FlowAgent("my_workflow")
    >>> agent.add_task("download", url="https://api.example.com/data.json")
    >>> agent.add_task("transform", operation="filter", condition="price > 100")
    >>> agent.run()
"""

__version__ = "0.1.0"
__author__ = "Idriss Bado"
__email__ = "idrissbado@gmail.com"
__license__ = "MIT"

from flowmind.agent import FlowAgent
from flowmind.core.task import BaseTask, TaskResult, TaskStatus
from flowmind.core.context import Context
from flowmind.core.pipeline import Pipeline

# Import built-in tasks
from flowmind.tasks.file_task import FileTask
from flowmind.tasks.web_task import WebTask
from flowmind.tasks.data_task import DataTask
from flowmind.tasks.email_task import EmailTask
from flowmind.tasks.pdf_task import PDFTask
from flowmind.tasks.ml_task import MLTask
from flowmind.tasks.shell_task import ShellTask

# Import plugin system
from flowmind.plugins.registry import register_task, get_task

__all__ = [
    # Core classes
    "FlowAgent",
    "BaseTask",
    "TaskResult",
    "TaskStatus",
    "Context",
    "Pipeline",
    
    # Built-in tasks
    "FileTask",
    "WebTask",
    "DataTask",
    "EmailTask",
    "PDFTask",
    "MLTask",
    "ShellTask",
    
    # Plugin system
    "register_task",
    "get_task",
]
