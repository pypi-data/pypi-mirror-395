geometor.divine
===============

.. py:module:: geometor.divine

.. autoapi-nested-parse::

   Tools for analyzing geometric models to identify divine proportions.

   **Key Components**
   - **Analysis Hook**: A mechanism :func:`register_divine_hook` to automatically analyze points as they are added to the model.
   - **Golden Sections**: Tools to find and verify golden ratio relationships (:mod:`geometor.divine.golden`).
   - **Events**: Listeners that trigger analysis on model updates.

   **Usage**
   Register the divine hook with a :class:`~geometor.model.Model` instance to enable real-time analysis.



Submodules
----------

.. toctree::
   :maxdepth: 1

   /modules/api/geometor/divine/__main__/index
   /modules/api/geometor/divine/divine/index
   /modules/api/geometor/divine/events/index
   /modules/api/geometor/divine/golden/index


Functions
---------

.. autoapisummary::

   geometor.divine.register_divine_hook


Package Contents
----------------

.. py:function:: register_divine_hook(model: geometor.model.Model) -> None

   Initializes the divine analysis by registering the listener with the model's hook.

   :param model: The model to attach the analysis hook to.


