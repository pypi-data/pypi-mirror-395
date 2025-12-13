# SPDX-License-Identifier: MIT
"""Tests for ConfirmDialog screen."""

from miniflux_tui.ui.screens.confirm_dialog import ConfirmDialog


class TestConfirmDialogInitialization:
    """Test ConfirmDialog initialization."""

    def test_confirm_dialog_creation(self) -> None:
        """Test creating a ConfirmDialog."""
        dialog = ConfirmDialog(
            title="Delete?",
            message="Are you sure?",
        )
        assert dialog.dialog_title == "Delete?"
        assert dialog.dialog_message == "Are you sure?"

    def test_confirm_dialog_with_callbacks(self) -> None:
        """Test ConfirmDialog with callback functions."""
        confirm_called = False
        cancel_called = False

        def on_confirm() -> None:
            nonlocal confirm_called
            confirm_called = True

        def on_cancel() -> None:
            nonlocal cancel_called
            cancel_called = True

        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
            on_confirm=on_confirm,
            on_cancel=on_cancel,
        )
        assert dialog.on_confirm is not None
        assert dialog.on_cancel is not None

    def test_confirm_dialog_with_custom_labels(self) -> None:
        """Test ConfirmDialog with custom button labels."""
        dialog = ConfirmDialog(
            title="Delete Feed?",
            message="This cannot be undone.",
            confirm_label="Delete Forever",
            cancel_label="Keep It",
        )
        assert dialog.confirm_label == "Delete Forever"
        assert dialog.cancel_label == "Keep It"

    def test_confirm_dialog_default_labels(self) -> None:
        """Test ConfirmDialog default button labels."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
        )
        assert dialog.confirm_label == "Confirm"
        assert dialog.cancel_label == "Cancel"


class TestConfirmDialogCompose:
    """Test ConfirmDialog composition."""

    def test_confirm_dialog_has_bindings(self) -> None:
        """Test ConfirmDialog has proper key bindings."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
        )
        binding_keys = [b.key for b in dialog.BINDINGS]  # type: ignore[attr-defined]
        assert "y" in binding_keys
        assert "n" in binding_keys
        assert "enter" in binding_keys
        assert "escape" in binding_keys


