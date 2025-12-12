"""Reusable objective functions for AMN optimization.

All objectives provide:
- evaluate(y): scalar energy value
- gradient(y): matrix of partial derivatives
"""
from __future__ import annotations

import math
from typing import List, Optional, Sequence

from .utils import Matrix, shape_of


class Objective:
    """Base class for differentiable objectives.

    Subclasses must implement evaluate() and gradient().
    """

    def __init__(self, weight: float = 1.0) -> None:
        self.weight: float = float(weight)

    def evaluate(self, y: Matrix) -> float:  # pragma: no cover - abstract
        raise NotImplementedError

    def gradient(self, y: Matrix) -> Matrix:  # pragma: no cover - abstract
        raise NotImplementedError


class CoverageObjective(Objective):
    """Encourage each row to sum to a target value (default 1.0).

    Useful for assignment problems where each task should be assigned exactly once.

    Energy: sum_i (sum_j y[i][j] - target)^2
    Gradient: dE/dy[i][j] = 2 * (sum_j y[i][j] - target)
    """

    def __init__(self, weight: float = 1.0, target: float = 1.0) -> None:
        super().__init__(weight=weight)
        self.target = float(target)

    def evaluate(self, y: Matrix) -> float:
        e = 0.0
        for row in y:
            d = sum(row) - self.target
            e += d * d
        return e

    def gradient(self, y: Matrix) -> Matrix:
        g: Matrix = [[0.0 for _ in row] for row in y]
        for i, row in enumerate(y):
            d = sum(row) - self.target
            val = 2.0 * d
            for j in range(len(row)):
                g[i][j] = val
        return g


class SparsityObjective(Objective):
    """Push values toward 0 or 1 (encourage discrete solutions).

    Energy: sum y*(1-y)
    Gradient: (1 - 2y)

    This objective has minimum at y=0 and y=1, with maximum at y=0.5.
    """

    def evaluate(self, y: Matrix) -> float:
        return sum(val * (1.0 - val) for row in y for val in row)

    def gradient(self, y: Matrix) -> Matrix:
        return [[1.0 - 2.0 * v for v in row] for row in y]


