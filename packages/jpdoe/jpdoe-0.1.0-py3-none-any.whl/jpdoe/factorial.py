"""
Core design-of-experiments routines for jpdoe.

Public functions
----------------
full_factorial(k, factor_names=None, include_interactions=True, blocks=None)
    Full 2^k factorial design with treatment labels and all interactions.
    Optionally assign blocks via block generator words.

fractional_factorial(factor_names, defining_relations,
                     include_interactions=True,
                     alias_labels=True,
                     unique_alias_labels=True,
                     blocks=None,
                     alias_cutoff=None)
    Regular 2^(k-p) fractional factorial constructed from defining
    relations such as ``I = ABC`` or ``I = ABC = ABD``.  Can optionally
    relabel columns by alias classes, drop duplicate alias columns,
    assign blocks via block generator words, and shorten alias labels
    by dropping high-order terms from the printed labels.

design_resolution(factor_names, defining_relations)
    Compute the resolution (II, III, IV, ...) of a regular fraction.

alias_structure(factor_names, defining_relations,
                as_dict=False, alphabetical=True)
    Compute alias classes for all effects and return either:
    - a formatted multiline string (default), or
    - a dict (if as_dict=True).
"""

from itertools import combinations
from typing import List, Dict, Optional

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Internal helpers: basic design building
# ---------------------------------------------------------------------------

def _treatment_labels(k: int) -> List[str]:
    """
    Generate standard 2^k treatment labels:

    (1), a, b, ab, c, ac, bc, abc, ...

    Assumes factors are A, B, C, ...
    """
    n = 2**k
    labels: List[str] = []
    for i in range(n):
        bits = f"{i:0{k}b}"[::-1]  # LSB = factor A
        name = "".join(chr(97 + j) for j, b in enumerate(bits) if b == "1")
        labels.append(name or "(1)")
    return labels


def _full_main_effects(k: int, factor_names: List[str]) -> pd.DataFrame:
    """
    Build full 2^k design with only main-effect columns and Treatment labels.
    """
    n = 2**k
    X = np.empty((n, k), dtype=int)
    labels = _treatment_labels(k)

    for i in range(n):
        bits = f"{i:0{k}b}"[::-1]
        for j, b in enumerate(bits):
            X[i, j] = 1 if b == "1" else -1

    df = pd.DataFrame(X, columns=factor_names)
    df.insert(0, "Treatment", labels)
    return df


def _add_interactions(df: pd.DataFrame, factor_names: List[str]) -> None:
    """
    Add all interaction columns (AB, AC, ..., ABC...) in-place.
    """
    for r in range(2, len(factor_names) + 1):
        for combo in combinations(factor_names, r):
            colname = "".join(combo)
            df[colname] = df[list(combo)].prod(axis=1)


# ---------------------------------------------------------------------------
# Internal helpers: defining relations, alias group, blocks
# ---------------------------------------------------------------------------

def _parse_defining_words(defining_relations):
    """
    Parse strings like 'I = ABC = ABD' into ['ABC', 'ABD'].
    """
    if isinstance(defining_relations, str):
        s = defining_relations.replace(" ", "")
        if s.startswith("I="):
            s = s[2:]
        words = [w for w in s.split("=") if w]
    else:
        # assume iterable of strings
        words = [w.replace(" ", "") for w in defining_relations]
    return words


def _parse_block_words(blocks):
    """
    Parse blocks argument into a list of block generator words.

    Examples
    --------
    blocks=None           -> []
    blocks="ABC"          -> ["ABC"]
    blocks="ABC,CDF"      -> ["ABC", "CDF"]
    blocks=["ABC","CDF"]  -> ["ABC", "CDF"]
    """
    if blocks is None:
        return []
    if isinstance(blocks, str):
        s = blocks.replace(" ", "")
        words = [w for w in s.split(",") if w]
    else:
        words = [w.replace(" ", "") for w in blocks]
    return words


def _word_to_int(word: str, factor_index: Dict[str, int]) -> int:
    """
    Encode an effect word (e.g. 'ACD') as an integer bitmask.
    """
    val = 0
    for ch in word:
        val |= 1 << factor_index[ch]
    return val


def _int_to_word(val: int, factor_names: List[str]) -> str:
    """
    Decode an integer bitmask back into an effect word (e.g. 0b101 -> 'AC').
    Identity (0) is returned as ''.
    """
    word = "".join(
        factor_names[j] for j in range(len(factor_names))
        if (val >> j) & 1
    )
    return word  # '' means identity


def _bit_weight(val: int) -> int:
    """Number of factors in an effect (Hamming weight)."""
    return val.bit_count()


