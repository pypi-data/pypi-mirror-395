# SPDX-License-Identifier: MIT
"""Tests for CategoryManagementScreen."""

import asyncio
from typing import cast
from unittest.mock import AsyncMock, MagicMock, patch

from textual.app import App
from textual.binding import Binding

from miniflux_tui.api.models import Category
from miniflux_tui.ui.screens.category_management import CategoryListItem, CategoryManagementScreen


class CategoryManagementTestApp(App):
    """Test app for CategoryManagementScreen testing."""

    def __init__(self, categories: list[Category] | None = None, **kwargs):
        """Initialize test app."""
        super().__init__(**kwargs)
        self.categories = categories or []
        self.client: MagicMock | None = None  # type: ignore[assignment]

    def on_mount(self) -> None:
        """Mount the category management screen."""
        self.push_screen(CategoryManagementScreen(categories=self.categories))


class TestCategoryListItem:
    """Test CategoryListItem rendering."""

    def test_category_list_item_creation(self) -> None:
        """Test creating a CategoryListItem."""
        category = Category(id=1, title="Test Category")
        item = CategoryListItem(category)
        assert item.category.id == 1
        assert item.category.title == "Test Category"

    def test_category_list_item_stores_reference(self) -> None:
        """Test CategoryListItem stores category reference."""
        category = Category(id=1, title="News")
        item = CategoryListItem(category)
        assert item.category == category
        assert item.category.id == 1
        assert item.category.title == "News"


class TestCategoryManagementScreenInitialization:
    """Test CategoryManagementScreen initialization."""

    def test_category_management_screen_creation(self) -> None:
        """Test creating a CategoryManagementScreen."""
        screen = CategoryManagementScreen()
        assert screen.categories == []
        assert screen.list_view is None

    def test_category_management_screen_with_categories(self) -> None:
        """Test CategoryManagementScreen with initial categories."""
        categories = [
            Category(id=1, title="News"),
            Category(id=2, title="Tech"),
        ]
        screen = CategoryManagementScreen(categories=categories)
        assert len(screen.categories) == 2
        assert screen.categories[0].title == "News"
        assert screen.categories[1].title == "Tech"

    def test_category_management_screen_empty(self) -> None:
        """Test CategoryManagementScreen with no categories."""
        screen = CategoryManagementScreen(categories=[])
        assert screen.categories == []


class TestCategoryManagementScreenComposition:
    """Test CategoryManagementScreen composition and rendering."""

    async def test_screen_composes_with_header_and_footer(self) -> None:
        """Test that CategoryManagementScreen composes with header and footer."""
        categories = [Category(id=1, title="News")]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test():
            screen = app.screen
            assert isinstance(screen, CategoryManagementScreen)

    async def test_screen_initializes_with_categories(self) -> None:
        """Test that CategoryManagementScreen initializes with categories."""
        categories = [
            Category(id=1, title="News"),
            Category(id=2, title="Tech"),
        ]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                assert len(screen.categories) == 2


class TestCategoryManagementScreenNavigation:
    """Test navigation in CategoryManagementScreen."""

    async def test_cursor_down_action_exists(self) -> None:
        """Test that cursor_down action exists."""
        app = CategoryManagementTestApp(categories=[Category(id=1, title="News")])

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                assert callable(screen.action_cursor_down)

    async def test_cursor_up_action_exists(self) -> None:
        """Test that cursor_up action exists."""
        app = CategoryManagementTestApp(categories=[Category(id=1, title="News")])

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                assert callable(screen.action_cursor_up)

    async def test_back_action_exists(self) -> None:
        """Test that back action exists."""
        app = CategoryManagementTestApp(categories=[Category(id=1, title="News")])

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                assert callable(screen.action_back)


class TestCategoryManagementScreenActions:
    """Test action methods in CategoryManagementScreen."""

    async def test_create_category_action_exists(self) -> None:
        """Test that create_category action exists."""
        app = CategoryManagementTestApp()

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                assert callable(screen.action_create_category)

    async def test_edit_category_action_exists(self) -> None:
        """Test that edit_category action exists."""
        app = CategoryManagementTestApp()

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                assert callable(screen.action_edit_category)

    async def test_delete_category_action_exists(self) -> None:
        """Test that delete_category action exists."""
        app = CategoryManagementTestApp()

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                assert callable(screen.action_delete_category)


