"""Tests for objective functions with numerical gradient verification."""
import unittest

from amn.core.objectives import (
    CoverageObjective,
    SparsityObjective,
    FairnessObjective,
    SumToOneObjective,
    QuadraticObjective,
    LinearObjective,
)


def numerical_gradient(obj, y, eps=1e-5):
    """Compute numerical gradient using finite differences."""
    n = len(y)
    m = len(y[0]) if n else 0
    grad = [[0.0 for _ in range(m)] for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            # Perturb positively
            y_plus = [row[:] for row in y]
            y_plus[i][j] += eps
            e_plus = obj.evaluate(y_plus)
            
            # Perturb negatively
            y_minus = [row[:] for row in y]
            y_minus[i][j] -= eps
            e_minus = obj.evaluate(y_minus)
            
            grad[i][j] = (e_plus - e_minus) / (2 * eps)
    
    return grad


def gradients_close(g1, g2, tol=1e-4):
    """Check if two gradient matrices are close."""
    for i in range(len(g1)):
        for j in range(len(g1[0])):
            if abs(g1[i][j] - g2[i][j]) > tol:
                return False
    return True


class TestCoverageObjective(unittest.TestCase):
    def test_gradient(self):
        """Test gradient matches numerical gradient."""
        obj = CoverageObjective()
        y = [[0.3, 0.4, 0.3], [0.5, 0.3, 0.2]]
        
        analytical = obj.gradient(y)
        numerical = numerical_gradient(obj, y)
        
        self.assertTrue(gradients_close(analytical, numerical))

    def test_minimum_at_target(self):
        """Test energy is zero when rows sum to target."""
        obj = CoverageObjective(target=1.0)
        y = [[0.5, 0.5], [0.3, 0.7]]
        
        energy = obj.evaluate(y)
        self.assertAlmostEqual(energy, 0.0, places=5)


class TestSparsityObjective(unittest.TestCase):
    def test_gradient(self):
        """Test gradient matches numerical gradient."""
        obj = SparsityObjective()
        y = [[0.3, 0.7], [0.5, 0.5]]
        
        analytical = obj.gradient(y)
        numerical = numerical_gradient(obj, y)
        
        self.assertTrue(gradients_close(analytical, numerical))

    def test_minimum_at_extremes(self):
        """Test energy is zero when all values are 0 or 1."""
        obj = SparsityObjective()
        y = [[0.0, 1.0], [1.0, 0.0]]
        
        energy = obj.evaluate(y)
        self.assertAlmostEqual(energy, 0.0, places=5)


class TestFairnessObjective(unittest.TestCase):
    def test_gradient(self):
        """Test gradient matches numerical gradient."""
        weights = [1.0, 2.0, 1.5]
        obj = FairnessObjective(weights)
        y = [[0.3, 0.7], [0.4, 0.6], [0.5, 0.5]]
        
        analytical = obj.gradient(y)
        numerical = numerical_gradient(obj, y)
        
        self.assertTrue(gradients_close(analytical, numerical))

    def test_minimum_when_balanced(self):
        """Test energy is zero when loads are equal."""
        weights = [1.0, 1.0]
        obj = FairnessObjective(weights)
        y = [[0.5, 0.5], [0.5, 0.5]]
        
        energy = obj.evaluate(y)
        self.assertAlmostEqual(energy, 0.0, places=5)


class TestSumToOneObjective(unittest.TestCase):
    def test_gradient_row(self):
        """Test gradient for row normalization."""
        obj = SumToOneObjective(axis="row")
        y = [[0.3, 0.4], [0.6, 0.2]]
        
        analytical = obj.gradient(y)
        numerical = numerical_gradient(obj, y)
        
        self.assertTrue(gradients_close(analytical, numerical))

    def test_gradient_col(self):
        """Test gradient for column normalization."""
        obj = SumToOneObjective(axis="col")
        y = [[0.3, 0.4], [0.6, 0.2]]
        
        analytical = obj.gradient(y)
        numerical = numerical_gradient(obj, y)
        
        self.assertTrue(gradients_close(analytical, numerical))


class TestQuadraticObjective(unittest.TestCase):
    def test_gradient(self):
        """Test gradient matches numerical gradient."""
        obj = QuadraticObjective()
        y = [[0.3, 0.4], [0.5, 0.2]]
        
        analytical = obj.gradient(y)
        numerical = numerical_gradient(obj, y)
        
        self.assertTrue(gradients_close(analytical, numerical))


class TestLinearObjective(unittest.TestCase):
    def test_gradient_minimize(self):
        """Test gradient for minimization."""
        coeffs = [[1.0, 2.0], [3.0, 4.0]]
        obj = LinearObjective(coeffs, minimize=True)
        y = [[0.3, 0.4], [0.5, 0.2]]
        
        analytical = obj.gradient(y)
        numerical = numerical_gradient(obj, y)
        
        self.assertTrue(gradients_close(analytical, numerical))

    def test_gradient_maximize(self):
        """Test gradient for maximization."""
        coeffs = [[1.0, 2.0], [3.0, 4.0]]
        obj = LinearObjective(coeffs, minimize=False)
        y = [[0.3, 0.4], [0.5, 0.2]]
        
        analytical = obj.gradient(y)
        numerical = numerical_gradient(obj, y)
        
        self.assertTrue(gradients_close(analytical, numerical))


if __name__ == "__main__":
    unittest.main()
