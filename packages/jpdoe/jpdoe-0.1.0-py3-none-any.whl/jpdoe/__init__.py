"""
jpdoe: simple helpers for 2^k factorial and fractional-factorial designs.

This package provides small, focused utilities for building 2-level
design matrices (full and fractional), inspecting alias structure,
computing design resolution, and optionally assigning blocks.

Available functions
-------------------
full_factorial(k, factor_names=None,
               include_interactions=True, blocks=None)
    Build a full 2^k factorial design with treatment labels and,
    optionally, all interaction columns and a 'Block' column.

fractional_factorial(factor_names, defining_relations,
                     include_interactions=True,
                     alias_labels=True,
                     unique_alias_labels=True,
                     blocks=None)
    Build a regular 2^(k-p) fractional factorial design from defining
    relations such as ``I = ABC`` or ``I = ABC = ABD``.  Can optionally
    relabel effect columns by alias classes, drop duplicate alias
    columns, and assign blocks via block generator words.

fractional_defining(...)
    Backwards-compatible alias for fractional_factorial.

design_resolution(factor_names, defining_relations)
    Compute the resolution (II, III, IV, ...) of a regular fraction
    from its defining relations.

alias_structure(factor_names, defining_relations,
                as_dict=False, alphabetical=True)
    Compute alias classes for all effects.  By default returns a
    formatted multiline string.  If as_dict=True, returns a dict.

Examples
--------------
Full 2^3 factorial with all interactions:
    >>> from jpdoe import full_factorial
    >>> df_full = full_factorial(3)
    >>> df_full
    >>> df_full.to_excel("full_2k3.xlsx", index=False)

Full 2^4 factorial with blocking by ABC:
    >>> df_full_blk = full_factorial(4, blocks="ABC")
    >>> df_full_blk[["Treatment", "A", "B", "C", "Block"]]
    >>> df_full_blk.to_excel("full_2k4_block_ABC.xlsx", index=False)

1/2 fraction of 2^3 with I = ABC, alias labels and unique columns:
    >>> from jpdoe import fractional_factorial
    >>> df_half = fractional_factorial(
    ...     ['A', 'B', 'C'],
    ...     "I = ABC",
    ... )
    >>> df_half
    >>> df_half.to_excel("half_2k3_ABC.xlsx", index=False)
    >>> df_half.resolution
    3

1/4 fraction of 2^4 with I = ABC = ABD, with blocking:
    >>> df_quarter_blk = fractional_factorial(
    ...     ['A', 'B', 'C', 'D'],
    ...     "I = ABC = ABD",
    ...     blocks="AB",
    ... )
    >>> df_quarter_blk
    >>> df_quarter_blk.to_excel("quarter_2k4_ABC_ABD_block_AB.xlsx",
    ...                         index=False)
    >>> df_quarter_blk.resolution
    2

Inspecting alias structure:
    >>> from jpdoe import alias_structure, design_resolution
    >>> print(alias_structure(['A','B','C','D'], "I = ABC = ABD"))
    [A] = [BC] = [BD] = [CD]
    [B] = [AC] = [AD] = [BCD]
    ...
    >>> aliases_dict = alias_structure(
    ...     ['A','B','C','D'],
    ...     "I = ABC = ABD",
    ...     as_dict=True
    ... )
    >>> aliases_dict['A']
    ['A', 'BC', 'BD', 'CD']
    >>> design_resolution(['A','B','C','D'], "I = ABC = ABD")
    2
"""

from .factorial import (
    full_factorial,
    fractional_factorial,
    fractional_defining,
    design_resolution,
    alias_structure,
)

__all__ = [
    "full_factorial",
    "fractional_factorial",
    "fractional_defining",
    "design_resolution",
    "alias_structure",
]
