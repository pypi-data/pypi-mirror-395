"""Find and analyze golden sections.

This module provides tools for identifying golden sections in lines and points.

.. todo:: create a sections module
"""

from __future__ import annotations


from itertools import combinations

from geometor.model import Model
from geometor.model.sections import Section
from geometor.model.utils import sort_points

import sympy as sp
import sympy.geometry as spg

from multiprocessing import Pool, cpu_count

from .chains import find_chains_in_sections, unpack_chains
from .groups import (
    group_sections_by_size,
    group_sections_by_segments,
    group_sections_by_points,
)
from .ranges import analyze_harmonics, analyze_harmonics_by_segment, check_range

__all__ = [
    "find_golden_sections_in_model",
    "find_golden_sections_in_points",
    "is_section_golden",
    "find_chains_in_sections",
    "unpack_chains",
    "group_sections_by_size",
    "group_sections_by_segments",
    "group_sections_by_points",
    "analyze_harmonics",
    "analyze_harmonics_by_segment",
    "check_range",
    "Φ",
    "phi",
]

Φ = sp.GoldenRatio
phi = sp.Rational(1, 2) + (sp.sqrt(5) / 2)


def find_golden_sections_in_model(
    model: Model,
) -> tuple[list[Section], dict[spg.Line, list[Section]]]:
    """Analyze all lines in the model for golden sections.

    Args:
        model: The model to analyze.

    Returns:
        tuple: A tuple containing a list of all golden sections and a dictionary
            mapping lines to their golden sections.
    """
    sections = []
    sections_by_line = {}

    # TODO: start the Pool here
    for i, line in enumerate(model.lines):
        # get points on the line
        line_pts = model[line].parents
        line_sections = find_golden_sections_in_points(line_pts)
        sections.extend(line_sections)
        sections_by_line[line] = line_sections

    return sections, sections_by_line


def find_golden_sections_in_points(pts: list[spg.Point]) -> list[Section]:
    """Find golden sections in combinations of 3 points in list.

    Args:
        pts: A list of points to analyze.

    Returns:
        list[Section]: A list of golden section objects found.
    """
    goldens = []
    pts = sort_points(pts)

    # this will walk the combinations of three points down the line
    sections = list(combinations(pts, 3))
    print(f"sections in line: {len(sections)}")

    with Pool(cpu_count()) as pool:
        results = pool.map(is_section_golden, sections)
        goldens = [Section(section) for i, section in enumerate(sections) if results[i]]

    print(f"goldens in line: {len(goldens)}")

    return goldens


def is_section_golden(section_points: tuple[spg.Point, ...]) -> bool:
    """Check if a set of points forms a golden section.

    Args:
        section_points: The points forming the section.

    Returns:
        bool: True if the section is a golden section.
    """
    section = Section(section_points)
    return section.is_golden
