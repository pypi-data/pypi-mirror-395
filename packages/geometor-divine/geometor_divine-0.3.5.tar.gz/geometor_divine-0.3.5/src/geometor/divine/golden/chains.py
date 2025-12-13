"""Golden Chain Analyzer: Harmonic Range Identification in Golden Sections.

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
"""

from __future__ import annotations

from geometor.model.sections import Section
from geometor.model.chains import Chain


def find_chains_in_sections(sections: list[Section]) -> dict:
    """Identify chains of connected golden sections to form harmonic ranges.

    Args:
        sections: A list of Section objects representing golden sections to be analyzed.

    Returns:
        dict: A dictionary representing a tree structure where each node is a
            Section and connected Sections are child nodes.
    """

    def add_to_chain_tree(section: Section, tree: dict) -> None:
        next_sections = find_connected_sections(section, sections, in_chain)
        for next_section in next_sections:
            in_chain.add(next_section)
            # TODO: don't add section to the tree until we know there is a chain section
            tree[next_section] = {}
            add_to_chain_tree(next_section, tree[next_section])

    def find_connected_sections(
        current_section: Section, sections: list[Section], in_chain: set
    ) -> list[Section]:
        connected_sections = []
        # The last two points of the current section must be the first two of the next
        current_end_points = current_section.points[1:]
        for section in sections:
            if section not in in_chain:
                next_start_points = section.points[:2]
                if current_end_points == next_start_points:
                    connected_sections.append(section)
        return connected_sections

    chain_tree = {}
    in_chain = set()

    for section in sections:
        if section not in in_chain:
            # TODO: don't add section to the tree until we know there is a chain section
            chain_tree[section] = {}
            in_chain.add(section)
            add_to_chain_tree(section, chain_tree[section])

    chain_tree = {k: v for k, v in chain_tree.items() if v}
    return chain_tree


def unpack_chains(tree: dict) -> list[Chain]:
    """Unpack the chain tree into a list of individual Chain objects.

    Args:
        tree: A dictionary representing a tree structure where each node is a
            Section and connected Sections are child nodes.

    Returns:
        list[Chain]: A list containing Chain objects, each representing a chain
            of connected golden sections.
    """

    def dfs(node: dict, path: list[Section], chains: list[Chain]) -> None:
        if not node:
            chains.append(Chain(path))  # Create a Chain object and add it to the chains
            return

        for child, subtree in node.items():
            dfs(subtree, path + [child], chains)

    chains = []
    for root, subtree in tree.items():
        if not subtree:  # Handle chains with only one section
            chains.append(Chain([root]))
        else:
            dfs(subtree, [root], chains)  # Starting the path with the root section

    return chains
