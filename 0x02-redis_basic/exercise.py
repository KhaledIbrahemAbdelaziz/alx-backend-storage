#!/usr/bin/env python3
"""Task 0"""
from typing import Union, Callable, Optional
from functools import wraps
import redis
import uuid


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function"""
    method_keys = method.__qualname__
    inputs, outputs = method_keys + ':inputs', method_keys + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Creates and returns function that increments the count \
        for that key every time the method is called and returns \
        the value returned by the original method"""
    method_keys = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""
    method_keys = method.__qualname__
    inputs, outputs = method_keys + ':inputs', method_keys + ':outputs'
    redis = method.__self__._redis
    method_counts = redis.get(method_keys).decode('utf-8')
    print(f'{method_keys} was called {method_counts} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, outp in list(IOTuple):
        attr, data = inp.decode("utf-8"), outp.decode("utf-8")
        print(f'{method_keys}(*{attr}) -> {data}')
        
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
