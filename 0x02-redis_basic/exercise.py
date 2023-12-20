#!/usr/bin/env python3
"""Task 0"""
from typing import Union, Callable, Optional
from functools import wraps
import redis
import uuid


class Cache:
    """Implements the cache class"""
    def __init__(self):
        """stores an instance of the Redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes and stores a data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self,
            key: str, fn: Optional[Callable] = None) -> str:
        """Takes a key string argument and an optional.
        Callable argument named fn. This callable will be used to\
            convertthe data back to a desired format."""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, data: str) -> str:
        """Returns str value of decoded byte """
        return data.decode('utf-8', 'strict')

    def get_int(self, data: str) -> int:
        """Returns int value of decoded byte """
        return int(data)
