from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .utils import Matrix, copy_matrix, shape_of, clip_matrix


class Constraint:
    """Base projection constraint.

    Subclasses implement project(y) returning a feasible matrix.
    """

    def project(self, y: Matrix) -> Matrix:  # pragma: no cover - abstract
        raise NotImplementedError


@dataclass
class BoundsConstraint(Constraint):
    low: float = 0.0
    high: float = 1.0

    def project(self, y: Matrix) -> Matrix:
        return clip_matrix(y, self.low, self.high)


@dataclass
class MaskConstraint(Constraint):
    """Zero-out entries where mask[i][j] == 0, then renormalize rows if possible."""

    mask: List[List[int]]  # 1 = allowed, 0 = forbidden

    def project(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        out = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            row_sum = 0.0
            for j in range(m):
                out[i][j] = y[i][j] * (1.0 if self.mask[i][j] else 0.0)
                row_sum += out[i][j]
            if row_sum > 0.0:
                inv = 1.0 / row_sum
                for j in range(m):
                    out[i][j] *= inv
        return out


@dataclass
class CapacityConstraint(Constraint):
    """Enforce per-column capacity: sum_i y[i][j] * durations[i] <= capacities[j].

    Projects by uniform scaling each column if it exceeds capacity.
    """

    durations: Sequence[float]
    capacities: Sequence[float]

    def project(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        out = copy_matrix(y)
        loads = [0.0 for _ in range(m)]
        for j in range(m):
            load_j = 0.0
            for i in range(n):
                load_j += out[i][j] * float(self.durations[i])
            loads[j] = load_j
        for j in range(m):
            cap = float(self.capacities[j])
            if cap <= 0.0:
                # Zero-out entire column if capacity non-positive
                for i in range(n):
                    out[i][j] = 0.0
                continue
            if loads[j] > cap:
                scale = cap / loads[j] if loads[j] > 0 else 0.0
                for i in range(n):
                    out[i][j] *= scale
        return out


class RowOneHotConstraint(Constraint):
    """For each row, keep only the max entry (ties prefer first)."""

    def project(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        out = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            if m == 0:
                continue
            # Find argmax index
            max_j = 0
            max_v = y[i][0]
            for j in range(1, m):
                v = y[i][j]
                if v > max_v:
                    max_v = v
                    max_j = j
            if max_v > 0.0:
                out[i][max_j] = 1.0
        return out


class RowNormalizeConstraint(Constraint):
    """Normalize each row to sum to 1 if sum > 0."""

    def project(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        out = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            s = sum(y[i])
            if s > 0.0:
                inv = 1.0 / s
                for j in range(m):
                    out[i][j] = y[i][j] * inv
            else:
                for j in range(m):
                    out[i][j] = y[i][j]
        return out
