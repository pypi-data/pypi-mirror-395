import subprocess
from enum import Enum
from pathlib import Path
from typing import Optional


class ContainerStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    STARTING = "starting"
    ERROR = "error"
    UNKNOWN = "unknown"


class DockerManager:
    """Manages Docker container operations via CLI."""

    def __init__(self, container_name: str = "reviewhound"):
        self.container_name = container_name
        self.project_root = Path(__file__).parent.parent.parent.parent

    def _run_command(
        self, args: list[str], capture_output: bool = True, timeout: int = 30
    ) -> Optional[subprocess.CompletedProcess]:
        """Run a command and return the result."""
        try:
            return subprocess.run(
                args,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                cwd=self.project_root,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None

    def is_docker_available(self) -> bool:
        """Check if Docker is available."""
        result = self._run_command(["docker", "version"])
        return result is not None and result.returncode == 0

    def get_container_status(self, name: Optional[str] = None) -> ContainerStatus:
        """Get the status of a container."""
        container = name or self.container_name
        result = self._run_command(
            [
                "docker",
                "ps",
                "--filter",
                f"name={container}",
                "--format",
                "{{.State}}",
            ]
        )

        if result is None:
            return ContainerStatus.UNKNOWN

        if result.returncode != 0:
            return ContainerStatus.ERROR

        state = result.stdout.strip().lower()
        if state == "running":
            return ContainerStatus.RUNNING
        elif state in ("created", "restarting"):
            return ContainerStatus.STARTING
        elif state == "":
            return ContainerStatus.STOPPED
        else:
            return ContainerStatus.STOPPED

    def get_container_info(self) -> dict:
        """Get detailed container info."""
        result = self._run_command(
            [
                "docker",
                "ps",
                "--filter",
                f"name={self.container_name}",
                "--format",
                "{{.ID}}\t{{.Status}}\t{{.Ports}}",
            ]
        )

        if result is None or result.returncode != 0 or not result.stdout.strip():
            return {}

        parts = result.stdout.strip().split("\t")
        if len(parts) >= 3:
            return {
                "id": parts[0],
                "status": parts[1],
                "ports": parts[2],
            }
        return {}

    def start(self) -> bool:
        """Start the container using docker-compose."""
        result = self._run_command(
            ["docker-compose", "up", "-d"],
            capture_output=True,
            timeout=60,
        )
        return result is not None and result.returncode == 0

    def stop(self) -> bool:
        """Stop the container using docker-compose."""
        result = self._run_command(
            ["docker-compose", "down"],
            capture_output=True,
            timeout=60,
        )
        return result is not None and result.returncode == 0

    def get_logs(self, tail: int = 100) -> str:
        """Get container logs."""
        result = self._run_command(
            ["docker", "logs", "--tail", str(tail), self.container_name],
            timeout=10,
        )

        if result is None or result.returncode != 0:
            return ""

        # Combine stdout and stderr (logs go to both)
        return result.stdout + (result.stderr or "")

    def stream_logs(self) -> Optional[subprocess.Popen]:
        """Start streaming logs. Returns Popen object for reading."""
        try:
            return subprocess.Popen(
                ["docker", "logs", "-f", "--tail", "50", self.container_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.project_root,
            )
        except FileNotFoundError:
            return None
