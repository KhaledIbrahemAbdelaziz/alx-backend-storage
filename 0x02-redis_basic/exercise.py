#!/usr/bin/env python3
"""Task 0"""
from typing import Union, Callable, Optional
from functools import wraps
import redis
import uuid


class Cache:
    """Implements the cache class"""
    def __init__(self):
        """Initializes the attributes in the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key (e.g. using uuid),
        store the input data in Redis using the random key
        and return the key."""
        keys = str(uuid.uuid4())
        self._redis.mset({key: data})
        return keys
