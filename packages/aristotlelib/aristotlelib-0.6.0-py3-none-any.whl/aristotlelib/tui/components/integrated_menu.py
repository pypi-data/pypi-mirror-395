"""Integrated menu widget combining prompt, file input, and menu options."""

from textual.widgets import TextArea, Input, Static
from textual.containers import Vertical
from textual.message import Message
from textual.app import ComposeResult
from textual.reactive import reactive
from textual import events
from textual.events import Key

from aristotlelib.tui.components.history_picker import HistoryPickerWidget
from aristotlelib.tui.components.file_path_input import FilePathInput
from aristotlelib.tui.menu_options import MenuOption, MenuOptionConfig, MENU_OPTIONS
from aristotlelib.project import ProjectStatus

# UI Constants for border formatting (removed hardcoded width - now dynamic)

class SubmittableTextArea(TextArea):
    """TextArea for multi-line input with Ctrl+S to submit.

    Ctrl+S is handled by the parent IntegratedMenuWidget via BINDINGS,
    allowing Enter to add newlines normally in the TextArea.
    """

    def on_mount(self) -> None:
        """Set up the widget after mounting."""
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


class IntegratedMenuWidget(Vertical):
    """
    Integrated menu with adaptive single input box and menu options.

    The widget allows users to:
    - Select from 4 menu options
    - Options 1-2: Single-line Input for file path
    - Option 3: Multi-line TextArea for freestyle prompt
    - Option 4: History picker
    - Submit with Ctrl+S
    """

    # Use Ctrl+S (save) as submit key - universally supported
    # Note: Ctrl+D doesn't work as it's intercepted by terminal/Textual as EOF
    BINDINGS = [
        ("ctrl+s", "submit_form", "Submit"),
    ]

    DEFAULT_CSS = """
    IntegratedMenuWidget {
        height: auto;
        padding: 1 0;
    }

    IntegratedMenuWidget Vertical {
        height: auto;
    }

    IntegratedMenuWidget #input-container {
        height: auto;
        margin-top: 1;
        margin-bottom: 1;
        width: 100%;
        max-width: 72;
        min-width: 40;
    }

    IntegratedMenuWidget TextArea {
        height: 6;
        border: solid $primary;
        margin-bottom: 1;
        width: 100%;
        max-width: 72;
        min-width: 40;
    }

    IntegratedMenuWidget Input {
        height: auto;
        border: solid $accent;
        margin-bottom: 1;
        width: 100%;
        max-width: 72;
        min-width: 40;
    }

    IntegratedMenuWidget .menu-options {
        height: auto;
        padding: 1 0;
        width: 100%;
        max-width: 72;
        min-width: 40;
    }

    IntegratedMenuWidget .menu-option {
        padding: 0;
    }

    IntegratedMenuWidget .menu-option.selected {
        color: $accent;
        text-style: bold;
    }
    """

    # Reactive state
    mode = reactive("navigation")  # "navigation" or "input"
    selected_option: MenuOption | None = reactive(None)  # None = no selection, or MenuOption enum value
    input_value = reactive("")  # Stores file path or prompt text
    context_file_path = reactive("")  # Stores optional Lean context file path
    nl_context_file_path = reactive("")  # Stores optional natural language context file/folder path
    history_filter: ProjectStatus | None = reactive(None)  # For VIEW_HISTORY option: None = all, or specific status
    history_selection_made = reactive(False)  # Track if history filter selection has been made

    class Submitted(Message):
        """Message emitted when user submits the form."""

        def __init__(self, option: MenuOption, prompt: str, file_path: str | None, context_file_path: str | None = None, nl_context_file_path: str | None = None, history_filter: ProjectStatus | None = None):
            self.option = option
            self.prompt = prompt
            self.file_path = file_path
            self.context_file_path = context_file_path
            self.nl_context_file_path = nl_context_file_path
            self.history_filter = history_filter
            super().__init__()

    def compose(self) -> ComposeResult:
        """Create the integrated menu layout."""
        # Menu options - now shown FIRST (above input)
        with Vertical(classes="menu-options"):
            yield Static(id="menu-top-border", markup=False)
            yield Static(id="menu-blank-top", markup=False)
            for option in MenuOption:
                config = MENU_OPTIONS[option]
                num = option.to_number()
                yield Static(f"│  [{num}] {config.label}│", classes="menu-option", id=f"option-{num}")
            yield Static(id="menu-blank-bottom", markup=False)
            yield Static(id="menu-bottom-border", markup=False)

        # Input container - shown SECOND (below menu)
        # Initially hidden in navigation mode, shown in input mode
        with Vertical(id="input-container", classes="input-container"):
            yield Static(id="input-header", markup=False)  # Dynamic header
            # Input widget will be dynamically added based on selection
            yield Static(id="input-footer", markup=False)  # Bottom border

    def on_mount(self) -> None:
        """Initialize the widget state."""
        # Calculate border width based on terminal size
        border_width = self._get_border_width()

        # Start in navigation mode - hide input container
        container = self.query_one("#input-container")
        container.display = False

        # Update menu borders with calculated width
        self._update_menu_borders(border_width)

        # Make the widget focusable
        self.can_focus = True

        # Defer focus until after layout is complete to avoid premature scrolling
        # This ensures Textual's layout engine has calculated the correct scroll region
        self.call_later(self._delayed_focus)

    def _delayed_focus(self) -> None:
        """Focus the widget after layout is complete."""
        self.focus(scroll_visible=False)

    def on_terminal_resized(self, message) -> None:
        """Handle terminal resize by updating menu borders."""
        # Import here to avoid circular dependency
        from aristotlelib.tui.app import TerminalResized

        if isinstance(message, TerminalResized):
            new_width = self._get_border_width()
            self._update_menu_borders(new_width)

            # Re-render input container if in input mode
            if self.mode == "input" and self.selected_option is not None:
                self._update_ui_for_option(self.selected_option, auto_focus=False)

    def _transition_to_input_mode(self, option: MenuOption) -> None:
        """Transition from navigation mode to input mode."""
        self.mode = "input"
        self.selected_option = option
        self._show_collapsed_menu(option)
        self._update_ui_for_option(option, auto_focus=True)

    def _transition_to_navigation_mode(self) -> None:
        """Transition from input mode to navigation mode."""
        self.mode = "navigation"
        self.selected_option = None
        self.context_file_path = ""  # Reset context file path
        self.nl_context_file_path = ""  # Reset NL context file path
        self.history_selection_made = False  # Reset history selection flag
        self._clear_input()
        self._show_full_menu()
        self.focus(scroll_visible=False)

    def _clear_input(self) -> None:
        """Clear the input widget and hide the input container."""
        try:
            # Remove all existing input widgets
            widgets = self.query(".input-widget")
            for widget in widgets:
                widget.remove()
        except Exception:
            pass

        # Remove labels if present (each one individually to avoid stopping on missing labels)
        for label_id in ["#context-label", "#nl-context-label", "#prompt-label", "#primary-label", "#file-label"]:
            try:
                label = self.query_one(label_id)
                label.remove()
            except Exception:
                pass

        # Hide input container
        container = self.query_one("#input-container")
        container.display = False

    def _show_full_menu(self) -> None:
        """Show the full menu with all options."""
        border_width = self._get_border_width()
        content_width = border_width - 2

        # Show all option lines
        for option in MenuOption:
            num = option.to_number()
            opt_widget = self.query_one(f"#option-{num}", Static)
            opt_widget.display = True
            opt_widget.remove_class("selected")

        # Show blank lines
        self.query_one("#menu-blank-top", Static).display = True
        self.query_one("#menu-blank-bottom", Static).display = True

        # Update borders to full menu style
        top_border = self.query_one("#menu-top-border", Static)
        header_text = "╭─ Available Modes "
        top_border.update(f"{header_text}{'─' * (content_width - len(header_text) + 1)}╮")

        bottom_border = self.query_one("#menu-bottom-border", Static)
        footer_text = " ctrl+c to exit ─╯"
        bottom_border.update(f"╰{'─' * (content_width - len(footer_text) + 1)}{footer_text}")

    def _highlight_option(self, option: MenuOption) -> None:
        """Highlight an option in navigation mode (doesn't transition to input mode)."""
        for opt in MenuOption:
            num = opt.to_number()
            opt_widget = self.query_one(f"#option-{num}", Static)
            if opt == option:
                opt_widget.add_class("selected")
            else:
                opt_widget.remove_class("selected")

    def _show_collapsed_menu(self, option: MenuOption) -> None:
        """Show collapsed menu with only the selected option."""
        border_width = self._get_border_width()
        content_width = border_width - 2
        label_width = border_width - 8

        # Hide all options except the selected one
        for opt in MenuOption:
            num = opt.to_number()
            opt_widget = self.query_one(f"#option-{num}", Static)
            if opt == option:
                opt_widget.display = True
                opt_widget.add_class("selected")
                # Update the option text to match collapsed width
                config = MENU_OPTIONS[opt]
                opt_widget.update(f"│  [{num}] {config.label:<{label_width}}│")
            else:
                opt_widget.display = False

        # Hide blank lines for compact view
        self.query_one("#menu-blank-top", Static).display = False
        self.query_one("#menu-blank-bottom", Static).display = False

        # Update borders to collapsed style
        top_border = self.query_one("#menu-top-border", Static)
        header_text = "╭─ Mode "
        top_border.update(f"{header_text}{'─' * (content_width - len(header_text) + 1)}╮")

        bottom_border = self.query_one("#menu-bottom-border", Static)
        bottom_border.update(f"╰{'─' * content_width}╯")

    def _get_border_width(self) -> int:
        """Calculate border width based on terminal size."""
        terminal_width = self.app.size.width

        # Calculate minimum width needed for content
        max_label_len = max(len(cfg.label) for cfg in MENU_OPTIONS.values())
        content_min = max_label_len + 8  # "│  [X] label│"

        # Menu width should not exceed 72 characters to stay well within 80
        # Use min of: 72 max, content minimum, or terminal_width - 8 for padding
        max_width = 72
        return min(max_width, max(content_min, terminal_width - 8))

    def _update_menu_borders(self, border_width: int) -> None:
        """Update menu borders with the calculated width."""
        # Calculate content width (border_width - 2 for the side borders)
        content_width = border_width - 2
        # Label width for menu options: total line is border_width
        # "│  [X] " = 7 chars on left, "│" = 1 char on right, so label gets: border_width - 8
        label_width = border_width - 8

        # Update top border: "╭─ Available Modes " = 19 chars, then fill to content_width, then "╮"
        top_border = self.query_one("#menu-top-border", Static)
        header_text = "╭─ Available Modes "
        top_border.update(f"{header_text}{'─' * (content_width - len(header_text) + 1)}╮")

        # Update blank lines
        blank_top = self.query_one("#menu-blank-top", Static)
        blank_top.update(f"│{' ' * content_width}│")

        blank_bottom = self.query_one("#menu-blank-bottom", Static)
        blank_bottom.update(f"│{' ' * content_width}│")

        # Update bottom border
        bottom_border = self.query_one("#menu-bottom-border", Static)
        footer_text = " ctrl+c to exit ─╯"
        bottom_border.update(f"╰{'─' * (content_width - len(footer_text) + 1)}{footer_text}")

        # Update menu option lines
        for option in MenuOption:
            num = option.to_number()
            config = MENU_OPTIONS[option]
            option_widget = self.query_one(f"#option-{num}", Static)

            # Format label with truncation if needed
            label = config.label
            if len(label) > label_width:
                # Truncate with ellipsis
                label = label[:label_width - 3] + "..."

            # Format: "│  [X] label with padding│"
            # "│  " = 3 chars, "[X] " = 4 chars (total 7), label (padded), "│" = 1 char
            option_widget.update(f"│  [{num}] {label:<{label_width}}│")

    def action_submit_form(self) -> None:
        """Action called when Ctrl+S is pressed (via BINDINGS)."""
        if self._is_form_ready():
            self._submit_form()

    def _on_key(self, event: Key) -> None:
        """Handle keyboard shortcuts with capture priority (before children).

        The underscore prefix (_on_key vs on_key) means this is called in the
        "capture" phase BEFORE child widgets receive the event.
        """
        # ESCAPE KEY: Always intercept and return to navigation mode from input mode
        # This must be handled here in capture phase to intercept before Input widgets
        if event.key == "escape":
            if self.mode == "input":
                self._transition_to_navigation_mode()
                event.prevent_default()
                event.stop()
                return

        # For all other keys, we need to handle them here in capture phase
        # Otherwise they bubble up to parent widgets
        self._handle_key_event(event)

    def _handle_key_event(self, event: events.Key) -> None:
        """Handle keyboard shortcuts for navigation and input."""
        # NUMBER KEYS (1-4): Select option
        if event.key in ["1", "2", "3", "4"]:
            # In input mode with TextArea focused, let numbers through for typing
            if self.mode == "input":
                try:
                    textarea = self.query_one(".input-widget", TextArea)
                    if textarea.has_focus:
                        return
                except Exception:
                    pass

            # Convert number key to MenuOption enum
            option = MenuOption.from_number(int(event.key))
            if option:
                self._transition_to_input_mode(option)
                event.prevent_default()
                event.stop()
            return

        # CTRL+T/CTRL+L/CTRL+F: Field switching in modes with dual/triple inputs
        if event.key in ["ctrl+t", "ctrl+l", "ctrl+f"]:
            if self.mode == "input" and self.selected_option is not None:
                config = MENU_OPTIONS[self.selected_option]
                # Handle FREESTYLE mode
                if self.selected_option == MenuOption.FREESTYLE:
                    try:
                        widgets = list(self.query(".input-widget"))
                        if len(widgets) >= 2:
                            textarea = None
                            lean_context_input = None
                            nl_context_input = None

                            for widget in widgets:
                                if isinstance(widget, TextArea):
                                    textarea = widget
                                elif isinstance(widget, FilePathInput):
                                    if widget.id == "context-file-input":
                                        lean_context_input = widget
                                    elif widget.id == "nl-context-file-input":
                                        nl_context_input = widget

                            if event.key == "ctrl+t" and textarea:
                                # Ctrl+T: Focus the text/prompt (TextArea)
                                textarea.focus(scroll_visible=False)
                                event.prevent_default()
                                event.stop()
                                return
                            elif event.key == "ctrl+l" and lean_context_input:
                                # Ctrl+L: Focus the Lean context file input
                                try:
                                    file_input = lean_context_input.query_one("#path-input", Input)
                                    file_input.focus(scroll_visible=False)
                                except Exception:
                                    lean_context_input.focus(scroll_visible=False)
                                event.prevent_default()
                                event.stop()
                                return
                            elif event.key == "ctrl+f" and nl_context_input:
                                # Ctrl+F: Focus the natural language context file input
                                try:
                                    file_input = nl_context_input.query_one("#path-input", Input)
                                    file_input.focus(scroll_visible=False)
                                except Exception:
                                    nl_context_input.focus(scroll_visible=False)
                                event.prevent_default()
                                event.stop()
                                return
                    except Exception:
                        pass
                # Handle options with optional lean context (dual/triple file inputs)
                elif config.supports_optional_lean_context:
                    try:
                        widgets = list(self.query(".input-widget"))
                        if len(widgets) >= 2:
                            primary_input = None
                            lean_context_input = None
                            nl_context_input = None

                            for widget in widgets:
                                if isinstance(widget, FilePathInput):
                                    if widget.id == "context-file-input":
                                        lean_context_input = widget
                                    elif widget.id == "nl-context-file-input":
                                        nl_context_input = widget
                                    else:
                                        primary_input = widget

                            if event.key == "ctrl+t" and primary_input:
                                # Ctrl+T: Focus the primary file input (paper)
                                try:
                                    file_input = primary_input.query_one("#path-input", Input)
                                    file_input.focus(scroll_visible=False)
                                except Exception:
                                    primary_input.focus(scroll_visible=False)
                                event.prevent_default()
                                event.stop()
                                return
                            elif event.key == "ctrl+l" and lean_context_input:
                                # Ctrl+L: Focus the Lean context file input
                                try:
                                    file_input = lean_context_input.query_one("#path-input", Input)
                                    file_input.focus(scroll_visible=False)
                                except Exception:
                                    lean_context_input.focus(scroll_visible=False)
                                event.prevent_default()
                                event.stop()
                                return
                            elif event.key == "ctrl+f" and nl_context_input:
                                # Ctrl+F: Focus the natural language context file input
                                try:
                                    file_input = nl_context_input.query_one("#path-input", Input)
                                    file_input.focus(scroll_visible=False)
                                except Exception:
                                    nl_context_input.focus(scroll_visible=False)
                                event.prevent_default()
                                event.stop()
                                return
                    except Exception:
                        pass
            return

        # ARROW KEYS: Navigation in navigation mode, cursor movement in input mode
        if event.key in ["up", "down"]:
            # In input mode, let widgets handle arrows for cursor movement
            if self.mode == "input":
                # Let TextArea handle arrows if focused
                try:
                    textarea = self.query_one(".input-widget", TextArea)
                    if textarea.has_focus:
                        return  # Let TextArea handle arrows
                except Exception:
                    pass
                # In input mode but not in TextArea - ignore arrows
                event.prevent_default()
                event.stop()
                return

            # Navigation mode: Handle menu navigation with up/down
            all_options = list(MenuOption)
            if event.key == "up":
                if self.selected_option is None:
                    # Start from last option if nothing selected
                    new_option = all_options[-1]
                else:
                    current_index = all_options.index(self.selected_option)
                    # Wrap around to last if at first
                    new_index = (current_index - 1) % len(all_options)
                    new_option = all_options[new_index]
                self.selected_option = new_option
                self._highlight_option(new_option)
                event.prevent_default()
                event.stop()
                return

            if event.key == "down":
                if self.selected_option is None:
                    # Start from first option if nothing selected
                    new_option = all_options[0]
                else:
                    current_index = all_options.index(self.selected_option)
                    # Wrap around to first if at last
                    new_index = (current_index + 1) % len(all_options)
                    new_option = all_options[new_index]
                self.selected_option = new_option
                self._highlight_option(new_option)
                event.prevent_default()
                event.stop()
                return

        # LEFT/RIGHT ARROWS: Let HistoryPicker handle them in input mode
        if event.key in ["left", "right"]:
            if self.mode == "input":
                try:
                    picker = self.query_one(".input-widget", HistoryPickerWidget)
                    if picker.has_focus:
                        return  # Let picker handle left/right
                except Exception:
                    pass
            # Otherwise prevent default
            event.prevent_default()
            event.stop()
            return

        # ENTER KEY: Different behavior based on mode
        if event.key == "enter":
            if self.mode == "navigation":
                # Transition to input mode if an option is selected
                if self.selected_option is not None:
                    self._transition_to_input_mode(self.selected_option)
                    event.prevent_default()
                    event.stop()
                    return
            else:  # input mode
                # In TextArea (freestyle), let Enter add newlines
                try:
                    textarea = self.query_one(".input-widget", TextArea)
                    if textarea.has_focus:
                        return  # Let TextArea handle Enter
                except Exception:
                    pass

                # Otherwise, submit if form is ready
                if self._is_form_ready():
                    self._submit_form()
                    event.prevent_default()
                    event.stop()
                    return

    def on_file_path_input_validated(self, event: FilePathInput.Validated) -> None:
        """Handle file path validation from FilePathInput widget."""
        # Check if this is the context file input or the main file input
        widget = event.control
        if hasattr(widget, 'id') and widget.id == "context-file-input":
            # Store context file path
            self.context_file_path = event.file_path
        else:
            # Store the validated path (for backward compatibility)
            self.input_value = event.file_path

    def on_history_picker_widget_selection_changed(self, event: HistoryPickerWidget.SelectionChanged) -> None:
        """Handle selection changes from HistoryPickerWidget."""
        # Update the history filter based on the picker's selection
        self.history_filter = event.filter_type
        self.history_selection_made = True

    def _update_ui_for_option(self, option: MenuOption, auto_focus: bool = True) -> None:
        """Update UI based on selected option.

        Args:
            option: The MenuOption enum value
            auto_focus: If True, auto-focus input widgets. If False, keep focus on parent (navigation mode).
        """
        config = MENU_OPTIONS[option]

        # Get the input container
        container = self.query_one("#input-container")

        container.display = True

        # Calculate border width dynamically
        border_width = self._get_border_width()

        # Update header with option label
        header = self.query_one("#input-header", Static)
        # Add Ctrl+T/L/F hint for modes with dual inputs
        if option == MenuOption.FREESTYLE:
            if config.supports_nl_context:
                header_text = "Ctrl+T=text, Ctrl+L=lean, Ctrl+F=files, Ctrl+S=submit ─┐"
            else:
                header_text = "Ctrl+T=text, Ctrl+L=lean, Ctrl+S=submit ─┐"
        elif config.supports_optional_lean_context:
            if config.supports_nl_context:
                header_text = "Ctrl+T=paper, Ctrl+L=lean, Ctrl+F=files, Ctrl+S=submit ─┐"
            else:
                header_text = "Ctrl+T=paper, Ctrl+L=lean, Ctrl+S=submit ─┐"
        else:
            header_text = "Ctrl+S to submit ─┐"
        # Left-align like footer: "┌─" + padding + text
        header.update(f"┌{'─' * (border_width - len(header_text) - 1)}{header_text}")

        # Update footer
        footer = self.query_one("#input-footer", Static)
        footer_text = " Esc to return to main menu ─┘"
        footer.update(f"└{'─' * (border_width - len(footer_text) - 1)}{footer_text}")

        # Check what type of widget we need
        needs_input = config.requires_file
        needs_picker = (option == MenuOption.VIEW_HISTORY)
        is_freestyle = (option == MenuOption.FREESTYLE)
        has_dual_inputs = is_freestyle or config.supports_optional_lean_context

        # For options with dual inputs (FREESTYLE or options with optional lean context), check if widgets exist
        if has_dual_inputs:
            try:
                # Check if we have dual input widgets
                widgets = self.query(".input-widget")
                has_context_label = bool(self.query("#context-label"))

                # Check if we have the correct labels for the current mode
                has_prompt_label = bool(self.query("#prompt-label"))
                has_primary_label = bool(self.query("#primary-label"))

                # Determine if labels match the current mode
                # We need the correct label AND no wrong labels
                correct_labels = False
                if is_freestyle and has_prompt_label and not has_primary_label:
                    correct_labels = True
                elif config.supports_optional_lean_context and has_primary_label and not has_prompt_label:
                    correct_labels = True

                if len(widgets) >= 2 and has_context_label and correct_labels:
                    # We have the dual input setup with correct labels, just clear the widgets
                    primary_widget = None
                    for widget in widgets:
                        if isinstance(widget, TextArea):
                            widget.text = ""
                            primary_widget = widget
                        elif isinstance(widget, FilePathInput):
                            try:
                                file_input = widget.query_one("#path-input", Input)
                                file_input.value = ""
                                widget.current_value = ""
                                widget._suggestions = []
                                widget._preserved_suggestions = []
                                widget._suggestion_index = -1
                                widget._preserved_dir_path = ""
                                widget._preserved_prefix = ""
                                suggestions_display = widget.query_one("#suggestions-display", Static)
                                suggestions_display.update("")
                                suggestions_display.remove_class("has-content")
                            except Exception:
                                pass
                    # Focus the primary widget (textarea for FREESTYLE, first file input for others)
                    if auto_focus and primary_widget:
                        primary_widget.focus(scroll_visible=False)
                    elif auto_focus and widgets:
                        widgets[0].focus(scroll_visible=False)
                else:
                    # Need to recreate dual input widgets (wrong labels or missing widgets)
                    self._clear_input()
                    container.display = True
                    self._create_and_mount_input(container, footer, config, option, auto_focus)
            except Exception:
                # No existing widgets, create them
                self._clear_input()
                container.display = True
                self._create_and_mount_input(container, footer, config, option, auto_focus)
        else:
            # Check current widget type for non-FREESTYLE options
            try:
                current_widget = self.query_one(".input-widget")
                is_file_input = isinstance(current_widget, FilePathInput)
                is_textarea = isinstance(current_widget, TextArea)
                is_picker = isinstance(current_widget, HistoryPickerWidget)

                # If the widget type matches what we need, just clear it and reuse
                if needs_picker and is_picker:
                    # Reuse existing picker
                    pass
                elif (needs_input and is_file_input):
                    # Check if we have the correct label for single file input
                    has_file_label = bool(self.query("#file-label"))

                    if has_file_label:
                        # Reuse FilePathInput widget - clear it by updating the internal input
                        try:
                            file_input = current_widget.query_one("#path-input", Input)
                            file_input.value = ""
                            current_widget.current_value = ""
                            # Update allowed extensions for the new option
                            current_widget.allowed_extensions = config.file_types
                            # Clear suggestions and cycling state
                            current_widget._suggestions = []
                            current_widget._preserved_suggestions = []
                            current_widget._suggestion_index = -1
                            current_widget._preserved_dir_path = ""
                            current_widget._preserved_prefix = ""
                            # Clear the suggestions display
                            suggestions_display = current_widget.query_one("#suggestions-display", Static)
                            suggestions_display.update("")
                            suggestions_display.remove_class("has-content")
                            # Only focus if auto_focus is True
                            if auto_focus:
                                file_input.focus(scroll_visible=False)
                        except Exception:
                            # If clearing fails, just recreate
                            current_widget.remove()
                            self._create_and_mount_input(container, footer, config, option, auto_focus)
                    else:
                        # No file label, need to recreate with label
                        self._clear_input()
                        container.display = True
                        self._create_and_mount_input(container, footer, config, option, auto_focus)
                elif (not needs_input and not needs_picker and is_textarea):
                    # Reuse TextArea widget (but not for FREESTYLE which is handled above)
                    current_widget.text = ""
                    current_widget.disabled = False
                    # Only focus if auto_focus is True
                    if auto_focus:
                        current_widget.focus(scroll_visible=False)
                else:
                    # Need to swap widget types - remove old and mount new
                    self._clear_input()
                    container.display = True
                    # Create and mount new widget immediately
                    self._create_and_mount_input(container, footer, config, option, auto_focus)
            except Exception:
                # No existing widget, create one
                self._create_and_mount_input(container, footer, config, option, auto_focus)

        # Note: Menu highlighting is handled by _show_collapsed_menu() in input mode
        # and _show_full_menu() in navigation mode

    def _create_and_mount_input(self, container, footer, config: MenuOptionConfig, option: MenuOption, auto_focus: bool = True):
        """Helper to create and mount appropriate input widget.

        Args:
            container: The container to mount the widget in
            footer: The footer element to mount before
            config: The MenuOptionConfig for this option
            option: The MenuOption enum value
            auto_focus: If True, focus the widget after mounting. If False, don't focus.
        """
        if option == MenuOption.VIEW_HISTORY:
            # History picker
            new_input = HistoryPickerWidget(classes="input-widget")
            container.mount(new_input, before=footer)
            if auto_focus:
                new_input.focus(scroll_visible=False)
        elif option == MenuOption.FREESTYLE:
            # FREESTYLE: TextArea for prompt + optional FilePathInput for context
            # Add label for prompt
            prompt_label = Static(" Enter your prompt:", id="prompt-label")
            container.mount(prompt_label, before=footer)

            # Mount TextArea
            textarea = SubmittableTextArea(
                text="",
                classes="input-widget"
            )
            container.mount(textarea, before=footer)

            # Add label for lean context file
            context_label = Static(" Optional: Attach a Lean file as context", id="context-label")
            container.mount(context_label, before=footer)

            # Mount FilePathInput for optional lean context file
            context_input = FilePathInput(
                allowed_extensions=[".lean"],
                classes="input-widget",
                id="context-file-input",
                auto_focus=False  # Don't auto-focus; TextArea should have focus
            )
            container.mount(context_input, before=footer)

            # Add natural language context input if supported
            config = MENU_OPTIONS[option]
            if config.supports_nl_context:
                # Add label for natural language context
                nl_context_label = Static(" Optional: Attach other context - file or folder", id="nl-context-label")
                container.mount(nl_context_label, before=footer)

                # Mount FilePathInput for optional NL context (file or folder)
                nl_context_input = FilePathInput(
                    allowed_extensions=[".md", ".txt", ".tex"],
                    classes="input-widget",
                    id="nl-context-file-input",
                    auto_focus=False,  # Don't auto-focus
                    allow_folders=True  # Allow folder paths
                )
                container.mount(nl_context_input, before=footer)

            # Focus the textarea
            if auto_focus:
                textarea.focus(scroll_visible=False)
        elif config.supports_optional_lean_context and config.requires_file:
            # Options with dual file inputs: primary file + optional lean context
            # Add label for primary file
            primary_label = Static(" Enter path to your paper:", id="primary-label")
            container.mount(primary_label, before=footer)

            # Mount primary file input
            primary_input = FilePathInput(
                allowed_extensions=config.file_types,
                classes="input-widget"
            )
            container.mount(primary_input, before=footer)

            # Add label for lean context file
            context_label = Static(" Optional: Attach a Lean file as context", id="context-label")
            container.mount(context_label, before=footer)

            # Mount FilePathInput for optional lean context file
            context_input = FilePathInput(
                allowed_extensions=[".lean"],
                classes="input-widget",
                id="context-file-input",
                auto_focus=False  # Don't auto-focus; primary input should have focus
            )
            container.mount(context_input, before=footer)

            # Add natural language context input if supported
            if config.supports_nl_context:
                # Add label for natural language context
                nl_context_label = Static(" Optional: Attach other context - file or folder", id="nl-context-label")
                container.mount(nl_context_label, before=footer)

                # Mount FilePathInput for optional NL context (file or folder)
                nl_context_input = FilePathInput(
                    allowed_extensions=[".md", ".txt", ".tex"],
                    classes="input-widget",
                    id="nl-context-file-input",
                    auto_focus=False,  # Don't auto-focus
                    allow_folders=True  # Allow folder paths
                )
                container.mount(nl_context_input, before=footer)

            # Focus the primary input
            if auto_focus:
                primary_input.focus(scroll_visible=False)
        elif config.requires_file:
            # File input with tab completion and validation
            # Add label for single file input (e.g., FILL_SORRIES)
            file_label = Static(" Enter the path to your Lean file:", id="file-label")
            container.mount(file_label, before=footer)

            new_input = FilePathInput(
                allowed_extensions=config.file_types,
                classes="input-widget"
            )
            container.mount(new_input, before=footer)
            if auto_focus:
                new_input.focus(scroll_visible=False)
        else:
            # Multi-line TextArea for other non-file options
            new_input = SubmittableTextArea(
                text="",
                classes="input-widget"
            )
            container.mount(new_input, before=footer)
            if auto_focus:
                new_input.focus(scroll_visible=False)

    def _is_form_ready(self) -> bool:
        """Check if the form is ready to be submitted."""
        if self.selected_option is None:
            # No option selected
            return False

        config = MENU_OPTIONS[self.selected_option]

        # VIEW_HISTORY is ready when picker has made a selection (even if it's None for "ALL")
        if self.selected_option == MenuOption.VIEW_HISTORY:
            return self.history_selection_made

        # Get the current input widget
        try:
            if config.requires_file:
                # File-based options: Check if primary FilePathInput is valid
                # For dual inputs, we need to exclude the context-file-input
                if config.supports_optional_lean_context:
                    # Get all file inputs and find the primary one (not context-file-input)
                    widgets = list(self.query(".input-widget"))
                    for widget in widgets:
                        if isinstance(widget, FilePathInput) and widget.id != "context-file-input":
                            return widget.is_valid
                    # Fallback if no primary input found
                    return False
                else:
                    # Single file input
                    file_input = self.query_one(".input-widget", FilePathInput)
                    return file_input.is_valid
            else:
                # FREESTYLE: Check if textarea has content
                textarea = self.query_one(".input-widget", TextArea)
                return bool(textarea.text and textarea.text.strip())
        except Exception:
            return False

    def _submit_form(self) -> None:
        """Submit the form."""
        if self.selected_option is None:
            # No option selected yet
            return

        config = MENU_OPTIONS[self.selected_option]

        # Get input based on option type
        if config.requires_file:
            # File-based options: File path from FilePathInput
            try:
                # For dual inputs, we need to get the primary input (not context-file-input)
                if config.supports_optional_lean_context:
                    widgets = list(self.query(".input-widget"))
                    file_path = None
                    for widget in widgets:
                        if isinstance(widget, FilePathInput) and widget.id != "context-file-input":
                            file_path = widget.get_validated_path()
                            break
                    if not file_path:
                        # File not valid - don't submit
                        return
                else:
                    # Single file input
                    file_input = self.query_one(".input-widget", FilePathInput)
                    file_path = file_input.get_validated_path()
                    if not file_path:
                        # File not valid - don't submit
                        return
            except Exception:
                return
            prompt_text = config.prompt  # Use default prompt for file-based options
        elif self.selected_option == MenuOption.VIEW_HISTORY:
            # VIEW_HISTORY: No input required, submit immediately
            prompt_text = config.prompt
            file_path = None
        else:
            # FREESTYLE: prompt from textarea
            try:
                textarea = self.query_one(".input-widget", TextArea)
                prompt_text = textarea.text
                if not prompt_text or not prompt_text.strip():
                    return
            except Exception:
                return
            file_path = None

        # Get context file path for options with optional lean context if provided
        context_file_path = None
        if config.supports_optional_lean_context:
            try:
                context_input = self.query_one("#context-file-input", FilePathInput)
                if context_input.is_valid:
                    context_file_path = context_input.get_validated_path()
            except Exception:
                # Context file is optional, so it's OK if it doesn't exist or isn't valid
                pass

        # Get natural language context file/folder path if provided
        nl_context_file_path = None
        if config.supports_nl_context:
            try:
                nl_context_input = self.query_one("#nl-context-file-input", FilePathInput)
                if nl_context_input.is_valid:
                    nl_context_file_path = nl_context_input.get_validated_path()
            except Exception:
                # NL context is optional, so it's OK if it doesn't exist or isn't valid
                pass

        # Emit submission message
        self.post_message(
            self.Submitted(
                option=self.selected_option,
                prompt=prompt_text,
                file_path=file_path,
                context_file_path=context_file_path,
                nl_context_file_path=nl_context_file_path,
                history_filter=self.history_filter if self.selected_option == MenuOption.VIEW_HISTORY else None
            )
        )
