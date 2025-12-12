"""Helper utilities for common operations."""

import json
import csv
from typing import Any, Dict, List
from pathlib import Path


def read_file(file_path: str, encoding: str = 'utf-8') -> str:
    """Read text file contents.
    
    Args:
        file_path: Path to file
        encoding: File encoding
        
    Returns:
        File contents
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()


def write_file(file_path: str, content: str, encoding: str = 'utf-8'):
    """Write content to file.
    
    Args:
        file_path: Path to file
        content: Content to write
        encoding: File encoding
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)


def parse_json(content: str) -> Dict[str, Any]:
    """Parse JSON string.
    
    Args:
        content: JSON string
        
    Returns:
        Parsed dictionary
    """
    return json.loads(content)


def parse_csv(file_path: str) -> List[Dict[str, Any]]:
    """Parse CSV file to list of dictionaries.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        List of row dictionaries
    """
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human-readable string.
    
    Args:
        bytes_val: Number of bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def ensure_dir(path: str):
    """Ensure directory exists.
    
    Args:
        path: Directory path
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def file_exists(path: str) -> bool:
    """Check if file exists.
    
    Args:
        path: File path
        
    Returns:
        True if file exists
    """
    return Path(path).exists()
