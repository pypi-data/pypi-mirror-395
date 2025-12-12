"""Main TUI application for Aristotle SDK."""

import asyncio
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static
from textual.theme import Theme
from textual.message import Message

from aristotlelib.project import Project, ProjectStatus
from aristotlelib.tui.components.logo import LogoWidget
from aristotlelib.tui.components.integrated_menu import IntegratedMenuWidget
from aristotlelib.tui.components.message import MessageWidget
from aristotlelib.tui.components.history_table import HistoryTableWidget
from aristotlelib.tui.components.progress import ProgressWidget
from aristotlelib.tui.components.api_key_setup import ApiKeySetupWidget
from aristotlelib.tui.components.terminal_warning import TerminalSizeWarning
from aristotlelib.tui.workflows.unified_solve import run_unified_solve_workflow
from aristotlelib.tui.workflows.history import run_history_workflow
from aristotlelib.tui.workflows.reattach import run_reattach_workflow
from aristotlelib.tui.workflows.download import run_download_workflow
from aristotlelib.tui.menu_options import MenuOption, MENU_OPTIONS
from aristotlelib.tui.terminal_size import TerminalSize
from aristotlelib import api_request


class TerminalResized(Message):
    """Message posted when terminal is resized."""
    def __init__(self, new_size: TerminalSize):
        self.new_size = new_size
        super().__init__()


