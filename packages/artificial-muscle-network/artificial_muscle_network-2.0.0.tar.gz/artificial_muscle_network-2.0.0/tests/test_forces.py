import unittest

from amn.core.optimizer import AMNOptimizer, Objective


class Linear(Objective):
    # Energy = sum(y), gradient = 1
    def evaluate(self, y):
        return sum(v for row in y for v in row)

    def gradient(self, y):
        return [[1.0 for _ in row] for row in y]


class TestForces(unittest.TestCase):
    def test_force_shape(self):
        y0 = [[0.2, 0.8, 0.1]]
        opt = AMNOptimizer(y0, constraints=[], objectives=[Linear(weight=1.0)])
        f = opt.compute_forces()
        self.assertEqual(len(f), len(y0))
        self.assertEqual(len(f[0]), len(y0[0]))


if __name__ == "__main__":
    unittest.main()