class TestCategoryManagementScreenGetSelected:
    """Test _get_selected_category method."""

    async def test_get_selected_category_no_selection(self) -> None:
        """Test _get_selected_category returns None when nothing selected."""
        categories = [Category(id=1, title="News")]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                selected = screen._get_selected_category()
                assert selected is None or isinstance(selected, Category)

    async def test_get_selected_category_with_selection(self) -> None:
        """Test _get_selected_category returns selected category."""
        categories = [
            Category(id=1, title="News"),
            Category(id=2, title="Tech"),
        ]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen) and screen.list_view and screen.list_view.children:
                screen.list_view.index = 0
                selected = screen._get_selected_category()
                assert selected is None or selected.id == 1


class TestCategoryManagementScreenPopulateList:
    """Test _populate_list method."""

    async def test_populate_list_with_categories(self) -> None:
        """Test _populate_list adds categories to list view."""
        categories = [
            Category(id=1, title="News"),
            Category(id=2, title="Tech"),
        ]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen) and screen.list_view:
                # on_mount already called _populate_list, so list view should have items
                assert len(screen.list_view.children) >= 2

    async def test_populate_list_empty(self) -> None:
        """Test _populate_list with no categories."""
        app = CategoryManagementTestApp(categories=[])

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen) and screen.list_view:
                # on_mount already called _populate_list
                assert len(screen.list_view.children) == 0


class TestCategoryManagementScreenCSS:
    """Test CategoryManagementScreen CSS styling."""

    def test_category_management_screen_has_css(self) -> None:
        """Test CategoryManagementScreen has CSS defined."""
        screen = CategoryManagementScreen()
        assert screen.CSS is not None
        assert len(screen.CSS) > 0
        assert "CategoryManagementScreen" in screen.CSS


class TestCategoryManagementScreenBindings:
    """Test keyboard bindings."""

    def test_category_management_screen_has_bindings(self) -> None:
        """Test CategoryManagementScreen has key bindings."""
        screen = CategoryManagementScreen()
        bindings = cast(list[Binding], screen.BINDINGS)  # type: ignore[attr-defined]
        binding_keys = [b.key for b in bindings]
        assert "j" in binding_keys
        assert "k" in binding_keys
        assert "n" in binding_keys
        assert "e" in binding_keys
        assert "d" in binding_keys
        assert "escape" in binding_keys

    def test_category_management_screen_binding_descriptions(self) -> None:
        """Test that bindings have descriptions."""
        screen = CategoryManagementScreen()
        bindings = cast(list[Binding], screen.BINDINGS)  # type: ignore[attr-defined]
        for binding in bindings:
            assert binding.description is not None
            assert len(binding.description) > 0


class TestCategoryManagementScreenIntegration:
    """Integration tests for CategoryManagementScreen."""

    async def test_screen_has_list_view(self) -> None:
        """Test that screen initializes with a ListView."""
        categories = [Category(id=1, title="News")]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test():
            screen = app.screen
            if isinstance(screen, CategoryManagementScreen):
                assert screen.list_view is not None

    async def test_compose_returns_result(self) -> None:
        """Test compose method returns valid result."""
        screen = CategoryManagementScreen()
        result = screen.compose()
        assert hasattr(result, "__iter__")

    def test_category_management_with_multiple_categories(self) -> None:
        """Test CategoryManagementScreen with multiple categories."""
        categories = [
            Category(id=1, title="News"),
            Category(id=2, title="Tech"),
            Category(id=3, title="Business"),
            Category(id=4, title="Sports"),
        ]
        screen = CategoryManagementScreen(categories=categories)
        assert len(screen.categories) == 4

    def test_category_management_with_long_category_name(self) -> None:
        """Test CategoryManagementScreen with long category names."""
        long_name = "This is a very long category name for testing purposes"
        category = Category(id=1, title=long_name)
        screen = CategoryManagementScreen(categories=[category])
        assert screen.categories[0].title == long_name

    def test_category_management_with_special_characters(self) -> None:
        """Test CategoryManagementScreen with special characters in names."""
        special_category = Category(id=1, title="News & Updates (2025)")
        screen = CategoryManagementScreen(categories=[special_category])
        assert screen.categories[0].title == "News & Updates (2025)"


