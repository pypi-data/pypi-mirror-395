geometor.divine.golden.chains
=============================

.. py:module:: geometor.divine.golden.chains

.. autoapi-nested-parse::

   Golden Chain Analyzer: Harmonic Range Identification in Golden Sections.

   This module is designed to analyze and explore chains of connected golden
   sections, unraveling the harmonic ranges within geometric structures.
   Utilizing sophisticated mathematical analysis and geometric algorithms,
   it aims to identify, categorize, and unpack chains, providing an intuitive
   understanding of their intrinsic geometric harmonies.

   Features:

   - ``find_chains_in_sections``: A function designed to meticulously identify
     chains within a collection of sections, resulting in a hierarchical tree
     structure representing connected sections.

   - ``unpack_chains``: Unveils the chains hidden within the tree structure,
     outputting a list of individual :class:`Chain` objects ready for analysis.

   Each chain’s flow is characterized by the comparative lengths of consecutive
   segments, represented symbolically to understand the progression and
   transitions in segment lengths. Furthermore, this module empowers users to
   explore symmetry lines within chains, unveiling a subtle, profound aspect of
   geometric harmony.



Functions
---------

.. autoapisummary::

   geometor.divine.golden.chains.find_chains_in_sections
   geometor.divine.golden.chains.unpack_chains


Module Contents
---------------

.. py:function:: find_chains_in_sections(sections: list[geometor.model.sections.Section]) -> dict

   Identify chains of connected golden sections to form harmonic ranges.

   :param sections: A list of Section objects representing golden sections to be analyzed.

   :returns:

             A dictionary representing a tree structure where each node is a
                 Section and connected Sections are child nodes.
   :rtype: dict


.. py:function:: unpack_chains(tree: dict) -> list[geometor.model.chains.Chain]

   Unpack the chain tree into a list of individual Chain objects.

   :param tree: A dictionary representing a tree structure where each node is a
                Section and connected Sections are child nodes.

   :returns:

             A list containing Chain objects, each representing a chain
                 of connected golden sections.
   :rtype: list[Chain]


