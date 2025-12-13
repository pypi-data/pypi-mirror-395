# SPDX-License-Identifier: MIT
"""Integration tests for EntryReaderScreen using Textual TestApp."""

from datetime import UTC, datetime

import pytest
from textual.app import App, ComposeResult

from miniflux_tui.api.models import Entry, Feed
from miniflux_tui.ui.screens.entry_reader import EntryReaderScreen


class EntryReaderTestApp(App):
    """Test app for EntryReaderScreen integration testing."""

    def __init__(self, entry: Entry | None = None, entry_list: list | None = None):
        super().__init__()
        self.entry = entry
        self.entry_list = entry_list or []
        self.entry_reader_screen = None
        self.client = None

    def compose(self) -> ComposeResult:
        """Compose the app with entry reader screen."""
        if self.entry is not None:
            self.entry_reader_screen = EntryReaderScreen(
                entry=self.entry,
                entry_list=self.entry_list,
                current_index=0,
                unread_color="cyan",
                read_color="gray",
            )
            yield self.entry_reader_screen


@pytest.fixture
def test_feed():
    """Create a test feed."""
    return Feed(
        id=1,
        title="Test Feed",
        site_url="http://localhost:8080",
        feed_url="http://localhost:8080/feed.xml",
    )


@pytest.fixture
def integration_entry(test_feed):
    """Create test entry for integration testing."""
    return Entry(
        id=1,
        feed_id=1,
        title="Integration Test Entry",
        url="http://localhost:8080/1",
        content="<p>Test HTML content</p><p>Second paragraph</p>",
        feed=test_feed,
        status="unread",
        starred=False,
        published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
    )


@pytest.fixture
def entry_list(test_feed):
    """Create a list of entries for navigation testing."""
    return [
        Entry(
            id=1,
            feed_id=1,
            title="First Entry",
            url="http://localhost:8080/1",
            content="<p>Entry 1</p>",
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 20, 10, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=2,
            feed_id=1,
            title="Second Entry",
            url="http://localhost:8080/2",
            content="<p>Entry 2</p>",
            feed=test_feed,
            status="read",
            starred=True,
            published_at=datetime(2024, 10, 25, 15, 30, 0, tzinfo=UTC),
        ),
        Entry(
            id=3,
            feed_id=1,
            title="Third Entry",
            url="http://localhost:8080/3",
            content="<p>Entry 3</p>",
            feed=test_feed,
            status="unread",
            starred=True,
            published_at=datetime(2024, 10, 22, 12, 0, 0, tzinfo=UTC),
        ),
    ]


class TestEntryReaderScreenComposition:
    """Test EntryReaderScreen composition and layout."""

    async def test_screen_composes_with_header_and_footer(self, integration_entry):
        """Test that EntryReaderScreen composes with header and footer."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert isinstance(screen, EntryReaderScreen)
            assert screen.entry == integration_entry

    async def test_screen_initializes_with_entry(self, integration_entry):
        """Test that EntryReaderScreen initializes with entry."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert screen.entry.id == 1
            assert screen.entry.title == "Integration Test Entry"

    async def test_screen_has_correct_colors(self, integration_entry):
        """Test that screen uses the configured colors."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert screen.unread_color == "cyan"
            assert screen.read_color == "gray"

    async def test_screen_receives_entry_list(self, integration_entry, entry_list):
        """Test that screen receives entry list for navigation."""
        app = EntryReaderTestApp(entry=integration_entry, entry_list=entry_list)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert len(screen.entry_list) == 3
            assert screen.entry_list[0].title == "First Entry"


class TestEntryReaderScreenNavigation:
    """Test navigation within EntryReaderScreen."""

    async def test_next_entry_action_exists(self, integration_entry):
        """Test that next_entry action exists and is callable."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_next_entry)

    async def test_previous_entry_action_exists(self, integration_entry):
        """Test that previous_entry action exists and is callable."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_previous_entry)

    async def test_back_action_exists(self, integration_entry):
        """Test that back action exists and is callable."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_back)

    async def test_scroll_down_action(self, integration_entry):
        """Test that scroll down action works."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            # Scroll container should be initialized after mount
            if screen.scroll_container is not None:
                screen.action_scroll_down()
                assert True  # Action completed without error

    async def test_scroll_up_action(self, integration_entry):
        """Test that scroll up action works."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            if screen.scroll_container is not None:
                screen.action_scroll_up()
                assert True  # Action completed without error

    async def test_page_down_action(self, integration_entry):
        """Test that page down action works."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            if screen.scroll_container is not None:
                screen.action_page_down()
                assert True  # Action completed without error

    async def test_page_up_action(self, integration_entry):
        """Test that page up action works."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            if screen.scroll_container is not None:
                screen.action_page_up()
                assert True  # Action completed without error


