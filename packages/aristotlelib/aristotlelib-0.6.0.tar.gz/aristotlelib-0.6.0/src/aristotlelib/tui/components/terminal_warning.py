"""Terminal size warning banner component."""

from textual.widgets import Static
from textual.containers import Vertical
from textual.app import ComposeResult

from aristotlelib.tui.terminal_size import TerminalSize, SizeConstants


class TerminalSizeWarning(Vertical):
    """
    Warning banner displayed when terminal is too small.
    Shows current dimensions and recommended size.
    Stays visible as a persistent banner bar at the top.
    """

    DEFAULT_CSS = """
    TerminalSizeWarning {
        height: auto;
        background: $warning;
        color: $text;
        padding: 1 2;
        dock: top;
    }

    TerminalSizeWarning .warning-text {
        text-align: center;
        text-style: bold;
    }
    """

    def __init__(self, terminal_size: TerminalSize, **kwargs):
        """
        Initialize the warning banner.

        Args:
            terminal_size: Current terminal size information
        """
        super().__init__(**kwargs)
        self.terminal_size = terminal_size

    def compose(self) -> ComposeResult:
        """Create the warning banner layout."""
        width = self.terminal_size.width
        height = self.terminal_size.height

        # Determine what's wrong
        width_ok = width >= SizeConstants.WIDTH_MINIMUM
        height_ok = height >= SizeConstants.HEIGHT_MINIMUM

        if not width_ok and not height_ok:
            issue = f"too small ({width}x{height})"
        elif not width_ok:
            issue = f"too narrow ({width} cols)"
        else:
            issue = f"too short ({height} rows)"

        warning_text = (
            f"⚠ Terminal {issue} • "
            f"Minimum: {SizeConstants.WIDTH_MINIMUM}x{SizeConstants.HEIGHT_MINIMUM} • "
            f"Recommended: {SizeConstants.WIDTH_RECOMMENDED}x{SizeConstants.HEIGHT_RECOMMENDED}+"
        )

        yield Static(warning_text, classes="warning-text")

    def update_size(self, terminal_size: TerminalSize) -> None:
        """Update the warning with new terminal size."""
        self.terminal_size = terminal_size

        # Remove existing warning text and recreate
        try:
            old_static = self.query_one(".warning-text", Static)
            old_static.remove()
        except Exception:
            pass

        width = terminal_size.width
        height = terminal_size.height

        width_ok = width >= SizeConstants.WIDTH_MINIMUM
        height_ok = height >= SizeConstants.HEIGHT_MINIMUM

        if not width_ok and not height_ok:
            issue = f"too small ({width}x{height})"
        elif not width_ok:
            issue = f"too narrow ({width} cols)"
        else:
            issue = f"too short ({height} rows)"

        warning_text = (
            f"⚠ Terminal {issue} • "
            f"Minimum: {SizeConstants.WIDTH_MINIMUM}x{SizeConstants.HEIGHT_MINIMUM} • "
            f"Recommended: {SizeConstants.WIDTH_RECOMMENDED}x{SizeConstants.HEIGHT_RECOMMENDED}+"
        )

        self.mount(Static(warning_text, classes="warning-text"))
