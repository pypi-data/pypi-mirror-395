import subprocess
import sys
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Static, Button, RichLog, Input
from textual.widget import Widget


class CommandsPanel(Widget):
    """Panel for running CLI commands."""

    DEFAULT_CSS = """
    CommandsPanel {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    CommandsPanel > .section-title {
        text-style: bold;
        padding-bottom: 1;
    }

    CommandsPanel > .button-group {
        height: auto;
        padding-bottom: 1;
    }

    CommandsPanel > .button-group Button {
        margin-right: 1;
        margin-bottom: 1;
    }

    CommandsPanel > .output-section {
        height: 1fr;
        border: solid $primary;
    }

    CommandsPanel > .output-section > .output-header {
        background: $surface;
        padding: 0 1;
        height: 1;
    }

    CommandsPanel > .output-section > RichLog {
        height: 1fr;
        padding: 0 1;
    }
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.project_root = Path(__file__).parent.parent.parent.parent

    def compose(self) -> ComposeResult:
        # Scraping commands
        yield Static("SCRAPING", classes="section-title")
        yield Horizontal(
            Button("Scrape All", id="cmd-scrape-all"),
            Button("List Businesses", id="cmd-list"),
            classes="button-group",
        )

        # Data commands
        yield Static("DATA", classes="section-title")
        yield Horizontal(
            Button("View Stats", id="cmd-stats"),
            Button("Export CSV", id="cmd-export"),
            classes="button-group",
        )

        # Output area
        yield Container(
            Static("OUTPUT", classes="output-header"),
            RichLog(highlight=True, markup=True, id="cmd-output"),
            classes="output-section",
        )

    def _run_command(self, args: list[str]) -> None:
        """Run a CLI command and show output."""
        output = self.query_one("#cmd-output", RichLog)
        output.clear()

        cmd = [sys.executable, "-m", "reviewhound"] + args
        output.write(f"[dim]$ reviewhound {' '.join(args)}[/dim]\n")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.project_root,
            )

            if result.stdout:
                output.write(result.stdout)
            if result.stderr:
                output.write(f"[red]{result.stderr}[/red]")

            if result.returncode == 0:
                output.write("\n[green]✓ Done[/green]")
            else:
                output.write(f"\n[red]✗ Exit code: {result.returncode}[/red]")

        except subprocess.TimeoutExpired:
            output.write("[red]Command timed out[/red]")
        except Exception as e:
            output.write(f"[red]Error: {e}[/red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "cmd-scrape-all":
            self.notify("Scraping all businesses...")
            self._run_command(["scrape", "--all"])

        elif button_id == "cmd-list":
            self._run_command(["list"])

        elif button_id == "cmd-stats":
            # Show stats for first business (simplified)
            self._run_command(["list"])
            self.notify("Use 'reviewhound stats <id>' for detailed stats")

        elif button_id == "cmd-export":
            self._run_command(["list"])
            self.notify("Use 'reviewhound export <id>' to export CSV")
