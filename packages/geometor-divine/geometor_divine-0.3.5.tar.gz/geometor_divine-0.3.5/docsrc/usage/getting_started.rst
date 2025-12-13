:order: 2

getting started
===============

``geometor.divine`` is typically used in conjunction with ``geometor.model``.

.. code-block:: python

   from geometor.model import Model
   from geometor.divine import analyze_model

   model = Model("example")
   # ... perform constructions ...

   # Run the analysis
   analyze_model(model)

   # Access results from standard model reports or specific divine attributes
   print(model.goldens)
