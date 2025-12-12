"""History workflow for viewing past proof attempts."""

from textual.widgets import Static

from aristotlelib.project import Project, ProjectStatus
from aristotlelib.tui.components.message import MessageWidget
from aristotlelib.tui.components.history_table import HistoryTableWidget


# History display configuration
INITIAL_PROJECTS_TO_SHOW = 10  # Initial number of recent projects to display


async def run_history_workflow(app, filter_type: set[ProjectStatus] | None = None) -> None:
    """
    Run the enhanced history workflow with interactive table.
    Steps:
    1. Fetch initial projects (10 at a time)
    2. Mount HistoryTableWidget with navigation and pagination
    3. User navigates and selects project (handled by table events)
    4. On selection: Will be handled in Phase 3 (reattach workflow)
    5. On back/escape: return to menu
    Args:
        app: The main TUI application instance
        filter_type: Optional status filter (set of ProjectStatus) or None for all
    """
    container = app.query_one(f"#{app.container_id}")

    # Show loading message
    container.mount(Static(""))  # Blank line
    if filter_type:
        loading_msg = "Loading active proof attempts..."
    else:
        loading_msg = "Loading all proof attempts..."
    container.mount(Static(loading_msg))
    container.scroll_end(animate=True)

    try:
        # Fetch recent projects with server-side filtering
        if filter_type:
            # Convert set to list for API
            projects, pagination_key = await Project.list_projects(
                limit=INITIAL_PROJECTS_TO_SHOW, status=list(filter_type)
            )
        else:
            projects, pagination_key = await Project.list_projects(
                limit=INITIAL_PROJECTS_TO_SHOW, status=None
            )

        # Remove loading message
        statics = container.query(Static)
        if len(statics) >= 2:
            statics[-1].remove()  # Remove "Loading..." message
            statics[-2].remove()  # Remove blank line

        if not projects:
            container.mount(MessageWidget("No proof attempts found.", "info"))
            container.scroll_end(animate=True)
            container.mount(Static(""))  # Blank line
            app.show_menu()
            return

        # Mount interactive table
        container.mount(Static(""))  # Blank line
        container.mount(Static("Recent proof attempts:"))
        container.mount(Static(""))  # Blank line

        table_widget = HistoryTableWidget(projects, pagination_key, filter_type)
        container.mount(table_widget)
        container.scroll_end(animate=True)

        # Table will post ProjectSelected or BackRequested messages
        # App will handle these messages via event handlers

    except Exception as e:
        # Show error
        container.mount(Static(""))  # Blank line
        container.mount(MessageWidget(f"Error loading history: {str(e)}", "error"))
        container.scroll_end(animate=True)
        container.mount(Static(""))  # Blank line
        app.show_menu()
