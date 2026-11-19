"""CLI for Lease Coordinator."""
import argparse
from .core import DistributedLeaseCoordinator

def main():
    parser = argparse.ArgumentParser(description="Agent Distributed Lease Coordinator CLI")
    parser.add_argument("--demo", action="store_true", help="Run lease demo")
    args = parser.parse_args()

    coord = DistributedLeaseCoordinator()
    lease = coord.acquire_lease("workspace/state.json", "agent-alpha", ttl_seconds=3.0)
    if lease:
        print(f"Lease granted: resource={lease.resource_id}, holder={lease.holder_id}, token={lease.fencing_token}")
        valid = coord.validate_fencing_token("workspace/state.json", lease.fencing_token)
        print(f"Token validity: {valid}")

if __name__ == "__main__":
    main()
