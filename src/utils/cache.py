from typing import Optional, Any, Callable
from pathlib import Path
import json
import hashlib
import time
from functools import wraps
import pickle

class Cache:
    """Simple file-based cache with TTL support."""
    
    def __init__(self, cache_dir: Path, ttl: int = 3600):
        """
        Initialize cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl: Time to live in seconds (default: 1 hour)
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> Path:
        """Generate cache file path from key."""
        hash_key = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.cache"
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve item from cache if it exists and hasn't expired."""
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None
            
        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
                
            if time.time() - data['timestamp'] > self.ttl:
                cache_path.unlink()
                return None
                
            return data['value']
        except Exception:
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Store item in cache with timestamp."""
        cache_path = self._get_cache_path(key)
        data = {
            'timestamp': time.time(),
            'value': value
        }
        
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
    
    def clear(self) -> None:
        """Clear all cached items."""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()

def cached(ttl: int = 3600):
    """Decorator for caching function results."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Create cache instance if it doesn't exist
            if not hasattr(self, '_cache'):
                cache_dir = self.file_handler.base_path / '.cache'
                self._cache = Cache(cache_dir, ttl)
            
            # Generate cache key
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            result = self._cache.get(key)
            
            if result is None:
                result = func(self, *args, **kwargs)
                self._cache.set(key, result)
            
            return result
        return wrapper
    return decorator
