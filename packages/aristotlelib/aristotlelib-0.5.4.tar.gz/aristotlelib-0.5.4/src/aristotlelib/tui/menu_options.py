"""Menu option definitions and centralized configuration for the TUI."""

from enum import Enum
from dataclasses import dataclass
from aristotlelib.project import ProjectInputType


class MenuOption(Enum):
    """Menu options for the integrated menu."""
    FILL_SORRIES = 1
    AUTOFORMALIZE_PAPER = 2
    FREESTYLE = 3
    VIEW_HISTORY = 4

    @classmethod
    def from_number(cls, num: int) -> "MenuOption | None":
        """Convert a number (1-4) to a MenuOption enum value."""
        try:
            return cls(num)
        except ValueError:
            return None

    def to_number(self) -> int:
        """Convert MenuOption to its numeric value."""
        return self.value


@dataclass(frozen=True)
class MenuOptionConfig:
    """Configuration for a menu option combining UI and workflow settings."""

    # UI Configuration
    label: str  # Display text for the menu option
    prompt: str  # Default prompt text for this option
    requires_file: bool  # Whether this option needs a file input
    file_types: list[str]  # Allowed file extensions (e.g., [".lean", ".txt"])

    # Workflow Configuration
    input_type: ProjectInputType | None  # Type of project input (None for VIEW_HISTORY)
    auto_add_imports: bool  # Whether to automatically add imports
    validate_lean_project: bool  # Whether to validate as a Lean project
    supports_optional_lean_context: bool = False  # Whether this option supports an optional .lean context file
    supports_nl_context: bool = False  # Whether this option supports natural language context files (.md, .txt, .tex)


# Centralized configuration registry - single source of truth
MENU_OPTIONS: dict[MenuOption, MenuOptionConfig] = {
    MenuOption.FILL_SORRIES: MenuOptionConfig(
        label="Fill sorries in a lean file (.lean)",
        prompt="Fill in the sorry statements in this Lean file",
        requires_file=True,
        file_types=[".lean"],
        input_type=ProjectInputType.FORMAL_LEAN,
        auto_add_imports=True,
        validate_lean_project=True,
    ),
    MenuOption.AUTOFORMALIZE_PAPER: MenuOptionConfig(
        label="Autoformalize your mathematical content (.tex, .md, .txt)",
        prompt="Autoformalize the mathematical content in this paper",
        requires_file=True,
        file_types=[".tex", ".md", ".txt"],
        supports_optional_lean_context=True,
        supports_nl_context=True,
        input_type=ProjectInputType.INFORMAL,
        auto_add_imports=True,
        validate_lean_project=False,
    ),
    MenuOption.FREESTYLE: MenuOptionConfig(
        label="Direct Aristotle in English (.lean optional)",
        prompt="Freestyle",
        requires_file=False,
        file_types=[],
        input_type=ProjectInputType.INFORMAL,
        auto_add_imports=False,
        validate_lean_project=False,
        supports_optional_lean_context=True,
        supports_nl_context=True,
    ),
    MenuOption.VIEW_HISTORY: MenuOptionConfig(
        label="View history",
        prompt="View recent proof attempts",
        requires_file=False,
        file_types=[],
        input_type=None,  # History doesn't create a project
        auto_add_imports=False,
        validate_lean_project=False,
    ),
}
