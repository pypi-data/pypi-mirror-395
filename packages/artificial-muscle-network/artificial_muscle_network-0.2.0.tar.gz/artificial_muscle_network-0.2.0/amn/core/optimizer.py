from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional, Protocol, Tuple

import random

from .utils import (
    Matrix,
    zeros_like,
    shape_of,
    clip_matrix,
    copy_matrix,
    argmax_index,
)
from .objectives import Objective


class ConstraintProtocol(Protocol):
    def project(self, y: Matrix) -> Matrix:  # pragma: no cover - interface only
        ...


@dataclass
class Solution:
    """Results container returned by Optimizer.optimize()."""

    assignments: List[Any]
    energy: float
    energies: List[float]
    converged: bool
    iterations: int


class AMNOptimizer:
    """Physics-inspired optimizer with momentum and constraint projections.

    This optimizer operates on a continuous assignment matrix y in [0,1].
    Objectives provide an energy scalar and gradient; constraints project y into
    the feasible set after each step.
    """

    def __init__(
        self,
        variables: Matrix,
        constraints: List[ConstraintProtocol],
        objectives: List[Objective],
        dt: float = 0.1,
        damping: float = 0.1,
        clip_bounds: Tuple[float, float] = (0.0, 1.0),
        seed: Optional[int] = None,
    ) -> None:
        if seed is not None:
            random.seed(seed)
        if not variables or not variables[0]:
            raise ValueError("variables must be a non-empty 2D matrix (list of lists)")
        self.y: Matrix = copy_matrix(variables)
        self.v: Matrix = zeros_like(self.y)
        self.objectives = objectives
        self.constraints = constraints
        self.dt = float(dt)
        self.damping = float(damping)
        self.clip_bounds = clip_bounds

    def compute_energy(self) -> float:
        energy = 0.0
        for obj in self.objectives:
            energy += obj.weight * obj.evaluate(self.y)
        return float(energy)

    def compute_forces(self) -> Matrix:
        n, m = shape_of(self.y)
        forces: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for obj in self.objectives:
            grad = obj.gradient(self.y)
            # forces = -grad (negative gradient), aggregated with weights
            for i in range(n):
                row_f = forces[i]
                row_g = grad[i]
                for j in range(m):
                    row_f[j] -= obj.weight * row_g[j]
        # damping term proportional to velocity
        for i in range(n):
            for j in range(m):
                forces[i][j] -= self.damping * self.v[i][j]
        return forces

    def step(self) -> float:
        # Compute forces
        f = self.compute_forces()
        # Update velocities and positions
        n, m = shape_of(self.y)
        for i in range(n):
            for j in range(m):
                self.v[i][j] += f[i][j] * self.dt
                self.y[i][j] += self.v[i][j] * self.dt
        # Project to constraints
        for c in self.constraints:
            self.y = c.project(self.y)
        # Keep within clip bounds (safety)
        self.y = clip_matrix(self.y, self.clip_bounds[0], self.clip_bounds[1])
        return self.compute_energy()

    def optimize(self, max_iterations: int = 500, tolerance: float = 1e-4) -> Solution:
        energies: List[float] = []
        last_check = 10
        for i in range(max_iterations):
            e = self.step()
            energies.append(e)
            if i >= last_check:
                if abs(energies[-1] - energies[-last_check]) < tolerance:
                    break
        assignments = self.decode()
        return Solution(
            assignments=assignments,
            energy=energies[-1] if energies else float("inf"),
            energies=energies,
            converged=(i < max_iterations - 1),
            iterations=i + 1,
        )

    def decode(self) -> List[Tuple[int, int]]:
        """Default decoding: pick argmax in each row.

        Returns list of (row_index, col_index) pairs for rows with any positive value.
        """
        out: List[Tuple[int, int]] = []
        for i, row in enumerate(self.y):
            j = argmax_index(row)
            if j >= 0 and row[j] > 0.0:
                out.append((i, j))
        return out
