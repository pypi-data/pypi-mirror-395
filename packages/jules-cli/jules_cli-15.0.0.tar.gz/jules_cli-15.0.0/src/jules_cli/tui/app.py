from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class Dashboard(Static):
    """A Dashboard widget."""

    def compose(self) -> ComposeResult:
        yield Static("Welcome to Jules CLI TUI", id="welcome-message")
        yield Static("Select a session or run a command.", id="instructions")

class JulesTui(App):
    """A Textual app for Jules CLI."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Dashboard()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
