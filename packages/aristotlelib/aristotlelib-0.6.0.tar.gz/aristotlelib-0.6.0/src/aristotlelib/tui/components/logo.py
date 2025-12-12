"""Logo/welcome banner component."""

from textual.widgets import Static
from textual.containers import Vertical
from textual.app import ComposeResult
from aristotlelib.cli.version import get_version


# Full ASCII logo for terminals >= 120 columns wide
FULL_ASCII_LOGO = """
                 ██████                             ███             █████                █████     ████            
       ███████████   ████                                             ███                  ███       ███           
     █████████████  ████       ██████    ████████   ████    █████   ███████     ██████   ███████     ███    ██████ 
    ██ ██          ██              ███    ███  ███   ███   ███        ███      ███  ███    ███       ███   ███  ███
   ██   ████   ████ ██         ███████    ███        ███    █████     ███      ███  ███    ███       ███   ███████ 
   ██  ███████████  ██        ███  ███    ███        ███       ███    ███ ███  ███  ███    ███ ███   ███   ███     
   ██ █████  ████   ██         ████████  █████      █████  ██████      █████    ██████      █████   █████   ██████ 
    ███         ██ ██                                                                                              
 ████  ███████████                                                                                                 
  ██████   ███                        Mathematical Superintelligence, by Harmonic • v{version}                     
"""

# Text banner for terminals 80-119 columns wide
TEXT_BANNER_LOGO = """
╔══════════════════════════════════════════════╗
║            ARISTOTLE SDK v{version_padded}            ║
║  Mathematical Superintelligence by Harmonic  ║
╚══════════════════════════════════════════════╝
"""


class LogoWidget(Vertical):
    """
    Display the Aristotle SDK welcome banner.
    Shows ASCII logo or text banner based on terminal width.
    Adapts to terminal resizes dynamically.
    """

    DEFAULT_CSS = """
    LogoWidget {
        height: auto;
        align: center middle;
    }
    LogoWidget Horizontal {
        height: auto;
        align: center middle;
        width: 100%;
    }
    LogoWidget .ascii-art {
        color: $accent;
        text-style: bold;
        text-align: center;
    }
    LogoWidget .tagline {
        text-align: center;
        color: $accent;
        text-style: bold;
        padding: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the logo widget with appropriate variant for terminal width."""
        logo_text = self._get_logo_for_width(self.app.size.width)
        yield Static(logo_text, classes="ascii-art", id="logo-display")

    def _get_logo_for_width(self, terminal_width: int) -> str:
        """Get appropriate logo variant based on terminal width."""
        version = get_version()

        if terminal_width >= 120:
            # Full ASCII logo
            return FULL_ASCII_LOGO.format(version=version)
        else:
            # Text banner (< 120 columns)
            # Pad version to fixed width for banner alignment
            version_padded = version.ljust(7)  # Pad to 7 chars (e.g., "1.0.0  ")
            return TEXT_BANNER_LOGO.format(version_padded=version_padded)

    def on_resize(self, event) -> None:
        """Handle terminal resize by updating logo variant."""
        # Get the new terminal width from the app
        new_width = self.app.size.width
        new_logo = self._get_logo_for_width(new_width)

        try:
            logo_display = self.query_one("#logo-display", Static)
            logo_display.update(new_logo)
        except Exception:
            pass
