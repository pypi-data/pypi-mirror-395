"""Resource Allocation module.

Provides high-level classes for solving portfolio optimization and
general resource allocation problems.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple
import random

from ..core.optimizer import AMNOptimizer, Solution
from ..core.utils import Matrix, shape_of
from ..core.objectives import Objective, SparsityObjective, SumToOneObjective
from ..core.constraints import BoundsConstraint


@dataclass(frozen=True)
class Asset:
    """An asset for portfolio allocation.

    Attributes:
        name: Human-readable name
        expected_return: Expected return rate (e.g., 0.08 for 8%)
        risk: Risk/variance measure
        min_weight: Minimum allocation (default 0)
        max_weight: Maximum allocation (default 1)
    """

    name: str
    expected_return: float
    risk: float
    min_weight: float = 0.0
    max_weight: float = 1.0


@dataclass(frozen=True)
class Resource:
    """A resource for general allocation problems.

    Attributes:
        name: Human-readable name
        value: Value/utility of the resource
        cost: Cost per unit
        min_allocation: Minimum allocation
        max_allocation: Maximum allocation
    """

    name: str
    value: float
    cost: float = 1.0
    min_allocation: float = 0.0
    max_allocation: float = 1.0


class ReturnObjective(Objective):
    """Maximize expected return (minimize negative return).

    Energy: -sum(weights * returns)
    """

    def __init__(self, returns: Sequence[float], weight: float = 1.0) -> None:
        super().__init__(weight=weight)
        self._returns = [float(r) for r in returns]

    def evaluate(self, y: Matrix) -> float:
        # y is 1 x n for portfolio
        row = y[0]
        return -sum(r * w for r, w in zip(self._returns, row))

    def gradient(self, y: Matrix) -> Matrix:
        return [[-r for r in self._returns]]


class RiskObjective(Objective):
    """Minimize portfolio risk (variance).

    For diagonal covariance (independent assets):
    Energy: sum(risk * weight^2)

    For full covariance matrix:
    Energy: w^T @ Cov @ w
    """

    def __init__(
        self,
        risks: Optional[Sequence[float]] = None,
        covariance: Optional[Matrix] = None,
        weight: float = 1.0,
    ) -> None:
        super().__init__(weight=weight)
        if covariance is not None:
            self._cov = covariance
            self._diagonal = False
        elif risks is not None:
            self._risks = [float(r) for r in risks]
            self._diagonal = True
        else:
            raise ValueError("Must provide either risks or covariance")

    def evaluate(self, y: Matrix) -> float:
        row = y[0]
        if self._diagonal:
            return sum(r * (w ** 2) for r, w in zip(self._risks, row))
        else:
            # w^T @ Cov @ w
            n = len(row)
            e = 0.0
            for i in range(n):
                for j in range(n):
                    e += row[i] * self._cov[i][j] * row[j]
            return e

    def gradient(self, y: Matrix) -> Matrix:
        row = y[0]
        if self._diagonal:
            return [[2.0 * r * w for r, w in zip(self._risks, row)]]
        else:
            n = len(row)
            g = [0.0 for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    # d/dw_i of w_i * cov_ij * w_j = cov_ij * w_j + w_i * cov_ji
                    g[i] += (self._cov[i][j] + self._cov[j][i]) * row[j]
            return [g]


class BudgetObjective(Objective):
    """Encourage weights to sum to a target (default 1.0).

    Energy: (sum(weights) - target)^2
    """

    def __init__(self, target: float = 1.0, weight: float = 1.0) -> None:
        super().__init__(weight=weight)
        self.target = float(target)

    def evaluate(self, y: Matrix) -> float:
        s = sum(y[0])
        d = s - self.target
        return d * d

    def gradient(self, y: Matrix) -> Matrix:
        s = sum(y[0])
        val = 2.0 * (s - self.target)
        return [[val for _ in y[0]]]


class DiversificationObjective(Objective):
    """Encourage diversification (avoid concentration).

    Uses Herfindahl-Hirschman Index (HHI): sum(w^2)
    Lower HHI = more diversified.

    Energy: sum(weights^2)
    """

    def evaluate(self, y: Matrix) -> float:
        return sum(w * w for w in y[0])

    def gradient(self, y: Matrix) -> Matrix:
        return [[2.0 * w for w in y[0]]]


class BoundsProjection:
    """Project weights to respect min/max bounds per asset."""

    def __init__(self, bounds: List[Tuple[float, float]]) -> None:
        self._bounds = bounds

    def project(self, y: Matrix) -> Matrix:
        row = y[0]
        new_row = [
            min(max(w, lo), hi) for w, (lo, hi) in zip(row, self._bounds)
        ]
        return [new_row]


class BudgetConstraint:
    """Project weights to sum to target budget."""

    def __init__(self, target: float = 1.0) -> None:
        self.target = target

    def project(self, y: Matrix) -> Matrix:
        row = y[0]
        s = sum(row)
        if s <= 0:
            # Distribute equally
            n = len(row)
            return [[self.target / n for _ in row]]
        scale = self.target / s
        return [[w * scale for w in row]]


class Allocator:
    """High-level solver for portfolio optimization.

    Example:
        assets = [
            Asset("Stocks", expected_return=0.10, risk=0.20),
            Asset("Bonds", expected_return=0.05, risk=0.05),
            Asset("Real Estate", expected_return=0.08, risk=0.15),
        ]
        allocator = Allocator(assets, risk_tolerance=0.5)
        solution = allocator.optimize()
        print(allocator.get_weights(solution))
    """

    def __init__(
        self,
        assets: List[Asset],
        *,
        risk_tolerance: float = 0.5,  # 0 = min risk, 1 = max return
        budget: float = 1.0,
        diversification_weight: float = 0.1,
        budget_weight: float = 5.0,
        covariance: Optional[Matrix] = None,  # Full covariance matrix if available
        dt: float = 0.1,
        damping: float = 0.1,
        seed: Optional[int] = None,
    ) -> None:
        if not assets:
            raise ValueError("assets must be non-empty")

        self.assets = assets
        self.risk_tolerance = float(risk_tolerance)
        self.budget = float(budget)
        self.diversification_weight = float(diversification_weight)
        self.budget_weight = float(budget_weight)
        self.covariance = covariance

        self.dt = float(dt)
        self.damping = float(damping)
        self.seed = seed

    def _returns(self) -> List[float]:
        return [a.expected_return for a in self.assets]

    def _risks(self) -> List[float]:
        return [a.risk for a in self.assets]

    def _bounds(self) -> List[Tuple[float, float]]:
        return [(a.min_weight, a.max_weight) for a in self.assets]

    def _initial(self) -> Matrix:
        n = len(self.assets)
        rng = random.Random(self.seed)
        row = [rng.random() for _ in range(n)]
        s = sum(row)
        if s > 0:
            row = [w / s * self.budget for w in row]
        return [row]

    def optimize(self, max_iterations: int = 500, tolerance: float = 1e-4) -> Solution:
        """Run optimization and return solution."""
        y0 = self._initial()

        # Balance return vs risk based on risk_tolerance
        return_weight = self.risk_tolerance
        risk_weight = 1.0 - self.risk_tolerance

        # Build objectives
        objectives: List[Objective] = [
            ReturnObjective(self._returns(), weight=return_weight),
            BudgetObjective(self.budget, weight=self.budget_weight),
        ]

        if risk_weight > 0:
            if self.covariance is not None:
                objectives.append(RiskObjective(covariance=self.covariance, weight=risk_weight))
            else:
                objectives.append(RiskObjective(risks=self._risks(), weight=risk_weight))

        if self.diversification_weight > 0:
            objectives.append(DiversificationObjective(weight=self.diversification_weight))

        # Build constraints
        constraints = [
            BoundsProjection(self._bounds()),
            BudgetConstraint(self.budget),
        ]

        opt = AMNOptimizer(
            variables=y0,
            constraints=constraints,
            objectives=objectives,
            dt=self.dt,
            damping=self.damping,
            seed=self.seed,
        )
        sol = opt.optimize(max_iterations=max_iterations, tolerance=tolerance)

        # Store final weights in assignments as list of (asset, weight) tuples
        weights = self._extract_weights(opt.y)
        return Solution(
            assignments=weights,
            energy=sol.energy,
            energies=sol.energies,
            converged=sol.converged,
            iterations=sol.iterations,
        )

    def _extract_weights(self, y: Matrix) -> List[Tuple[Asset, float]]:
        """Extract final weights from optimization result."""
        row = y[0]
        return [(asset, weight) for asset, weight in zip(self.assets, row)]

    def get_weights(self, solution: Solution) -> dict:
        """Get weights as a dictionary.

        Args:
            solution: Solution returned by optimize()

        Returns:
            Dict mapping asset name to weight
        """
        return {asset.name: weight for asset, weight in solution.assignments}

    def expected_return(self, solution: Solution) -> float:
        """Calculate expected return of the portfolio."""
        return sum(
            asset.expected_return * weight
            for asset, weight in solution.assignments
        )

    def expected_risk(self, solution: Solution) -> float:
        """Calculate expected risk of the portfolio.

        Uses diagonal approximation if no covariance matrix provided.
        """
        if self.covariance is not None:
            weights = [w for _, w in solution.assignments]
            n = len(weights)
            risk = 0.0
            for i in range(n):
                for j in range(n):
                    risk += weights[i] * self.covariance[i][j] * weights[j]
            return risk ** 0.5
        else:
            return sum(
                (asset.risk * weight) ** 2
                for asset, weight in solution.assignments
            ) ** 0.5


class ResourceAllocator:
    """General resource allocator for budget allocation problems.

    Example:
        resources = [
            Resource("Marketing", value=1.5, cost=1.0),
            Resource("R&D", value=2.0, cost=1.2),
            Resource("Operations", value=1.0, cost=0.8),
        ]
        allocator = ResourceAllocator(resources, budget=100.0)
        solution = allocator.optimize()
    """

    def __init__(
        self,
        resources: List[Resource],
        *,
        budget: float = 1.0,
        value_weight: float = 1.0,
        cost_weight: float = 0.5,
        dt: float = 0.1,
        damping: float = 0.1,
        seed: Optional[int] = None,
    ) -> None:
        if not resources:
            raise ValueError("resources must be non-empty")

        self.resources = resources
        self.budget = float(budget)
        self.value_weight = float(value_weight)
        self.cost_weight = float(cost_weight)
        self.dt = float(dt)
        self.damping = float(damping)
        self.seed = seed

    def _bounds(self) -> List[Tuple[float, float]]:
        return [(r.min_allocation, r.max_allocation) for r in self.resources]

    def _initial(self) -> Matrix:
        n = len(self.resources)
        rng = random.Random(self.seed)
        row = [rng.random() for _ in range(n)]
        s = sum(row)
        if s > 0:
            row = [w / s * self.budget for w in row]
        return [row]

    def optimize(self, max_iterations: int = 500, tolerance: float = 1e-4) -> Solution:
        """Run optimization and return solution."""
        y0 = self._initial()

        # Value objective (maximize value, so minimize negative value)
        values = [[r.value for r in self.resources]]
        costs = [[r.cost for r in self.resources]]

        objectives: List[Objective] = [
            # Maximize value
            _LinearObjective(values, minimize=False, weight=self.value_weight),
            # Minimize cost
            _LinearObjective(costs, minimize=True, weight=self.cost_weight),
            # Budget constraint as soft objective
            BudgetObjective(self.budget, weight=5.0),
        ]

        constraints = [
            BoundsProjection(self._bounds()),
            BudgetConstraint(self.budget),
        ]

        opt = AMNOptimizer(
            variables=y0,
            constraints=constraints,
            objectives=objectives,
            dt=self.dt,
            damping=self.damping,
            seed=self.seed,
        )
        sol = opt.optimize(max_iterations=max_iterations, tolerance=tolerance)

        allocations = [(res, w) for res, w in zip(self.resources, opt.y[0])]
        return Solution(
            assignments=allocations,
            energy=sol.energy,
            energies=sol.energies,
            converged=sol.converged,
            iterations=sol.iterations,
        )

    def get_allocations(self, solution: Solution) -> dict:
        """Get allocations as a dictionary."""
        return {res.name: alloc for res, alloc in solution.assignments}


class _LinearObjective(Objective):
    """Internal linear objective for resource allocation."""

    def __init__(self, coefficients: Matrix, minimize: bool = True, weight: float = 1.0) -> None:
        super().__init__(weight=weight)
        self._coeffs = coefficients
        self._sign = 1.0 if minimize else -1.0

    def evaluate(self, y: Matrix) -> float:
        e = sum(c * w for c, w in zip(self._coeffs[0], y[0]))
        return self._sign * e

    def gradient(self, y: Matrix) -> Matrix:
        return [[self._sign * c for c in self._coeffs[0]]]
