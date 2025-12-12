from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
import random

from ..core.optimizer import AMNOptimizer, Solution
from ..core.utils import Matrix
from ..core.objectives import Objective, CoverageObjective, SparsityObjective, FairnessObjective
from ..core.constraints import BoundsConstraint, MaskConstraint, CapacityConstraint, RowOneHotConstraint


@dataclass(frozen=True)
class Resource:
    """Represents a worker/machine/vehicle, with capacity and skills."""

    name: str
    capacity: float
    skills: Set[str]


@dataclass(frozen=True)
class Task:
    """Represents a job/shift/delivery with duration and required skills."""

    name: str
    duration: float
    required_skills: Set[str]


@dataclass(frozen=True)
class ConstraintSpec:
    """Scheduling constraint specification.

    Acts as a factory for constraint types; interpreted by Scheduler.
    """

    kind: str
    params: Dict[str, float]

    @staticmethod
    def no_overlap() -> "ConstraintSpec":
        return ConstraintSpec(kind="no_overlap", params={})

    @staticmethod
    def skill_match() -> "ConstraintSpec":
        return ConstraintSpec(kind="skill_match", params={})

    @staticmethod
    def capacity(max_hours: float) -> "ConstraintSpec":
        return ConstraintSpec(kind="capacity", params={"max_hours": float(max_hours)})


# Backward compatibility alias
Constraint = ConstraintSpec


class Scheduler:
    """High-level convenience wrapper for scheduling problems.

    Example:
        resources = [Resource("A", 40, {"welding"}), Resource("B", 35, {"painting"})]
        tasks = [Task("Job1", 4, {"welding"}), Task("Job2", 3, {"painting"})]
        constraints = [ConstraintSpec.no_overlap(), ConstraintSpec.skill_match(), ConstraintSpec.capacity(40)]
        scheduler = Scheduler(resources, tasks, constraints)
        solution = scheduler.optimize(max_iterations=300)
    """

    def __init__(
        self,
        resources: List[Resource],
        tasks: List[Task],
        constraints: List[ConstraintSpec],
        *,
        coverage_weight: float = 2.0,
        fairness_weight: float = 1.0,
        sparsity_weight: float = 0.5,
        dt: float = 0.1,
        damping: float = 0.1,
        seed: Optional[int] = None,
    ) -> None:
        if not resources:
            raise ValueError("resources must be non-empty")
        if not tasks:
            raise ValueError("tasks must be non-empty")
        self.resources = resources
        self.tasks = tasks
        self.constraint_specs = constraints
        self.coverage_weight = float(coverage_weight)
        self.fairness_weight = float(fairness_weight)
        self.sparsity_weight = float(sparsity_weight)
        self.dt = float(dt)
        self.damping = float(damping)
        self.seed = seed

    def _mask(self) -> List[List[int]]:
        n = len(self.tasks)
        m = len(self.resources)
        mask = [[0 for _ in range(m)] for _ in range(n)]
        for i, t in enumerate(self.tasks):
            for j, r in enumerate(self.resources):
                ok = t.required_skills.issubset(r.skills)
                mask[i][j] = 1 if ok else 0
        return mask

    def _durations(self) -> List[float]:
        return [float(t.duration) for t in self.tasks]

    def _capacities(self) -> List[float]:
        # If capacity constraint is provided with max_hours, cap each resource by min(resource.capacity, max_hours)
        max_hours_param = None
        for spec in self.constraint_specs:
            if spec.kind == "capacity" and "max_hours" in spec.params:
                max_hours_param = float(spec.params["max_hours"])
        caps: List[float] = []
        for r in self.resources:
            cap = float(r.capacity)
            if max_hours_param is not None:
                cap = min(cap, max_hours_param)
            caps.append(cap)
        return caps

    def _initial(self, mask: List[List[int]]) -> Matrix:
        n = len(self.tasks)
        m = len(self.resources)
        rng = random.Random(self.seed)
        y: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            # initialize only allowed entries
            for j in range(m):
                if mask[i][j]:
                    y[i][j] = rng.random()
            s = sum(y[i])
            if s > 0.0:
                inv = 1.0 / s
                for j in range(m):
                    y[i][j] *= inv
        return y

    def optimize(self, max_iterations: int = 500, tolerance: float = 1e-4) -> Solution:
        mask = self._mask()
        y0 = self._initial(mask)
        durations = self._durations()
        capacities = self._capacities()

        # Build objectives
        objectives: List[Objective] = [
            CoverageObjective(weight=self.coverage_weight),
            FairnessObjective(durations, weight=self.fairness_weight),
            SparsityObjective(weight=self.sparsity_weight),
        ]

        # Build constraints
        constraints_low = [
            BoundsConstraint(0.0, 1.0),
            MaskConstraint(mask),
            CapacityConstraint(durations=durations, capacities=capacities),
        ]
        if any(spec.kind == "no_overlap" for spec in self.constraint_specs):
            constraints_low.append(RowOneHotConstraint())

        opt = AMNOptimizer(
            variables=y0,
            constraints=constraints_low,
            objectives=objectives,
            dt=self.dt,
            damping=self.damping,
            seed=self.seed,
        )
        sol = opt.optimize(max_iterations=max_iterations, tolerance=tolerance)

        # Decode to discrete assignments with capacity and skills respected
        assignments = self._decode_with_capacities(opt)
        return Solution(
            assignments=assignments,
            energy=sol.energy,
            energies=sol.energies,
            converged=sol.converged,
            iterations=sol.iterations,
        )

    def _decode_with_capacities(self, opt: AMNOptimizer) -> List[Tuple[Task, Resource]]:
        y = opt.y
        durations = self._durations()
        capacities = self._capacities()
        mask = self._mask()
        remaining = [c for c in capacities]
        # Greedy: sort tasks by confidence (max y in row)
        task_order = list(range(len(self.tasks)))
        task_order.sort(key=lambda i: max(y[i]) if y[i] else 0.0, reverse=True)
        assignments: List[Tuple[Task, Resource]] = []
        for i in task_order:
            # Try best resource first
            prefs = list(range(len(self.resources)))
            prefs.sort(key=lambda j: y[i][j], reverse=True)
            for j in prefs:
                if mask[i][j] == 0:
                    continue
                d = durations[i]
                if remaining[j] >= d:
                    assignments.append((self.tasks[i], self.resources[j]))
                    remaining[j] -= d
                    break
        return assignments