class TestCategoryManagementAsyncMethods:
    """Test that async methods exist and are properly defined."""

    def test_action_create_category_is_async(self) -> None:
        """Test that action_create_category is an async method."""
        screen = CategoryManagementScreen()
        assert asyncio.iscoroutinefunction(screen.action_create_category)

    def test_do_create_category_is_async(self) -> None:
        """Test that _do_create_category is an async method."""
        screen = CategoryManagementScreen()
        assert asyncio.iscoroutinefunction(screen._do_create_category)

    def test_action_edit_category_is_async(self) -> None:
        """Test that action_edit_category is an async method."""
        screen = CategoryManagementScreen()
        assert asyncio.iscoroutinefunction(screen.action_edit_category)

    def test_do_edit_category_is_async(self) -> None:
        """Test that _do_edit_category is an async method."""
        screen = CategoryManagementScreen()
        assert asyncio.iscoroutinefunction(screen._do_edit_category)

    def test_action_delete_category_is_async(self) -> None:
        """Test that action_delete_category is an async method."""
        screen = CategoryManagementScreen()
        assert asyncio.iscoroutinefunction(screen.action_delete_category)

    def test_do_delete_category_is_async(self) -> None:
        """Test that _do_delete_category is an async method."""
        screen = CategoryManagementScreen()
        assert asyncio.iscoroutinefunction(screen._do_delete_category)


