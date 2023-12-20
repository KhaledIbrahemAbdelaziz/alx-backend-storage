#!/usr/bin/env python3
"""Task 0"""
from typing import Union, Callable, Optional
from functools import wraps
import redis
import uuid


class Cache:
    """Implements the cache class"""
    def __init__(self):
        """Initializes the attributes of the Redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes and stores a data argument and returns a string."""
        keys = str(uuid.uuid4())
        self._redis.mset({keys: data})
        return keys
