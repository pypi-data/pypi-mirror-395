# SPDX-License-Identifier: MIT
"""Tests for SettingsEditDialog."""

from textual.app import App

from miniflux_tui.ui.screens.settings_edit_dialog import SettingsEditDialog


class SettingsEditTestApp(App):
    """Test app for SettingsEditDialog testing."""

    def on_mount(self) -> None:
        """Mount the settings edit dialog."""
        current_settings = {
            "timezone": "UTC",
            "language": "en_US",
            "theme": "system_serif",
            "entries_per_page": 100,
            "entry_sorting_order": "published_at",
            "entry_sorting_direction": "desc",
            "keyboard_shortcuts": True,
            "show_reading_time": True,
            "mark_read_on_view": False,
        }
        self.push_screen(SettingsEditDialog(current_settings))


class TestSettingsEditDialogInitialization:
    """Test SettingsEditDialog initialization."""

    def test_dialog_creation(self) -> None:
        """Test creating a SettingsEditDialog."""
        settings = {"timezone": "UTC", "language": "en_US"}
        dialog = SettingsEditDialog(settings)
        assert dialog.current_settings == settings

    def test_dialog_has_bindings(self) -> None:
        """Test that dialog has proper key bindings."""
        dialog = SettingsEditDialog({})
        binding_keys = [binding.key for binding in dialog.BINDINGS]
        assert "escape" in binding_keys


class TestSettingsEditDialogComposition:
    """Test SettingsEditDialog composition."""

    async def test_dialog_composes_with_widgets(self) -> None:
        """Test that dialog composes with all required widgets."""
        app = SettingsEditTestApp()

        async with app.run_test():
            # The dialog is pushed as a screen
            dialog = app.screen
            # Check that key widgets exist
            assert dialog.query_one("#timezone")
            assert dialog.query_one("#language")
            assert dialog.query_one("#theme")
            assert dialog.query_one("#entries_per_page")
            assert dialog.query_one("#entry_sorting_order")
            assert dialog.query_one("#entry_sorting_direction")
            assert dialog.query_one("#keyboard_shortcuts")
            assert dialog.query_one("#show_reading_time")
            assert dialog.query_one("#mark_read_on_view")
            assert dialog.query_one("#save")
            assert dialog.query_one("#cancel")


class TestSettingsEditDialogActions:
    """Test SettingsEditDialog actions."""

    async def test_cancel_dismisses_with_none(self) -> None:
        """Test that cancel button dismisses with None."""
        app = SettingsEditTestApp()

        async with app.run_test():
            dialog = app.screen

            # Mock dismiss to capture result
            captured_result = []

            def mock_dismiss(value):
                captured_result.append(value)
                # Don't call original to avoid actual dismissal

            dialog.dismiss = mock_dismiss  # type: ignore[method-assign]

            # Trigger cancel action
            dialog.action_cancel()  # type: ignore[attr-defined]

            # Should dismiss with None
            assert len(captured_result) == 1
            assert captured_result[0] is None

    async def test_save_gathers_settings(self) -> None:
        """Test that save button gathers all settings."""
        app = SettingsEditTestApp()

        async with app.run_test():
            dialog = app.screen

            # Mock dismiss to capture result
            captured_result = []

            def mock_dismiss(value):
                captured_result.append(value)

            dialog.dismiss = mock_dismiss  # type: ignore[method-assign]

            # Trigger save action
            dialog.action_save()  # type: ignore[attr-defined]

            # Should have captured settings
            assert len(captured_result) == 1
            settings = captured_result[0]
            assert isinstance(settings, dict)
            assert "timezone" in settings
            assert "language" in settings
            assert "theme" in settings
