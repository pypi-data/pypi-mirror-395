geometor.divine.events
======================

.. py:module:: geometor.divine.events

.. autoapi-nested-parse::

   Event listeners for divine analysis.

   This module contains listeners that trigger analysis when elements are added to the model.



Functions
---------

.. autoapisummary::

   geometor.divine.events.point_added_listener


Module Contents
---------------

.. py:function:: point_added_listener(model: geometor.model.Model, pt: sympy.geometry.Point) -> None

   Logs the creation of a point and then analyzes it to find all possible line sections.

   :param model: The model containing the point.
   :param pt: The point that was added.


