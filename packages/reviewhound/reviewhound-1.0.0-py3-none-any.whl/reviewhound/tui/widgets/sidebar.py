from textual.app import ComposeResult
from textual.widgets import Static, ListItem, ListView
from textual.widget import Widget
from textual.message import Message


class MenuItem(ListItem):
    """A menu item in the sidebar."""

    def __init__(self, label: str, key: str, selected: bool = False) -> None:
        super().__init__()
        self.label = label
        self.key = key
        self._selected = selected

    def compose(self) -> ComposeResult:
        icon = "▸" if self._selected else " "
        yield Static(f"{icon} {self.label}", id=f"label-{self.key}")

    def set_selected(self, selected: bool) -> None:
        """Update the selected state and refresh display."""
        self._selected = selected
        icon = "▸" if selected else " "
        label_widget = self.query_one(f"#label-{self.key}", Static)
        label_widget.update(f"{icon} {self.label}")


class Sidebar(Widget):
    """Navigation sidebar for the TUI."""

    DEFAULT_CSS = """
    Sidebar {
        width: 22;
        background: $surface;
        border-right: solid $primary;
    }

    Sidebar > .title {
        text-style: bold;
        color: $text;
        padding: 1;
        text-align: center;
        background: $primary;
    }

    Sidebar ListView {
        padding: 1;
        height: auto;
    }

    Sidebar ListView > ListItem {
        padding: 0 1;
    }

    Sidebar ListView > ListItem:hover {
        background: $primary 20%;
    }

    Sidebar > .shortcuts {
        dock: bottom;
        padding: 1;
        color: $text-muted;
        text-align: center;
    }
    """

    class Selected(Message):
        """Message sent when a menu item is selected."""

        def __init__(self, key: str) -> None:
            self.key = key
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Static("REVIEW HOUND", classes="title")
        yield ListView(
            MenuItem("Services", "services", selected=True),
            MenuItem("Logs", "logs"),
            MenuItem("Commands", "commands"),
            MenuItem("Config", "config"),
            id="menu",
        )
        yield Static("[1-4] Navigate  [q] Quit", classes="shortcuts")

    def select_by_key(self, key: str) -> None:
        """Programmatically select a menu item by its key."""
        list_view = self.query_one("#menu", ListView)
        for item in list_view.children:
            if isinstance(item, MenuItem):
                item.set_selected(item.key == key)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle menu item selection via click/enter."""
        if isinstance(event.item, MenuItem):
            self.select_by_key(event.item.key)
            self.post_message(self.Selected(event.item.key))