def _defining_group_ints(words, factor_index: Dict[str, int]) -> List[int]:
    """
    Build all group elements (as ints) generated by defining words.

    The order of the group elements follows the natural mask order over
    the defining words, so that for generators g1, g2, ..., gp we get:

        0, g1, g2, g1^g2, g3, g1^g3, ...

    This ordering is then used to define the order of aliases within
    each alias class (so rows follow the "multiply by each I term"
    pattern implied by the user-specified defining relations).
    """
    gens = [_word_to_int(w, factor_index) for w in words]
    p = len(gens)
    group: List[int] = []
    seen = set()
    for mask in range(1 << p):
        v = 0
        for i in range(p):
            if mask & (1 << i):
                v ^= gens[i]
        if v not in seen:
            seen.add(v)
            group.append(v)
    return group


def _run_index(df: pd.DataFrame, factor_names: List[str]) -> np.ndarray:
    """
    Compute a Yates-order run index for each row based on the main effects.

    -1 is treated as 0, +1 as 1, with factor_names[0] as LSB.
    Sorting by this index reproduces the canonical order:
    (1), a, b, ab, c, ac, bc, abc, ...
    """
    arr = df[factor_names].to_numpy()
    idx = []
    for row in arr:
        code = 0
        for j, val in enumerate(row):
            bit = 0 if val == -1 else 1
            code |= bit << j
        idx.append(code)
    return np.array(idx, dtype=int)


def _add_blocks(df: pd.DataFrame, factor_names: List[str], blocks) -> None:
    """
    Add a 'Block' column based on block generator words.

    Parameters
    ----------
    df : DataFrame
        Design with Treatment and main-effect columns already present.
    factor_names : list of str
        Main effect factor names, e.g. ['A','B','C','D'].
    blocks : None, str, or sequence of str
        Block generator words, e.g. "ABC" or ["ABC","CDF"].

    Notes
    -----
    For p block generators, there are up to 2^p blocks.  For each row:

    - Compute each block generator as the product of its factor columns.
    - Map the vector of ±1 signs to a code with -1 -> 0, +1 -> 1.
    - Compress that bit pattern into an integer and relabel sorted
      unique codes as Block = 1, 2, 3, ...

    This adds a single integer 'Block' column to df.
    """
    block_words = _parse_block_words(blocks)
    if not block_words:
        return

    valid_letters = set("".join(factor_names))
    for w in block_words:
        if not set(w) <= valid_letters:
            raise ValueError(
                "Block word '{}' contains letters not in factor_names.".format(w)
            )

    # Build block generator level matrix (±1)
    block_levels = []
    for w in block_words:
        cols = list(w)
        block_levels.append(df[cols].prod(axis=1).to_numpy())
    block_levels = np.vstack(block_levels).T  # shape (n_runs, n_blocks)

    # Encode ±1 patterns into integer codes
    block_codes: List[int] = []
    for row in block_levels:
        code = 0
        for j, val in enumerate(row):
            bit = 0 if val == -1 else 1
            code |= bit << j
        block_codes.append(code)

    unique_codes = sorted(set(block_codes))
    code_to_block = {code: i + 1 for i, code in enumerate(unique_codes)}
    block_num = [code_to_block[c] for c in block_codes]

    df["Block"] = block_num


# ---------------------------------------------------------------------------
# Public: full factorial
# ---------------------------------------------------------------------------

def full_factorial(
    k: int,
    factor_names: Optional[List[str]] = None,
    include_interactions: bool = True,
    blocks=None,
) -> pd.DataFrame:
    """
    Build a full 2^k factorial design with treatment labels.

    Parameters
    ----------
    k : int
        Number of factors.
    factor_names : list of str, optional
        Names of the factors, e.g. ['A', 'B', 'C'].  If None, uses
        ['A', 'B', ...] automatically.
    include_interactions : bool, default True
        If True, add all interaction columns (AB, AC, ..., ABC...).
    blocks : None, str, or sequence of str, optional
        Block generator words, e.g. "ABC" or ["ABC","CDF"].  If
        provided, a 'Block' column with integer block numbers is
        appended to the design.

    Returns
    -------
    df : pandas.DataFrame
        Design matrix with a 'Treatment' column, main-effect columns,
        optionally all interaction columns, and optionally a 'Block'
        column.
    """
    if factor_names is None:
        factor_names = [chr(65 + i) for i in range(k)]  # A, B, C, ...

    if len(factor_names) != k:
        raise ValueError("len(factor_names) must equal k")

    df = _full_main_effects(k, factor_names)

    if include_interactions:
        _add_interactions(df, factor_names)

    # Add blocking if requested
    _add_blocks(df, factor_names, blocks)

    return df


