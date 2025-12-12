import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class ProcessType(Enum):
    WEB = "web"
    SCHEDULER = "scheduler"


@dataclass
class ProcessInfo:
    """Information about a managed process."""
    process_type: ProcessType
    running: bool
    pid: Optional[int] = None
    port: Optional[int] = None


class ProcessManager:
    """Manages Python subprocess operations."""

    COMMANDS = {
        ProcessType.WEB: [
            sys.executable, "-m", "reviewhound", "web",
            "--host", "0.0.0.0", "--port", "5000"
        ],
        ProcessType.SCHEDULER: [
            sys.executable, "-m", "reviewhound", "watch"
        ],
    }

    def __init__(self):
        self._processes: dict[ProcessType, subprocess.Popen] = {}
        self.project_root = Path(__file__).parent.parent.parent.parent

    def start(self, process_type: ProcessType) -> bool:
        """Start a process."""
        if process_type in self._processes:
            proc = self._processes[process_type]
            if proc.poll() is None:
                # Already running
                return True

        cmd = self.COMMANDS[process_type]

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered
                cwd=self.project_root,
            )
            self._processes[process_type] = proc
            return True
        except (FileNotFoundError, OSError):
            return False

    def stop(self, process_type: ProcessType) -> bool:
        """Stop a process."""
        if process_type not in self._processes:
            return True

        proc = self._processes[process_type]

        try:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=2)
        except OSError:
            pass

        del self._processes[process_type]
        return True

    def stop_all(self) -> None:
        """Stop all managed processes."""
        for process_type in list(self._processes.keys()):
            self.stop(process_type)

    def get_info(self, process_type: ProcessType) -> ProcessInfo:
        """Get info about a process."""
        if process_type not in self._processes:
            return ProcessInfo(
                process_type=process_type,
                running=False,
            )

        proc = self._processes[process_type]
        is_running = proc.poll() is None

        if not is_running:
            # Clean up dead process
            del self._processes[process_type]
            return ProcessInfo(
                process_type=process_type,
                running=False,
            )

        port = 5000 if process_type == ProcessType.WEB else None

        return ProcessInfo(
            process_type=process_type,
            running=True,
            pid=proc.pid,
            port=port,
        )

    def is_running(self, process_type: ProcessType) -> bool:
        """Check if a process is running."""
        return self.get_info(process_type).running

    def read_output(self, process_type: ProcessType) -> Optional[str]:
        """Read a line of output from a process (non-blocking)."""
        if process_type not in self._processes:
            return None

        proc = self._processes[process_type]
        if proc.stdout is None:
            return None

        try:
            return proc.stdout.readline()
        except (OSError, ValueError):
            return None

    def get_all_running(self) -> list[ProcessInfo]:
        """Get info for all running processes."""
        return [
            self.get_info(pt)
            for pt in ProcessType
            if self.is_running(pt)
        ]