class AristotleTUIApp(App):
    """
    Aristotle SDK Text User Interface.
    A scrolling, chat-like interface for interacting with the Aristotle
    automated theorem proving service.
    """

    CSS = """
    VerticalScroll {
        background: transparent;
        padding: 1 2;
    }
    """

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]

    def __init__(self, api_key: str | None = None):
        super().__init__()
        self.api_key = api_key
        self.container_id = "main-scroll"
        self._current_progress_widget = None
        self._current_monitor_task = None
        self._terminal_size: TerminalSize | None = None
        self._size_warning: TerminalSizeWarning | None = None
        self._last_resize_time = 0.0

    def compose(self) -> ComposeResult:
        """Create the main layout."""
        yield VerticalScroll(id=self.container_id)

    def on_mount(self) -> None:
        """Called when app starts."""
        # Register custom theme with Aristotle blue accent
        aristotle_theme = Theme(
            name="aristotle",
            primary="#0C337A",
            accent="#0C337A",
        )
        self.register_theme(aristotle_theme)
        self.theme = "aristotle"

        # Configure container
        container = self.query_one(f"#{self.container_id}", VerticalScroll)
        container.can_focus = False

        # Detect terminal size and show warning if needed
        self._update_terminal_size()
        self._update_size_warning()

        # Show logo
        self.show_logo()

        # Set API key if provided via CLI
        if self.api_key:
            api_request.set_api_key(self.api_key)

        # Validate API key if one exists, otherwise show setup
        self.run_worker(self._check_and_validate_api_key())

    def on_resize(self, event) -> None:
        """Handle terminal resize events with debouncing."""
        import time
        current_time = time.time()

        # Debounce: only update if 100ms have passed since last resize
        if current_time - self._last_resize_time < 0.1:
            return

        self._last_resize_time = current_time

        # Update terminal size
        old_size = self._terminal_size
        self._update_terminal_size()

        # Check if size actually changed (avoid spurious resize events)
        if old_size and old_size.width == self._terminal_size.width and old_size.height == self._terminal_size.height:
            return

        # Update or remove size warning
        self._update_size_warning()

        # Post resize message for components to handle
        self.post_message(TerminalResized(self._terminal_size))

        # Scroll to bottom after resize to ensure current content is visible
        # This is especially important when reattaching to screen sessions
        try:
            container = self.query_one(f"#{self.container_id}", VerticalScroll)
            container.call_after_refresh(lambda: container.scroll_end(animate=False))
        except Exception:
            # Container might not exist yet during initialization
            pass

    def _update_terminal_size(self) -> None:
        """Update the stored terminal size from current app dimensions."""
        self._terminal_size = TerminalSize.from_dimensions(
            width=self.size.width,
            height=self.size.height
        )

    def _update_size_warning(self) -> None:
        """Update or remove size warning based on current terminal size."""
        if self._terminal_size.is_too_small:
            # Terminal is too small
            if self._size_warning:
                # Update existing warning
                self._size_warning.update_size(self._terminal_size)
            else:
                # Show new warning
                self._size_warning = TerminalSizeWarning(self._terminal_size)
                self.mount(self._size_warning)
        else:
            # Terminal is adequate - remove warning if present
            if self._size_warning:
                self._size_warning.remove()
                self._size_warning = None

    async def _check_and_validate_api_key(self) -> None:
        """Check if API key exists and validate it, or show setup if missing/invalid."""
        container = self.query_one(f"#{self.container_id}", VerticalScroll)

        # Check if API key exists
        try:
            api_request.get_api_key()
        except ValueError:
            # No API key available - show setup
            self.show_api_key_setup()
            return

        # API key exists, validate it
        try:
            await Project.list_projects(limit=1)
            # If successful, show the menu
            self.show_menu()
        except Exception:
            # Invalid API key - show error and setup
            container.mount(MessageWidget(
                "Invalid API key. Please check your API key and try again.",
                "error"
            ))
            container.mount(Static(""))  # Blank line
            container.scroll_end(animate=True)
            self.show_api_key_setup()

    def show_api_key_setup(self) -> None:
        """Display the API key setup widget."""
        container = self.query_one(f"#{self.container_id}", VerticalScroll)
        setup_widget = ApiKeySetupWidget()
        container.mount(setup_widget)

    def on_api_key_setup_widget_submitted(self, message: ApiKeySetupWidget.Submitted) -> None:
        """Handle API key submission from setup widget."""
        # Set the API key (without logging it)
        api_request.set_api_key(message.api_key)
        self.api_key = message.api_key

        # Remove the setup widget
        container = self.query_one(f"#{self.container_id}", VerticalScroll)
        try:
            setup_widgets = self.query(ApiKeySetupWidget)
            for widget in setup_widgets:
                widget.remove()
        except Exception:
            pass

        # Show validating message and validate
        container.mount(Static("Validating API key..."))
        container.scroll_end(animate=True)
        self.run_worker(self._validate_submitted_api_key())

    async def _validate_submitted_api_key(self) -> None:
        """Validate the API key submitted by the user."""
        container = self.query_one(f"#{self.container_id}", VerticalScroll)

        try:
            # Make a simple request to list projects with limit 1 to test the API key
            await Project.list_projects(limit=1)

            # Remove validating message
            statics = container.query(Static)
            if statics:
                statics[-1].remove()  # Remove "Validating..." message

            # Show confirmation message (without the key)
            container.mount(Static("✓ API key set successfully"))
            container.mount(Static(""))  # Blank line
            container.scroll_end(animate=True)

            # Show the menu
            self.show_menu()

        except Exception:
            # Remove validating message
            statics = container.query(Static)
            if statics:
                statics[-1].remove()  # Remove "Validating..." message

            # Show error message
            container.mount(MessageWidget(
                "Invalid API key. Please check your API key and try again.",
                "error"
            ))
            container.mount(Static(""))  # Blank line
            container.scroll_end(animate=True)

            # Show the API key setup again
            self.show_api_key_setup()

    def show_logo(self) -> None:
        """Display the welcome banner (once at startup)."""
        container = self.query_one(f"#{self.container_id}", VerticalScroll)
        container.mount(LogoWidget())

    def show_menu(self) -> None:
        """Display the integrated menu after workflow content."""
        container = self.query_one(f"#{self.container_id}", VerticalScroll)
        menu = IntegratedMenuWidget()
        container.mount(menu)

    def on_integrated_menu_widget_submitted(self, message: IntegratedMenuWidget.Submitted) -> None:
        """Handle form submission from IntegratedMenuWidget."""
        container = self.query_one(f"#{self.container_id}", VerticalScroll)

        # Get the option label from the configuration
        config = MENU_OPTIONS.get(message.option)
        option_label = config.label if config else f"Option {message.option.value}"

        # Remove the menu widget
        try:
            menu_widgets = self.query(IntegratedMenuWidget)
            for menu_widget in menu_widgets:
                menu_widget.remove()
        except Exception:
            pass

        # Show what was submitted in compact form

        container.mount(Static(f"> {option_label}"))

        # Show preview of input
        if message.file_path:
            import os
            file_name = os.path.basename(message.file_path)
            container.mount(Static(f"  {file_name}"))
        else:
            # Show first line of prompt, truncated if needed
            first_line = message.prompt.split('\n')[0]
            if len(first_line) > 80:
                first_line = first_line[:77] + "..."
            container.mount(Static(f"  {first_line}"))

        container.scroll_end(animate=True)

        # Route to appropriate workflow based on option
        if message.option == MenuOption.VIEW_HISTORY:
            # History workflow
            self.run_worker(run_history_workflow(self, filter_type=message.history_filter))
        else:
            # Unified solving workflow (other options)
            self.run_worker(
                run_unified_solve_workflow(
                    self,
                    option=message.option,
                    prompt=message.prompt,
                    file_path=message.file_path,
                    context_file_path=message.context_file_path,
                    nl_context_file_path=message.nl_context_file_path,
                )
            )

    def on_history_table_widget_back_requested(self, message: HistoryTableWidget.BackRequested) -> None:
        """Handle back request from history table."""
        container = self.query_one(f"#{self.container_id}", VerticalScroll)

        # Remove the history table
        try:
            tables = self.query(HistoryTableWidget)
            for table in tables:
                table.remove()
        except Exception:
            pass

        # Return to menu
        container.mount(Static(""))  # Blank line
        self.show_menu()

    def on_history_table_widget_project_selected(self, message: HistoryTableWidget.ProjectSelected) -> None:
        """Handle project selection from history table."""
        container = self.query_one(f"#{self.container_id}", VerticalScroll)

        # Remove the history table
        try:
            tables = self.query(HistoryTableWidget)
            for table in tables:
                table.remove()
        except Exception:
            pass

        # Show selected project
        project = message.project
        container.mount(Static(""))  # Blank line
        container.mount(Static(f"Selected project: {project.project_id}"))

        # Scroll after a refresh to ensure content is rendered
        self.call_after_refresh(lambda: container.scroll_end(animate=True))

        # Route based on status
        if project.status == ProjectStatus.COMPLETE:
            # Download workflow
            self.run_worker(run_download_workflow(self, project))
        elif project.status == ProjectStatus.FAILED:
            # Show error
            container.mount(Static(""))  # Blank line
            container.mount(MessageWidget(
                "This project failed. The Aristotle team has been notified.\n"
                "   Please try submitting a new proof request.",
                "error"
            ))
            container.scroll_end(animate=True)
            container.mount(Static(""))  # Blank line
            self.show_menu()
        elif project.status in (ProjectStatus.IN_PROGRESS, ProjectStatus.QUEUED, ProjectStatus.PENDING_RETRY):
            # Reattach to monitoring
            self.run_worker(run_reattach_workflow(self, project))
        else:
            container.mount(Static(""))  # Blank line
            container.mount(MessageWidget(
                f"Project status: {project.status.name}. Cannot reattach.",
                "error"
            ))
            container.scroll_end(animate=True)
            container.mount(Static(""))  # Blank line
            self.show_menu()

    def on_progress_widget_detach_requested(self, message: ProgressWidget.DetachRequested) -> None:
        """Handle detach request from progress widget."""
        # Cancel the current monitoring task if it exists
        if self._current_monitor_task:
            self._current_monitor_task.cancel()



async def run_tui(api_key: str | None = None) -> int:
    """
    Launch the TUI application.
    Args:
        api_key: Optional API key for Aristotle service
    Returns:
        Exit code (0 for success)
    """
    app = AristotleTUIApp(api_key=api_key)
    await app.run_async(mouse=False)  # Disable mouse to prevent escape codes on disconnect
    return 0


def main():
    """Entry point for testing the TUI standalone."""
    asyncio.run(run_tui())


if __name__ == "__main__":
    main()
