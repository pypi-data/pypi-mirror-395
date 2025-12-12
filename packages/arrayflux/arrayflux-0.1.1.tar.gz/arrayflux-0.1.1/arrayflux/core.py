from __future__ import annotations
from typing import Iterable
import numpy as np


class ArrayFlux(np.ndarray):
    """NumPy ndarray subclass with extended features."""

    __array_priority__ = 1000.0

    def __new__(cls, obj: Iterable) -> "ArrayFlux":
        arr = np.asarray(obj).view(cls)
        return arr

    def __array_finalize__(self, parent) -> None:
        if parent is None:
            return

    def rolling(self, window: int):
        from .rolling import Rolling
        return Rolling(self, window)
