"""Plugin loader for dynamically loading FlowMind plugins."""

import importlib
import importlib.util
from pathlib import Path
from typing import Optional


def load_plugin(plugin_path: str) -> bool:
    """Load a plugin from a Python file.
    
    Args:
        plugin_path: Path to plugin file (.py)
        
    Returns:
        True if plugin loaded successfully
        
    Example:
        >>> load_plugin("my_plugins/custom_task.py")
    """
    try:
        path = Path(plugin_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Plugin file not found: {plugin_path}")
        
        # Load module from file
        spec = importlib.util.spec_from_file_location(path.stem, plugin_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True
        
        return False
        
    except Exception as e:
        print(f"Failed to load plugin: {e}")
        return False


def load_plugins_from_directory(directory: str) -> int:
    """Load all plugins from a directory.
    
    Args:
        directory: Path to directory containing plugins
        
    Returns:
        Number of plugins loaded
    """
    path = Path(directory)
    loaded = 0
    
    if not path.exists():
        return loaded
    
    for plugin_file in path.glob("*.py"):
        if plugin_file.stem.startswith("_"):
            continue
        
        if load_plugin(str(plugin_file)):
            loaded += 1
    
    return loaded
