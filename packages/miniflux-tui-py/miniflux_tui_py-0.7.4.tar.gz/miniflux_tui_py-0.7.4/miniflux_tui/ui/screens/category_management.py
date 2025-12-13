# SPDX-License-Identifier: MIT
"""Category management screen for viewing and managing categories."""

# pylint: disable=no-value-for-parameter
import asyncio
from typing import TYPE_CHECKING, ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView

from miniflux_tui.api.models import Category
from miniflux_tui.security import sanitize_error_message
from miniflux_tui.ui.screens.confirm_dialog import ConfirmDialog
from miniflux_tui.ui.screens.input_dialog import InputDialog
from miniflux_tui.utils import api_call

if TYPE_CHECKING:
    from miniflux_tui.api.models import Entry


class CategoryListItem(ListItem):
    """Custom list item for displaying a category with entry counts.

    Attributes:
        category: The Category object to display
        unread_count: Number of unread entries in this category
        read_count: Number of read entries in this category
    """

    def __init__(self, category: Category, unread_count: int = 0, read_count: int = 0):
        """Initialize category list item with counts.

        Args:
            category: Category object to display
            unread_count: Number of unread entries in this category
            read_count: Number of read entries in this category
        """
        self.category = category
        self.unread_count = unread_count
        self.read_count = read_count

        # Format: 📁 Category Name (3 unread / 10 total)
        total = unread_count + read_count
        label_text = f"📁 {category.title} ({unread_count} unread / {total} total)" if total > 0 else f"📁 {category.title}"

        super().__init__(Label(label_text))


