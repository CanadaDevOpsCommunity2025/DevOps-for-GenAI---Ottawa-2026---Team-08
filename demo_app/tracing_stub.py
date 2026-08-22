"""Temporary no-op stand-in for obeverfy.tracing.traced.

The SDK (Task 2 of docs/plans/obeverfy-implementation-plan.md) hasn't been
built yet. Once it exists, swap each `from .tracing_stub import traced` in
this package for `from obeverfy.tracing import traced` -- same decorator
signature (`traced(name=None, kind="chain")`), so nothing else needs to change.
"""
from __future__ import annotations

import functools
from typing import Callable, Optional


def traced(name: Optional[str] = None, kind: str = "chain") -> Callable:
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    return decorator
