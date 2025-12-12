"""AMN: Artificial Muscle Network

Zero-dependency optimization library using physics-inspired dynamics.

Three problem domains:
- Scheduling: Assign tasks to resources with skills and capacity constraints
- Routing: Vehicle routing with capacities, distances, and time windows
- Allocation: Portfolio optimization and resource allocation
"""
from .core.optimizer import AMNOptimizer as Optimizer, Solution
from .core.objectives import (
    Objective,
    CoverageObjective,
    SparsityObjective,
    FairnessObjective,
    SumToOneObjective,
    EntropyObjective,
    LinearObjective,
    QuadraticObjective,
)
from .problems.scheduling import (
    Scheduler,
    Resource as SchedulingResource,
    Task,
    ConstraintSpec,
)
from .problems.routing import (
    Router,
    Location,
    Vehicle,
    Delivery,
)
from .problems.allocation import (
    Allocator,
    Asset,
    Resource as AllocationResource,
    ResourceAllocator,
)

# Backward compatibility aliases
Resource = SchedulingResource
Constraint = ConstraintSpec

__version__ = "0.2.0"

__all__ = [
    # Core
    "Optimizer",
    "Objective",
    "Solution",
    # Objectives
    "CoverageObjective",
    "SparsityObjective",
    "FairnessObjective",
    "SumToOneObjective",
    "EntropyObjective",
    "LinearObjective",
    "QuadraticObjective",
    # Scheduling
    "Scheduler",
    "Resource",
    "SchedulingResource",
    "Task",
    "Constraint",
    "ConstraintSpec",
    # Routing
    "Router",
    "Location",
    "Vehicle",
    "Delivery",
    # Allocation
    "Allocator",
    "Asset",
    "AllocationResource",
    "ResourceAllocator",
    # Meta
    "__version__",
]
