from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button, Select, RichLog
from textual.widget import Widget
from textual.timer import Timer

from reviewhound.tui.services import DockerManager, ProcessManager, ProcessType


class LogsPanel(Widget):
    """Panel for viewing service logs."""

    DEFAULT_CSS = """
    LogsPanel {
        width: 100%;
        height: 100%;
    }

    LogsPanel > .controls {
        height: 3;
        padding: 0 1;
        align: left middle;
        background: $surface;
    }

    LogsPanel > .controls Button {
        margin-left: 1;
    }

    LogsPanel > .controls Select {
        width: 20;
    }

    LogsPanel > RichLog {
        height: 1fr;
        border: solid $primary;
        background: $surface;
        padding: 0 1;
    }
    """

    SOURCES = [
        ("All", "all"),
        ("Docker", "docker"),
        ("Web", "web"),
        ("Scheduler", "scheduler"),
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.docker = DockerManager()
        self.process = ProcessManager()
        self._paused = False
        self._timer: Timer | None = None
        self._current_source = "all"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Static("Source: "),
            Select(self.SOURCES, value="all", id="source-select"),
            Button("Clear", id="clear"),
            Button("Pause", id="pause"),
            classes="controls",
        )
        yield RichLog(highlight=True, markup=True, id="log-output")

    def on_mount(self) -> None:
        """Start log polling."""
        self._timer = self.set_interval(0.5, self._poll_logs)

    def _poll_logs(self) -> None:
        """Poll for new log output."""
        if self._paused:
            return

        log = self.query_one("#log-output", RichLog)

        # Poll based on selected source
        if self._current_source in ("all", "docker"):
            docker_logs = self.docker.get_logs(tail=5)
            if docker_logs:
                for line in docker_logs.strip().split("\n")[-3:]:
                    if line.strip():
                        log.write(f"[blue][DOCKER][/blue] {line}")

        if self._current_source in ("all", "web"):
            output = self.process.read_output(ProcessType.WEB)
            if output and output.strip():
                log.write(f"[green][WEB][/green] {output.strip()}")

        if self._current_source in ("all", "scheduler"):
            output = self.process.read_output(ProcessType.SCHEDULER)
            if output and output.strip():
                log.write(f"[yellow][SCHED][/yellow] {output.strip()}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "clear":
            log = self.query_one("#log-output", RichLog)
            log.clear()
            self.notify("Logs cleared")

        elif event.button.id == "pause":
            self._paused = not self._paused
            event.button.label = "Resume" if self._paused else "Pause"
            self.notify("Paused" if self._paused else "Resumed")

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle source filter change."""
        self._current_source = event.value
        log = self.query_one("#log-output", RichLog)
        log.clear()
        log.write(f"[dim]Filtering: {event.value}[/dim]")
