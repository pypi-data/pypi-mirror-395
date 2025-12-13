GEOMETOR • divine
=================

.. image:: https://img.shields.io/pypi/v/geometor-divine.svg
   :target: https://pypi.python.org/pypi/geometor-divine
.. image:: https://img.shields.io/github/license/geometor/divine.svg
   :target: https://github.com/geometor/divine/blob/main/LICENSE

An analysis engine for identifying golden sections and harmonic ranges.

Overview
--------

**geometor.divine** provides tools to identify deep geometric relationships within a model. It specifically focuses on the "Divine Proportion" (Golden Ratio) and harmonic ranges, revealing the hidden structure in geometric constructions.

Key Features
------------

- **Golden Section Analysis**: Automatically detects points that divide segments in the golden ratio.
- **Harmonic Ranges**: Identifies harmonic relationships between points on a line.
- **Pattern Recognition**: Groups related elements into chains and families.

Usage
-----

**divine** is primarily designed to work with `geometor.model` and is integrated directly into `geometor.explorer`.

You can also run the analysis script directly:

.. code-block:: bash

    divine

Or use it as a library:

.. code-block:: python

    from geometor.model import Model
    from geometor.divine import analyze_model

    model = Model("example")
    # ... perform constructions ...
    
    analysis = analyze_model(model)
    print(analysis.golden_sections)

Resources
---------

- **Source Code**: https://github.com/geometor/divine
- **Issues**: https://github.com/geometor/divine/issues

Related Projects
----------------

- `GEOMETOR Model <https://github.com/geometor/model>`_: The core symbolic engine.
- `GEOMETOR Explorer <https://github.com/geometor/explorer>`_: Interactive visualization.
