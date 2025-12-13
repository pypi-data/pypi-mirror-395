"""
Minimal end-to-end smoke test for the Universal Agent Kernel.
Run: python -m examples.minimal_e2e.run
"""

import asyncio
import os

from universal_agent.manifests.loader import ManifestLoader
from universal_agent.runtime.api import startup_event
from universal_agent.task.manager import TaskManager
from universal_agent.task.store import SQLTaskStore


async def main() -> None:
    # 1. Setup Env
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

    # 2. Boot Kernel
    print("Booting Kernel...")
    await startup_event()

    # 3. Load Manifest
    manifest = ManifestLoader.load_from_path("examples/minimal_e2e/manifest.yaml")
    print(f"Universe Loaded: {manifest.name}")

    # 4. Trigger Execution
    store = SQLTaskStore(os.environ["DATABASE_URL"])
    await store.init_db()
    manager = TaskManager(store)

    print("Creating Task...")
    state = await manager.create_execution(
        graph_name="cleanup-workflow",
        version="1.0.0",
        context={"target_path": "/tmp"},
    )

    print(f"Task ID: {state.execution_id} | Status: {state.status}")
    # Engine run loop would be invoked here in a full runtime.


if __name__ == "__main__":
    asyncio.run(main())

