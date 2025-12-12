from __future__ import annotations

from typing import List, Tuple

from .utils import Matrix


def argmax_decode(y: Matrix) -> List[Tuple[int, int]]:
    """Decode by selecting the maximum column per row.

    Returns (row_index, col_index) pairs for rows with any positive value.
    """
    out: List[Tuple[int, int]] = []
    for i, row in enumerate(y):
        if not row:
            continue
        j = 0
        mv = row[0]
        for k, v in enumerate(row):
            if v > mv:
                j = k
                mv = v
        if mv > 0.0:
            out.append((i, j))
    return out
