import unittest

from amn.core.constraints import CapacityConstraint


class TestConstraints(unittest.TestCase):
    def test_capacity_projection(self):
        durations = [4.0, 6.0]
        capacities = [8.0, 8.0]
        y = [
            [0.9, 0.1],
            [0.9, 0.1],
        ]
        c = CapacityConstraint(durations=durations, capacities=capacities)
        y2 = c.project(y)
        # Check column loads <= capacity
        loads = [
            y2[0][0] * durations[0] + y2[1][0] * durations[1],
            y2[0][1] * durations[0] + y2[1][1] * durations[1],
        ]
        self.assertLessEqual(loads[0], capacities[0] + 1e-6)
        self.assertLessEqual(loads[1], capacities[1] + 1e-6)


if __name__ == "__main__":
    unittest.main()