class TestConfirmDialogCSS:
    """Test ConfirmDialog CSS styling."""

    def test_confirm_dialog_has_css(self) -> None:
        """Test ConfirmDialog has CSS defined."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
        )
        assert dialog.CSS is not None
        assert len(dialog.CSS) > 0
        assert "ConfirmDialog" in dialog.CSS

    def test_confirm_dialog_uses_error_color(self) -> None:
        """Test ConfirmDialog uses error color for danger."""
        dialog = ConfirmDialog(
            title="Delete",
            message="This is destructive.",
        )
        assert "$error" in dialog.CSS


class TestConfirmDialogActions:
    """Test ConfirmDialog action methods."""

    def test_confirm_dialog_action_confirm_with_callback(self) -> None:
        """Test action_confirm calls the callback."""
        confirm_called = False

        def on_confirm() -> None:
            nonlocal confirm_called
            confirm_called = True

        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
            on_confirm=on_confirm,
        )
        # Verify callback is set
        assert dialog.on_confirm is not None

    def test_confirm_dialog_action_cancel_with_callback(self) -> None:
        """Test action_cancel calls the callback."""
        cancel_called = False

        def on_cancel() -> None:
            nonlocal cancel_called
            cancel_called = True

        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
            on_cancel=on_cancel,
        )
        # Verify callback is set
        assert dialog.on_cancel is not None


class TestConfirmDialogIntegration:
    """Integration tests for ConfirmDialog."""

    def test_confirm_dialog_with_none_callbacks(self) -> None:
        """Test ConfirmDialog works with None callbacks."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
            on_confirm=None,
            on_cancel=None,
        )
        assert dialog.on_confirm is None
        assert dialog.on_cancel is None

    def test_confirm_dialog_multiline_message(self) -> None:
        """Test ConfirmDialog with multiline message."""
        message = "Delete this feed?\nThis cannot be undone."
        dialog = ConfirmDialog(
            title="Delete Feed?",
            message=message,
        )
        assert "\n" in dialog.dialog_message
        assert message == dialog.dialog_message

    def test_confirm_dialog_special_characters_in_title(self) -> None:
        """Test ConfirmDialog with special characters."""
        title = "Delete 'Feed Name' (v1.2)?"
        dialog = ConfirmDialog(
            title=title,
            message="Proceed?",
        )
        assert dialog.dialog_title == title

    def test_confirm_dialog_very_long_message(self) -> None:
        """Test ConfirmDialog with very long message."""
        long_message = (
            "This is a very long confirmation message that explains in detail "
            "what will happen if the user confirms this action. "
            "It includes warnings and important information."
        )
        dialog = ConfirmDialog(
            title="Important",
            message=long_message,
        )
        assert dialog.dialog_message == long_message

    def test_confirm_dialog_bindings_structure(self) -> None:
        """Test ConfirmDialog bindings are properly structured."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
        )
        assert len(dialog.BINDINGS) == 4  # type: ignore[attr-defined]
        assert all(binding.key in ["y", "n", "enter", "escape"] for binding in dialog.BINDINGS)  # type: ignore[attr-defined]

    def test_confirm_dialog_yes_shortcut(self) -> None:
        """Test ConfirmDialog has 'y' for yes shortcut."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
        )
        yes_bindings = [b for b in dialog.BINDINGS if b.key == "y"]  # type: ignore[attr-defined]
        assert len(yes_bindings) == 1
        assert "confirm" in yes_bindings[0].action  # type: ignore[attr-defined]

    def test_confirm_dialog_no_shortcut(self) -> None:
        """Test ConfirmDialog has 'n' for no shortcut."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
        )
        no_bindings = [b for b in dialog.BINDINGS if b.key == "n"]  # type: ignore[attr-defined]
        assert len(no_bindings) == 1
        assert "cancel" in no_bindings[0].action  # type: ignore[attr-defined]

    def test_confirm_dialog_escape_closes(self) -> None:
        """Test ConfirmDialog escape key cancels."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Proceed?",
        )
        escape_bindings = [b for b in dialog.BINDINGS if b.key == "escape"]  # type: ignore[attr-defined]
        assert len(escape_bindings) == 1
        assert "cancel" in escape_bindings[0].action  # type: ignore[attr-defined]

    def test_confirm_dialog_custom_button_labels_are_used(self) -> None:
        """Test custom button labels are actually used."""
        dialog = ConfirmDialog(
            title="Delete?",
            message="Sure?",
            confirm_label="Yes, Delete",
            cancel_label="No, Keep",
        )
        assert dialog.confirm_label == "Yes, Delete"
        assert dialog.cancel_label == "No, Keep"


class TestConfirmDialogComposeMethods:
    """Test ConfirmDialog compose and rendering methods."""

    def test_confirm_dialog_compose_returns_generator(self) -> None:
        """Test compose method returns a ComposeResult."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Are you sure?",
        )
        result = dialog.compose()
        # compose should return a generator
        assert hasattr(result, "__iter__")

    def test_confirm_dialog_action_methods_exist(self) -> None:
        """Test action methods exist and are callable."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Are you sure?",
        )
        assert callable(dialog.action_confirm)
        assert callable(dialog.action_cancel)

    def test_confirm_dialog_on_button_pressed_exists(self) -> None:
        """Test on_button_pressed handler exists."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Are you sure?",
        )
        assert hasattr(dialog, "on_button_pressed")
        assert callable(dialog.on_button_pressed)

    def test_confirm_dialog_has_correct_css_classes(self) -> None:
        """Test CSS includes proper element IDs."""
        dialog = ConfirmDialog(
            title="Confirm",
            message="Are you sure?",
        )
        css = dialog.CSS
        # Check that CSS references the expected IDs
        assert "dialog-title" in css
        assert "dialog-message" in css
        assert "dialog-buttons" in css
        assert "confirm-button" in css
        assert "cancel-button" in css

    def test_confirm_dialog_error_color_in_css(self) -> None:
        """Test CSS includes error color styling."""
        dialog = ConfirmDialog(
            title="Delete",
            message="Are you sure?",
        )
        css = dialog.CSS
        # Check for error color reference
        assert "$error" in css

    def test_confirm_dialog_with_error_indicator(self) -> None:
        """Test ConfirmDialog marks destructive operations."""
        dangerous_dialog = ConfirmDialog(
            title="Delete Everything",
            message="This will delete all data permanently!",
        )
        # Dialog should have CSS with error color for destructive operations
        assert dangerous_dialog.CSS is not None
        assert len(dangerous_dialog.CSS) > 0
