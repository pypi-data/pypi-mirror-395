"""Terminal size detection and breakpoint management."""

from dataclasses import dataclass
from enum import Enum


class WidthBreakpoint(Enum):
    """Terminal width breakpoints."""
    FULL = "full"           # >= 120 cols
    COMPACT = "compact"     # 80-119 cols
    TOO_SMALL = "too_small" # < 80 cols


class HeightBreakpoint(Enum):
    """Terminal height breakpoints."""
    COMFORTABLE = "comfortable" # >= 24 rows
    COMPACT = "compact"         # 16-23 rows
    TOO_SHORT = "too_short"     # < 16 rows


@dataclass
class TerminalSize:
    """Terminal size information with breakpoints."""
    width: int
    height: int
    width_breakpoint: WidthBreakpoint
    height_breakpoint: HeightBreakpoint

    @property
    def is_adequate(self) -> bool:
        """Check if terminal meets minimum requirements (80x24)."""
        return self.width >= 80 and self.height >= 24

    @property
    def is_too_small(self) -> bool:
        """Check if terminal is below minimum requirements."""
        return not self.is_adequate

    @staticmethod
    def from_dimensions(width: int, height: int) -> "TerminalSize":
        """Create TerminalSize from width and height dimensions."""
        # Determine width breakpoint
        if width >= 120:
            width_bp = WidthBreakpoint.FULL
        elif width >= 80:
            width_bp = WidthBreakpoint.COMPACT
        else:
            width_bp = WidthBreakpoint.TOO_SMALL

        # Determine height breakpoint
        if height >= 24:
            height_bp = HeightBreakpoint.COMFORTABLE
        elif height >= 16:
            height_bp = HeightBreakpoint.COMPACT
        else:
            height_bp = HeightBreakpoint.TOO_SHORT

        return TerminalSize(
            width=width,
            height=height,
            width_breakpoint=width_bp,
            height_breakpoint=height_bp
        )


# Size constants
class SizeConstants:
    """Constants for terminal size requirements."""
    # Width breakpoints
    WIDTH_FULL = 120
    WIDTH_COMPACT = 80
    WIDTH_MINIMUM = 80
    WIDTH_RECOMMENDED = 100

    # Height breakpoints
    HEIGHT_COMFORTABLE = 24
    HEIGHT_COMPACT = 16
    HEIGHT_MINIMUM = 24
    HEIGHT_RECOMMENDED = 24