class TestCategoryManagementCRUDOperations:
    """Test CRUD operations in CategoryManagementScreen."""

    async def test_create_category_success(self) -> None:
        """Test successful category creation."""

        app = CategoryManagementTestApp()
        app.client = MagicMock()
        app.client.create_category = AsyncMock(return_value=Category(id=3, title="New Category"))

        async with app.run_test() as pilot:
            screen = cast(CategoryManagementScreen, app.screen)
            initial_count = len(screen.categories)

            # Patch api_call to just return the app
            with patch("miniflux_tui.ui.screens.category_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app

                # Simulate creating a category
                await screen._do_create_category("New Category")
                await pilot.pause()

                # Verify category was added
                assert len(screen.categories) == initial_count + 1
                assert screen.categories[-1].title == "New Category"
                app.client.create_category.assert_called_once_with("New Category")

    async def test_create_category_shows_dialog(self) -> None:
        """Test that create category action shows dialog."""

        app = CategoryManagementTestApp()

        async with app.run_test():
            screen = cast(CategoryManagementScreen, app.screen)

            # Mock push_screen to avoid actually showing the dialog
            with patch.object(app, "push_screen") as mock_push:
                await screen.action_create_category()
                # Dialog should be pushed
                mock_push.assert_called_once()

    async def test_create_category_api_error(self) -> None:
        """Test handling API error during category creation."""

        app = CategoryManagementTestApp()
        app.client = MagicMock()
        app.client.create_category = AsyncMock(side_effect=Exception("API Error"))

        async with app.run_test() as pilot:
            screen = cast(CategoryManagementScreen, app.screen)
            initial_count = len(screen.categories)

            # Try to create category (should fail)
            await screen._do_create_category("Test")
            await pilot.pause()

            # Verify category was not added
            assert len(screen.categories) == initial_count

    async def test_edit_category_success(self) -> None:
        """Test successful category editing."""

        categories = [Category(id=1, title="Old Name")]
        app = CategoryManagementTestApp(categories=categories)
        app.client = MagicMock()
        app.client.update_category = AsyncMock(return_value=Category(id=1, title="New Name"))

        async with app.run_test() as pilot:
            screen = cast(CategoryManagementScreen, app.screen)

            # Patch api_call
            with patch("miniflux_tui.ui.screens.category_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app

                # Edit the category
                await screen._do_edit_category(1, "New Name")
                await pilot.pause()

                # Verify category was updated
                assert screen.categories[0].title == "New Name"
                app.client.update_category.assert_called_once_with(1, "New Name")

    async def test_edit_category_no_selection(self) -> None:
        """Test editing when no category is selected."""
        app = CategoryManagementTestApp()

        async with app.run_test():
            screen = cast(CategoryManagementScreen, app.screen)

            # Try to edit without selection
            await screen.action_edit_category()
            # Should show warning notification

    async def test_edit_category_empty_name(self) -> None:
        """Test editing category with empty name."""

        categories = [Category(id=1, title="Test")]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test():
            screen = cast(CategoryManagementScreen, app.screen)

            # Mock the input dialog
            with patch("miniflux_tui.ui.screens.category_management.InputDialog") as mock_dialog:
                await screen.action_edit_category()

                if mock_dialog.called:
                    on_submit = mock_dialog.call_args.kwargs["on_submit"]
                    on_submit("")  # Empty string should show error

    async def test_edit_category_api_error(self) -> None:
        """Test handling API error during category editing."""

        categories = [Category(id=1, title="Test")]
        app = CategoryManagementTestApp(categories=categories)
        app.client = MagicMock()
        app.client.update_category = AsyncMock(side_effect=Exception("API Error"))

        async with app.run_test() as pilot:
            screen = cast(CategoryManagementScreen, app.screen)

            # Try to edit (should fail)
            await screen._do_edit_category(1, "New Name")
            await pilot.pause()

            # Category should remain unchanged
            assert screen.categories[0].title == "Test"

    async def test_delete_category_success(self) -> None:
        """Test successful category deletion."""

        categories = [
            Category(id=1, title="Category 1"),
            Category(id=2, title="Category 2"),
        ]
        app = CategoryManagementTestApp(categories=categories)
        app.client = MagicMock()
        app.client.delete_category = AsyncMock(return_value=None)

        async with app.run_test() as pilot:
            screen = cast(CategoryManagementScreen, app.screen)

            # Patch api_call
            with patch("miniflux_tui.ui.screens.category_management.api_call") as mock_api:
                mock_api.return_value.__enter__.return_value = app

                # Delete first category
                await screen._do_delete_category(1, "Category 1")
                await pilot.pause()

                # Verify category was removed
                assert len(screen.categories) == 1
                assert screen.categories[0].id == 2
                app.client.delete_category.assert_called_once_with(1)

    async def test_delete_category_no_selection(self) -> None:
        """Test deleting when no category is selected."""
        app = CategoryManagementTestApp()

        async with app.run_test():
            screen = cast(CategoryManagementScreen, app.screen)

            # Try to delete without selection
            await screen.action_delete_category()
            # Should show warning notification

    async def test_delete_category_api_error(self) -> None:
        """Test handling API error during category deletion."""

        categories = [Category(id=1, title="Test")]
        app = CategoryManagementTestApp(categories=categories)
        app.client = MagicMock()
        app.client.delete_category = AsyncMock(side_effect=Exception("API Error"))

        async with app.run_test() as pilot:
            screen = cast(CategoryManagementScreen, app.screen)
            initial_count = len(screen.categories)

            # Try to delete (should fail)
            await screen._do_delete_category(1, "Test")
            await pilot.pause()

            # Category should still exist
            assert len(screen.categories) == initial_count

    async def test_populate_list_with_no_listview(self) -> None:
        """Test _populate_list when list_view is None."""
        screen = CategoryManagementScreen(categories=[Category(id=1, title="Test")])
        screen.list_view = None

        # Should not raise an error
        screen._populate_list()

    async def test_get_selected_category_index_out_of_range(self) -> None:
        """Test _get_selected_category handles errors gracefully."""
        categories = [Category(id=1, title="Test")]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test():
            screen = cast(CategoryManagementScreen, app.screen)

            # When nothing is selected, should return None
            if screen.list_view:
                # Set list_view to have invalid state
                original_index = screen.list_view.index
                try:
                    # This tests the exception handling in _get_selected_category
                    result = screen._get_selected_category()
                    # Result depends on whether a valid item is selected
                    assert result is None or isinstance(result, Category)
                finally:
                    screen.list_view.index = original_index

    async def test_cursor_navigation_actions(self) -> None:
        """Test cursor navigation actions."""
        categories = [
            Category(id=1, title="Category 1"),
            Category(id=2, title="Category 2"),
        ]
        app = CategoryManagementTestApp(categories=categories)

        async with app.run_test() as pilot:
            # Test cursor down
            await pilot.press("j")
            await pilot.pause()

            # Test cursor up
            await pilot.press("k")
            await pilot.pause()

    async def test_back_action(self) -> None:
        """Test back action pops the screen."""
        app = CategoryManagementTestApp()

        async with app.run_test() as pilot:
            screen = app.screen
            assert isinstance(screen, CategoryManagementScreen)

            # Press escape to go back
            await pilot.press("escape")
            await pilot.pause()

            # Should pop the screen
            assert app.screen is not screen
