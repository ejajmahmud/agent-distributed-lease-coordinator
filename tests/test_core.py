"""Tests for Lease Coordinator."""
import unittest
from agent_distributed_lease_coordinator.core import DistributedLeaseCoordinator

class TestDistributedLeaseCoordinator(unittest.TestCase):
    def test_acquire_and_contention(self):
        c = DistributedLeaseCoordinator()
        l1 = c.acquire_lease("res1", "a1", ttl_seconds=10.0)
        self.assertIsNotNone(l1)
        self.assertTrue(c.validate_fencing_token("res1", l1.fencing_token))

        # Contention by another agent
        l2 = c.acquire_lease("res1", "a2", ttl_seconds=10.0)
        self.assertIsNone(l2)

        # Release
        self.assertTrue(c.release_lease("res1", "a1", l1.fencing_token))
        self.assertFalse(c.validate_fencing_token("res1", l1.fencing_token))
