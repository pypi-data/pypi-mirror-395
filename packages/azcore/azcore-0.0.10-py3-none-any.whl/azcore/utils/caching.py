"""
Caching utilities for the Azcore..

This module provides various caching strategies to improve workflow efficiency:
- LLM response caching (exact and semantic)
- Embedding caching
- State caching
- Time-based TTL caching
- LRU caching with size limits
"""

import hashlib
import json
import time
import pickle
from pathlib import Path
from typing import Any, Dict, Optional, Callable, Tuple
from functools import wraps
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class CacheEntry:
    """
    A cache entry with metadata.
    
    Attributes:
        value: The cached value
        timestamp: When the entry was created
        hits: Number of times accessed
        size_bytes: Approximate size in bytes
    """
    
    def __init__(self, value: Any, size_bytes: Optional[int] = None):
        """Initialize cache entry."""
        self.value = value
        self.timestamp = time.time()
        self.hits = 0
        self.size_bytes = size_bytes or len(str(value))
    
    def access(self) -> Any:
        """Record access and return value."""
        self.hits += 1
        return self.value
    
    def age(self) -> float:
        """Get age in seconds."""
        return time.time() - self.timestamp
    
    def is_expired(self, ttl: float) -> bool:
        """Check if entry has expired."""
        return self.age() > ttl


class LRUCache:
    """
    Least Recently Used (LRU) cache with size limit.
    
    Evicts least recently used items when size limit is reached.
    """
    
    def __init__(self, max_size: int = 1000, max_memory_mb: float = 100.0):
        """
        Initialize LRU cache.
        
        Args:
            max_size: Maximum number of entries
            max_memory_mb: Maximum memory usage in MB
        """
        self.max_size = max_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024)
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.total_size_bytes = 0
        self._hits = 0
        self._misses = 0
        
        logger.info(f"LRU Cache initialized: max_size={max_size}, max_memory={max_memory_mb}MB")
    
    def _make_key(self, *args, **kwargs) -> str:
        """Create cache key from arguments."""
        key_data = {"args": args, "kwargs": kwargs}
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            self._hits += 1
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key].access()
        
        self._misses += 1
        return None
    
    def put(self, key: str, value: Any, size_bytes: Optional[int] = None) -> None:
        """Put value in cache."""
        entry = CacheEntry(value, size_bytes)
        
        # If key exists, update and move to end
        if key in self.cache:
            old_entry = self.cache[key]
            self.total_size_bytes -= old_entry.size_bytes
            del self.cache[key]
        
        # Add new entry
        self.cache[key] = entry
        self.cache.move_to_end(key)
        self.total_size_bytes += entry.size_bytes
        
        # Evict if necessary
        self._evict_if_needed()
    
    def _evict_if_needed(self) -> None:
        """Evict least recently used items if limits exceeded."""
        while len(self.cache) > self.max_size or self.total_size_bytes > self.max_memory_bytes:
            if not self.cache:
                break
            
            # Remove oldest (least recently used)
            key, entry = self.cache.popitem(last=False)
            self.total_size_bytes -= entry.size_bytes
            logger.debug(f"Evicted cache entry: {key[:16]}... (size={entry.size_bytes})")
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self.total_size_bytes = 0
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "memory_bytes": self.total_size_bytes,
            "max_memory_bytes": self.max_memory_bytes,
            "memory_mb": self.total_size_bytes / (1024 * 1024),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }


