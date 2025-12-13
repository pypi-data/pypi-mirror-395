geometor.divine.golden
======================

.. py:module:: geometor.divine.golden

.. autoapi-nested-parse::

   Find and analyze golden sections.

   This module provides tools for identifying golden sections in lines and points.

   .. todo:: create a sections module



Submodules
----------

.. toctree::
   :maxdepth: 1

   /modules/api/geometor/divine/golden/chains/index
   /modules/api/geometor/divine/golden/groups/index
   /modules/api/geometor/divine/golden/ranges/index


Attributes
----------

.. autoapisummary::

   geometor.divine.golden.Φ
   geometor.divine.golden.phi


Functions
---------

.. autoapisummary::

   geometor.divine.golden.find_chains_in_sections
   geometor.divine.golden.unpack_chains
   geometor.divine.golden.group_sections_by_size
   geometor.divine.golden.group_sections_by_segments
   geometor.divine.golden.group_sections_by_points
   geometor.divine.golden.analyze_harmonics
   geometor.divine.golden.analyze_harmonics_by_segment
   geometor.divine.golden.check_range
   geometor.divine.golden.find_golden_sections_in_model
   geometor.divine.golden.find_golden_sections_in_points
   geometor.divine.golden.is_section_golden


Package Contents
----------------

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


.. py:function:: group_sections_by_size(sections: list[geometor.model.sections.Section]) -> dict[sympy.Expr, list[geometor.model.sections.Section]]

   Group sections by their minimum length.

   :param sections: List of sections to group.

   :returns: Mapping of length expression to list of sections.
   :rtype: dict


.. py:function:: group_sections_by_segments(sections: list[geometor.model.sections.Section]) -> dict[sympy.geometry.Segment, list[geometor.model.sections.Section]]

   Group sections by the segments they contain.

   :param sections: List of sections to group.

   :returns: Mapping of segment to list of sections.
   :rtype: dict


.. py:function:: group_sections_by_points(sections: list[geometor.model.sections.Section]) -> dict[sympy.geometry.Point, list[geometor.model.sections.Section]]

   Group sections by the points they contain.

   :param sections: List of sections to group.

   :returns: Mapping of point to list of sections.
   :rtype: dict


.. py:function:: analyze_harmonics(line: sympy.geometry.Line) -> list[tuple[sympy.geometry.Point, Ellipsis]]

   Analyze a line for harmonic ranges.

   :param line: The line to analyze.

   :returns: A list of harmonic ranges (tuples of 4 points).
   :rtype: list


.. py:function:: analyze_harmonics_by_segment(sections_by_line: dict) -> dict

   Group harmonic ranges by segment.

   :param sections_by_line: Dictionary of sections by line.

   :returns: Nested dictionary mapping lines to segments to harmonic ranges.
   :rtype: dict


.. py:function:: check_range(r: tuple[sympy.geometry.Point, Ellipsis]) -> sympy.Expr

   Check if a range of 4 points forms a harmonic range.

   :param r: A tuple of 4 points.

   :returns: The cross ratio value (0 if harmonic).
   :rtype: sp.Expr


.. py:data:: Φ

.. py:data:: phi

.. py:function:: find_golden_sections_in_model(model: geometor.model.Model) -> tuple[list[geometor.model.sections.Section], dict[sympy.geometry.Line, list[geometor.model.sections.Section]]]

   Analyze all lines in the model for golden sections.

   :param model: The model to analyze.

   :returns:

             A tuple containing a list of all golden sections and a dictionary
                 mapping lines to their golden sections.
   :rtype: tuple


.. py:function:: find_golden_sections_in_points(pts: list[sympy.geometry.Point]) -> list[geometor.model.sections.Section]

   Find golden sections in combinations of 3 points in list.

   :param pts: A list of points to analyze.

   :returns: A list of golden section objects found.
   :rtype: list[Section]


.. py:function:: is_section_golden(section_points: tuple[sympy.geometry.Point, Ellipsis]) -> bool

   Check if a set of points forms a golden section.

   :param section_points: The points forming the section.

   :returns: True if the section is a golden section.
   :rtype: bool


