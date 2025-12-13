"""Main entry point for the divine analysis module.

This module provides the primary hook for integrating divine analysis with the
geometor model.
"""

from __future__ import annotations
from geometor.model import Model
from .events import point_added_listener


def register_divine_hook(model: Model) -> None:
    """Initializes the divine analysis by registering the listener with the model's hook.

    Args:
        model: The model to attach the analysis hook to.
    """
    model.set_analysis_hook(lambda model, pt: point_added_listener(model, pt))
