"""Interactive history table for browsing and selecting projects."""

import os

from textual.widgets import DataTable, Static
from textual.message import Message
from textual.app import ComposeResult
from textual.containers import Vertical
from textual import events

from aristotlelib.project import Project, ProjectStatus
from aristotlelib.date_utils import format_relative_time


# Status icon mapping for project statuses
STATUS_ICONS = {
    ProjectStatus.COMPLETE: "✅",
    ProjectStatus.FAILED: "❌",
    ProjectStatus.IN_PROGRESS: "⏳",
    ProjectStatus.QUEUED: "🕐",
    ProjectStatus.NOT_STARTED: "⚪",
    ProjectStatus.PENDING_RETRY: "🔄"
}


class HistoryTableWidget(Vertical):
    """
    Interactive table for browsing project history.

    Features:
    - DataTable with scrolling and navigation
    - Keyboard shortcuts: arrows/vim keys (j/k) to navigate
    - Press Enter to select project
    - Press 'm' to load more (pagination)
    - Press Esc or 'b' to go back to menu
    """

    # Configuration constants
    TABLE_HEIGHT = 10  # Total height including header row
    HEADER_ROWS = 1    # Number of header rows
    PAGINATION_PAGE_SIZE = 10  # Number of items to load per page
    MIN_TERMINAL_HEIGHT_FOR_FOOTER = 16  # Minimum terminal height to show footer
    ROW_NUMBER_COLUMN_WIDTH = 7  # Width of the row number column (supports 3-digit row numbers + indicators)

    DEFAULT_CSS = """
    HistoryTableWidget {
        height: auto;
        padding: 0;
    }

    HistoryTableWidget DataTable {
        height: 10;
        scrollbar-gutter: stable;
    }

    HistoryTableWidget .footer-hint {
        padding: 1 0 0 0;
        color: $text-muted;
    }
    """

    class ProjectSelected(Message):
        """Emitted when user selects a project."""

        def __init__(self, project: Project):
            self.project = project
            super().__init__()

    class BackRequested(Message):
        """Emitted when user wants to go back to menu."""
        pass

    def __init__(
        self,
        projects: list[Project],
        pagination_key: str | None = None,
        status_filter: set[ProjectStatus] | None = None,
    ):
        super().__init__()
        self.projects = projects
        self.pagination_key = pagination_key
        self.status_filter = status_filter
        self.table: DataTable | None = None
        self._last_scroll_position = 0

    @property
    def visible_data_rows(self) -> int:
        """Calculate how many data rows are visible (excluding header)."""
        return self.TABLE_HEIGHT - self.HEADER_ROWS

    def compose(self) -> ComposeResult:
        """Create the table layout."""
        yield DataTable(cursor_type="row", zebra_stripes=True, show_cursor=True)

        # Footer with hints - only show if terminal is tall enough
        if self.app.size.height >= self.MIN_TERMINAL_HEIGHT_FOR_FOOTER:
            hint_text = "↑↓ or j/k: navigate | Enter: select | "
            if self.pagination_key:
                hint_text += "m: load more | "
            hint_text += "Esc/b: back to menu"

            yield Static(hint_text, classes="footer-hint", id="footer-hint")

    def _calculate_column_widths(self) -> dict[str, int]:
        """Calculate column widths based on terminal width."""
        terminal_width = self.app.size.width

        if terminal_width >= 120:
            # Full width layout
            return {
                "   #": self.ROW_NUMBER_COLUMN_WIDTH,
                "Project": 28,
                "Last Updated": 18,
                "Status": 16,
                "Created": 18
            }
        else:  # 80-119
            # Compact layout
            return {
                "   #": self.ROW_NUMBER_COLUMN_WIDTH,
                "Project": 20,
                "Last Updated": 14,
                "Status": 13,
                "Created": 14
            }

    def on_mount(self) -> None:
        """Setup table columns and rows."""
        self.table = self.query_one(DataTable)

        # Add columns with dynamic widths
        widths = self._calculate_column_widths()
        for col_name, width in widths.items():
            self.table.add_column(col_name, width=width)

        # Populate initial rows
        self._populate_rows()

        # Update scroll indicators and footer
        self.call_after_refresh(self._update_scroll_indicators)
        self.call_after_refresh(self._update_footer_with_position)

        # Focus the table for keyboard input
        self.table.focus()

        # Scroll the parent container to show this widget
        # Use call_after_refresh to ensure the widget is fully laid out first
        self.call_after_refresh(self._scroll_into_view)

    def _scroll_into_view(self) -> None:
        """Scroll the parent container to show this widget."""
        # Find the parent scroll container
        try:
            from textual.containers import VerticalScroll
            parent = self.parent
            while parent and not isinstance(parent, VerticalScroll):
                parent = parent.parent
            if parent:
                parent.scroll_end(animate=True)
        except Exception:
            # If we can't find the scroll container, just skip
            pass

    def _scroll_to_new_rows(self) -> None:
        """Scroll the table to show newly loaded rows."""
        if self.table and len(self.table.rows) > 0:
            # Move cursor to the first newly added row
            # This will automatically scroll the table to show that row
            try:
                # Calculate where the new rows start (total rows - page size)
                new_row_start = len(self.table.rows) - self.PAGINATION_PAGE_SIZE
                if new_row_start > 0:
                    # Move cursor to first new row
                    self.table.move_cursor(row=new_row_start)
            except Exception:
                # If that fails, just scroll to the end
                try:
                    self.table.move_cursor(row=len(self.table.rows) - 1)
                except Exception:
                    pass

    def _populate_rows(self) -> None:
        """Add project rows to table."""
        start_idx = len(self.table.rows)

        # Get the Project column width for truncation
        project_width = self._calculate_column_widths()["Project"]

        for idx, project in enumerate(self.projects[start_idx:], start=start_idx):
            # Format row number (1-based for display)
            row_num = str(idx + 1)

            # Format data - use file_name or description, fallback to project_id
            if project.file_name:
                # Extract just the filename from the path
                file_display = os.path.basename(project.file_name)
            elif project.description:
                file_display = project.description
            else:
                # Fallback to shortened project ID
                file_display = project.project_id[:12] + "..."

            # Truncate project name to fit column width
            if len(file_display) > project_width:
                # Truncate with ellipsis, leaving room for "..."
                file_display = file_display[:project_width - 3] + "..."

            updated_str = format_relative_time(project.last_updated_at)
            status_icon = STATUS_ICONS.get(project.status, "●")
            status_str = f"{status_icon} {project.status.value}"
            created_str = format_relative_time(project.created_at)

            # Add row with all columns (row number first)
            self.table.add_row(
                row_num,
                file_display,
                updated_str,
                status_str,
                created_str
            )

    def _get_visible_rows(self) -> tuple[int, int]:
        """Get the range of visible rows (start_idx, end_idx) in the table viewport."""
        if not self.table or len(self.table.rows) == 0:
            return (0, 0)

        total_rows = len(self.table.rows)
        visible_count = self.visible_data_rows

        # If all rows fit, no scrolling needed
        if total_rows <= visible_count:
            return (0, total_rows - 1)

        # Try to get the actual scroll position from the DataTable
        try:
            # Get scroll_y which tells us which row is at the top
            scroll_y = int(self.table.scroll_y)
            visible_start = scroll_y
            visible_end = min(scroll_y + visible_count - 1, total_rows - 1)
            return (visible_start, visible_end)
        except:
            pass

        # Fallback: use cursor position
        # Textual DataTable scrolls to keep cursor visible
        cursor_row = self.table.cursor_row

        # When cursor is near the top
        if cursor_row < visible_count:
            return (0, visible_count - 1)

        # When cursor is near the bottom
        if cursor_row >= total_rows - visible_count:
            return (total_rows - visible_count, total_rows - 1)

        # Middle: cursor is somewhere in the middle of visible area
        # Assume cursor is in the middle of the viewport
        half = visible_count // 2
        visible_start = max(0, cursor_row - half)
        visible_end = min(visible_start + visible_count - 1, total_rows - 1)

        return (visible_start, visible_end)

    def _update_scroll_indicators(self) -> None:
        """Update row number cells to show scroll indicators."""
        if not self.table or len(self.table.rows) == 0:
            return

        total_rows = len(self.table.rows)
        visible_start, visible_end = self._get_visible_rows()

        # Only update visible rows to improve performance
        # But update a slightly wider range to ensure indicators are cleared
        update_start = max(0, visible_start - 1)
        update_end = min(total_rows - 1, visible_end + 1)

        for row_idx in range(update_start, update_end + 1):
            row_num = row_idx + 1  # 1-based display

            # Determine if this row should have indicators
            show_up = (row_idx == visible_start and visible_start > 0)
            show_down = (row_idx == visible_end and visible_end < total_rows - 1)

            # Format the row number with indicators
            if show_up and show_down:
                row_text = f"▲▼ {row_num}"
            elif show_up:
                row_text = f"▲  {row_num}"
            elif show_down:
                row_text = f"▼  {row_num}"
            else:
                row_text = "   " + str(row_num)

            # Update the cell
            try:
                self.table.update_cell_at((row_idx, 0), row_text)
            except Exception:
                # Cell might not exist yet
                pass

    async def load_more(self) -> None:
        """Load next page of projects."""
        if not self.pagination_key:
            return

        try:
            # Fetch next page with server-side filtering
            if self.status_filter:
                # Convert set to list for API
                new_projects, self.pagination_key = await Project.list_projects(
                    pagination_key=self.pagination_key,
                    limit=self.PAGINATION_PAGE_SIZE,
                    status=list(self.status_filter),
                )
            else:
                new_projects, self.pagination_key = await Project.list_projects(
                    pagination_key=self.pagination_key,
                    limit=self.PAGINATION_PAGE_SIZE,
                    status=None,
                )

            if not new_projects:
                # No more projects
                self._update_footer_hint("No more projects to load.")
                return

            # Add to our list
            self.projects.extend(new_projects)

            # Add new rows to table
            self._populate_rows()

            # Scroll to the newly added rows
            # Use call_after_refresh to ensure rows are rendered first
            self.call_after_refresh(self._scroll_to_new_rows)

            # Update scroll indicators and footer hint
            self.call_after_refresh(self._update_scroll_indicators)
            self._update_footer_with_position()

        except Exception as e:
            self._update_footer_hint(f"Error loading more: {str(e)}")

    def _update_footer_hint(self, text: str) -> None:
        """Update the footer hint text."""
        try:
            footer = self.query_one(".footer-hint", Static)
            footer.update(text)
        except Exception:
            # Footer may not exist on short terminals
            pass

    def _update_footer_with_position(self) -> None:
        """Update footer hint with current position."""
        if not self.table or len(self.table.rows) == 0:
            self._update_footer_hint_with_pagination()
            return

        current_row = self.table.cursor_row + 1  # 1-based
        total_rows = len(self.table.rows)

        hint_text = f"Row {current_row}/{total_rows} | ↑↓ or j/k: navigate | Enter: select | "
        if self.pagination_key:
            hint_text += "m: load more | "
        hint_text += "Esc/b: back to menu"
        self._update_footer_hint(hint_text)

    def _update_footer_hint_with_pagination(self) -> None:
        """Update footer hint with pagination status."""
        hint_text = "↑↓ or j/k: navigate | Enter: select | "
        if self.pagination_key:
            hint_text += "m: load more | "
        hint_text += "Esc/b: back to menu"
        self._update_footer_hint(hint_text)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection from DataTable (triggered by Enter key)."""
        row_idx = event.cursor_row
        if row_idx < len(self.projects):
            self.post_message(self.ProjectSelected(self.projects[row_idx]))

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle cursor movement in the table."""
        # Update scroll indicators when cursor moves
        self._update_scroll_indicators()
        # Update footer with current position
        self._update_footer_with_position()

    def _on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts at higher priority."""
        # Vim-style navigation
        if event.key == "j":
            # Move down (delegate to table's down action)
            if self.table:
                self.table.action_cursor_down()
            event.prevent_default()
            event.stop()
            return

        if event.key == "k":
            # Move up (delegate to table's up action)
            if self.table:
                self.table.action_cursor_up()
            event.prevent_default()
            event.stop()
            return

        # Load more
        if event.key == "m" and self.pagination_key:
            self.run_worker(self.load_more())
            event.prevent_default()
            event.stop()
            return

        # Go back
        if event.key in ("escape", "b"):
            self.post_message(self.BackRequested())
            event.prevent_default()
            event.stop()
            return
