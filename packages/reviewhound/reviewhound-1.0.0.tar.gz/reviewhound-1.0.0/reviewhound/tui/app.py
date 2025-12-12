from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer

from reviewhound.tui.widgets import (
    Sidebar,
    ServicesPanel,
    LogsPanel,
    CommandsPanel,
    ConfigPanel,
)
from reviewhound.tui.services import ProcessManager


class ReviewHoundApp(App):
    """Review Hound TUI Dashboard."""

    CSS = """
    Screen {
        layout: horizontal;
    }

    #main-container {
        width: 1fr;
    }

    .panel {
        width: 100%;
        height: 100%;
    }

    .panel.hidden {
        display: none;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("1", "switch('services')", "Services"),
        ("2", "switch('logs')", "Logs"),
        ("3", "switch('commands')", "Commands"),
        ("4", "switch('config')", "Config"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.process_manager = ProcessManager()
        self._current_panel = "services"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Sidebar()
        yield Container(
            ServicesPanel(classes="panel", id="panel-services"),
            LogsPanel(classes="panel hidden", id="panel-logs"),
            CommandsPanel(classes="panel hidden", id="panel-commands"),
            ConfigPanel(classes="panel hidden", id="panel-config"),
            id="main-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Show services panel by default."""
        self.action_switch("services")

    def on_sidebar_selected(self, event: Sidebar.Selected) -> None:
        """Handle sidebar selection."""
        self.action_switch(event.key)

    def action_switch(self, panel: str) -> None:
        """Switch the main panel view."""
        # Hide all panels
        for p in self.query(".panel"):
            p.add_class("hidden")

        # Show selected panel
        selected = self.query_one(f"#panel-{panel}")
        selected.remove_class("hidden")

        # Update sidebar selection
        sidebar = self.query_one(Sidebar)
        sidebar.select_by_key(panel)

        self._current_panel = panel

    def action_quit(self) -> None:
        """Handle quit with cleanup prompt."""
        running = self.process_manager.get_all_running()
        if running:
            self.notify(f"Stopping {len(running)} process(es)...")
            self.process_manager.stop_all()
        self.exit()
