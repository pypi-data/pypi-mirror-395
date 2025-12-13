geometor.divine.golden.groups
=============================

.. py:module:: geometor.divine.golden.groups


Functions
---------

.. autoapisummary::

   geometor.divine.golden.groups.group_sections_by_size
   geometor.divine.golden.groups.group_sections_by_segments
   geometor.divine.golden.groups.group_sections_by_points


Module Contents
---------------

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


