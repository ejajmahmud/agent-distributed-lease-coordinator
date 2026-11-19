"""Core Distributed Lease Coordinator with Monotonic Fencing Tokens."""
from typing import Dict, Optional
import time

class LeaseRecord:
    def __init__(self, resource_id: str, holder_id: str, fencing_token: int, expires_at: float):
        self.resource_id = resource_id
        self.holder_id = holder_id
        self.fencing_token = fencing_token
        self.expires_at = expires_at

    def is_expired(self) -> bool:
        return time.time() > self.expires_at

class DistributedLeaseCoordinator:
    def __init__(self):
        self._leases: Dict[str, LeaseRecord] = {}
        self._next_fencing_token = 100

    def acquire_lease(self, resource_id: str, holder_id: str, ttl_seconds: float = 5.0) -> Optional[LeaseRecord]:
        now = time.time()
        current = self._leases.get(resource_id)
        if current and not current.is_expired():
            if current.holder_id != holder_id:
                return None
            # Renew existing lease
            current.expires_at = now + ttl_seconds
            return current

        self._next_fencing_token += 1
        lease = LeaseRecord(resource_id, holder_id, self._next_fencing_token, now + ttl_seconds)
        self._leases[resource_id] = lease
        return lease

    def release_lease(self, resource_id: str, holder_id: str, fencing_token: int) -> bool:
        current = self._leases.get(resource_id)
        if not current or current.holder_id != holder_id or current.fencing_token != fencing_token:
            return False
        del self._leases[resource_id]
        return True

    def validate_fencing_token(self, resource_id: str, token: int) -> bool:
        current = self._leases.get(resource_id)
        return bool(current and not current.is_expired() and current.fencing_token == token)
