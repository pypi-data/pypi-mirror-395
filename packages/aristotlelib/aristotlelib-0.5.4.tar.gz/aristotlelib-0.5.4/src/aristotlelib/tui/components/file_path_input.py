"""Enhanced file path input widget with tab completion and validation."""

import os
from textual.widgets import Input, Static
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive
from textual import events

# Constants
MAX_ITEM_LENGTH = 40


class FilePathInput(Vertical):
    """
    File path input widget with real-time validation and tab completion.

    Features:
    - Real-time validation with visual feedback
    - Tab completion for paths
    - Directory/file suggestions
    - Extension validation
    - Color-coded borders (green=valid, red=invalid, blue=neutral)
    - Always editable input
    """

    DEFAULT_CSS = """
    FilePathInput {
        height: auto;
        width: 100%;
    }

    FilePathInput Input {
        border: solid $accent;
        margin-bottom: 0;
    }

    FilePathInput Input.valid-input {
        border: solid green;
    }

    FilePathInput Input.invalid-input {
        border: solid red;
    }

    FilePathInput .error-message {
        color: red;
        padding: 0 1;
        height: auto;
    }

    FilePathInput .success-message {
        color: green;
        padding: 0 1;
        height: auto;
    }

    FilePathInput .suggestions {
        color: $text-muted;
        height: 0;
        display: none;
        background: $surface;
    }

    FilePathInput .suggestions.has-content {
        padding: 0 1;
        height: auto;
        display: block;
    }
    """

    # Reactive properties
    current_value = reactive("")
    is_valid = reactive(False)
    validation_message = reactive("")
    suggestions_text = reactive("")

    class Validated(Message):
        """Message emitted when input becomes valid."""

        def __init__(self, file_path: str):
            self.file_path = file_path
            super().__init__()

    def __init__(self, allowed_extensions: list[str], placeholder: str = "", auto_focus: bool = True, allow_folders: bool = False, **kwargs):
        """
        Initialize the file path input.

        Args:
            allowed_extensions: List of allowed file extensions (e.g., [".lean", ".txt"])
            placeholder: Placeholder text for the input (defaults to current working directory)
            auto_focus: Whether to automatically focus the input when mounted (default: True)
            allow_folders: Whether to allow folder paths (default: False)
        """
        super().__init__(**kwargs)
        self.allowed_extensions = allowed_extensions
        self.auto_focus = auto_focus
        self.allow_folders = allow_folders
        # Use current working directory as placeholder if not specified
        if not placeholder:
            placeholder = os.getcwd()
        self.placeholder = placeholder
        self._suggestions = []  # Current list of suggestions
        self._suggestion_index = -1  # Current index in suggestions for cycling (-1 = not cycling)
        self._is_cycling = False  # Flag to prevent reset during programmatic updates
        self._preserved_suggestions = []  # Preserved suggestions during cycling
        self._in_tab_operation = False  # Flag to indicate we're in a tab completion operation
        self._preserved_dir_path = ""  # Directory path when cycling started
        self._preserved_prefix = ""  # Prefix when cycling started

    def compose(self):
        """Create the widget layout."""
        yield Input(placeholder=self.placeholder, id="path-input")
        yield Static("", id="feedback-message", classes="error-message")
        yield Static("", id="suggestions-display", classes="suggestions")

    def on_mount(self) -> None:
        """Set up the widget after mounting."""
        # Focus the input if auto_focus is enabled
        if self.auto_focus:
            self.query_one("#path-input", Input).focus()

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

    def on_terminal_resized(self, message) -> None:
        """Handle terminal resize by refreshing suggestions display."""
        # Import here to avoid circular dependency
        from aristotlelib.tui.app import TerminalResized

        if isinstance(message, TerminalResized):
            # Refresh suggestions display with new width
            if self._suggestions or self._preserved_suggestions:
                self._refresh_suggestions_display()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input value changes."""
        if event.input.id != "path-input":
            return

        self.current_value = event.value

        # Only reset cycling if this is a user-initiated change
        # If we're in a tab operation, preserve everything but clear the flag after processing
        if not self._in_tab_operation:
            self._suggestion_index = -1
            self._preserved_suggestions = []  # Clear preserved suggestions on user typing
            self._preserved_dir_path = ""
            self._preserved_prefix = ""

        self._validate_and_update()

        # Only update suggestions if not in a tab operation
        if not self._in_tab_operation:
            self._update_suggestions()
        else:
            # Clear the flag now that we've processed the tab-initiated change
            self._in_tab_operation = False

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard events."""
        if event.key == "tab":
            # Handle tab completion (forward)
            self._handle_tab_completion(direction="forward")
            event.prevent_default()
            event.stop()
        elif event.key == "shift+tab":
            # Handle reverse tab completion (backward)
            self._handle_tab_completion(direction="backward")
            event.prevent_default()
            event.stop()
        elif event.key == "enter":
            # If we're cycling through suggestions, select the highlighted one
            if self._suggestion_index >= 0 and self._preserved_suggestions:
                self._select_current_suggestion()
                event.prevent_default()
                event.stop()
            # Otherwise, let the parent handle Enter (for form submission)
        elif event.key == "escape":
            # Let escape bubble up to parent (for navigation mode transition)
            # Don't consume it for clearing suggestions - that's not terminal-like behavior
            pass

    def _validate_and_update(self) -> None:
        """Validate current input and update UI."""
        input_widget = self.query_one("#path-input", Input)
        feedback = self.query_one("#feedback-message", Static)

        value = self.current_value.strip()

        # Empty input - neutral state
        if not value:
            self.is_valid = False
            self.validation_message = ""
            input_widget.remove_class("valid-input", "invalid-input")
            feedback.update("")
            feedback.remove_class("success-message")
            feedback.add_class("error-message")
            return

        # Expand path
        expanded = os.path.expanduser(value)
        if not os.path.isabs(expanded):
            expanded = os.path.abspath(expanded)

        # Check if path exists first
        if not os.path.exists(expanded):
            # Check if the input looks like a complete file path (has an extension)
            # If it's just a partial path (like "test_files/e" or "test_files/"), stay neutral
            basename = os.path.basename(value)
            has_extension = '.' in basename and not basename.startswith('.')

            # If typing a directory path or partial name without extension, stay neutral
            if not has_extension:
                self.is_valid = False
                self.validation_message = ""
                input_widget.remove_class("valid-input", "invalid-input")
                feedback.update("")
                feedback.remove_class("success-message", "error-message")
                return

            # Path doesn't exist and looks like a complete file path
            self.is_valid = False
            self.validation_message = "✗ File not found"
            input_widget.remove_class("valid-input")
            input_widget.add_class("invalid-input")
            feedback.update(self.validation_message)
            feedback.remove_class("success-message")
            feedback.add_class("error-message")
            return

        # Path exists - check if it's a folder
        if os.path.isdir(expanded):
            if self.allow_folders:
                # Folder is valid when allow_folders is True
                self.is_valid = True
                self.validation_message = ""
                input_widget.remove_class("invalid-input")
                input_widget.add_class("valid-input")
                feedback.update("✓ Folder")
                feedback.remove_class("error-message")
                feedback.add_class("success-message")
                self.post_message(self.Validated(expanded))
                return
            else:
                # Folder not allowed
                self.is_valid = False
                self.validation_message = "✗ Expected a file, got directory"
                input_widget.remove_class("valid-input")
                input_widget.add_class("invalid-input")
                feedback.update(self.validation_message)
                feedback.remove_class("success-message")
                feedback.add_class("error-message")
                return

        # It's a file - check extension
        ext = os.path.splitext(expanded)[1].lower()
        if ext not in self.allowed_extensions:
            extensions_str = ", ".join(self.allowed_extensions)
            self.is_valid = False
            self.validation_message = f"✗ Invalid extension (expected: {extensions_str})"
            input_widget.remove_class("valid-input")
            input_widget.add_class("invalid-input")
            feedback.update(self.validation_message)
            feedback.remove_class("success-message")
            feedback.add_class("error-message")
            return

        # Valid file!
        self.is_valid = True
        self.validation_message = ""
        input_widget.remove_class("invalid-input")
        input_widget.add_class("valid-input")
        feedback.update("")
        feedback.remove_class("error-message", "success-message")

        # Emit validated message
        self.post_message(self.Validated(expanded))

    def _update_suggestions(self) -> None:
        """Update path suggestions based on current input."""
        suggestions_display = self.query_one("#suggestions-display", Static)

        value = self.current_value.strip()

        # Don't show suggestions if input is empty
        if not value:
            suggestions_display.update("")
            suggestions_display.remove_class("has-content")
            self._suggestions = []
            return

        # Expand path
        expanded = os.path.expanduser(value)

        # Don't show suggestions if we have a valid file (but DO show if it's a valid folder)
        if self.is_valid and not (os.path.exists(expanded) and os.path.isdir(expanded)):
            suggestions_display.update("")
            suggestions_display.remove_class("has-content")
            self._suggestions = []
            return

        # Parse into directory and filename parts
        if expanded.endswith(os.sep):
            # User typed a trailing slash - show directory contents
            dir_path = expanded
            prefix = ""
        else:
            # Split into directory and filename prefix
            dir_path = os.path.dirname(expanded)
            prefix = os.path.basename(expanded)

        # Default to current directory if no directory specified
        if not dir_path:
            dir_path = "."

        # Get suggestions
        suggestions = self._get_path_suggestions(dir_path, prefix)
        self._suggestions = suggestions

        # Only show suggestions if there are actual results
        if suggestions and len(suggestions) > 0:
            # Format suggestions as a clean list with multiple columns
            # Pass the current cycling index if we're cycling
            highlight_index = self._suggestion_index if self._suggestion_index >= 0 else -1
            formatted = self._format_suggestions(suggestions, highlight_index=highlight_index)
            suggestions_display.update(formatted)
            suggestions_display.add_class("has-content")
        else:
            # Clear suggestions display when there are no matches
            suggestions_display.update("")
            suggestions_display.remove_class("has-content")
            self._suggestions = []

    def _get_available_width(self) -> int:
        """Calculate available width for suggestions display."""
        # Try to get parent container width
        try:
            container = self.parent
            if hasattr(container, 'size') and container.size.width > 0:
                return max(40, container.size.width - 4)  # Padding
        except Exception:
            pass

        # Fall back to terminal width
        terminal_width = self.app.size.width
        if terminal_width >= 120:
            return 116
        else:  # 80-119
            return max(40, terminal_width - 10)

    def _format_suggestions(self, suggestions: list[str], max_display: int = 20, highlight_index: int = -1) -> str:
        """
        Format suggestions as a clean multi-column list.

        Args:
            suggestions: List of suggestion strings
            max_display: Maximum number of items to display
            highlight_index: Index of the item to highlight (or -1 for no highlight)

        Returns:
            Formatted string for display
        """
        if not suggestions:
            return ""

        # Limit display
        display_items = suggestions[:max_display]
        has_more = len(suggestions) > max_display

        # Truncate long items with ellipsis in middle, preserving extension
        truncated_items = []
        for item in display_items:
            if len(item) > MAX_ITEM_LENGTH:
                # Check if it's a directory (ends with /)
                if item.endswith('/'):
                    # Directory - truncate before the /
                    name = item[:-1]
                    if len(name) > MAX_ITEM_LENGTH - 1:
                        # Keep first part and last part with ellipsis
                        keep_start = (MAX_ITEM_LENGTH - 4) // 2  # -4 for "..." and "/"
                        keep_end = MAX_ITEM_LENGTH - 4 - keep_start
                        truncated_items.append(f"{name[:keep_start]}...{name[-keep_end:]}/")
                    else:
                        truncated_items.append(item)
                else:
                    # File - preserve extension
                    name, ext = os.path.splitext(item)
                    target_name_len = MAX_ITEM_LENGTH - len(ext)
                    if len(name) > target_name_len:
                        # Keep first part and last part of name with ellipsis
                        keep_start = (target_name_len - 3) // 2  # -3 for "..."
                        keep_end = target_name_len - 3 - keep_start
                        truncated_items.append(f"{name[:keep_start]}...{name[-keep_end:]}{ext}")
                    else:
                        truncated_items.append(item)
            else:
                truncated_items.append(item)

        # Calculate column width (find longest item after truncation, cap at MAX_ITEM_LENGTH chars)
        max_len = min(max(len(item) for item in truncated_items), MAX_ITEM_LENGTH)
        col_width = max_len + 2  # Add padding

        # Calculate number of columns based on available width
        available_width = self._get_available_width()

        # For narrow terminals (< 80), force single column
        if self.app.size.width < 80:
            num_cols = 1
        else:
            num_cols = max(1, available_width // col_width)

        # Build rows
        lines = ["Suggestions:"]
        for i in range(0, len(truncated_items), num_cols):
            row_items = truncated_items[i:i + num_cols]
            # Format each item to fixed width, with highlighting if needed
            formatted_items = []
            for j, item in enumerate(row_items):
                item_index = i + j
                if item_index == highlight_index:
                    # Highlight with reverse video or bold
                    formatted_items.append(f"[reverse]{item}[/reverse]".ljust(col_width + 18))  # +18 for markup
                else:
                    formatted_items.append(item.ljust(col_width))
            lines.append("  " + "".join(formatted_items).rstrip())

        # Add "more" indicator
        if has_more:
            lines.append(f"  ... and {len(suggestions) - max_display} more")

        return "\n".join(lines)

    def _get_path_suggestions(self, dir_path: str, prefix: str) -> list[str]:
        """
        Get path suggestions for a directory and prefix.

        Args:
            dir_path: Directory to search in
            prefix: Filename prefix to match

        Returns:
            List of matching file/directory names
        """
        try:
            if not os.path.exists(dir_path):
                return []

            if not os.path.isdir(dir_path):
                return []

            # List directory contents
            items = os.listdir(dir_path)

            # Filter out hidden files and folders (starting with .)
            items = [item for item in items if not item.startswith('.')]

            # Filter by prefix (case-insensitive)
            if prefix:
                items = [item for item in items if item.lower().startswith(prefix.lower())]

            # Separate into files and directories
            suggestions = []
            for item in items:
                full_path = os.path.join(dir_path, item)

                if os.path.isdir(full_path):
                    # Only include directories that contain valid files somewhere in their subtree
                    if self._directory_contains_valid_files(full_path):
                        suggestions.append(item + "/")
                else:
                    # Only include files with valid extensions at THIS level
                    ext = os.path.splitext(item)[1].lower()
                    if ext in self.allowed_extensions:
                        suggestions.append(item)

            # Sort: directories first, then files
            dirs = [s for s in suggestions if s.endswith("/")]
            files = [s for s in suggestions if not s.endswith("/")]

            return sorted(dirs) + sorted(files)

        except PermissionError:
            # Can't read directory
            return []
        except Exception:
            # Other errors - just return empty
            return []

    def _directory_contains_valid_files(self, dir_path: str, max_depth: int = 3) -> bool:
        """
        Check if a directory contains files with valid extensions (recursively).

        Args:
            dir_path: Directory to check
            max_depth: Maximum recursion depth to avoid performance issues

        Returns:
            True if directory contains valid files, False otherwise
        """
        if max_depth <= 0:
            return False

        try:
            for item in os.listdir(dir_path):
                full_path = os.path.join(dir_path, item)

                # Skip hidden files/directories
                if item.startswith('.'):
                    continue

                if os.path.isfile(full_path):
                    # Check if file has valid extension
                    ext = os.path.splitext(item)[1].lower()
                    if ext in self.allowed_extensions:
                        return True
                elif os.path.isdir(full_path):
                    # Recursively check subdirectory
                    if self._directory_contains_valid_files(full_path, max_depth - 1):
                        return True

            return False

        except PermissionError:
            # Can't read directory - assume it might contain valid files
            return True
        except Exception:
            return False

    def _handle_tab_completion(self, direction: str = "forward") -> None:
        """Handle Tab key press for path completion.

        Args:
            direction: "forward" for Tab, "backward" for Shift+Tab
        """
        # Set flag to prevent on_input_changed from clearing state
        self._in_tab_operation = True

        input_widget = self.query_one("#path-input", Input)
        value = self.current_value.strip()

        # Special case: If input is empty, populate with pwd and show suggestions
        if not value:
            pwd = os.getcwd()
            # Add trailing slash to show directory contents
            new_path = pwd + os.sep
            input_widget.value = new_path
            input_widget.cursor_position = len(new_path)
            self.current_value = new_path
            self._in_tab_operation = False
            # Update suggestions will be called via on_input_changed
            return

        # Determine which suggestion list to use
        if self._suggestion_index >= 0 and self._preserved_suggestions:
            # We're cycling - use preserved suggestions
            active_suggestions = self._preserved_suggestions
        else:
            # Not cycling - use current suggestions
            if not self._suggestions:
                # No suggestions - try to update them first
                self._update_suggestions()
                if not self._suggestions:
                    self._in_tab_operation = False  # Clear flag before returning
                    return
            active_suggestions = self._suggestions

        # Expand path
        expanded = os.path.expanduser(value)

        # If we're cycling, use the preserved dir_path and prefix
        # Otherwise, parse the current value
        if self._suggestion_index >= 0 and self._preserved_dir_path:
            # We're cycling - use the original context
            dir_path = self._preserved_dir_path
            prefix = self._preserved_prefix
        else:
            # Parse into directory and filename parts
            if expanded.endswith(os.sep):
                dir_path = expanded
                prefix = ""
            else:
                dir_path = os.path.dirname(expanded)
                prefix = os.path.basename(expanded)

            if not dir_path:
                dir_path = "."

        # Single match - complete fully
        if len(active_suggestions) == 1:
            completed = active_suggestions[0]

            # Build new path
            if dir_path == ".":
                new_path = completed
            else:
                new_path = os.path.join(dir_path, completed)

            # Update input and move cursor to end
            input_widget.value = new_path
            input_widget.cursor_position = len(new_path)
            self.current_value = new_path
            self._suggestion_index = -1  # Reset cycling
            self._preserved_suggestions = []  # Clear preserved
            self._preserved_dir_path = ""  # Clear preserved dir
            self._preserved_prefix = ""  # Clear preserved prefix

            # Re-validate and update suggestions
            self._validate_and_update()
            self._update_suggestions()

        # Multiple matches - cycle through suggestions
        elif len(active_suggestions) > 1:
            # If not currently cycling, start cycling immediately at first suggestion
            if self._suggestion_index == -1:
                # Start at index 0 for forward, or last index for backward
                self._suggestion_index = 0 if direction == "forward" else len(active_suggestions) - 1
                # Preserve suggestions for cycling (if not already preserved)
                if not self._preserved_suggestions:
                    self._preserved_suggestions = active_suggestions.copy()
                    self._preserved_dir_path = dir_path
                    self._preserved_prefix = prefix
            else:
                # Already cycling - move to next/previous suggestion based on direction
                if direction == "forward":
                    self._suggestion_index = (self._suggestion_index + 1) % len(self._preserved_suggestions)
                else:  # backward
                    self._suggestion_index = (self._suggestion_index - 1) % len(self._preserved_suggestions)

            # Apply the current suggestion from preserved list
            completed = self._preserved_suggestions[self._suggestion_index]

            # Build new path
            if dir_path == ".":
                new_path = completed
            else:
                new_path = os.path.join(dir_path, completed)

            # Update input and move cursor to end (cycling mode)
            self._is_cycling = True
            input_widget.value = new_path
            input_widget.cursor_position = len(new_path)
            self.current_value = new_path
            self._is_cycling = False

            # Validate current completion but don't update suggestions
            self._validate_and_update()

            # Update the suggestions display to show the highlighted item
            self._refresh_suggestions_display()

        # Note: _in_tab_operation flag will be cleared in on_input_changed after it processes the change

    def _refresh_suggestions_display(self) -> None:
        """Refresh the suggestions display with current highlighting."""
        suggestions_display = self.query_one("#suggestions-display", Static)

        # Use preserved suggestions if we're cycling, otherwise current suggestions
        suggestions = self._preserved_suggestions if self._preserved_suggestions else self._suggestions

        if suggestions:
            highlight_index = self._suggestion_index if self._suggestion_index >= 0 else -1
            formatted = self._format_suggestions(suggestions, highlight_index=highlight_index)
            suggestions_display.update(formatted)
            suggestions_display.add_class("has-content")
        else:
            suggestions_display.update("")
            suggestions_display.remove_class("has-content")

    def _get_common_prefix(self, strings: list[str]) -> str:
        """
        Get the common prefix of a list of strings.

        Args:
            strings: List of strings

        Returns:
            Common prefix
        """
        if not strings:
            return ""

        # Remove trailing slashes for comparison
        cleaned = [s.rstrip("/") for s in strings]

        prefix = cleaned[0]
        for s in cleaned[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""

        return prefix

    def _clear_suggestions(self) -> None:
        """Clear the suggestions display."""
        suggestions_display = self.query_one("#suggestions-display", Static)
        suggestions_display.update("")
        suggestions_display.remove_class("has-content")
        self._suggestions = []

    def _select_current_suggestion(self) -> None:
        """Select the currently highlighted suggestion and finalize it."""
        if self._suggestion_index < 0 or not self._preserved_suggestions:
            return

        input_widget = self.query_one("#path-input", Input)

        # Get the highlighted suggestion
        completed = self._preserved_suggestions[self._suggestion_index]

        # Build new path using preserved directory
        dir_path = self._preserved_dir_path
        if dir_path == ".":
            new_path = completed
        else:
            new_path = os.path.join(dir_path, completed)

        # Update input
        input_widget.value = new_path
        input_widget.cursor_position = len(new_path)
        self.current_value = new_path

        # Reset cycling state
        self._suggestion_index = -1
        self._preserved_suggestions = []
        self._preserved_dir_path = ""
        self._preserved_prefix = ""

        # Re-validate and update suggestions
        self._validate_and_update()
        self._update_suggestions()

    def get_validated_path(self) -> str | None:
        """
        Get the validated absolute path if input is valid.

        Returns:
            Absolute path if valid, None otherwise
        """
        if not self.is_valid:
            return None

        value = self.current_value.strip()
        expanded = os.path.expanduser(value)

        if not os.path.isabs(expanded):
            expanded = os.path.abspath(expanded)

        return expanded
