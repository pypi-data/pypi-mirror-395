"""Vehicle Routing Problem (VRP) module.

Provides a high-level Router class for solving delivery/routing problems
with vehicle capacities, time windows, and distance optimization.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import random

from ..core.optimizer import AMNOptimizer, Solution
from ..core.utils import Matrix, euclidean_distance, shape_of
from ..core.objectives import (
    Objective,
    CoverageObjective,
    SparsityObjective,
    FairnessObjective,
)
from ..core.constraints import BoundsConstraint, CapacityConstraint, RowOneHotConstraint


@dataclass(frozen=True)
class Location:
    """A location with coordinates.

    Attributes:
        name: Human-readable name for the location
        x: X coordinate
        y: Y coordinate
    """

    name: str
    x: float
    y: float

    @property
    def coords(self) -> Tuple[float, float]:
        return (self.x, self.y)


@dataclass(frozen=True)
class Vehicle:
    """A vehicle with capacity and optional depot.

    Attributes:
        name: Human-readable name for the vehicle
        capacity: Maximum load capacity
        depot_index: Index of the depot location (default 0)
    """

    name: str
    capacity: float
    depot_index: int = 0


@dataclass(frozen=True)
class Delivery:
    """A delivery request.

    Attributes:
        name: Human-readable name for the delivery
        location_index: Index into locations list
        demand: Amount of capacity consumed by this delivery
        time_window: Optional (earliest, latest) delivery time tuple
        service_time: Time spent at location (default 0)
    """

    name: str
    location_index: int
    demand: float
    time_window: Optional[Tuple[float, float]] = None
    service_time: float = 0.0


class DepotDistanceObjective(Objective):
    """Minimize total distance from depot to all assigned deliveries.

    For each vehicle, sums the distance from its depot to each delivery
    weighted by assignment strength. This encourages assigning nearby
    deliveries to vehicles with closer depots.

    Energy: sum_j sum_i y[i][j] * dist(depot[j], location[i])
    """

    def __init__(
        self,
        depot_distances: Matrix,  # depot_distances[i][j] = dist from delivery i to vehicle j's depot
        weight: float = 1.0,
    ) -> None:
        super().__init__(weight=weight)
        self._dist = depot_distances

    def evaluate(self, y: Matrix) -> float:
        e = 0.0
        for i, row in enumerate(y):
            for j, v in enumerate(row):
                e += v * self._dist[i][j]
        return e

    def gradient(self, y: Matrix) -> Matrix:
        return [[self._dist[i][j] for j in range(len(row))] for i, row in enumerate(y)]


class RouteCompactnessObjective(Objective):
    """Encourage deliveries assigned to the same vehicle to be close together.

    Penalizes spread-out assignments by computing variance of locations per vehicle.

    Energy: sum_j variance_of_locations_assigned_to_j
    """

    def __init__(
        self,
        locations: List[Tuple[float, float]],
        weight: float = 1.0,
    ) -> None:
        super().__init__(weight=weight)
        self._locs = locations

    def evaluate(self, y: Matrix) -> float:
        n, m = shape_of(y)
        e = 0.0
        for j in range(m):
            # Weighted mean of locations
            total_w = sum(y[i][j] for i in range(n)) + 1e-8
            mean_x = sum(y[i][j] * self._locs[i][0] for i in range(n)) / total_w
            mean_y = sum(y[i][j] * self._locs[i][1] for i in range(n)) / total_w
            # Weighted variance
            for i in range(n):
                dx = self._locs[i][0] - mean_x
                dy = self._locs[i][1] - mean_y
                e += y[i][j] * (dx * dx + dy * dy)
        return e

    def gradient(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        g: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for j in range(m):
            total_w = sum(y[i][j] for i in range(n)) + 1e-8
            mean_x = sum(y[i][j] * self._locs[i][0] for i in range(n)) / total_w
            mean_y = sum(y[i][j] * self._locs[i][1] for i in range(n)) / total_w
            for i in range(n):
                dx = self._locs[i][0] - mean_x
                dy = self._locs[i][1] - mean_y
                # Derivative of y[i][j] * (dist^2) term
                g[i][j] = dx * dx + dy * dy
        return g


class TimeWindowObjective(Objective):
    """Soft penalty for time window violations.

    Assumes sequential service along route. This is an approximation that
    penalizes deliveries assigned to vehicles that would arrive outside
    the time window, based on distance from depot.

    Energy: sum of violation penalties for each assignment
    """

    def __init__(
        self,
        time_windows: List[Optional[Tuple[float, float]]],  # Per delivery
        travel_times: Matrix,  # travel_times[i][j] = time from depot j to delivery i
        penalty: float = 10.0,
        weight: float = 1.0,
    ) -> None:
        super().__init__(weight=weight)
        self._windows = time_windows
        self._travel = travel_times
        self._penalty = penalty

    def evaluate(self, y: Matrix) -> float:
        e = 0.0
        for i, row in enumerate(y):
            window = self._windows[i]
            if window is None:
                continue
            earliest, latest = window
            for j, v in enumerate(row):
                arrival = self._travel[i][j]
                if arrival < earliest:
                    e += v * self._penalty * (earliest - arrival)
                elif arrival > latest:
                    e += v * self._penalty * (arrival - latest)
        return e

    def gradient(self, y: Matrix) -> Matrix:
        n, m = shape_of(y)
        g: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            window = self._windows[i]
            if window is None:
                continue
            earliest, latest = window
            for j in range(m):
                arrival = self._travel[i][j]
                if arrival < earliest:
                    g[i][j] = self._penalty * (earliest - arrival)
                elif arrival > latest:
                    g[i][j] = self._penalty * (arrival - latest)
        return g


class Router:
    """High-level solver for Vehicle Routing Problems.

    Example:
        locations = [
            Location("Depot", 0, 0),
            Location("Customer A", 1, 2),
            Location("Customer B", 3, 1),
        ]
        vehicles = [
            Vehicle("Truck 1", capacity=100),
            Vehicle("Truck 2", capacity=80),
        ]
        deliveries = [
            Delivery("Order 1", location_index=1, demand=30),
            Delivery("Order 2", location_index=2, demand=50),
        ]
        router = Router(locations, vehicles, deliveries)
        solution = router.optimize()
    """

    def __init__(
        self,
        locations: List[Location],
        vehicles: List[Vehicle],
        deliveries: List[Delivery],
        *,
        coverage_weight: float = 2.0,
        distance_weight: float = 1.0,
        compactness_weight: float = 0.5,
        fairness_weight: float = 0.5,
        sparsity_weight: float = 0.3,
        time_window_weight: float = 1.0,
        speed: float = 1.0,  # Units per time unit for travel time calculation
        dt: float = 0.1,
        damping: float = 0.1,
        seed: Optional[int] = None,
    ) -> None:
        if not locations:
            raise ValueError("locations must be non-empty")
        if not vehicles:
            raise ValueError("vehicles must be non-empty")
        if not deliveries:
            raise ValueError("deliveries must be non-empty")

        self.locations = locations
        self.vehicles = vehicles
        self.deliveries = deliveries

        self.coverage_weight = float(coverage_weight)
        self.distance_weight = float(distance_weight)
        self.compactness_weight = float(compactness_weight)
        self.fairness_weight = float(fairness_weight)
        self.sparsity_weight = float(sparsity_weight)
        self.time_window_weight = float(time_window_weight)
        self.speed = float(speed)

        self.dt = float(dt)
        self.damping = float(damping)
        self.seed = seed

    def _distance_matrix(self) -> Matrix:
        """Compute pairwise distance matrix between delivery locations."""
        n = len(self.deliveries)
        dist: Matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            loc_i = self.locations[self.deliveries[i].location_index]
            for k in range(n):
                if i != k:
                    loc_k = self.locations[self.deliveries[k].location_index]
                    dist[i][k] = euclidean_distance(loc_i.coords, loc_k.coords)
        return dist

    def _depot_distances(self) -> Matrix:
        """Compute distance from each delivery to each vehicle's depot."""
        n = len(self.deliveries)
        m = len(self.vehicles)
        dist: Matrix = [[0.0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            loc_i = self.locations[self.deliveries[i].location_index]
            for j in range(m):
                depot = self.locations[self.vehicles[j].depot_index]
                dist[i][j] = euclidean_distance(loc_i.coords, depot.coords)
        return dist

    def _travel_times(self) -> Matrix:
        """Compute travel time from each vehicle's depot to each delivery."""
        depot_dist = self._depot_distances()
        return [[d / self.speed for d in row] for row in depot_dist]

    def _delivery_locations(self) -> List[Tuple[float, float]]:
        """Get coordinates for each delivery location."""
        return [self.locations[d.location_index].coords for d in self.deliveries]

    def _demands(self) -> List[float]:
        """Get demand for each delivery."""
        return [float(d.demand) for d in self.deliveries]

    def _capacities(self) -> List[float]:
        """Get capacity for each vehicle."""
        return [float(v.capacity) for v in self.vehicles]

    def _time_windows(self) -> List[Optional[Tuple[float, float]]]:
        """Get time window for each delivery."""
        return [d.time_window for d in self.deliveries]

    def _initial(self) -> Matrix:
        """Initialize assignment matrix."""
        n = len(self.deliveries)
        m = len(self.vehicles)
        rng = random.Random(self.seed)
        y: Matrix = [[rng.random() for _ in range(m)] for _ in range(n)]
        # Normalize rows to sum to 1
        for i in range(n):
            s = sum(y[i])
            if s > 0:
                for j in range(m):
                    y[i][j] /= s
        return y

    def optimize(self, max_iterations: int = 500, tolerance: float = 1e-4) -> Solution:
        """Run optimization and return solution."""
        y0 = self._initial()
        demands = self._demands()
        capacities = self._capacities()

        # Build objectives
        objectives: List[Objective] = [
            CoverageObjective(weight=self.coverage_weight),
            SparsityObjective(weight=self.sparsity_weight),
        ]

        if self.distance_weight > 0:
            depot_dist = self._depot_distances()
            objectives.append(DepotDistanceObjective(depot_dist, weight=self.distance_weight))

        if self.compactness_weight > 0:
            locs = self._delivery_locations()
            objectives.append(RouteCompactnessObjective(locs, weight=self.compactness_weight))

        if self.fairness_weight > 0:
            objectives.append(FairnessObjective(demands, weight=self.fairness_weight))

        # Time window objective
        time_windows = self._time_windows()
        if self.time_window_weight > 0 and any(tw is not None for tw in time_windows):
            travel_times = self._travel_times()
            objectives.append(
                TimeWindowObjective(time_windows, travel_times, weight=self.time_window_weight)
            )

        # Build constraints
        constraints = [
            BoundsConstraint(0.0, 1.0),
            CapacityConstraint(durations=demands, capacities=capacities),
            RowOneHotConstraint(),
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

        # Decode to discrete assignments
        assignments = self._decode(opt.y)
        return Solution(
            assignments=assignments,
            energy=sol.energy,
            energies=sol.energies,
            converged=sol.converged,
            iterations=sol.iterations,
        )

    def _decode(self, y: Matrix) -> List[Tuple[Delivery, Vehicle]]:
        """Convert continuous solution to discrete assignments with capacity respect."""
        demands = self._demands()
        capacities = self._capacities()
        remaining = list(capacities)

        # Sort deliveries by confidence (max assignment strength)
        order = list(range(len(self.deliveries)))
        order.sort(key=lambda i: max(y[i]) if y[i] else 0.0, reverse=True)

        assignments: List[Tuple[Delivery, Vehicle]] = []
        for i in order:
            # Try vehicles in order of preference
            prefs = list(range(len(self.vehicles)))
            prefs.sort(key=lambda j: y[i][j], reverse=True)
            for j in prefs:
                if remaining[j] >= demands[i]:
                    assignments.append((self.deliveries[i], self.vehicles[j]))
                    remaining[j] -= demands[i]
                    break

        return assignments

    def get_routes(self, solution: Solution) -> Dict[str, List[Delivery]]:
        """Organize solution assignments into routes per vehicle.

        Args:
            solution: Solution returned by optimize()

        Returns:
            Dict mapping vehicle name to list of assigned deliveries
        """
        routes: Dict[str, List[Delivery]] = {v.name: [] for v in self.vehicles}
        for delivery, vehicle in solution.assignments:
            routes[vehicle.name].append(delivery)
        return routes