class TTLCache:
    """
    Time-To-Live (TTL) cache.
    
    Entries expire after a specified time period.
    """
    
    def __init__(self, ttl: float = 3600.0, max_size: int = 1000):
        """
        Initialize TTL cache.
        
        Args:
            ttl: Time to live in seconds (default: 1 hour)
            max_size: Maximum number of entries
        """
        self.ttl = ttl
        self.max_size = max_size
        self.cache: Dict[str, CacheEntry] = {}
        self._hits = 0
        self._misses = 0
        
        logger.info(f"TTL Cache initialized: ttl={ttl}s, max_size={max_size}")
    
    def _clean_expired(self) -> None:
        """Remove expired entries."""
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired(self.ttl)
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.debug(f"Cleaned {len(expired_keys)} expired entries")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        self._clean_expired()
        
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired(self.ttl):
                self._hits += 1
                return entry.access()
            else:
                del self.cache[key]
        
        self._misses += 1
        return None
    
    def put(self, key: str, value: Any) -> None:
        """Put value in cache."""
        self._clean_expired()
        
        # Enforce max size
        if len(self.cache) >= self.max_size and key not in self.cache:
            # Remove oldest entry
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k].timestamp)
            del self.cache[oldest_key]
        
        self.cache[key] = CacheEntry(value)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        logger.info("TTL cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        self._clean_expired()
        
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl": self.ttl,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }


class SemanticCache:
    """
    Semantic cache using embedding similarity.
    
    Caches responses based on semantic similarity rather than exact match.
    """
    
    def __init__(
        self,
        embedding_function: Optional[Callable] = None,
        similarity_threshold: float = 0.95,
        max_size: int = 500
    ):
        """
        Initialize semantic cache.
        
        Args:
            embedding_function: Function to generate embeddings
            similarity_threshold: Minimum similarity for cache hit (0.0-1.0)
            max_size: Maximum number of cached entries
        """
        self.embedding_function = embedding_function
        self.similarity_threshold = similarity_threshold
        self.max_size = max_size
        self.cache: Dict[str, Tuple[Any, Any]] = {}  # key -> (embedding, value)
        self._hits = 0
        self._misses = 0
        
        logger.info(
            f"Semantic Cache initialized: threshold={similarity_threshold}, "
            f"max_size={max_size}"
        )
    
    def _compute_similarity(self, emb1: Any, emb2: Any) -> float:
        """Compute cosine similarity between embeddings."""
        try:
            import numpy as np
            emb1 = np.array(emb1)
            emb2 = np.array(emb2)
            
            # Cosine similarity
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            return float(similarity)
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
    
    def get(self, query: str) -> Optional[Any]:
        """Get value from cache if semantically similar."""
        if not self.embedding_function:
            return None
        
        try:
            query_emb = self.embedding_function(query)
            
            # Find most similar cached entry
            best_similarity = 0.0
            best_value = None
            
            for key, (cached_emb, cached_value) in self.cache.items():
                similarity = self._compute_similarity(query_emb, cached_emb)
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_value = cached_value
            
            # Check if similarity meets threshold
            if best_similarity >= self.similarity_threshold:
                self._hits += 1
                logger.debug(f"Semantic cache hit: similarity={best_similarity:.3f}")
                return best_value
            
            self._misses += 1
            return None
            
        except Exception as e:
            logger.error(f"Error in semantic cache lookup: {e}")
            self._misses += 1
            return None
    
    def put(self, query: str, value: Any) -> None:
        """Put value in cache with its embedding."""
        if not self.embedding_function:
            return
        
        try:
            query_emb = self.embedding_function(query)
            
            # Enforce max size (simple FIFO)
            if len(self.cache) >= self.max_size:
                # Remove oldest entry
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            
            key = hashlib.sha256(query.encode()).hexdigest()
            self.cache[key] = (query_emb, value)
            
        except Exception as e:
            logger.error(f"Error caching with embedding: {e}")
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        logger.info("Semantic cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "threshold": self.similarity_threshold,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }


class PersistentCache:
    """
    Persistent cache that saves to disk.
    
    Useful for caching expensive computations across sessions.
    """
    
    def __init__(self, cache_dir: str = "cache", ttl: float = 86400.0):
        """
        Initialize persistent cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl: Time to live in seconds (default: 24 hours)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        self._hits = 0
        self._misses = 0
        
        logger.info(f"Persistent cache initialized: dir={cache_dir}, ttl={ttl}s")
    
    def _get_cache_path(self, key: str) -> Path:
        """Get path for cache file."""
        return self.cache_dir / f"{key}.pkl"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from persistent cache."""
        cache_path = self._get_cache_path(key)
        
        if cache_path.exists():
            try:
                # Check if expired
                file_age = time.time() - cache_path.stat().st_mtime
                if file_age > self.ttl:
                    cache_path.unlink()
                    self._misses += 1
                    return None
                
                # Load from disk
                with open(cache_path, 'rb') as f:
                    value = pickle.load(f)
                
                self._hits += 1
                logger.debug(f"Persistent cache hit: {key[:16]}...")
                return value
                
            except Exception as e:
                logger.error(f"Error loading from persistent cache: {e}")
                self._misses += 1
                return None
        
        self._misses += 1
        return None
    
    def put(self, key: str, value: Any) -> None:
        """Put value in persistent cache."""
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
            logger.debug(f"Cached to disk: {key[:16]}...")
        except Exception as e:
            logger.error(f"Error saving to persistent cache: {e}")
    
    def clear(self) -> None:
        """Clear all persistent cache files."""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
        logger.info("Persistent cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0
        
        cache_files = list(self.cache_dir.glob("*.pkl"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            "size": len(cache_files),
            "directory": str(self.cache_dir),
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
            "total_requests": total_requests,
            "ttl": self.ttl
        }


def cached(cache: Any, key_func: Optional[Callable] = None):
    """
    Decorator for caching function results.
    
    Args:
        cache: Cache instance (LRUCache, TTLCache, etc.)
        key_func: Optional function to generate cache key from args
        
    Example:
        >>> cache = LRUCache(max_size=100)
        >>> 
        >>> @cached(cache)
        >>> def expensive_function(x, y):
        ...     return x * y
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key_data = {"func": func.__name__, "args": args, "kwargs": kwargs}
                key_str = json.dumps(key_data, sort_keys=True, default=str)
                key = hashlib.sha256(key_str.encode()).hexdigest()
            
            # Try to get from cache
            cached_value = cache.get(key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.put(key, result)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        
        return wrapper
    return decorator


# Global caches for common use cases
_llm_cache = LRUCache(max_size=500, max_memory_mb=50.0)
_embedding_cache = LRUCache(max_size=1000, max_memory_mb=100.0)
_state_cache = TTLCache(ttl=3600.0, max_size=100)


def get_llm_cache() -> LRUCache:
    """Get global LLM response cache."""
    return _llm_cache


def get_embedding_cache() -> LRUCache:
    """Get global embedding cache."""
    return _embedding_cache


def get_state_cache() -> TTLCache:
    """Get global state cache."""
    return _state_cache


def clear_all_caches() -> None:
    """Clear all global caches."""
    _llm_cache.clear()
    _embedding_cache.clear()
    _state_cache.clear()
    logger.info("All global caches cleared")


def get_all_cache_stats() -> Dict[str, Dict[str, Any]]:
    """Get statistics for all global caches."""
    return {
        "llm_cache": _llm_cache.get_stats(),
        "embedding_cache": _embedding_cache.get_stats(),
        "state_cache": _state_cache.get_stats()
    }
