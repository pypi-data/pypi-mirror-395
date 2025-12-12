"""Tests for the Scheduler class."""
import unittest

from amn import Scheduler, Resource, Task, Constraint


class TestScheduler(unittest.TestCase):
    def test_basic_scheduling(self):
        """Test basic task assignment."""
        resources = [
            Resource("Worker A", capacity=40, skills={"welding", "assembly"}),
            Resource("Worker B", capacity=35, skills={"painting", "assembly"}),
        ]
        tasks = [
            Task("Job 1", duration=4, required_skills={"welding"}),
            Task("Job 2", duration=3, required_skills={"painting"}),
        ]
        constraints = [
            Constraint.no_overlap(),
            Constraint.skill_match(),
            Constraint.capacity(max_hours=40),
        ]

        scheduler = Scheduler(resources, tasks, constraints, seed=42)
        solution = scheduler.optimize(max_iterations=200)

        # Should have assignments for both tasks
        self.assertEqual(len(solution.assignments), 2)
        self.assertGreater(solution.iterations, 0)

    def test_skill_matching(self):
        """Test that skill matching is respected."""
        resources = [
            Resource("Welder", capacity=40, skills={"welding"}),
            Resource("Painter", capacity=40, skills={"painting"}),
        ]
        tasks = [
            Task("Weld Job", duration=8, required_skills={"welding"}),
        ]
        constraints = [Constraint.skill_match()]

        scheduler = Scheduler(resources, tasks, constraints, seed=42)
        solution = scheduler.optimize(max_iterations=200)

        # Task should be assigned to welder
        self.assertEqual(len(solution.assignments), 1)
        task, resource = solution.assignments[0]
        self.assertEqual(resource.name, "Welder")

    def test_capacity_constraint(self):
        """Test that capacity constraints are respected."""
        resources = [
            Resource("Worker", capacity=10, skills={"general"}),
        ]
        tasks = [
            Task("Job 1", duration=6, required_skills={"general"}),
            Task("Job 2", duration=6, required_skills={"general"}),
        ]
        constraints = [Constraint.capacity(max_hours=10)]

        scheduler = Scheduler(resources, tasks, constraints, seed=42)
        solution = scheduler.optimize(max_iterations=200)

        # Only one task should be assigned (capacity exceeded)
        self.assertEqual(len(solution.assignments), 1)

    def test_convergence(self):
        """Test that optimization converges."""
        resources = [Resource("A", 40, {"skill"}), Resource("B", 40, {"skill"})]
        tasks = [Task(f"T{i}", 4, {"skill"}) for i in range(4)]
        constraints = [Constraint.no_overlap(), Constraint.skill_match()]

        scheduler = Scheduler(resources, tasks, constraints, seed=42)
        solution = scheduler.optimize(max_iterations=500, tolerance=1e-4)

        # Should converge before max iterations
        self.assertTrue(solution.converged)


if __name__ == "__main__":
    unittest.main()
