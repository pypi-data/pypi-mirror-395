"""Tools for analyzing geometric models to identify divine proportions.

**Key Components**
- **Analysis Hook**: A mechanism :func:`register_divine_hook` to automatically analyze points as they are added to the model.
- **Golden Sections**: Tools to find and verify golden ratio relationships (:mod:`geometor.divine.golden`).
- **Events**: Listeners that trigger analysis on model updates.

**Usage**
Register the divine hook with a :class:`~geometor.model.Model` instance to enable real-time analysis.
"""

from __future__ import annotations
from .divine import register_divine_hook

__all__ = [
    "register_divine_hook",
]


__version__ = "0.3.5"
