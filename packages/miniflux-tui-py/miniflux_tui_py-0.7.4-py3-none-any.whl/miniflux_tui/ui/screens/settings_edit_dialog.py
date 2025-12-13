# SPDX-License-Identifier: MIT
"""Dialog for editing user settings."""

from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Input, Label, Select, Static


class SettingsEditDialog(ModalScreen[dict | None]):
    """Modal dialog for editing user settings."""

    BINDINGS: list[Binding] = [  # noqa: RUF012
        Binding("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
    SettingsEditDialog {
        align: center middle;
    }

    #dialog {
        width: 70;
        height: auto;
        max-height: 90%;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }

    #dialog-content {
        height: auto;
        max-height: 30;
    }

    #button-container {
        height: auto;
        width: 100%;
        align: center middle;
        padding-top: 1;
    }

    .setting-row {
        height: auto;
        width: 100%;
        padding: 0 1;
    }

    .setting-label {
        width: 24;
        padding-right: 1;
    }

    .setting-input {
        width: 1fr;
    }
    """

    # Available options for dropdowns
    TIMEZONES: ClassVar[list[str]] = [
        "UTC",
        "America/New_York",
        "America/Chicago",
        "America/Denver",
        "America/Los_Angeles",
        "Europe/London",
        "Europe/Paris",
        "Europe/Berlin",
        "Asia/Tokyo",
        "Asia/Shanghai",
        "Australia/Sydney",
    ]

    LANGUAGES: ClassVar[list[tuple[str, str]]] = [
        ("English", "en_US"),
        ("German", "de_DE"),
        ("Spanish", "es_ES"),
        ("French", "fr_FR"),
        ("Italian", "it_IT"),
        ("Japanese", "ja_JP"),
        ("Dutch", "nl_NL"),
        ("Polish", "pl_PL"),
        ("Portuguese (Brazil)", "pt_BR"),
        ("Russian", "ru_RU"),
        ("Chinese (Simplified)", "zh_CN"),
    ]

    THEMES: ClassVar[list[tuple[str, str]]] = [
        ("System Serif", "system_serif"),
        ("System Sans-Serif", "system_sans_serif"),
        ("Light Serif", "light_serif"),
        ("Light Sans-Serif", "light_sans_serif"),
        ("Dark Serif", "dark_serif"),
        ("Dark Sans-Serif", "dark_sans_serif"),
        ("Light High Contrast", "light_high_contrast"),
        ("Dark High Contrast", "dark_high_contrast"),
    ]

    SORT_ORDERS: ClassVar[list[tuple[str, str]]] = [
        ("Published Date", "published_at"),
        ("Created Date", "created_at"),
        ("Status", "status"),
        ("Title", "title"),
    ]

    SORT_DIRECTIONS: ClassVar[list[tuple[str, str]]] = [("Descending (Newest First)", "desc"), ("Ascending (Oldest First)", "asc")]

    def __init__(self, current_settings: dict, **kwargs):
        """Initialize the settings edit dialog.

        Args:
            current_settings: Dictionary of current setting values
        """
        super().__init__(**kwargs)
        self.current_settings = current_settings

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with VerticalScroll(id="dialog"):
            yield Static("[bold cyan]Edit User Settings[/bold cyan]\n", id="title")

            with VerticalScroll(id="dialog-content"):
                # Timezone
                yield Label("Timezone:")
                timezone_options = [(tz, tz) for tz in self.TIMEZONES]
                current_tz = self.current_settings.get("timezone", "UTC")
                if current_tz not in self.TIMEZONES:
                    timezone_options.insert(0, (current_tz, current_tz))
                yield Select(timezone_options, value=current_tz, id="timezone", allow_blank=False)

                # Language
                yield Label("Language:")
                current_lang = self.current_settings.get("language", "en_US")
                # Create a copy of languages list with current language ensured
                lang_options = list(self.LANGUAGES)
                lang_values = [value for _, value in lang_options]
                if current_lang not in lang_values:
                    lang_options.insert(0, (current_lang, current_lang))
                yield Select(lang_options, value=current_lang, id="language", allow_blank=False)

                # Theme
                yield Label("Theme:")
                current_theme = self.current_settings.get("theme", "system_serif")
                theme_options = list(self.THEMES)
                theme_values = [value for _, value in theme_options]
                if current_theme not in theme_values:
                    theme_options.insert(0, (current_theme, current_theme))
                yield Select(theme_options, value=current_theme, id="theme", allow_blank=False)

                # Entries per page
                yield Label("Entries per page:")
                yield Input(str(self.current_settings.get("entries_per_page", 100)), id="entries_per_page", type="integer")

                # Sort order
                yield Label("Entry sort order:")
                current_order = self.current_settings.get("entry_sorting_order", "published_at")
                yield Select(self.SORT_ORDERS, value=current_order, id="entry_sorting_order", allow_blank=False)

                # Sort direction
                yield Label("Entry sort direction:")
                current_direction = self.current_settings.get("entry_sorting_direction", "desc")
                yield Select(self.SORT_DIRECTIONS, value=current_direction, id="entry_sorting_direction", allow_blank=False)

                # Boolean settings
                yield Checkbox("Enable keyboard shortcuts", self.current_settings.get("keyboard_shortcuts", True), id="keyboard_shortcuts")
                yield Checkbox("Show reading time", self.current_settings.get("show_reading_time", True), id="show_reading_time")
                yield Checkbox("Mark as read on view", self.current_settings.get("mark_read_on_view", False), id="mark_read_on_view")

            # Buttons
            with Grid(id="button-container"):
                yield Button("Save", variant="primary", id="save")
                yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "save":
            self.action_save()
        elif event.button.id == "cancel":
            self.action_cancel()

    def action_save(self) -> None:
        """Save the settings and dismiss."""
        try:
            # Gather all settings from widgets
            settings = {}

            # Get values from Select widgets
            timezone_select = self.query_one("#timezone", Select)
            if timezone_select.value is not None:
                settings["timezone"] = timezone_select.value

            language_select = self.query_one("#language", Select)
            if language_select.value is not None:
                settings["language"] = language_select.value

            theme_select = self.query_one("#theme", Select)
            if theme_select.value is not None:
                settings["theme"] = theme_select.value

            order_select = self.query_one("#entry_sorting_order", Select)
            if order_select.value is not None:
                settings["entry_sorting_order"] = order_select.value

            direction_select = self.query_one("#entry_sorting_direction", Select)
            if direction_select.value is not None:
                settings["entry_sorting_direction"] = direction_select.value

            # Get entries per page
            entries_input = self.query_one("#entries_per_page", Input)
            try:
                entries_per_page = int(entries_input.value or "100")
                if entries_per_page > 0:
                    settings["entries_per_page"] = entries_per_page
            except ValueError:
                self.app.notify("Invalid entries per page value", severity="warning")
                return

            # Get checkbox values
            settings["keyboard_shortcuts"] = self.query_one("#keyboard_shortcuts", Checkbox).value
            settings["show_reading_time"] = self.query_one("#show_reading_time", Checkbox).value
            settings["mark_read_on_view"] = self.query_one("#mark_read_on_view", Checkbox).value

            # Dismiss with settings
            self.dismiss(settings)

        except Exception as e:
            self.app.log(f"Error saving settings: {e}")
            self.app.notify(f"Error: {e}", severity="error")

    def action_cancel(self) -> None:
        """Cancel and dismiss without saving."""
        self.dismiss(None)
