"""History picker widget for selecting filter type."""

from textual.widgets import Static
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.message import Message
from textual import events
from aristotlelib.project import ProjectStatus


class HistoryPickerWidget(Vertical):
    """
    Interactive picker for history filter options with button-style navigation.

    Features:
    - Two selectable button options
    - Left/Right arrow navigation between buttons
    - Letter key shortcuts (A for in progress, B for all)
    - Enter to confirm selection
    - Visual feedback for selected option
    """

    DEFAULT_CSS = """
    HistoryPickerWidget {
        height: auto;
        padding: 1 2;
        background: $panel;
    }

    HistoryPickerWidget .picker-header {
        color: $text-muted;
        text-style: italic;
        padding-bottom: 1;
        text-align: center;
    }

    HistoryPickerWidget .buttons-container {
        height: auto;
        width: 100%;
        align-horizontal: center;
        padding-top: 1;
    }

    HistoryPickerWidget .picker-button {
        width: 1fr;
        height: auto;
        padding: 1 2;
        text-align: center;
        border: round $primary;
        background: $surface;
        color: $text;
    }

    HistoryPickerWidget .picker-button.selected {
        border: heavy $accent;
        background: $accent-darken-1;
        color: $text;
        text-style: bold;
    }

    HistoryPickerWidget .button-label {
        text-align: center;
        color: $text;
    }

    HistoryPickerWidget .button-label.selected {
        color: $accent;
        text-style: bold;
    }

    HistoryPickerWidget .button-description {
        text-align: center;
        color: $text-muted;
        padding-top: 0;
    }

    HistoryPickerWidget .button-description.selected {
        color: $text;
    }
    """

    # Reactive state
    selected_index = reactive(1)  # 0 = ACTIVE, 1 = ALL (default to ALL)

    class SelectionChanged(Message):
        """Message emitted when selection changes."""

        def __init__(self, index: int, filter_type: set[ProjectStatus] | None):
            self.index = index
            self.filter_type = filter_type
            super().__init__()

    def compose(self):
        """Create the picker layout."""
        yield Static("Select a filter (← → or A/B):", classes="picker-header")

        with Horizontal(classes="buttons-container"):
            with Vertical(id="button-0", classes="picker-button"):
                yield Static("ACTIVE [A]", classes="button-label", id="label-0")
                yield Static("Active projects only", classes="button-description", id="desc-0")

            with Vertical(id="button-1", classes="picker-button selected"):
                yield Static("ALL [B]", classes="button-label selected", id="label-1")
                yield Static("Show all projects", classes="button-description selected", id="desc-1")

    def on_mount(self) -> None:
        """Set up the widget after mounting."""
        self.can_focus = True
        self.focus()

        # Emit initial selection state (ALL is selected by default)
        filter_type = {ProjectStatus.QUEUED, ProjectStatus.IN_PROGRESS, ProjectStatus.PENDING_RETRY} if self.selected_index == 0 else None
        self.post_message(self.SelectionChanged(self.selected_index, filter_type))

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

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard navigation."""
        if event.key == "left":
            # Move to previous option (wraps around)
            self.selected_index = (self.selected_index - 1) % 2
            self._update_selection()
            event.prevent_default()
            event.stop()
        elif event.key == "right":
            # Move to next option (wraps around)
            self.selected_index = (self.selected_index + 1) % 2
            self._update_selection()
            event.prevent_default()
            event.stop()
        elif event.key in ["a", "A"]:
            # Select ACTIVE
            self.selected_index = 0
            self._update_selection()
            event.prevent_default()
            event.stop()
        elif event.key in ["b", "B"]:
            # Select ALL
            self.selected_index = 1
            self._update_selection()
            event.prevent_default()
            event.stop()
        # Let up/down keys bubble up to parent for main menu navigation

    def _update_selection(self) -> None:
        """Update the visual state based on current selection."""
        for i in range(2):
            button = self.query_one(f"#button-{i}")
            label = self.query_one(f"#label-{i}")
            desc = self.query_one(f"#desc-{i}")

            if i == self.selected_index:
                button.add_class("selected")
                label.add_class("selected")
                desc.add_class("selected")
            else:
                button.remove_class("selected")
                label.remove_class("selected")
                desc.remove_class("selected")

        # Emit selection changed message
        filter_type = {ProjectStatus.QUEUED, ProjectStatus.IN_PROGRESS, ProjectStatus.PENDING_RETRY} if self.selected_index == 0 else None
        self.post_message(self.SelectionChanged(self.selected_index, filter_type))

    def get_selected_filter(self) -> set[ProjectStatus] | None:
        """Get the currently selected filter type."""
        return {ProjectStatus.QUEUED, ProjectStatus.IN_PROGRESS, ProjectStatus.PENDING_RETRY} if self.selected_index == 0 else None
