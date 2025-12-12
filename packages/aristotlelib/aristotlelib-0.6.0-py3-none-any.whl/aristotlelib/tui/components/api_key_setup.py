"""API key setup widget with input field."""

from textual.widgets import Static, Input
from textual.containers import Vertical
from textual.message import Message


class ApiKeySetupWidget(Vertical):
    """
    Widget for entering API key.
    Allows users to enter their API key directly in the TUI.
    """

    class Submitted(Message):
        """Message sent when user submits their API key."""

        def __init__(self, api_key: str) -> None:
            super().__init__()
            self.api_key = api_key

    DEFAULT_CSS = """
    ApiKeySetupWidget {
        height: auto;
        width: 100%;
        padding: 1 0;
    }
    ApiKeySetupWidget .setup-header {
        color: $warning;
        text-style: bold;
        padding-bottom: 1;
    }
    ApiKeySetupWidget .setup-instructions {
        color: $text;
        padding-bottom: 1;
    }
    ApiKeySetupWidget Input {
        margin: 1 0;
    }
    """

    def compose(self):
        """Create the widget layout."""
        # Adapt message based on terminal width
        terminal_width = self.app.size.width

        if terminal_width >= 80:
            # Full message on one line
            instructions = (
                "Get your free API key at: https://aristotle.harmonic.fun\n"
                "Set the ARISTOTLE_API_KEY environment variable to avoid this step. See the docs at https://pypi.org/project/aristotlelib for detailed instructions\n\n"
                "Enter your API key below:"
            )
        else:
            # Break URL onto separate line for narrow terminals
            instructions = (
                "Get your free API key at:\n"
                "https://aristotle.harmonic.fun\n"
                "Set ARISTOTLE_API_KEY to avoid this.\n"
                "See docs at https://pypi.org/project/aristotlelib\n\n"
                "Enter your API key below:"
            )

        yield Static("🔑 API Key Required", classes="setup-header")
        yield Static(instructions, classes="setup-instructions")
        yield Input(
            placeholder="Enter your API key here", password=True, id="api-key-input"
        )

    def on_mount(self) -> None:
        """Focus the input when mounted."""
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle API key submission."""
        api_key = event.value.strip()
        if api_key:
            self.post_message(self.Submitted(api_key))
