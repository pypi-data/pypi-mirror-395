"""Simple cache manager for FlowMind."""

import time
from typing import Any, Dict, Optional


class Cache:
    """In-memory cache with expiration.
    
    Attributes:
        ttl: Default time-to-live in seconds
    """
    
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self._cache: Dict[str, tuple] = {}  # key -> (value, expiry_time)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cache value.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional custom TTL
        """
        expiry = time.time() + (ttl if ttl is not None else self.ttl)
        self._cache[key] = (value, expiry)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get cache value.
        
        Args:
            key: Cache key
            default: Default value if not found
            
        Returns:
            Cached value or default
        """
        if key not in self._cache:
            return default
        
        value, expiry = self._cache[key]
        
        # Check if expired
        if time.time() > expiry:
            del self._cache[key]
            return default
        
        return value
    
    def delete(self, key: str) -> bool:
        """Delete cache entry.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
    
    def cleanup(self):
        """Remove expired entries."""
        now = time.time()
        expired = [k for k, (_, expiry) in self._cache.items() if now > expiry]
        for key in expired:
            del self._cache[key]
    
    def __len__(self) -> int:
        """Get number of cached items."""
        self.cleanup()
        return len(self._cache)
