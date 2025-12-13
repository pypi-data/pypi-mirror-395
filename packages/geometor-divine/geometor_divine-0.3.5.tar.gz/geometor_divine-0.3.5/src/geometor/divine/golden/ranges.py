"""Analysis of harmonic ranges in geometric lines.

This module provides functions to identify and analyze harmonic ranges within
lines and segments of the model.
"""

from __future__ import annotations
from collections import defaultdict

import sympy as sp
import sympy.geometry as spg

from itertools import combinations
from geometor.model.utils import sort_points


def check_range(r: tuple[spg.Point, ...]) -> sp.Expr:
    """Check if a range of 4 points forms a harmonic range.

    Args:
        r: A tuple of 4 points.

    Returns:
        sp.Expr: The cross ratio value (0 if harmonic).
    """
    ad = spg.Segment(r[0], r[3]).length
    cd = spg.Segment(r[2], r[3]).length
    ac = spg.Segment(r[0], r[2]).length
    bc = spg.Segment(r[1], r[2]).length
    return sp.simplify((ad / cd) - (ac / bc))


def analyze_harmonics(line: spg.Line) -> list[tuple[spg.Point, ...]]:
    """Analyze a line for harmonic ranges.

    Args:
        line: The line to analyze.

    Returns:
        list: A list of harmonic ranges (tuples of 4 points).
    """
    line_pts = sort_points(line.pts)
    #  for pt in line_pts:
    #  print(pt.x, pt.x.evalf(), pt.y, pt.y.evalf())
    ranges = list(combinations(line_pts, 4))
    harmonics = []
    for i, r in enumerate(ranges):
        chk = check_range(r)
        #  if chk == 1 or chk == -1:
        #  if chk == 0 or chk == -1:
        if chk == 0:
            #  print(i, chk)
            #  print(f'    {r}')
            harmonics.append(r)
    return harmonics


def analyze_harmonics_by_segment(sections_by_line: dict) -> dict:
    """Group harmonic ranges by segment.

    Args:
        sections_by_line: Dictionary of sections by line.

    Returns:
        dict: Nested dictionary mapping lines to segments to harmonic ranges.
    """
    harmonics_by_segment = {}
    for line, line_sections in sections_by_line.items():
        #  print(line)
        group_by_segments = defaultdict(list)
        for line_section in line_sections:
            group_by_segments[line_section[0]].append(line_section)
            group_by_segments[line_section[1]].append(line_section)
        harmonics_by_segment[line] = group_by_segments

    return harmonics_by_segment
