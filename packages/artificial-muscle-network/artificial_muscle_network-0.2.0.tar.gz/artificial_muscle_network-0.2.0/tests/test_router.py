"""Tests for the Router class."""
import unittest

from amn import Router, Location, Vehicle, Delivery


class TestRouter(unittest.TestCase):
    def test_basic_routing(self):
        """Test basic delivery assignment."""
        locations = [
            Location("Depot", 0, 0),
            Location("Customer A", 1, 2),
            Location("Customer B", 3, 1),
            Location("Customer C", 2, 3),
        ]
        vehicles = [
            Vehicle("Truck 1", capacity=100),
            Vehicle("Truck 2", capacity=80),
        ]
        deliveries = [
            Delivery("Order 1", location_index=1, demand=30),
            Delivery("Order 2", location_index=2, demand=50),
            Delivery("Order 3", location_index=3, demand=40),
        ]

        router = Router(locations, vehicles, deliveries, seed=42)
        solution = router.optimize(max_iterations=200)

        # All deliveries should be assigned
        self.assertEqual(len(solution.assignments), 3)
        self.assertGreater(solution.iterations, 0)

    def test_capacity_constraint(self):
        """Test that vehicle capacity is respected."""
        locations = [
            Location("Depot", 0, 0),
            Location("A", 1, 0),
            Location("B", 2, 0),
        ]
        vehicles = [
            Vehicle("Small Truck", capacity=50),
        ]
        deliveries = [
            Delivery("Order 1", location_index=1, demand=30),
            Delivery("Order 2", location_index=2, demand=30),
        ]

        router = Router(locations, vehicles, deliveries, seed=42)
        solution = router.optimize(max_iterations=200)

        # Only one delivery should be assigned (capacity = 50, total demand = 60)
        self.assertEqual(len(solution.assignments), 1)

    def test_get_routes(self):
        """Test route organization."""
        locations = [
            Location("Depot", 0, 0),
            Location("A", 1, 0),
            Location("B", 0, 1),
        ]
        vehicles = [
            Vehicle("Truck 1", capacity=100),
            Vehicle("Truck 2", capacity=100),
        ]
        deliveries = [
            Delivery("Order 1", location_index=1, demand=10),
            Delivery("Order 2", location_index=2, demand=10),
        ]

        router = Router(locations, vehicles, deliveries, seed=42)
        solution = router.optimize(max_iterations=200)
        routes = router.get_routes(solution)

        # Should have routes for both vehicles
        self.assertIn("Truck 1", routes)
        self.assertIn("Truck 2", routes)
        # Total deliveries across routes should match assignments
        total = sum(len(r) for r in routes.values())
        self.assertEqual(total, len(solution.assignments))

    def test_time_windows(self):
        """Test time window handling."""
        locations = [
            Location("Depot", 0, 0),
            Location("Urgent", 10, 0),  # Far away
            Location("Nearby", 1, 0),
        ]
        vehicles = [Vehicle("Truck", capacity=100)]
        deliveries = [
            Delivery("Urgent Order", location_index=1, demand=10, time_window=(0, 5)),
            Delivery("Regular Order", location_index=2, demand=10),
        ]

        router = Router(locations, vehicles, deliveries, seed=42, speed=1.0)
        solution = router.optimize(max_iterations=300)

        # Both should be assigned (time window is soft constraint)
        self.assertEqual(len(solution.assignments), 2)


if __name__ == "__main__":
    unittest.main()
