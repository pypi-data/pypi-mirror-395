"""Plugin system for FlowMind."""

from flowmind.plugins.registry import register_task, get_task, list_tasks
from flowmind.plugins.loader import load_plugin

__all__ = [
    "register_task",
    "get_task",
    "list_tasks",
    "load_plugin",
]
