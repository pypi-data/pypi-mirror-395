"""Message display component."""

from textual.widgets import Static


class MessageWidget(Static):
    """
    Display status messages with appropriate styling.
    Supports three message types:
    - success: Green with ✅ icon
    - error: Red with ❌ icon
    - info: Muted with ℹ️  icon
    """

    DEFAULT_CSS = """
    MessageWidget {
        padding: 1 0;
    }
    MessageWidget.success {
        color: $success;
    }
    MessageWidget.error {
        color: $error;
    }
    MessageWidget.info {
        color: $text-muted;
    }
    """

    def __init__(self, message: str, message_type: str = "info", **kwargs) -> None:
        """
        Initialize the message widget.
        Args:
            message: The message text to display
            message_type: Type of message ('success', 'error', or 'info')
            **kwargs: Additional arguments passed to Static
        """
        super().__init__(**kwargs)
        self.message_text = message
        self.message_type = message_type

    def on_mount(self) -> None:
        """Apply the appropriate CSS class when mounted."""
        self.add_class(self.message_type)

    def render(self) -> str:
        """Render the message with appropriate icon."""
        icons = {
            "success": "✅",
            "error": "❌",
            "info": ">"
        }
        icon = icons.get(self.message_type, ">")
        return f"{icon} {self.message_text}"
