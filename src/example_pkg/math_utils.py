"""Tiny math utilities used in examples and tests.

Currently provides:
- add(a, b): return the sum of two integers.
"""

from __future__ import annotations


def add(a: int, b: int) -> int:
    """Return the sum of two integers.

    Examples
    --------
    >>> add(1, 2)
    3
    """
    return a + b
