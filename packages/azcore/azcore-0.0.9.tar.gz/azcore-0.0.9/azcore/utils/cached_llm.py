"""
Cached LLM wrapper for the Azcore..

This module provides wrappers around LangChain LLMs that add caching
to reduce API calls and improve response times.
"""

import hashlib
from typing import Any, Dict, List, Optional, Union
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from azcore.utils.caching import SemanticCache, get_llm_cache
import logging

logger = logging.getLogger(__name__)


class CachedLLM:
    """
    Wrapper around LangChain LLM that adds caching.
    
    Caches LLM responses to reduce API calls and costs.
    Supports both exact matching and semantic caching.
    
    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> llm = ChatOpenAI(model="gpt-4o-mini")
        >>> cached_llm = CachedLLM(llm, cache_type="exact")
        >>> 
        >>> # First call hits API
        >>> response1 = cached_llm.invoke("What is 2+2?")
        >>> 
        >>> # Second call uses cache
        >>> response2 = cached_llm.invoke("What is 2+2?")
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        cache_type: str = "exact",
        cache: Optional[Any] = None,
        semantic_threshold: float = 0.95,
        enable_logging: bool = True
    ):
        """
        Initialize cached LLM.
        
        Args:
            llm: Base LLM to wrap
            cache_type: Type of cache ("exact" or "semantic")
            cache: Optional custom cache instance
            semantic_threshold: Similarity threshold for semantic caching
            enable_logging: Enable cache hit/miss logging
        """
        self.llm = llm
        self.cache_type = cache_type
        self.enable_logging = enable_logging
        
        # Initialize cache
        if cache:
            self.cache = cache
        elif cache_type == "semantic":
            # Semantic cache requires embedding function
            try:
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer('all-MiniLM-L6-v2')
                embed_func = lambda text: model.encode(text).tolist()
                self.cache = SemanticCache(
                    embedding_function=embed_func,
                    similarity_threshold=semantic_threshold,
                    max_size=500
                )
                logger.info("Initialized semantic caching for LLM")
            except ImportError:
                logger.warning(
                    "sentence-transformers not installed, falling back to exact caching"
                )
                self.cache_type = "exact"
                self.cache = get_llm_cache()
        else:
            # Use global LLM cache
            self.cache = get_llm_cache()
        
        logger.info(f"CachedLLM initialized with {cache_type} caching")
    
    def _make_cache_key(self, messages: Union[str, List]) -> str:
        """Create cache key from messages."""
        if isinstance(messages, str):
            key_str = messages
        elif isinstance(messages, list):
            # Handle list of messages
            key_parts = []
            for msg in messages:
                if isinstance(msg, BaseMessage):
                    key_parts.append(f"{msg.type}:{msg.content}")
                elif isinstance(msg, dict):
                    key_parts.append(f"{msg.get('role', 'unknown')}:{msg.get('content', '')}")
                elif isinstance(msg, tuple):
                    key_parts.append(f"{msg[0]}:{msg[1]}")
                else:
                    key_parts.append(str(msg))
            key_str = "|".join(key_parts)
        else:
            key_str = str(messages)
        
        # For exact caching, use hash
        if self.cache_type == "exact":
            return hashlib.sha256(key_str.encode()).hexdigest()
        else:
            # For semantic caching, return text directly
            return key_str
    
    def invoke(self, input: Union[str, List], **kwargs) -> Any:
        """
        Invoke LLM with caching.
        
        Args:
            input: Prompt string or list of messages
            **kwargs: Additional arguments for LLM
            
        Returns:
            LLM response (from cache or API)
        """
        # Create cache key
        cache_key = self._make_cache_key(input)
        
        # Try cache
        cached_response = self.cache.get(cache_key)
        if cached_response is not None:
            if self.enable_logging:
                logger.info(f"Cache HIT for {self.cache_type} cache")
            return cached_response
        
        # Cache miss - call actual LLM
        if self.enable_logging:
            logger.info(f"Cache MISS - calling LLM")
        
        response = self.llm.invoke(input, **kwargs)
        
        # Store in cache
        self.cache.put(cache_key, response)
        
        return response
    
    async def ainvoke(self, input: Union[str, List], **kwargs) -> Any:
        """
        Async invoke LLM with caching.
        
        Args:
            input: Prompt string or list of messages
            **kwargs: Additional arguments for LLM
            
        Returns:
            LLM response (from cache or API)
        """
        # Create cache key
        cache_key = self._make_cache_key(input)
        
        # Try cache
        cached_response = self.cache.get(cache_key)
        if cached_response is not None:
            if self.enable_logging:
                logger.info(f"Cache HIT for {self.cache_type} cache")
            return cached_response
        
        # Cache miss - call actual LLM
        if self.enable_logging:
            logger.info(f"Cache MISS - calling LLM")
        
        response = await self.llm.ainvoke(input, **kwargs)
        
        # Store in cache
        self.cache.put(cache_key, response)
        
        return response
    
    def batch(self, inputs: List, **kwargs) -> List:
        """
        Batch invoke with caching.
        
        Args:
            inputs: List of inputs
            **kwargs: Additional arguments
            
        Returns:
            List of responses
        """
        results = []
        uncached_inputs = []
        uncached_indices = []
        
        # Check cache for each input
        for i, input_item in enumerate(inputs):
            cache_key = self._make_cache_key(input_item)
            cached_response = self.cache.get(cache_key)
            
            if cached_response is not None:
                results.append(cached_response)
            else:
                results.append(None)  # Placeholder
                uncached_inputs.append(input_item)
                uncached_indices.append(i)
        
        # Batch call for uncached inputs
        if uncached_inputs:
            if self.enable_logging:
                logger.info(
                    f"Batch: {len(uncached_inputs)}/{len(inputs)} cache misses"
                )
            
            uncached_responses = self.llm.batch(uncached_inputs, **kwargs)
            
            # Store in cache and update results
            for idx, response in zip(uncached_indices, uncached_responses):
                cache_key = self._make_cache_key(inputs[idx])
                self.cache.put(cache_key, response)
                results[idx] = response
        elif self.enable_logging:
            logger.info(f"Batch: All {len(inputs)} inputs cached!")
        
        return results
    
    def with_structured_output(self, schema: Any, **kwargs):
        """
        Get LLM with structured output (delegates to wrapped LLM).
        
        Note: Structured outputs are not cached as they may vary.
        """
        return self.llm.with_structured_output(schema, **kwargs)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if hasattr(self.cache, 'get_stats'):
            return self.cache.get_stats()
        return {}
    
    def clear_cache(self) -> None:
        """Clear the cache."""
        if hasattr(self.cache, 'clear'):
            self.cache.clear()
            logger.info("LLM cache cleared")
    
    def __getattr__(self, name: str):
        """Delegate unknown attributes to wrapped LLM."""
        return getattr(self.llm, name)


def create_cached_llm(
    llm: BaseChatModel,
    cache_type: str = "exact",
    **kwargs
) -> CachedLLM:
    """
    Factory function to create a cached LLM.
    
    Args:
        llm: Base LLM to wrap
        cache_type: "exact" or "semantic"
        **kwargs: Additional arguments for CachedLLM
        
    Returns:
        CachedLLM instance
        
    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> llm = ChatOpenAI(model="gpt-4o-mini")
        >>> cached_llm = create_cached_llm(llm, cache_type="exact")
    """
    return CachedLLM(llm, cache_type=cache_type, **kwargs)


def enable_llm_caching(llm: BaseChatModel, cache_type: str = "exact") -> CachedLLM:
    """
    Convenience function to wrap an LLM with caching.
    
    Args:
        llm: LLM to wrap
        cache_type: Type of caching
        
    Returns:
        Cached LLM
        
    Example:
        >>> llm = ChatOpenAI(model="gpt-4o-mini")
        >>> llm = enable_llm_caching(llm)  # Now cached!
    """
    return create_cached_llm(llm, cache_type=cache_type)
