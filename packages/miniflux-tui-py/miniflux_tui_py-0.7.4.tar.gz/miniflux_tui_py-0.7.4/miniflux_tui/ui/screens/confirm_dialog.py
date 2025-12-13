# SPDX-License-Identifier: MIT
"""Confirmation dialog screen for destructive operations."""

from collections.abc import Callable
from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, Static


class ConfirmDialog(Screen):
    """Generic confirmation dialog for destructive actions.

    Attributes:
        title: Dialog title
        message: Confirmation message
        on_confirm: Callback function when user confirms
        on_cancel: Optional callback when user cancels
        confirm_label: Label for confirm button (default: "Confirm")
        cancel_label: Label for cancel button (default: "Cancel")
    """

    BINDINGS: ClassVar = [
        Binding("y", "confirm", "Yes", show=True),
        Binding("n", "cancel", "No", show=True),
        Binding("enter", "confirm", "Confirm", show=False),
        Binding("escape", "cancel", "Cancel", show=False),
    ]

    CSS = """
    ConfirmDialog {
        align: center middle;
    }

    ConfirmDialog > Vertical {
        width: 60;
        height: auto;
        border: solid $error;
        background: $panel;
    }

    ConfirmDialog #dialog-title {
        dock: top;
        height: 1;
        padding: 1 2;
        background: $error;
        color: $text;
        text-align: center;
        text-style: bold;
    }

    ConfirmDialog #dialog-content {
        height: auto;
        padding: 1 2;
    }

    ConfirmDialog #dialog-message {
        height: auto;
        margin-bottom: 1;
    }

    ConfirmDialog #dialog-buttons {
        height: auto;
        padding: 1 2;
        align: center middle;
    }

    ConfirmDialog Button {
        margin: 0 1;
    }

    ConfirmDialog #confirm-button {
        variant: error;
    }

    ConfirmDialog #cancel-button {
        variant: default;
    }
    """

    def __init__(
        self,
        title: str,
        message: str,
        on_confirm: Callable[[], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
        confirm_label: str = "Confirm",
        cancel_label: str = "Cancel",
        **kwargs,
    ):
        """Initialize confirmation dialog.

        Args:
            title: Dialog title
            message: Confirmation message
            on_confirm: Callback when user confirms
            on_cancel: Callback when user cancels
            confirm_label: Label for confirm button
            cancel_label: Label for cancel button

        Raises:
            TypeError: If callbacks are not callable
        """
        super().__init__(**kwargs)
        self.dialog_title = title
        self.dialog_message = message

        # Validate callbacks are callable before storing
        if on_confirm is not None and not callable(on_confirm):
            msg = "on_confirm must be callable or None"
            raise TypeError(msg)
        if on_cancel is not None and not callable(on_cancel):
            msg = "on_cancel must be callable or None"
            raise TypeError(msg)

        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.confirm_label = confirm_label
        self.cancel_label = cancel_label

    def compose(self) -> ComposeResult:
        """Create dialog layout."""
        with Vertical(id="dialog-container"):
            yield Static(self.dialog_title, id="dialog-title")
            with Container(id="dialog-content"):
                yield Label(self.dialog_message, id="dialog-message")
            with Horizontal(id="dialog-buttons"):
                yield Button(self.confirm_label, id="confirm-button", variant="error")
                yield Button(self.cancel_label, id="cancel-button", variant="default")

    def on_mount(self) -> None:
        """Focus cancel button by default (safer)."""
        cancel_button = self.query_one("#cancel-button", Button)
        cancel_button.focus()

    def action_confirm(self) -> None:
        """Handle confirm action."""
        if self.on_confirm:
            self.on_confirm()
        self.app.pop_screen()

    def action_cancel(self) -> None:
        """Handle cancel action."""
        if self.on_cancel:
            self.on_cancel()
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "confirm-button":
            self.action_confirm()
        elif event.button.id == "cancel-button":
            self.action_cancel()