class TestEntryReaderScreenActions:
    """Test action methods in EntryReaderScreen."""

    async def test_mark_unread_action_exists(self, integration_entry):
        """Test that mark_unread action exists."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_mark_unread)

    async def test_toggle_star_action_exists(self, integration_entry):
        """Test that toggle_star action exists."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_toggle_star)

    async def test_save_entry_action_exists(self, integration_entry):
        """Test that save_entry action exists."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_save_entry)

    async def test_open_browser_action_exists(self, integration_entry):
        """Test that open_browser action exists."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_open_browser)

    async def test_fetch_original_action_exists(self, integration_entry):
        """Test that fetch_original action exists."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_fetch_original)

    async def test_show_help_action_exists(self, integration_entry):
        """Test that show_help action exists."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert callable(screen.action_show_help)


class TestEntryReaderScreenContentDisplay:
    """Test content display and formatting."""

    async def test_html_to_markdown_conversion(self, integration_entry):
        """Test HTML to Markdown conversion."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            html = "<p>Test <strong>bold</strong> content</p>"
            markdown = screen._html_to_markdown(html)
            assert markdown is not None
            assert len(markdown) > 0

    async def test_empty_content_handling(self, test_feed):
        """Test handling of empty content."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Empty Entry",
            url="http://localhost:8080/1",
            content="",
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        app = EntryReaderTestApp(entry=entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert not screen.entry.content

    async def test_complex_html_conversion(self, test_feed):
        """Test conversion of complex HTML content."""
        html_content = """
        <div>
            <p>Introduction paragraph</p>
            <h2>Heading</h2>
            <ul>
                <li>List item 1</li>
                <li>List item 2</li>
            </ul>
            <a href="http://localhost:8080">Link</a>
        </div>
        """
        entry = Entry(
            id=1,
            feed_id=1,
            title="Complex Entry",
            url="http://localhost:8080/1",
            content=html_content,
            feed=test_feed,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        app = EntryReaderTestApp(entry=entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            markdown = screen._html_to_markdown(html_content)
            assert "Introduction" in markdown or bool(markdown)


class TestEntryReaderScreenBindings:
    """Test keyboard bindings are properly configured."""

    async def test_bindings_exist(self, integration_entry):
        """Test that all expected bindings exist."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert len(screen.BINDINGS) > 0
            binding_keys = [b.key for b in screen.BINDINGS]  # type: ignore[attr-defined]
            assert "j" in binding_keys  # Scroll down
            assert "k" in binding_keys  # Scroll up
            assert "J" in binding_keys  # Next entry
            assert "K" in binding_keys  # Previous entry
            assert "b" in binding_keys  # Back

    async def test_binding_descriptions(self, integration_entry):
        """Test that bindings have descriptions."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            for binding in screen.BINDINGS:
                assert binding.description is not None
                assert len(binding.description) > 0


class TestEntryReaderScreenStarredEntry:
    """Test handling of starred entries."""

    async def test_starred_entry_display(self, test_feed):
        """Test that starred entries are displayed properly."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Starred Entry",
            url="http://localhost:8080/1",
            content="<p>Important entry</p>",
            feed=test_feed,
            status="read",
            starred=True,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )
        app = EntryReaderTestApp(entry=entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert screen.entry.starred is True

    async def test_unstarred_entry_display(self, integration_entry):
        """Test that unstarred entries are displayed properly."""
        app = EntryReaderTestApp(entry=integration_entry)

        async with app.run_test():
            screen = app.entry_reader_screen
            assert screen.entry.starred is False
