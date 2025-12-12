"""Reattach workflow for resuming monitoring of previously detached projects."""

import asyncio
from textual.widgets import Static

from aristotlelib.project import Project, ProjectStatus
from aristotlelib.tui.components.progress import ProgressWidget
from aristotlelib.tui.components.message import MessageWidget
from aristotlelib.tui.workflows.download import run_download_workflow



async def run_reattach_workflow(app, project: Project) -> None:
    """
    Reattach to a running project and monitor progress.
    Similar to unified_solve_workflow but skips project creation.
    Steps:
    1. Show reattaching message
    2. Refresh project to get latest status
    3. If still running: show ProgressWidget and monitor
    4. Support detach again via Escape
    5. On completion: download results
    6. Return to menu
    Args:
        app: The main TUI application instance
        project: The Project instance to reattach to
    """
    container = app.query_one(f"#{app.container_id}")

    # Show reattaching
    container.mount(Static(""))
    container.mount(Static("Reattaching to project..."))
    container.scroll_end(animate=True)

    try:
        # Refresh to get latest status
        await project.refresh()

        # Check if already finished
        if project.status in (ProjectStatus.COMPLETE, ProjectStatus.FAILED):
            # Already finished - go to download or show error
            container.mount(Static(""))
            container.mount(Static(f"Project already completed with status: {project.status.name}"))
            container.scroll_end(animate=True)

            if project.status == ProjectStatus.COMPLETE:
                await run_download_workflow(app, project)
            else:
                container.mount(Static(""))
                container.mount(MessageWidget(
                    "This project failed. The Aristotle team has been notified.\n"
                    "   Please try submitting a new proof request.",
                    "error"
                ))
                container.scroll_end(animate=True)
                container.mount(Static(""))
                app.show_menu()
            return

        # Still running - show progress
        container.mount(Static(f"Project ID: {project.project_id}"))
        container.mount(Static(""))
        container.scroll_end(animate=True)

        progress_widget = ProgressWidget(project_id=project.project_id)
        container.mount(progress_widget)
        container.scroll_end(animate=True)

        # Store widget reference in app for detach handling
        app._current_progress_widget = progress_widget
        app._current_monitor_task = asyncio.create_task(progress_widget.monitor_project(project))

        try:
            # Wait for monitoring to complete (or be cancelled by detach handler)
            await app._current_monitor_task
            detached = False
        except asyncio.CancelledError:
            # Detached by user
            detached = True
        finally:
            # Clean up references
            if hasattr(app, '_current_progress_widget'):
                delattr(app, '_current_progress_widget')
            if hasattr(app, '_current_monitor_task'):
                delattr(app, '_current_monitor_task')

        # Show result only if not detached
        if detached:
            # Show detached message
            container.mount(Static(""))
            container.mount(MessageWidget(
                f"Detached from project {project.project_id[:12]}...\n"
                f"   View in History (option 4) to check progress or download results.",
                "info"
            ))
            container.scroll_end(animate=True)
            container.mount(Static(""))
            app.show_menu()
        else:
            # Completed
            container.mount(Static(""))
            container.scroll_end(animate=True)

            if project.status == ProjectStatus.COMPLETE:
                await run_download_workflow(app, project)
            else:
                container.mount(MessageWidget(
                    "This project failed. The Aristotle team has been notified.\n"
                    "   Please try submitting a new proof request.",
                    "error"
                ))
                container.scroll_end(animate=True)
                container.mount(Static(""))
                app.show_menu()

    except Exception as e:
        container.mount(Static(""))
        container.mount(MessageWidget(f"Error reattaching: {str(e)}", "error"))
        container.scroll_end(animate=True)
        container.mount(Static(""))
        app.show_menu()
