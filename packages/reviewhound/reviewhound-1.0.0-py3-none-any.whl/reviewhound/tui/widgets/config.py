import os
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button, DataTable
from textual.widget import Widget

from reviewhound.config import Config
from reviewhound.database import get_session
from reviewhound.models import Review, Business


class ConfigPanel(Widget):
    """Panel showing current configuration."""

    DEFAULT_CSS = """
    ConfigPanel {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    ConfigPanel > .section-title {
        text-style: bold;
        padding: 1 0;
    }

    ConfigPanel > DataTable {
        height: auto;
        max-height: 50%;
        margin-bottom: 1;
    }

    ConfigPanel > .footer {
        dock: bottom;
        height: 3;
        padding: 1;
        background: $surface;
        border-top: solid $primary;
    }

    ConfigPanel > .reload-btn {
        dock: top;
        width: auto;
    }
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.project_root = Path(__file__).parent.parent.parent.parent

    def compose(self) -> ComposeResult:
        yield Button("Reload Env", id="reload", classes="reload-btn")

        yield Static("DATABASE", classes="section-title")
        yield DataTable(id="db-table")

        yield Static("SCRAPING", classes="section-title")
        yield DataTable(id="scrape-table")

        yield Static("WEB SERVER", classes="section-title")
        yield DataTable(id="web-table")

        yield Static("EMAIL ALERTS", classes="section-title")
        yield DataTable(id="email-table")

        yield Static("", id="env-path", classes="footer")

    def on_mount(self) -> None:
        """Initialize tables."""
        self._refresh_config()

    def _refresh_config(self) -> None:
        """Refresh all configuration displays."""
        # Database config
        db_table = self.query_one("#db-table", DataTable)
        db_table.clear(columns=True)
        db_table.add_columns("Setting", "Value")

        db_path = Path(Config.DATABASE_PATH)
        if db_path.exists():
            size_mb = db_path.stat().st_size / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB"
        else:
            size_str = "Not found"

        db_error = False
        try:
            with get_session() as session:
                review_count = session.query(Review).count()
                business_count = session.query(Business).count()
        except Exception:
            review_count = 0
            business_count = 0
            db_error = True

        db_table.add_rows([
            ("Path", str(Config.DATABASE_PATH)),
            ("Size", size_str),
            ("Reviews", "(error)" if db_error else str(review_count)),
            ("Businesses", "(error)" if db_error else str(business_count)),
        ])

        # Scraping config
        scrape_table = self.query_one("#scrape-table", DataTable)
        scrape_table.clear(columns=True)
        scrape_table.add_columns("Setting", "Value")
        scrape_table.add_rows([
            ("Request Delay", f"{Config.REQUEST_DELAY_MIN} - {Config.REQUEST_DELAY_MAX} sec"),
            ("Max Pages", str(Config.MAX_PAGES_PER_SOURCE)),
            ("Interval", f"{Config.SCRAPE_INTERVAL_HOURS} hours"),
        ])

        # Web config
        web_table = self.query_one("#web-table", DataTable)
        web_table.clear(columns=True)
        web_table.add_columns("Setting", "Value")
        web_table.add_rows([
            ("Host", "127.0.0.1"),
            ("Port", "5000"),
            ("Debug", "On" if Config.FLASK_DEBUG else "Off"),
        ])

        # Email config
        email_table = self.query_one("#email-table", DataTable)
        email_table.clear(columns=True)
        email_table.add_columns("Setting", "Value")

        smtp_configured = bool(Config.SMTP_USER and Config.SMTP_PASSWORD)
        email_table.add_rows([
            ("SMTP Host", f"{Config.SMTP_HOST}:{Config.SMTP_PORT}"),
            ("Status", "✓ Configured" if smtp_configured else "✗ Not configured"),
        ])

        # Env path
        env_path = self.query_one("#env-path", Static)
        env_file = self.project_root / ".env"
        env_path.update(f".env path: {env_file}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle reload button."""
        if event.button.id == "reload":
            # Reload dotenv
            from dotenv import load_dotenv
            load_dotenv(override=True)
            self._refresh_config()
            self.notify("Configuration reloaded")
