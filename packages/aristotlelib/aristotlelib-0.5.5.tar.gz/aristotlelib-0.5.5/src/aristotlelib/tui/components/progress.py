"""Progress display component."""

import asyncio
from datetime import datetime
from textual.widgets import Static
from textual.reactive import reactive
from textual.message import Message

from aristotlelib.project import ProjectStatus
from aristotlelib.date_utils import format_relative_time


# Progress bar configuration
POLL_INTERVAL_SECONDS = 15  # How often to poll project status


class ProgressWidget(Static):
    """
    Live-updating progress display for proof solving with detach capability.
    Shows project status, progress bar, percentage, and last updated time.
    Updates in-place using reactive properties.
    Users can press Escape to detach from monitoring and return to menu
    while the proof continues server-side.
    """

    DEFAULT_CSS = """
    ProgressWidget {
        padding: 1 0;
    }
    ProgressWidget:focus {
        border: solid $accent;
        background: $surface;
    }
    ProgressWidget .detach-hint {
        color: $text-muted;
        padding: 1 0 0 0;
    }
    """

    BINDINGS = [
        ("escape", "request_detach", "Detach"),
    ]

    class DetachRequested(Message):
        """Emitted when user requests to detach from monitoring."""
        pass

    # Reactive properties that trigger automatic re-rendering
    status = reactive(ProjectStatus.QUEUED)
    progress = reactive(0)
    last_updated_at = reactive(datetime.now())
    is_monitoring = reactive(True)
    project_id = reactive("")

    def __init__(self, project_id: str = "", **kwargs) -> None:
        """
        Initialize the progress widget.
        Args:
            project_id: The project ID to display
            **kwargs: Additional arguments passed to Static
        """
        super().__init__(**kwargs)
        self.project_id = project_id
        # Make widget focusable so it can receive keyboard events
        self.can_focus = True
        self._refresh_timer = None

    def on_mount(self) -> None:
        """Focus the widget when mounted so it receives keyboard events."""
        self.focus()
        # Set up a timer to refresh the display every second to update the relative time
        self._refresh_timer = self.set_interval(1.0, self.refresh)

        # Scroll parent container to show this widget after it's fully rendered
        # This is especially important when reattaching to screen sessions or when zoomed in
        self.call_after_refresh(self._scroll_into_view)

    def _scroll_into_view(self) -> None:
        """Scroll the parent container to show this widget."""
        try:
            from textual.containers import VerticalScroll
            parent = self.parent
            while parent and not isinstance(parent, VerticalScroll):
                parent = parent.parent
            if parent:
                parent.scroll_end(animate=False)
        except Exception:
            # If we can't find the scroll container, just skip
            pass

    def watch_status(self, old_value: ProjectStatus, new_value: ProjectStatus) -> None:
        """Maintain focus when status updates."""
        # Re-focus after reactive update to ensure we keep receiving key events
        if self.is_monitoring:
            self.call_after_refresh(self.focus)
            # Also scroll into view in case widget height changed
            self.call_after_refresh(self._scroll_into_view)

    def watch_progress(self, old_value: int, new_value: int) -> None:
        """Maintain focus when progress updates."""
        # Re-focus after reactive update to ensure we keep receiving key events
        if self.is_monitoring:
            self.call_after_refresh(self.focus)
            # Also scroll into view in case widget height changed
            self.call_after_refresh(self._scroll_into_view)

    def render(self) -> str:
        """Render the progress display with optional detach hint."""
        # Determine progress bar width based on terminal width
        terminal_width = self.app.size.width
        if terminal_width >= 100:
            bar_width = 20
        else:  # 80-99
            bar_width = 15

        # Progress bar
        filled = min(bar_width, max(0, int(self.progress / (100 / bar_width))))
        bar = "█" * filled + " " * (bar_width - filled)

        # Format last updated time
        time_str = format_relative_time(self.last_updated_at)

        status_line = f"Status: {self.status.value:<15} [{bar}] {self.progress}%  |  Updated {time_str}"

        # Determine if we should show hints (only on tall terminals)
        terminal_height = self.app.size.height
        show_hints = terminal_height >= 16

        # Show detach hint if monitoring and not complete
        if show_hints and self.is_monitoring and self.status not in (ProjectStatus.COMPLETE, ProjectStatus.FAILED):
            return status_line + "\n\n  Press \\[Esc] to detach and return to menu"
        elif show_hints and not self.is_monitoring:
            # Detached state
            return status_line + "\n\n  \\[Detached] View this project in History (option 4) to check progress"
        else:
            # Complete/Failed or compact mode - no detach option
            return status_line

    def action_request_detach(self) -> None:
        """Action called when Escape is pressed."""
        if self.is_monitoring and self.status not in (ProjectStatus.COMPLETE, ProjectStatus.FAILED):
            self.post_message(self.DetachRequested())

    async def monitor_project(self, project) -> None:
        """
        Monitor project progress and update display with detach support.
        Args:
            project: The Project instance to monitor
        This coroutine polls the project status every 15 seconds and updates
        the reactive properties, which automatically triggers re-rendering.
        Can be cancelled when user detaches (Escape key).
        """
        # Initial update
        self.status = project.status
        self.progress = project.percent_complete or 0
        self.last_updated_at = project.last_updated_at

        try:
            # Poll until complete, failed, or cancelled
            while project.status not in (ProjectStatus.COMPLETE, ProjectStatus.FAILED):
                await asyncio.sleep(POLL_INTERVAL_SECONDS)

                # Refresh project data
                await project.refresh()

                # Update reactive properties (triggers re-render)
                self.status = project.status
                self.progress = project.percent_complete or 0
                self.last_updated_at = project.last_updated_at

            # Final update
            self.status = project.status
            self.progress = project.percent_complete or 0
            self.last_updated_at = project.last_updated_at

        except asyncio.CancelledError:
            # User detached - mark as detached and stop refresh timer
            self.is_monitoring = False
            if self._refresh_timer:
                self._refresh_timer.stop()
            raise  # Re-raise so caller knows we were cancelled
