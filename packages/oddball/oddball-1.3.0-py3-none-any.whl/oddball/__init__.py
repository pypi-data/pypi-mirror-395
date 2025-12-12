"""oddball anomaly detection datasets."""

from .data.loader import (
    clear_cache,
    get_cache_location,
    list_available,
    load,
    split_by_label,
)
from .enums import Dataset
from .generator import BaseDataGenerator, BatchGenerator, OnlineGenerator

__all__ = [
    "Dataset",
    "BaseDataGenerator",
    "BatchGenerator",
    "clear_cache",
    "get_cache_location",
    "list_available",
    "load",
    "OnlineGenerator",
    "split_by_label",
]
__version__ = "1.3.0"
