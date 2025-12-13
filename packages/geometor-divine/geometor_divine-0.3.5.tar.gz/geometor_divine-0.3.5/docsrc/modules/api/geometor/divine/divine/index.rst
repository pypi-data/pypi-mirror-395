geometor.divine.divine
======================

.. py:module:: geometor.divine.divine

.. autoapi-nested-parse::

   Main entry point for the divine analysis module.

   This module provides the primary hook for integrating divine analysis with the
   geometor model.



Functions
---------

.. autoapisummary::

   geometor.divine.divine.register_divine_hook


Module Contents
---------------

.. py:function:: register_divine_hook(model: geometor.model.Model) -> None

   Initializes the divine analysis by registering the listener with the model's hook.

   :param model: The model to attach the analysis hook to.


