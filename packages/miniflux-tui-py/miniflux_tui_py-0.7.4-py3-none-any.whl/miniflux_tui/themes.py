# SPDX-License-Identifier: MIT
"""Theme management for Miniflux TUI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class Theme:
    """Represents a color theme with CSS variable mappings."""

    name: str
    display_name: str
    colors: dict[str, str]

    def to_css_variables(self) -> str:
        """Convert theme colors to CSS variable definitions.

        Returns:
            CSS string with variable definitions for use in CSS.
        """
        css_lines = []
        for var_name, color_value in self.colors.items():
            css_lines.append(f"${var_name}: {color_value};")
        return "\n    ".join(css_lines)


# Dark theme - Dracula inspired
DARK_THEME = Theme(
    name="dark",
    display_name="Dark",
    colors={
        # Background and surface
        "surface": "#282a36",
        "boost": "#44475a",
        "border": "#6272a4",
        # Text
        "text": "#f8f8f2",
        "text-muted": "#6272a4",
        # Accent and highlights
        "accent": "#50fa7b",
        "primary": "#8be9fd",
        # Custom colors for entries
        "unread": "#8be9fd",  # cyan
        "read": "#6272a4",  # muted
        # Link highlighting
        "link-highlight-bg": "#ff79c6",  # pink/magenta for visibility
        "link-highlight-fg": "#282a36",  # dark text on bright background
    },
)

# Light theme - Solarized inspired
LIGHT_THEME = Theme(
    name="light",
    display_name="Light",
    colors={
        # Background and surface
        "surface": "#fdf6e3",
        "boost": "#eee8d5",
        "border": "#93a1a1",
        # Text
        "text": "#657b83",
        "text-muted": "#93a1a1",
        # Accent and highlights
        "accent": "#268bd2",
        "primary": "#2aa198",
        # Custom colors for entries
        "unread": "#2aa198",  # cyan
        "read": "#93a1a1",  # muted
        # Link highlighting
        "link-highlight-bg": "#d33682",  # magenta for contrast
        "link-highlight-fg": "#fdf6e3",  # light text on dark background
    },
)

# Theme registry
THEMES: dict[str, Theme] = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
}


def get_theme(name: str) -> Theme:
    """Get a theme by name.

    Args:
        name: Theme name ("dark" or "light")

    Returns:
        Theme object

    Raises:
        ValueError: If theme name not found
    """
    if name not in THEMES:
        msg = f"Theme '{name}' not found. Available themes: {', '.join(THEMES.keys())}"
        raise ValueError(msg)
    return THEMES[name]


def get_available_themes() -> list[str]:
    """Get list of available theme names.

    Returns:
        List of theme names
    """
    return list(THEMES.keys())