# ---------------------------------------------------------------------------
# Public: alias structure and resolution
# ---------------------------------------------------------------------------

def alias_structure(
    factor_names,
    defining_relations,
    as_dict: bool = False,
    alphabetical: bool = True,
):
    """
    Compute alias classes for all non-identity effects.

    Parameters
    ----------
    factor_names : sequence of str
        Names of the factors in order, e.g. ['A', 'B', 'C', 'D'].
    defining_relations : str or sequence of str
        Defining relations, e.g. "I = ABC = ABD" or ["ABC", "ABD"].
    as_dict : bool, default False
        If False (default), return a formatted multiline string where
        each line looks like:
            [A] = [BC] = [BD] = [CD]
        If True, return a dict mapping representative effects to lists
        of all effects in the alias class.
    alphabetical : bool, default True
        If True, order the representatives roughly alphabetically /
        by increasing order (main effects, then 2-factor, etc.).

    Returns
    -------
    aliases : str or dict
        - If as_dict=False: a formatted multiline string.
        - If as_dict=True: dict mapping rep -> list of effects.
    """
    factor_names = list(factor_names)
    k = len(factor_names)
    factor_index: Dict[str, int] = {name: i for i, name in enumerate(factor_names)}

    words = _parse_defining_words(defining_relations)
    if not words:
        raise ValueError("No defining relations supplied.")

    # Build defining group elements (in generator-based order)
    group = _defining_group_ints(words, factor_index)

    # All possible non-identity effects
    all_effects = list(range(1, 1 << k))

    seen = set()
    classes: Dict[str, List[str]] = {}

    for e in all_effects:
        if e in seen:
            continue

        # Alias class for effect e, in group order
        eqs = [e ^ g for g in group]
        seen.update(eqs)

        # Choose canonical representative: smallest (order, name)
        rep = min(
            eqs,
            key=lambda x: (_bit_weight(x), _int_to_word(x, factor_names))
        )
        rep_word = _int_to_word(rep, factor_names) or "I"

        # Translate to words in this natural group order, deduped
        class_words: List[str] = []
        for x in eqs:
            w = _int_to_word(x, factor_names) or "I"
            if w not in class_words:
                class_words.append(w)

        classes[rep_word] = class_words

    if as_dict:
        if alphabetical:
            ordered: Dict[str, List[str]] = {}
            for rep in sorted(
                classes.keys(),
                key=lambda k_: (0 if k_ == "I" else len(k_), k_)
            ):
                ordered[rep] = classes[rep]
            return ordered
        return classes

    reps = list(classes.keys())
    if alphabetical:
        reps = sorted(
            reps,
            key=lambda k_: (0 if k_ == "I" else len(k_), k_)
        )

    lines = []
    for rep in reps:
        cls = classes[rep]
        rest = [w for w in cls if w != rep]
        items = [f"[{rep}]"] + [f"[{w}]" for w in rest]
        line = " = ".join(items)
        lines.append(line)
    return "\n".join(lines)


def design_resolution(
    factor_names,
    defining_relations,
) -> int:
    """
    Compute the design resolution (II, III, IV, ...) for a regular fraction.

    Resolution is defined as the smallest word length (number of letters)
    among the non-identity elements of the defining relation group.
    """
    factor_names = list(factor_names)
    factor_index: Dict[str, int] = {name: i for i, name in enumerate(factor_names)}

    words = _parse_defining_words(defining_relations)
    if not words:
        raise ValueError("No defining relations supplied.")

    group = _defining_group_ints(words, factor_index)

    # Skip identity (0); resolution is min positive weight
    weights = [_bit_weight(g) for g in group if g != 0]
    if not weights:
        raise ValueError("Defining group has no non-identity elements.")
    return min(weights)


# ---------------------------------------------------------------------------
# Public: fractional factorial with optional alias-based labels and blocks
# ---------------------------------------------------------------------------

