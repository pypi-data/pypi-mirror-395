"""
universal_agent.runtime.sandbox

Abstraction for isolated execution environments.
Supports local execution and stubs for Docker/E2B.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int


class Sandbox(ABC):
    @abstractmethod
    async def run_command(self, cmd: str, env: Optional[Dict[str, str]] = None) -> ExecutionResult:
        """Run a shell command in the sandbox."""

    @abstractmethod
    async def write_file(self, path: str, content: str) -> None:
        """Write content to a file in the sandbox."""

    @abstractmethod
    async def read_file(self, path: str) -> str:
        """Read content from a file in the sandbox."""


class LocalSandbox(Sandbox):
    """Runs commands directly on the host machine. Use only for trusted workloads."""

    async def run_command(self, cmd: str, env: Optional[Dict[str, str]] = None) -> ExecutionResult:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )
        stdout, stderr = await proc.communicate()
        return ExecutionResult(
            stdout=stdout.decode().strip(),
            stderr=stderr.decode().strip(),
            exit_code=proc.returncode or 0,
        )

    async def write_file(self, path: str, content: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    async def read_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()


class DockerSandbox(Sandbox):
    """Stub for Docker-based sandboxing."""

    def __init__(self, image: str):
        self.image = image

    async def run_command(self, cmd: str, env: Optional[Dict[str, str]] = None) -> ExecutionResult:
        raise NotImplementedError("Docker sandbox not yet implemented")

    async def write_file(self, path: str, content: str) -> None:
        raise NotImplementedError("Docker sandbox not yet implemented")

    async def read_file(self, path: str) -> str:
        raise NotImplementedError("Docker sandbox not yet implemented")

