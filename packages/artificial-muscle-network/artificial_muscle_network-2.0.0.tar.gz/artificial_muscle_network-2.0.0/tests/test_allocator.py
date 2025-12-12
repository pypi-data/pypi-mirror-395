"""Tests for the Allocator class."""
import unittest

from amn import Allocator, Asset


class TestAllocator(unittest.TestCase):
    def test_basic_allocation(self):
        """Test basic portfolio allocation."""
        assets = [
            Asset("Stocks", expected_return=0.10, risk=0.20),
            Asset("Bonds", expected_return=0.05, risk=0.05),
            Asset("Real Estate", expected_return=0.08, risk=0.15),
        ]

        allocator = Allocator(assets, risk_tolerance=0.5, seed=42)
        solution = allocator.optimize(max_iterations=200)

        # Should have allocation for all assets
        self.assertEqual(len(solution.assignments), 3)
        self.assertGreater(solution.iterations, 0)

    def test_budget_constraint(self):
        """Test that weights sum to budget."""
        assets = [
            Asset("A", expected_return=0.10, risk=0.10),
            Asset("B", expected_return=0.08, risk=0.08),
        ]

        allocator = Allocator(assets, budget=1.0, seed=42)
        solution = allocator.optimize(max_iterations=300)

        weights = allocator.get_weights(solution)
        total = sum(weights.values())
        # Should sum to approximately 1.0
        self.assertAlmostEqual(total, 1.0, places=2)

    def test_risk_tolerance(self):
        """Test that risk tolerance affects allocation."""
        assets = [
            Asset("High Risk", expected_return=0.15, risk=0.30),
            Asset("Low Risk", expected_return=0.03, risk=0.02),
        ]

        # Low risk tolerance should favor low-risk asset
        low_risk = Allocator(assets, risk_tolerance=0.1, seed=42)
        sol_low = low_risk.optimize(max_iterations=300)
        weights_low = low_risk.get_weights(sol_low)

        # High risk tolerance should favor high-risk asset
        high_risk = Allocator(assets, risk_tolerance=0.9, seed=42)
        sol_high = high_risk.optimize(max_iterations=300)
        weights_high = high_risk.get_weights(sol_high)

        # High risk tolerance should have more in high-risk asset
        self.assertGreater(
            weights_high["High Risk"],
            weights_low["High Risk"]
        )

    def test_get_weights(self):
        """Test weight extraction."""
        assets = [
            Asset("A", expected_return=0.10, risk=0.10),
            Asset("B", expected_return=0.08, risk=0.08),
        ]

        allocator = Allocator(assets, seed=42)
        solution = allocator.optimize(max_iterations=200)
        weights = allocator.get_weights(solution)

        self.assertIn("A", weights)
        self.assertIn("B", weights)
        self.assertGreaterEqual(weights["A"], 0)
        self.assertGreaterEqual(weights["B"], 0)

    def test_expected_return_calculation(self):
        """Test expected return calculation."""
        assets = [
            Asset("A", expected_return=0.10, risk=0.10),
            Asset("B", expected_return=0.05, risk=0.05),
        ]

        allocator = Allocator(assets, seed=42)
        solution = allocator.optimize(max_iterations=200)
        exp_return = allocator.expected_return(solution)

        # Expected return should be positive
        self.assertGreater(exp_return, 0)
        # Should be between min and max asset returns
        self.assertLessEqual(exp_return, 0.10)
        self.assertGreaterEqual(exp_return, 0.05)

    def test_min_max_weights(self):
        """Test min/max weight constraints."""
        assets = [
            Asset("A", expected_return=0.10, risk=0.10, min_weight=0.2, max_weight=0.8),
            Asset("B", expected_return=0.08, risk=0.08, min_weight=0.2, max_weight=0.8),
        ]

        allocator = Allocator(assets, seed=42)
        solution = allocator.optimize(max_iterations=300)
        weights = allocator.get_weights(solution)

        # Weights should respect bounds
        self.assertGreaterEqual(weights["A"], 0.2 - 0.01)  # Small tolerance
        self.assertLessEqual(weights["A"], 0.8 + 0.01)


if __name__ == "__main__":
    unittest.main()
