from __future__ import annotations
from typing import Iterable
from .core import ArrayFlux


def arrayflux(obj: Iterable) -> ArrayFlux:
    """Public API: create an ArrayFlux object."""
    return ArrayFlux(obj)
