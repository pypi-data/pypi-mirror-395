"""
divine
"""
from __future__ import annotations
from geometor.model import Model
from .events import point_added_listener

def register_divine_hook(model: Model):
    """
    Initializes the divine analysis by registering the listener with the model's hook.

    Args:
        model: The model to attach the analysis hook to.
    """
    model.set_analysis_hook(lambda model, pt: point_added_listener(model, pt))

