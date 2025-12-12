"""Download workflow for completed projects."""

from textual.widgets import Static

from aristotlelib.project import Project
from aristotlelib.tui.components.message import MessageWidget


async def run_download_workflow(app, project: Project) -> None:
    """
    Download completed project solution.
    Steps:
    1. Show download prompt
    2. Auto-download with default name (MVP approach)
    3. Show success message
    4. Return to menu
    Args:
        app: The main TUI application instance
        project: The completed Project instance
    """
    container = app.query_one(f"#{app.container_id}")

    container.mount(Static(""))
    container.mount(Static("Project complete! Downloading solution..."))
    container.mount(Static(""))
    container.scroll_end(animate=True)

    # Auto-download with default name
    try:
        output_path = await project.get_solution()

        container.mount(MessageWidget(
            f"✅ Solution downloaded!\n   Saved to: {output_path}",
            "success"
        ))
        container.scroll_end(animate=True)
    except Exception as e:
        container.mount(MessageWidget(
            f"❌ Error downloading solution: {str(e)}",
            "error"
        ))
        container.scroll_end(animate=True)

    container.mount(Static(""))
    app.show_menu()
