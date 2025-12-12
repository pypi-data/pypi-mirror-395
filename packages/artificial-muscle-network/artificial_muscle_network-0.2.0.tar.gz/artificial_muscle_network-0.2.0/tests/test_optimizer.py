import unittest

from amn.core.optimizer import AMNOptimizer
from amn.core.objectives import Objective
from amn.core.constraints import BoundsConstraint


class Quadratic(Objective):
    # Minimize sum(y^2)
    def evaluate(self, y):
        return sum(v * v for row in y for v in row)

    def gradient(self, y):
        return [[2.0 * v for v in row] for row in y]


class TestOptimizer(unittest.TestCase):
    def test_energy_decreases(self):
        y0 = [[0.8, 0.2], [0.5, 0.5]]
        opt = AMNOptimizer(y0, [BoundsConstraint()], [Quadratic(weight=1.0)], dt=0.2, damping=0.05)
        sol = opt.optimize(max_iterations=100)
        self.assertLess(sol.energy, Quadratic().evaluate(y0))
        self.assertGreater(sol.iterations, 0)


if __name__ == "__main__":
    unittest.main()