def fractional_factorial(
    factor_names,
    defining_relations,
    include_interactions: bool = True,
    alias_labels: bool = True,
    unique_alias_labels: bool = True,
    blocks=None,
    alias_cutoff=None,
) -> pd.DataFrame:
    """
    Build a regular 2^(k-p) fractional factorial design using defining relations.

    Parameters
    ----------
    factor_names : sequence of str
        Names of the factors in order, e.g. ['A', 'B', 'C', 'D'].
    defining_relations : str or sequence of str
        Defining relations, e.g. "I = ABC = ABD" or ["ABC", "ABD"].
    include_interactions : bool, default True
        If True, add all interaction columns AB, AC, ..., ABC...
    alias_labels : bool, default True
        If True, relabel each effect column with its entire alias class,
        e.g. 'A + BC + BD + CD' instead of just 'A'.  Also attaches:

        * df.alias_structure : dict of alias classes
        * df.resolution      : int, resolution of the design

    unique_alias_labels : bool, default True
        Only used when alias_labels is True.  If True, after relabeling
        columns by alias class, keep only the **first** occurrence of
        each alias label (per alias class) and drop the redundant
        duplicate columns.  This leaves at most one column per alias
        class.

    blocks : None, str, or sequence of str, optional
        Block generator words, e.g. "ABC" or ["ABC","CDF"].  If
        provided, a 'Block' column with integer block numbers is
        appended to the design.

    alias_cutoff : None, bool, or int, optional
        Controls how many alias terms are printed in the column labels.

        - None (default): include **all** non-identity alias terms in
          the label, e.g. 'A + BC + BD + CD'.
        - True: same as alias_cutoff=3 (common practice: ignore 3+
          factor terms in labels when lower-order terms exist).
        - int n: drop alias terms whose word length is >= n from the
          printed label, *unless* the alias class contains no terms
          shorter than n, in which case all terms are kept.

        This only affects the *text* of the column labels.  The alias
        structure and math are unchanged.

    Returns
    -------
    df : pandas.DataFrame
        Fractional factorial design with a 'Treatment' column, all
        main effects, (optionally) all interaction columns, and
        (optionally) a 'Block' column.  If alias_labels is True, the
        effect column names will reflect alias classes and df.resolution
        will be set.
    """
    factor_names = list(factor_names)
    k = len(factor_names)

    # Parse and validate defining words
    words = _parse_defining_words(defining_relations)
    if not words:
        raise ValueError("No defining relations supplied.")

    valid_letters = set("".join(factor_names))
    for w in words:
        if not set(w) <= valid_letters:
            raise ValueError(
                "Defining word '{}' contains letters not in factor_names.".format(w)
            )

    # Start from full 2^k design (main effects only)
    df = _full_main_effects(k, factor_names)

    # Apply defining relations: keep rows where each defining word = +1
    for w in words:
        cols = list(w)
        prod = df[cols].prod(axis=1)
        df = df.loc[prod == 1]

    # Restore canonical run order (just "cut out" invalid rows)
    run_idx = _run_index(df, factor_names)
    df = df.iloc[np.argsort(run_idx)].reset_index(drop=True)

    # Add interactions if requested
    if include_interactions:
        _add_interactions(df, factor_names)

    # Add blocks (based on main-effect columns) before alias relabel
    _add_blocks(df, factor_names, blocks)

    # If alias_labels requested, compute alias structure and resolution
    if alias_labels:
        aliases = alias_structure(
            factor_names, defining_relations, as_dict=True, alphabetical=True
        )
        R = design_resolution(factor_names, defining_relations)

        # Interpret alias_cutoff parameter
        cutoff = None
        if alias_cutoff is True:
            cutoff = 3
        elif isinstance(alias_cutoff, int) and alias_cutoff > 0:
            cutoff = alias_cutoff

        # Build mapping: effect word -> label string
        word_to_label: Dict[str, str] = {}
        for rep, class_words in aliases.items():
            # All non-identity words in this alias class
            non_id = [w for w in class_words if w != "I"]
            if not non_id:
                continue

            if cutoff is None:
                visible = non_id
            else:
                # keep only words with length < cutoff
                visible = [w for w in non_id if len(w) < cutoff]
                # if nothing short enough, fall back to including all
                if not visible:
                    visible = non_id

            visible_sorted = sorted(
                visible, key=lambda s: (len(s), s)
            )
            label = " + ".join(visible_sorted)

            # Map *all* non-identity words in this alias class to this label
            for w in non_id:
                word_to_label[w] = label

        # Relabel columns (except Treatment and Block) using alias labels
        new_cols = []
        for c in df.columns:
            if c in ("Treatment", "Block"):
                new_cols.append(c)
            else:
                new_cols.append(word_to_label.get(c, c))
        df.columns = new_cols

        # Optionally drop duplicate alias columns, keeping the first
        if unique_alias_labels:
            seen = set()
            keep_indices = []
            for idx, c in enumerate(df.columns):
                if c in ("Treatment", "Block"):
                    keep_indices.append(idx)
                    continue
                if c not in seen:
                    seen.add(c)
                    keep_indices.append(idx)
            df = df.iloc[:, keep_indices]

        # Attach metadata for interactive use
        df.alias_structure = aliases   # type: ignore[attr-defined]
        df.resolution = R              # type: ignore[attr-defined]

    return df


# Backwards-compat alias (old name)
fractional_defining = fractional_factorial