class CategoryManagementScreen(Screen):
    """Screen for managing categories (create, edit, delete, view).

    Features:
    - List all categories
    - Create new categories
    - Edit category names
    - Delete categories with confirmation
    """

    BINDINGS: ClassVar = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("up", "cursor_up", "Up", show=False),
        Binding("n", "create_category", "New Category"),
        Binding("e", "edit_category", "Edit"),
        Binding("d", "delete_category", "Delete"),
        Binding("escape", "back", "Back"),
    ]

    CSS = """
    CategoryManagementScreen {
        layout: vertical;
    }

    CategoryManagementScreen > Header {
        dock: top;
    }

    CategoryManagementScreen > Footer {
        dock: bottom;
    }

    CategoryManagementScreen #category-list {
        border: solid $accent;
        height: 1fr;
    }

    CategoryManagementScreen ListItem {
        padding: 0 1;
        height: 1;
    }

    CategoryManagementScreen ListItem Label {
        width: 1fr;
    }
    """

    def __init__(self, categories: list[Category] | None = None, entries: list["Entry"] | None = None, **kwargs):
        """Initialize category management screen.

        Args:
            categories: List of categories to display
            entries: List of all entries to calculate counts from
        """
        super().__init__(**kwargs)
        self.categories = categories or []
        self.entries = entries or []
        self.list_view: ListView | None = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        list_view = ListView(id="category-list")
        self.list_view = list_view
        with Container():
            yield list_view
        yield Footer()

    def on_mount(self) -> None:
        """Initialize list view with categories."""
        self._populate_list()

    def _populate_list(self) -> None:
        """Populate the list view with category items, including entry counts."""
        if self.list_view is None:
            return

        self.list_view.clear()
        for category in self.categories:
            # Calculate entry counts for this category
            unread_count = sum(1 for entry in self.entries if entry.feed.category_id == category.id and entry.is_unread)
            read_count = sum(1 for entry in self.entries if entry.feed.category_id == category.id and not entry.is_unread)

            self.list_view.append(CategoryListItem(category, unread_count, read_count))

        # Focus the list view
        if self.list_view.children:
            self.set_focus(self.list_view)

    def _get_selected_category(self) -> Category | None:
        """Get the currently selected category.

        Returns:
            The selected Category or None if nothing is selected
        """
        if self.list_view is None or self.list_view.index is None:
            return None

        try:
            highlighted_child = self.list_view.children[self.list_view.index]
            if isinstance(highlighted_child, CategoryListItem):
                return highlighted_child.category
        except (IndexError, AttributeError):
            # If the list is empty or the child cannot be accessed, return None
            pass

        return None

    async def action_create_category(self) -> None:
        """Show dialog to create a new category."""

        def on_submit(title: str) -> None:
            """Handle category creation."""
            if not title or not title.strip():
                self.app.notify("Category name cannot be empty", severity="error")
                return

            asyncio.create_task(self._do_create_category(title.strip()))  # noqa: RUF006

        dialog = InputDialog(
            title="Create Category",
            label="Category name:",
            on_submit=on_submit,
        )
        self.app.push_screen(dialog)

    async def _do_create_category(self, title: str) -> None:
        """Create a new category via API.

        Args:
            title: The name of the new category
        """
        with api_call(self, "creating category") as app:  # type: ignore
            if app is None:
                return

            try:
                new_category = await app.client.create_category(title)
                self.categories.append(new_category)
                self._populate_list()
                self.app.notify(f"Created category: {title}")
            except Exception as e:
                error_msg = sanitize_error_message(e, "creating category")
                self.app.notify(f"Failed to create category: {error_msg}", severity="error")

    async def action_edit_category(self) -> None:
        """Show dialog to edit the selected category."""
        selected = self._get_selected_category()
        if selected is None:
            self.app.notify("No category selected", severity="warning")
            return

        def on_submit(new_title: str) -> None:
            """Handle category edit."""
            if not new_title or not new_title.strip():
                self.app.notify("Category name cannot be empty", severity="error")
                return

            asyncio.create_task(self._do_edit_category(selected.id, new_title.strip()))  # noqa: RUF006

        dialog = InputDialog(
            title="Edit Category",
            label="New name:",
            value=selected.title,
            on_submit=on_submit,
        )
        self.app.push_screen(dialog)

    async def _do_edit_category(self, category_id: int, new_title: str) -> None:
        """Update a category via API.

        Args:
            category_id: ID of the category to update
            new_title: New name for the category
        """
        with api_call(self, "updating category") as app:  # type: ignore
            if app is None:
                return

            try:
                updated_category = await app.client.update_category(category_id, new_title)
                # Update in our list
                for i, cat in enumerate(self.categories):
                    if cat.id == category_id:
                        self.categories[i] = updated_category
                        break
                self._populate_list()
                self.app.notify(f"Updated category to: {new_title}")
            except Exception as e:
                error_msg = sanitize_error_message(e, "updating category")
                self.app.notify(f"Failed to update category: {error_msg}", severity="error")

    async def action_delete_category(self) -> None:
        """Show confirmation dialog to delete selected category."""
        selected = self._get_selected_category()
        if selected is None:
            self.app.notify("No category selected", severity="warning")
            return

        def on_confirm() -> None:
            """Handle deletion confirmation."""
            asyncio.create_task(self._do_delete_category(selected.id, selected.title))  # noqa: RUF006

        dialog = ConfirmDialog(
            title="Delete Category?",
            message=f"Delete category: {selected.title}?\n\n(Feeds in this category will be moved to Uncategorized)",
            confirm_label="Delete",
            cancel_label="Cancel",
            on_confirm=on_confirm,
        )
        self.app.push_screen(dialog)

    async def _do_delete_category(self, category_id: int, category_title: str) -> None:
        """Delete a category via API.

        Args:
            category_id: ID of the category to delete
            category_title: Title of the category (for notifications)
        """
        with api_call(self, "deleting category") as app:  # type: ignore
            if app is None:
                return

            try:
                await app.client.delete_category(category_id)
                self.categories = [c for c in self.categories if c.id != category_id]
                self._populate_list()
                self.app.notify(f"Deleted category: {category_title}")
            except Exception as e:
                error_msg = sanitize_error_message(e, "deleting category")
                self.app.notify(f"Failed to delete category: {error_msg}", severity="error")

    def action_cursor_down(self) -> None:
        """Move cursor down in the list."""
        if self.list_view is not None:
            self.list_view.action_cursor_down()

    def action_cursor_up(self) -> None:
        """Move cursor up in the list."""
        if self.list_view is not None:
            self.list_view.action_cursor_up()

    def action_back(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()
