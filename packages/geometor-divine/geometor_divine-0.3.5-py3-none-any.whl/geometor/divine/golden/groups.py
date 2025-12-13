from __future__ import annotations
from collections import defaultdict

import sympy as sp
import sympy.geometry as spg
from geometor.model.sections import Section


def group_sections_by_size(sections: list[Section]) -> dict[sp.Expr, list[Section]]:
    """
    Group sections by their minimum length.

    Args:
        sections: List of sections to group.

    Returns:
        dict: Mapping of length expression to list of sections.
    """
    groups = defaultdict(list)
    for section in sections:
        key = section.min_length
        groups[key].append(section)

    sorted_groups = dict(
        sorted(groups.items(), key=lambda item: float(item[0].evalf()))
    )

    return sorted_groups


def group_sections_by_segments(
    sections: list[Section],
) -> dict[spg.Segment, list[Section]]:
    """
    Group sections by the segments they contain.

    Args:
        sections: List of sections to group.

    Returns:
        dict: Mapping of segment to list of sections.
    """
    groups = defaultdict(list)
    for section in sections:
        for segment in section.segments:
            groups[segment].append(section)

    sorted_groups = dict(
        sorted(groups.items(), key=lambda item: float(item[0].length.evalf()))
    )

    return sorted_groups


def group_sections_by_points(sections: list[Section]) -> dict[spg.Point, list[Section]]:
    """
    Group sections by the points they contain.

    Args:
        sections: List of sections to group.

    Returns:
        dict: Mapping of point to list of sections.
    """
    groups = defaultdict(list)
    for section in sections:
        for point in section.points:
            groups[point].append(section)

    sorted_groups = dict(
        sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    )

    return sorted_groups
