"""Local file storage for FlowMind."""

import json
import pickle
from pathlib import Path
from typing import Any, Optional


class LocalStorage:
    """Local file-based storage.
    
    Provides simple key-value storage using local files.
    
    Attributes:
        storage_dir: Directory for storing files
    """
    
    def __init__(self, storage_dir: str = ".flowmind"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, key: str, value: Any, format: str = "pickle"):
        """Save value to storage.
        
        Args:
            key: Storage key
            value: Value to store
            format: Storage format ("pickle" or "json")
        """
        file_path = self.storage_dir / key
        
        if format == "json":
            with open(file_path, 'w') as f:
                json.dump(value, f, indent=2)
        else:
            with open(file_path, 'wb') as f:
                pickle.dump(value, f)
    
    def load(self, key: str, format: str = "pickle") -> Optional[Any]:
        """Load value from storage.
        
        Args:
            key: Storage key
            format: Storage format ("pickle" or "json")
            
        Returns:
            Stored value or None
        """
        file_path = self.storage_dir / key
        
        if not file_path.exists():
            return None
        
        if format == "json":
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
    
    def exists(self, key: str) -> bool:
        """Check if key exists.
        
        Args:
            key: Storage key
            
        Returns:
            True if key exists
        """
        return (self.storage_dir / key).exists()
    
    def delete(self, key: str) -> bool:
        """Delete stored value.
        
        Args:
            key: Storage key
            
        Returns:
            True if deleted
        """
        file_path = self.storage_dir / key
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    def list_keys(self) -> list:
        """List all stored keys.
        
        Returns:
            List of keys
        """
        return [f.name for f in self.storage_dir.iterdir() if f.is_file()]
