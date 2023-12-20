#!/usr/bin/env python3
"""Task advanced"""
import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    """It uses the requests module to obtain the HTML content of a particular
    URL and returns it."""
    if url is None or len(url.strip()) == 0:
        return ''
    store = redis.Redis()
    res_keys = 'result:{}'.format(url)
    req_keys = 'count:{}'.format(url)
    result = store.get(res_keys)
    if result is not None:
        store.incr(req_keys)
        return result
    result = requests.get(url).content.decode('utf-8')
    store.setex(res_keys, timedelta(seconds=10), result)
    return result
