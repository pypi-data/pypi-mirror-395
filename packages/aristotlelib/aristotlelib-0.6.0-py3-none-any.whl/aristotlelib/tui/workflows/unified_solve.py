"""Unified solving workflow for all menu options."""

import asyncio
import os
from pathlib import Path
from textual.widgets import Static

from aristotlelib.project import Project, ProjectStatus
from aristotlelib.tui.components.progress import ProgressWidget
from aristotlelib.tui.components.message import MessageWidget
from aristotlelib.tui.menu_options import MenuOption, MENU_OPTIONS


async def run_unified_solve_workflow(
    app,
    option: MenuOption,
    prompt: str,
    file_path: str | None,
    context_file_path: str | None = None,
    nl_context_file_path: str | None = None,
) -> None:
    """
    Run the unified solving workflow for all solving options.
    Steps:
    1. Show what was submitted
    2. Determine input type and parameters based on option
    3. Use Project.prove_from_file to create project and start solving (with auto import handling)
    4. Show ProgressWidget with live updates
    5. On completion, download solution and show success
    6. Return to menu
    Args:
        app: The main TUI application instance
        option: MenuOption enum value (FILL_SORRIES, AUTOFORMALIZE_PAPER, or FREESTYLE)
        prompt: The prompt text from the user
        file_path: Optional file path (required for file-based options)
        context_file_path: Optional Lean file path for formal context
        nl_context_file_path: Optional path to natural language context (file or folder)
    """
    container = app.query_one(f"#{app.container_id}")

    # Get configuration for this option
    config = MENU_OPTIONS.get(option)
    if not config:
        container.mount(MessageWidget(f"Invalid option: {option}", "error"))
        return

    input_type = config.input_type
    auto_add_imports = config.auto_add_imports
    validate_lean_project = config.validate_lean_project

    # Process NL context file/folder path
    context_file_paths = None
    context_is_folder = False
    if nl_context_file_path:
        # Check if it's a folder or file
        if os.path.isdir(nl_context_file_path):
            # Folder mode
            context_file_paths = [nl_context_file_path]
            context_is_folder = True
        else:
            # Single file mode
            context_file_paths = [nl_context_file_path]

    # Show starting message with clean terminal formatting
    container.mount(Static(""))  # Blank line
    container.mount(Static("Aristotle is at work..."))
    container.scroll_end(animate=True)

    try:
        # Create project
        if config.requires_file:
            # File-based options
            assert file_path is not None, "File path required for this option"

        # Use prove_from_file to handle project creation, import gathering, and solving
        # This replaces the manual Project.create() -> add_context() -> solve() flow
        if config.requires_file:
            # File-based options: use prove_from_file with auto_add_imports
            # If context_file_path is provided for options that support it, pass as formal_input_context
            project_id = await Project.prove_from_file(
                input_file_path=file_path,
                auto_add_imports=auto_add_imports,
                validate_lean_project=validate_lean_project,
                wait_for_completion=False,
                project_input_type=input_type,
                formal_input_context=context_file_path if config.supports_optional_lean_context else None,
                context_file_paths=context_file_paths,
                context_is_folder=context_is_folder,
            )
        else:
            # Freestyle: use prove_from_file with input_content
            # If context_file_path is provided, enable auto_add_imports and validate_lean_project
            use_auto_imports = bool(context_file_path)
            use_validate_project = bool(context_file_path)

            project_id = await Project.prove_from_file(
                input_content=prompt,
                auto_add_imports=use_auto_imports,
                validate_lean_project=use_validate_project,
                wait_for_completion=False,
                project_input_type=input_type,
                formal_input_context=context_file_path,
                context_file_paths=context_file_paths,
                context_is_folder=context_is_folder,
            )

        # Get the project object for monitoring
        project = await Project.from_id(project_id)

        container.mount(Static(f"[dim]Project ID: {project.project_id}[/dim]"))
        container.mount(Static(""))  # Blank line
        container.scroll_end(animate=True)

        # Show progress and monitor with detach support
        progress_widget = ProgressWidget(project_id=project.project_id)
        container.mount(progress_widget)
        container.scroll_end(animate=True)

        # Store widget reference in app for detach handling
        app._current_progress_widget = progress_widget
        app._current_monitor_task = asyncio.create_task(
            progress_widget.monitor_project(project)
        )

        try:
            # Wait for monitoring to complete (or be cancelled by detach handler)
            await app._current_monitor_task
            detached = False
        except asyncio.CancelledError:
            # Detached by user
            detached = True
        finally:
            # Clean up references
            app._current_progress_widget = None
            app.current_monitor_task = None

        # Show result only if not detached
        if detached:
            # Show detached message
            container.mount(Static(""))  # Blank line
            container.mount(Static("[bold yellow]DETACHED[/bold yellow]"))
            container.mount(Static(""))
            container.mount(Static(f"Project ID: [dim]{project.project_id}[/dim]"))
            container.mount(Static("Proof is running in the background."))
            container.mount(Static(""))
            container.mount(
                Static(
                    "Use option 4 (View history) to check progress or download results."
                )
            )
            container.scroll_end(animate=True)
        else:
            # Show completion result
            if project.status == ProjectStatus.COMPLETE:
                # Download solution
                if config.requires_file and file_path:
                    # Auto-generate output path for file-based options
                    output_path = _generate_output_path(file_path)
                    await project.get_solution(output_path)

                    container.mount(Static("[bold green]COMPLETE[/bold green]"))
                    container.mount(Static(""))
                    container.mount(Static(f"Saved to: [cyan]{output_path}[/cyan]"))
                    container.scroll_end(animate=True)
                else:
                    # Freestyle - download with default name
                    output_path = await project.get_solution()

                    container.mount(Static("[bold green]COMPLETE[/bold green]"))
                    container.mount(Static(""))
                    container.mount(Static(f"Saved to: [cyan]{output_path}[/cyan]"))
                    container.scroll_end(animate=True)
            else:
                container.mount(Static("[bold red]FAILED[/bold red]"))
                container.mount(Static(""))
                container.mount(Static(f"Project ID: [dim]{project.project_id}[/dim]"))
                container.mount(Static("View in History for details."))
                container.scroll_end(animate=True)

    except Exception as e:
        # Show error with clean formatting
        container.mount(Static(""))  # Blank line
        container.mount(Static("[bold #FFA500]ERROR[/bold #FFA500]"))
        container.mount(Static(""))
        container.mount(Static(f"[#FFA500]{str(e)}[/#FFA500]"))
        container.scroll_end(animate=True)

    # Return to menu
    container.mount(Static(""))  # Blank line
    app.show_menu()


def _generate_output_path(input_path: str) -> str:
    """
    Generate output path based on input path.
    Format: {input_stem}_aristotle{input_extension}
    Example: my/file.lean -> my/file_aristotle.lean
             my/paper.tex -> my/paper_aristotle.lean
    Args:
        input_path: The input file path
    Returns:
        Generated output path in the same directory
    """
    input_file = Path(input_path)
    parent_dir = input_file.parent
    stem = input_file.stem  # Filename without extension
    # Always use .lean extension for output (since we're generating Lean proofs)
    output_filename = f"{stem}_aristotle.lean"
    return str(parent_dir / output_filename)
