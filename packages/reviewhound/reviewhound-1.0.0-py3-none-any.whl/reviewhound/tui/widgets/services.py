from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Static, Button, Rule
from textual.widget import Widget
from textual.reactive import reactive
from textual.timer import Timer

from reviewhound.tui.services import (
    DockerManager,
    ProcessManager,
    HealthChecker,
    ContainerStatus,
    ProcessType,
)


class ServiceRow(Horizontal):
    """A row showing a single service status."""

    DEFAULT_CSS = """
    ServiceRow {
        height: 3;
        padding: 0 1;
        align: left middle;
    }

    ServiceRow > .status-icon {
        width: 3;
    }

    ServiceRow > .name {
        width: 16;
    }

    ServiceRow > .state {
        width: 12;
    }

    ServiceRow > .details {
        width: 1fr;
        color: $text-muted;
    }

    ServiceRow > Button {
        min-width: 8;
    }
    """

    def __init__(
        self,
        name: str,
        service_type: str,
        running: bool = False,
        details: str = "",
    ) -> None:
        super().__init__()
        self.service_name = name
        self.service_type = service_type
        self._running = running
        self._details = details

    def compose(self) -> ComposeResult:
        icon = "●" if self._running else "○"
        icon_class = "running" if self._running else "stopped"
        state = "Running" if self._running else "Stopped"
        button_label = "Stop" if self._running else "Start"

        yield Static(icon, classes=f"status-icon {icon_class}")
        yield Static(self.service_name, classes="name")
        yield Static(state, classes="state")
        yield Static(self._details, classes="details")
        yield Button(button_label, id=f"btn-{self.service_type}", variant="primary" if not self._running else "warning")


class ServicesPanel(Widget):
    """Panel showing all services and their status."""

    DEFAULT_CSS = """
    ServicesPanel {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    ServicesPanel > .section-title {
        text-style: bold;
        padding: 0 0 1 0;
    }

    ServicesPanel > .section {
        border: solid $primary;
        padding: 1;
        margin-bottom: 1;
    }

    ServicesPanel > .actions {
        height: 3;
        align: center middle;
    }

    ServicesPanel > .actions Button {
        margin: 0 1;
    }

    ServicesPanel > .health {
        dock: bottom;
        height: 5;
        border-top: solid $primary;
        padding: 1;
    }

    .status-icon.running {
        color: $success;
    }

    .status-icon.stopped {
        color: $text-muted;
    }
    """

    last_check = reactive("Never")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.docker = DockerManager()
        self.process = ProcessManager()
        self.health = HealthChecker()
        self._timer: Timer | None = None

    def compose(self) -> ComposeResult:
        # Docker section
        yield Static("DOCKER", classes="section-title")
        yield Container(
            ServiceRow("reviewhound", "docker", False, ""),
            classes="section",
            id="docker-section",
        )

        # Python processes section
        yield Static("PYTHON PROCESSES", classes="section-title")
        yield Container(
            ServiceRow("Web Server", "web", False, ""),
            ServiceRow("Scheduler", "scheduler", False, ""),
            classes="section",
            id="python-section",
        )

        # Action buttons
        yield Horizontal(
            Button("Start All Python", id="start-all"),
            Button("Stop All", id="stop-all", variant="error"),
            Button("Refresh", id="refresh"),
            classes="actions",
        )

        # Health status
        yield Static("", id="health-status", classes="health")

    def on_mount(self) -> None:
        """Start the health check timer."""
        self._timer = self.set_interval(5, self.refresh_status)
        self.refresh_status()

    def refresh_status(self) -> None:
        """Refresh all service statuses."""
        # Docker status
        docker_status = self.docker.get_container_status()
        docker_running = docker_status == ContainerStatus.RUNNING
        docker_info = self.docker.get_container_info()
        docker_details = docker_info.get("ports", "") if docker_running else ""

        docker_section = self.query_one("#docker-section", Container)
        docker_section.remove_children()
        docker_section.mount(ServiceRow("reviewhound", "docker", docker_running, docker_details))

        # Python process status
        python_section = self.query_one("#python-section", Container)
        python_section.remove_children()

        web_info = self.process.get_info(ProcessType.WEB)
        web_details = f"Port {web_info.port}" if web_info.running and web_info.port else ""
        python_section.mount(ServiceRow("Web Server", "web", web_info.running, web_details))

        sched_info = self.process.get_info(ProcessType.SCHEDULER)
        sched_details = f"PID {sched_info.pid}" if sched_info.running and sched_info.pid else ""
        python_section.mount(ServiceRow("Scheduler", "scheduler", sched_info.running, sched_details))

        # Health checks
        health_status = self.query_one("#health-status", Static)
        all_health = self.health.check_all()

        web_health = all_health["web"]
        db_health = all_health["database"]

        web_icon = "✓" if web_health.healthy else "✗"
        db_icon = "✓" if db_health.healthy else "✗"

        # Show URL when web is running
        web_url = "http://localhost:5000" if web_health.healthy else ""
        url_line = f"  → {web_url}\n" if web_url else "\n"

        health_status.update(
            f"Last check: {web_health.checked_at.strftime('%H:%M:%S')}\n"
            f"Web: {web_icon} {web_health.message}{url_line}"
            f"DB: {db_icon} {db_health.message}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "refresh":
            self.refresh_status()
            self.notify("Refreshed")

        elif button_id == "start-all":
            self.process.start(ProcessType.WEB)
            self.process.start(ProcessType.SCHEDULER)
            self.set_timer(1, self.refresh_status)
            self.notify("Starting Python services...")

        elif button_id == "stop-all":
            self.process.stop_all()
            self.docker.stop()
            self.set_timer(1, self.refresh_status)
            self.notify("Stopping all services...")

        elif button_id == "btn-docker":
            if self.docker.get_container_status() == ContainerStatus.RUNNING:
                self.docker.stop()
                self.notify("Stopping Docker...")
            else:
                self.docker.start()
                self.notify("Starting Docker...")
            self.set_timer(2, self.refresh_status)

        elif button_id == "btn-web":
            if self.process.is_running(ProcessType.WEB):
                self.process.stop(ProcessType.WEB)
                self.notify("Stopping web server...")
            else:
                self.process.start(ProcessType.WEB)
                self.notify("Starting web server...")
            self.set_timer(1, self.refresh_status)

        elif button_id == "btn-scheduler":
            if self.process.is_running(ProcessType.SCHEDULER):
                self.process.stop(ProcessType.SCHEDULER)
                self.notify("Stopping scheduler...")
            else:
                self.process.start(ProcessType.SCHEDULER)
                self.notify("Starting scheduler...")
            self.set_timer(1, self.refresh_status)
