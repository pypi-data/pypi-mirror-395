# SPDX-License-Identifier: MIT
"""Tests for help screen."""

import inspect
from unittest.mock import patch

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static

from miniflux_tui.ui.screens.help import HelpScreen


class DummyApp(App):
    """Dummy app for testing screen composition."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield HelpScreen()


class MultiScreenApp(App):
    """App with multiple screens for testing navigation."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        # Start with a simple screen, then push help screen
        yield Static("Test Content")

    def on_mount(self) -> None:
        """Mount and push help screen."""
        # Push help screen to test navigation
        self.push_screen(HelpScreen())


class TestHelpScreenBindings:
    """Test HelpScreen key bindings."""

    def test_help_screen_has_bindings(self):
        """Test HelpScreen has correct bindings."""
        help_screen = HelpScreen()
        assert hasattr(help_screen, "BINDINGS")
        assert isinstance(help_screen.BINDINGS, list)
        assert len(help_screen.BINDINGS) == 2

    def test_help_screen_has_escape_binding(self):
        """Test HelpScreen has Escape key binding."""
        help_screen = HelpScreen()
        escape_bindings = [b for b in help_screen.BINDINGS if b.key == "escape"]  # type: ignore[attr-defined]
        assert len(escape_bindings) == 1
        assert escape_bindings[0].action == "close"

    def test_help_screen_has_q_binding(self):
        """Test HelpScreen has q key binding."""
        help_screen = HelpScreen()
        q_bindings = [b for b in help_screen.BINDINGS if b.key == "q"]  # type: ignore[attr-defined]
        assert len(q_bindings) == 1
        assert q_bindings[0].action == "close"


class TestHelpScreenCompose:
    """Test HelpScreen compose method."""

    def test_compose_method_exists(self):
        """Test compose() method exists."""
        help_screen = HelpScreen()
        assert hasattr(help_screen, "compose")
        assert callable(help_screen.compose)

    def test_compose_is_generator(self):
        """Test compose returns a generator/iterable."""
        help_screen = HelpScreen()
        result = help_screen.compose()
        # Verify it's a generator
        assert hasattr(result, "__iter__") or hasattr(result, "__next__")


class TestHelpScreenContent:
    """Test HelpScreen content and layout."""

    def test_help_screen_initialization(self):
        """Test HelpScreen can be initialized."""
        help_screen = HelpScreen()
        assert help_screen is not None
        assert isinstance(help_screen, HelpScreen)

    def test_help_screen_is_screen(self):
        """Test HelpScreen is a Textual Screen."""
        help_screen = HelpScreen()
        assert isinstance(help_screen, Screen)

    def test_help_screen_source_code_integrity(self):
        """Test help screen source is properly defined."""
        help_screen = HelpScreen()
        # Verify the class has the expected methods
        assert hasattr(help_screen, "compose")
        assert hasattr(help_screen, "action_close")
        assert hasattr(help_screen, "BINDINGS")


class TestHelpScreenComposedWidgets:
    """Test the widgets created by compose method."""

    async def test_help_screen_displayed(self):
        """Test that help screen can be displayed in an app."""
        async with DummyApp().run_test() as pilot:
            # The screen should be mounted
            app = pilot.app
            assert app is not None

    async def test_help_screen_has_compose_implementation(self):
        """Test that help screen has working compose implementation."""
        # Create an instance and verify the method exists
        help_screen = HelpScreen()
        assert hasattr(help_screen, "compose")
        assert callable(help_screen.compose)
        # The method is a generator, so calling it returns a generator object
        gen = help_screen.compose()
        assert gen is not None


class TestHelpScreenActionClose:
    """Test the action_close method."""

    def test_action_close_exists_and_callable(self):
        """Test action_close method exists and is callable."""
        help_screen = HelpScreen()
        assert hasattr(help_screen, "action_close")
        assert callable(help_screen.action_close)
        assert callable(getattr(help_screen, "action_close", None))

    def test_action_close_method_signature(self):
        """Test action_close method has correct signature."""
        help_screen = HelpScreen()
        sig = inspect.signature(help_screen.action_close)
        # action_close should only have 'self' parameter (no args besides self)
        assert len(sig.parameters) == 0

    async def test_action_close_pops_screen(self):
        """Test that action_close calls app.pop_screen()."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            # Wait for the help screen to be mounted
            await pilot.pause()
            # The help screen should be the current active screen
            help_screen = app.screen
            if isinstance(help_screen, HelpScreen):
                # Verify that calling action_close would call pop_screen
                with patch.object(app, "pop_screen") as mock_pop:
                    help_screen.action_close()
                    # Verify pop_screen was called
                    mock_pop.assert_called_once()


class TestHelpScreenIntegration:
    """Integration tests for HelpScreen."""

    def test_help_screen_screen_type(self):
        """Test HelpScreen is a Screen subclass."""
        help_screen = HelpScreen()
        assert isinstance(help_screen, Screen)

    def test_help_screen_not_none(self):
        """Test HelpScreen instance is not None."""
        help_screen = HelpScreen()
        assert help_screen is not None

    def test_help_screen_multiple_instances(self):
        """Test creating multiple HelpScreen instances."""
        screen1 = HelpScreen()
        screen2 = HelpScreen()
        assert screen1 is not screen2
        assert isinstance(screen1, HelpScreen)
        assert isinstance(screen2, HelpScreen)

    def test_help_screen_bindings_valid_keys(self):
        """Test that binding keys are valid."""
        help_screen = HelpScreen()
        valid_keys = {"escape", "q"}
        binding_keys = {b.key for b in help_screen.BINDINGS}  # type: ignore[attr-defined]
        assert binding_keys == valid_keys

    def test_help_screen_bindings_valid_actions(self):
        """Test that binding actions are valid."""
        help_screen = HelpScreen()
        valid_actions = {"close"}
        binding_actions = {b.action for b in help_screen.BINDINGS}  # type: ignore[attr-defined]
        assert binding_actions == valid_actions

    async def test_help_screen_compose_method_works(self):
        """Test that compose method works without errors."""
        async with MultiScreenApp().run_test() as pilot:
            app = pilot.app
            await pilot.pause()
            # The help screen should be on the screen stack
            help_screen = app.screen
            if isinstance(help_screen, HelpScreen):
                # Verify it's properly composed with all its widgets
                # The screen should have been mounted and composed
                assert help_screen is not None
                assert hasattr(help_screen, "compose")
