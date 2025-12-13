"""
baqup-agent - SDK for building baqup backup agents.

This package provides everything needed to build a compliant baqup agent:

- Contract types (ExitCode, AgentState, LogLevel)
- Structured logging
- Redis communication with filesystem fallback
- Heartbeat management
- Staging utilities
- Secret handling

Part of the baqup project: https://github.com/baqupio/baqup

Example:
    from baqup_agent import ExitCode, AgentState, Logger, BusClient
    from baqup_agent.config import load_config

    class MyAgent:
        def __init__(self):
            self.config = load_config("agent-schema.json")
            self.logger = Logger(
                job_id=self.config["BAQUP_JOB_ID"],
                agent_id="my-agent-123",
            )

        def run(self) -> int:
            # Your agent logic here
            return ExitCode.SUCCESS
"""

__version__ = "0.0.1"
__all__ = [
    # Contract constants
    "ExitCode",
    "AgentState",
    "LogLevel",
    # Classes
    "Logger",
    "Secret",
    "BusClient",
    "HeartbeatThread",
    "Manifest",
    "Artifact",
    # Functions
    "compute_checksum",
    "validate_path",
    "atomic_write",
]

from enum import IntEnum
from dataclasses import dataclass
from typing import Any


class ExitCode(IntEnum):
    """Exit codes from AGENT-CONTRACT-SPEC.md §5."""
    SUCCESS = 0
    GENERAL_FAILURE = 1
    USAGE_CONFIG_ERROR = 64
    DATA_ERROR = 65
    RESOURCE_UNAVAILABLE = 69
    INTERNAL_ERROR = 70
    CANT_CREATE_OUTPUT = 73
    IO_ERROR = 74
    COMPLETED_UNREPORTED = 75
    PARTIAL_FAILURE = 76


class AgentState(str):
    """Agent lifecycle states from AGENT-CONTRACT-SPEC.md §1."""
    INITIALIZING = "initializing"
    RUNNING = "running"
    COMPLETING = "completing"
    TERMINATED = "terminated"
    FAILED = "failed"


class LogLevel(IntEnum):
    """Log levels from AGENT-CONTRACT-SPEC.md §6."""
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5


@dataclass
class Artifact:
    """A single backup artifact."""
    filename: str
    size_bytes: int
    checksum_algorithm: str
    checksum_value: str
    compression: str | None = None
    encrypted: bool = False


@dataclass
class Manifest:
    """Backup manifest from AGENT-CONTRACT-SPEC.md §4."""
    version: str
    job_id: str
    agent: str
    agent_version: str
    role: str
    created_at: str
    artifacts: list[Artifact]
    source_metadata: dict[str, Any] | None = None


_PLACEHOLDER_MESSAGE = (
    "baqup-agent is currently a placeholder package. "
    "Full implementation coming soon. "
    "See https://github.com/baqupio/baqup for updates."
)


class Secret:
    """
    Secret wrapper that prevents accidental exposure in logs.

    From AGENT-CONTRACT-SPEC.md §7.
    """

    def __init__(self, value: str) -> None:
        self._value = value

    def __str__(self) -> str:
        return "[REDACTED]"

    def __repr__(self) -> str:
        return "Secret([REDACTED])"

    def reveal(self) -> str:
        """Get the actual secret value."""
        return self._value


class Logger:
    """Structured JSON logger - placeholder."""

    def __init__(
        self,
        job_id: str,
        agent_id: str,
        level: LogLevel = LogLevel.INFO,
        format: str = "json",
    ) -> None:
        raise NotImplementedError(_PLACEHOLDER_MESSAGE)


class BusClient:
    """Redis bus client with filesystem fallback - placeholder."""

    def __init__(self, config: dict[str, Any], logger: Logger) -> None:
        raise NotImplementedError(_PLACEHOLDER_MESSAGE)


class HeartbeatThread:
    """Background heartbeat thread - placeholder."""

    def __init__(
        self,
        bus: BusClient,
        agent_id: str,
        interval: int,
        logger: Logger,
    ) -> None:
        raise NotImplementedError(_PLACEHOLDER_MESSAGE)


def compute_checksum(path: str, algorithm: str = "sha256") -> str:
    """Compute file checksum - placeholder."""
    raise NotImplementedError(_PLACEHOLDER_MESSAGE)


def validate_path(path: str, boundary: str) -> bool:
    """Validate path is within boundary - placeholder."""
    raise NotImplementedError(_PLACEHOLDER_MESSAGE)


def atomic_write(staging_dir: str, job_id: str, logger: Logger) -> str:
    """Atomic write pattern - placeholder."""
    raise NotImplementedError(_PLACEHOLDER_MESSAGE)
