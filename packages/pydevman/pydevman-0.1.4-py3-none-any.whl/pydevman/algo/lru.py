"""
create_time: 2025-06-22 16:12:08
author: jackylee
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

# from cachetools import LRUCache
# TODO 了解其功能


class LRU(ABC):
    @abstractmethod
    def get(self, key: str) -> object: ...

    @abstractmethod
    def put(self, key: str, val: object) -> bool: ...


class BuildInLRU(LRU):
    """使用 python 内置 OrderedDict 实现 LRU"""

    def __init__(self, capacity=10):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache.keys():
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, val):
        if key in self.cache.keys():
            self.cache.move_to_end(key)
        self.cache[key] = val
        if len(self.cache) > self.capacity:
            self.cache.popitem(False)
