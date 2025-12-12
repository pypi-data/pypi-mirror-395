"""Shared utilities for AMN core modules."""
from __future__ import annotations

from typing import List, Sequence, Tuple

Matrix = List[List[float]]


def zeros_like(y: Matrix) -> Matrix:
    """Create a zero matrix with the same shape as y."""
    return [[0.0 for _ in row] for row in y]


def shape_of(y: Matrix) -> Tuple[int, int]:
    """Return (rows, cols) of a matrix."""
    return (len(y), len(y[0]) if y else 0)


def clip_matrix(y: Matrix, low: float, high: float) -> Matrix:
    """Clip all values in y to [low, high]."""
    return [[min(max(val, low), high) for val in row] for row in y]


def copy_matrix(y: Matrix) -> Matrix:
    """Return a deep copy of a matrix."""
    return [row[:] for row in y]


def add_inplace(a: Matrix, b: Matrix) -> None:
    """Add matrix b to matrix a in place."""
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] += b[i][j]


def scale_inplace(a: Matrix, s: float) -> None:
    """Multiply matrix a by scalar s in place."""
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] *= s


def argmax_index(row: Sequence[float]) -> int:
    """Return the index of the maximum value in a row."""
    if not row:
        return -1
    m = row[0]
    idx = 0
    for i, v in enumerate(row):
        if v > m:
            m = v
            idx = i
    return idx


def sum_matrix(y: Matrix) -> float:
    """Sum all elements in a matrix."""
    return sum(val for row in y for val in row)


def matrix_max(y: Matrix) -> float:
    """Return the maximum value in a matrix."""
    return max(val for row in y for val in row)


def matrix_min(y: Matrix) -> float:
    """Return the minimum value in a matrix."""
    return min(val for row in y for val in row)


def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Compute Euclidean distance between two 2D points."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return (dx * dx + dy * dy) ** 0.5
