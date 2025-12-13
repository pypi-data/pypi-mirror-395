# SPDX-License-Identifier: MIT
"""Input dialog screen for requesting user input."""

from collections.abc import Callable
from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static


class InputDialog(Screen):
    """Generic input dialog for collecting user text input.

    Attributes:
        title: Dialog title
        label: Label for the input field
        value: Initial value (optional)
        on_submit: Callback function when user confirms
        on_cancel: Optional callback when user cancels
    """

    BINDINGS: ClassVar = [
        Binding("enter", "submit", "Submit", show=True),
        Binding("escape", "cancel", "Cancel", show=True),
    ]

    CSS = """
    InputDialog {
        align: center middle;
    }

    InputDialog > Vertical {
        width: 60;
        height: auto;
        border: solid $accent;
        background: $panel;
    }

    InputDialog #dialog-title {
        dock: top;
        height: 1;
        padding: 1 2;
        background: $accent;
        color: $text;
        text-align: center;
        text-style: bold;
    }

    InputDialog #dialog-content {
        height: auto;
        padding: 1 2;
    }

    InputDialog #dialog-label {
        height: auto;
        margin-bottom: 1;
    }

    InputDialog #dialog-input {
        margin-bottom: 1;
    }

    InputDialog #dialog-buttons {
        height: auto;
        padding: 1 2;
        align: center middle;
    }

    InputDialog Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        title: str,
        label: str,
        value: str = "",
        on_submit: Callable[[str], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
        **kwargs,
    ):
        """Initialize input dialog.

        Args:
            title: Dialog title
            label: Input field label
            value: Initial value for input
            on_submit: Callback when user confirms (receives input value)
            on_cancel: Callback when user cancels

        Raises:
            TypeError: If callbacks are not callable
        """
        super().__init__(**kwargs)
        self.dialog_title = title
        self.dialog_label = label
        self.initial_value = value

        # Validate callbacks are callable before storing
        if on_submit is not None and not callable(on_submit):
            msg = "on_submit must be callable or None"
            raise TypeError(msg)
        if on_cancel is not None and not callable(on_cancel):
            msg = "on_cancel must be callable or None"
            raise TypeError(msg)

        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.input_widget: Input | None = None

    def compose(self) -> ComposeResult:
        """Create dialog layout."""
        with Vertical(id="dialog-container"):
            yield Static(self.dialog_title, id="dialog-title")
            with Container(id="dialog-content"):
                yield Label(self.dialog_label, id="dialog-label")
                yield Input(value=self.initial_value, id="dialog-input")
            with Horizontal(id="dialog-buttons"):
                yield Button("Submit", id="submit-button", variant="primary")
                yield Button("Cancel", id="cancel-button", variant="default")

    def on_mount(self) -> None:
        """Focus input field when dialog is shown."""
        self.input_widget = self.query_one("#dialog-input", Input)
        self.input_widget.focus()
        if self.initial_value:
            # Select all text if there's an initial value
            self.input_widget.select_all()

    def action_submit(self) -> None:
        """Handle submit action."""
        if self.input_widget and self.on_submit:
            self.on_submit(self.input_widget.value)
        self.app.pop_screen()

    def action_cancel(self) -> None:
        """Handle cancel action."""
        if self.on_cancel:
            self.on_cancel()
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "submit-button":
            self.action_submit()
        elif event.button.id == "cancel-button":
            self.action_cancel()
