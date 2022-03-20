"""
Interface for Data Access
"""
from typing import Union

from .memory_store import MemoryStore
from .dynamodb_store import DynamoDBStore


__all__ = ["make_store"]


def make_store(db: str = "memory") -> Union[MemoryStore, DynamoDBStore]:
    if db == "memory":
        return MemoryStore()
    return DynamoDBStore()