class FairnessObjective(Objective):
    """Balance workload across columns based on row weights.

    Useful for ensuring even distribution of tasks across resources.

    Energy: sum_j (load_j - mean_load)^2
    where load_j = sum_i y[i][j] * weights[i]
    """

    def __init__(self, weights: Sequence[float], weight: float = 1.0) -> None:
        super().__init__(weight=weight)
        self._weights = [float(w) for w in weights]

    def _loads(self, y: Matrix) -> List[float]:
        n, m = shape_of(y)
        loads = [0.0 for _ in range(m)]
        for j in range(m):
            for i in range(n):
                loads[j] += y[i][j] * self._weights[i]
        return loads

    def evaluate(self, y: Matrix) -> float:
        loads = self._loads(y)
        if not loads:
            return 0.0
        mean = sum(loads) / len(loads)
        return sum((load - mean) ** 2 for load in loads)

    def gradient(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        loads = self._loads(y)
        mean = sum(loads) / m if m else 0.0
        g: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            wi = self._weights[i]
            for j in range(m):
                g[i][j] = 2.0 * (loads[j] - mean) * wi
        return g


class SumToOneObjective(Objective):
    """Encourage either rows or columns to sum to 1.

    Args:
        axis: 'row' to normalize rows, 'col' to normalize columns
    """

    def __init__(self, weight: float = 1.0, axis: str = "row") -> None:
        super().__init__(weight=weight)
        if axis not in ("row", "col"):
            raise ValueError("axis must be 'row' or 'col'")
        self.axis = axis

    def evaluate(self, y: Matrix) -> float:
        n, m = shape_of(y)
        if self.axis == "row":
            return sum((sum(row) - 1.0) ** 2 for row in y)
        else:
            e = 0.0
            for j in range(m):
                col_sum = sum(y[i][j] for i in range(n))
                e += (col_sum - 1.0) ** 2
            return e

    def gradient(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        g: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        if self.axis == "row":
            for i, row in enumerate(y):
                d = 2.0 * (sum(row) - 1.0)
                for j in range(m):
                    g[i][j] = d
        else:
            for j in range(m):
                col_sum = sum(y[i][j] for i in range(n))
                d = 2.0 * (col_sum - 1.0)
                for i in range(n):
                    g[i][j] = d
        return g


class EntropyObjective(Objective):
    """Encourage or discourage diversity using entropy.

    Positive weight encourages uniform distribution (high entropy).
    Negative weight encourages concentrated distribution (low entropy).

    Energy: -sum(p * log(p + eps)) where p = y / sum(y) per row
    """

    def __init__(self, weight: float = 1.0, eps: float = 1e-8) -> None:
        super().__init__(weight=weight)
        self.eps = eps

    def evaluate(self, y: Matrix) -> float:
        e = 0.0
        for row in y:
            s = sum(row) + self.eps * len(row)
            for v in row:
                p = (v + self.eps) / s
                e -= p * math.log(p)
        return e

    def gradient(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        g: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for i, row in enumerate(y):
            s = sum(row) + self.eps * m
            for j, v in enumerate(row):
                p = (v + self.eps) / s
                # d/dy_j of -sum(p_k log(p_k)) where p_k = (y_k + eps) / s
                # = -1/s * (log(p) + 1) + sum_k p_k * (log(p_k) + 1) / s
                term1 = -(math.log(p) + 1.0) / s
                term2 = sum(
                    ((row[k] + self.eps) / s) * (math.log((row[k] + self.eps) / s) + 1.0)
                    for k in range(m)
                ) / s
                g[i][j] = term1 + term2
        return g


class QuadraticObjective(Objective):
    """Minimize quadratic form: sum(y^2).

    Useful as a regularization term to keep values small.
    """

    def evaluate(self, y: Matrix) -> float:
        return sum(v * v for row in y for val in row for v in [val])

    def gradient(self, y: Matrix) -> Matrix:
        return [[2.0 * v for v in row] for row in y]


class LinearObjective(Objective):
    """Minimize/maximize a linear combination: sum(coeffs * y).

    Useful for maximizing returns or minimizing costs.

    Args:
        coefficients: Matrix of coefficients (same shape as y)
        minimize: If True, minimize sum(c*y). If False, maximize (minimize -sum).
    """

    def __init__(
        self, coefficients: Matrix, weight: float = 1.0, minimize: bool = True
    ) -> None:
        super().__init__(weight=weight)
        self.coefficients = coefficients
        self.sign = 1.0 if minimize else -1.0

    def evaluate(self, y: Matrix) -> float:
        e = 0.0
        for i, row in enumerate(y):
            for j, v in enumerate(row):
                e += self.coefficients[i][j] * v
        return self.sign * e

    def gradient(self, y: Matrix) -> Matrix:
        return [[self.sign * c for c in row] for row in self.coefficients]


class DistanceObjective(Objective):
    """Minimize total weighted distance based on a distance matrix.

    For routing problems where y[i][j] represents assignment of delivery i to vehicle j.
    Distance is computed as sum of y[i][j] * distance_from_depot[i].

    For more complex routing (TSP-style), use with appropriate constraints.
    """

    def __init__(self, distances: Sequence[float], weight: float = 1.0) -> None:
        """
        Args:
            distances: Distance for each row (e.g., distance from depot to delivery i)
        """
        super().__init__(weight=weight)
        self._distances = [float(d) for d in distances]

    def evaluate(self, y: Matrix) -> float:
        e = 0.0
        for i, row in enumerate(y):
            for v in row:
                e += v * self._distances[i]
        return e

    def gradient(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        g: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            d = self._distances[i]
            for j in range(m):
                g[i][j] = d
        return g


class PairwiseDistanceObjective(Objective):
    """Minimize total route distance using a full distance matrix.

    For VRP-style problems where we want to minimize distances between
    consecutive stops assigned to the same vehicle.

    Energy approximation: For each vehicle j, sum of distances between
    all pairs of deliveries assigned to j, weighted by assignment strengths.
    """

    def __init__(self, distance_matrix: Matrix, weight: float = 1.0) -> None:
        """
        Args:
            distance_matrix: n x n matrix where distance_matrix[i][k] is
                            distance from location i to location k
        """
        super().__init__(weight=weight)
        self._dist = distance_matrix

    def evaluate(self, y: Matrix) -> float:
        n, m = shape_of(y)
        e = 0.0
        # For each vehicle, approximate route cost as sum of pairwise distances
        for j in range(m):
            for i in range(n):
                for k in range(n):
                    if i != k:
                        # Both i and k assigned to vehicle j
                        e += y[i][j] * y[k][j] * self._dist[i][k]
        return e

    def gradient(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        g: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for j in range(m):
            for i in range(n):
                grad_ij = 0.0
                for k in range(n):
                    if i != k:
                        # Derivative: y[k][j] * dist[i][k] + y[k][j] * dist[k][i]
                        grad_ij += y[k][j] * (self._dist[i][k] + self._dist[k][i])
                g[i][j] = grad_ij
        return g
