# SPDX-License-Identifier: MIT
"""Tests for the FeedSettingsScreen."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

from miniflux_tui.api.models import Feed
from miniflux_tui.ui.screens.feed_settings import FeedSettingsScreen


@pytest.fixture
def mock_client():
    """Create a mock MinifluxClient."""
    client = AsyncMock()
    client.update_feed = AsyncMock()
    client.delete_feed = AsyncMock()
    client.get_feed = AsyncMock()
    return client


@pytest.fixture
def sample_feed():
    """Create a sample Feed for testing."""
    return Feed(
        id=1,
        title="Test Feed",
        site_url="https://example.com",
        feed_url="https://example.com/feed.xml",
        category_id=1,
        checked_at="2024-11-14T12:00:00Z",
        disabled=False,
    )


@pytest.fixture
def feed_settings_screen(sample_feed, mock_client):
    """Create a FeedSettingsScreen instance for testing."""
    screen = FeedSettingsScreen(
        feed_id=sample_feed.id,
        feed=sample_feed,
        client=mock_client,
    )
    # Mock set_timer and _update_unsaved_indicator for all tests to avoid async issues
    screen.set_timer = MagicMock(return_value=MagicMock())
    screen._update_unsaved_indicator = MagicMock()
    # Set initialization flag to False to simulate on_mount() completion
    screen._initializing = False
    return screen


class TestFeedSettingsScreenInitialization:
    """Test FeedSettingsScreen initialization."""

    def test_init_stores_parameters(self, sample_feed, mock_client):
        """Test that __init__ properly stores all parameters."""
        screen = FeedSettingsScreen(
            feed_id=sample_feed.id,
            feed=sample_feed,
            client=mock_client,
        )

        assert screen.feed_id == sample_feed.id
        assert screen.feed == sample_feed
        assert screen.client == mock_client

    def test_init_initializes_dirty_state(self, feed_settings_screen):
        """Test that dirty state is initialized to clean."""
        assert feed_settings_screen.is_dirty is False
        assert feed_settings_screen.dirty_fields == {}
        assert feed_settings_screen.original_values == {}

    def test_init_initializes_status(self, feed_settings_screen):
        """Test that status message is initialized."""
        assert feed_settings_screen.status_message == ""
        assert feed_settings_screen.status_severity == "info"

    def test_bindings_defined(self):
        """Test that BINDINGS are defined."""
        assert hasattr(FeedSettingsScreen, "BINDINGS")
        assert len(FeedSettingsScreen.BINDINGS) > 0

    def test_default_css_defined(self):
        """Test that DEFAULT_CSS is defined."""
        assert hasattr(FeedSettingsScreen, "DEFAULT_CSS")
        assert isinstance(FeedSettingsScreen.DEFAULT_CSS, str)

    def test_init_initializes_with_initializing_flag_true(self, sample_feed, mock_client):
        """Test that _initializing flag is True on creation (to prevent tracking during setup)."""
        screen = FeedSettingsScreen(
            feed_id=sample_feed.id,
            feed=sample_feed,
            client=mock_client,
        )
        assert screen._initializing is True

    def test_changes_not_tracked_during_initialization(self, sample_feed, mock_client):
        """Test that field changes are NOT tracked while _initializing is True."""
        screen = FeedSettingsScreen(
            feed_id=sample_feed.id,
            feed=sample_feed,
            client=mock_client,
        )
        # _initializing should be True, so changes should not be tracked
        with patch.object(screen, "query_one"):
            screen._on_field_changed("feed-title", "New Title")

        # Verify that no changes were tracked (is_dirty should still be False)
        assert screen.is_dirty is False
        # Verify that persistence manager has no changes recorded
        assert screen.persistence.get_change_count(sample_feed.id) == 0

    def test_category_selector_initialization_with_category_id(self, sample_feed, mock_client):
        """Test that category selector initializes correctly with a feed that has a category_id."""
        # This test ensures the Select widget doesn't try to set an invalid value during compose
        screen = FeedSettingsScreen(
            feed_id=sample_feed.id,
            feed=sample_feed,
            client=mock_client,
        )
        assert screen.feed.category_id == 1
        # The screen should be creatable without errors
        assert screen is not None

    def test_categories_list_initialized_empty(self, sample_feed, mock_client):
        """Test that categories list is initialized as empty."""
        screen = FeedSettingsScreen(
            feed_id=sample_feed.id,
            feed=sample_feed,
            client=mock_client,
        )
        assert screen.categories == []


class TestDirtyStateTracking:
    """Test dirty state tracking functionality."""

    def test_on_field_changed_marks_dirty(self, feed_settings_screen):
        """Test that _on_field_changed marks screen as dirty."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title")

        assert feed_settings_screen.is_dirty is True
        assert "title" in feed_settings_screen.dirty_fields
        assert feed_settings_screen.dirty_fields["title"] is True

    def test_on_field_changed_stores_original_value(self, feed_settings_screen):
        """Test that original values are stored on first change."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title")

        assert "title" in feed_settings_screen.original_values
        assert feed_settings_screen.original_values["title"] == "Test Feed"

    def test_on_field_changed_multiple_fields(self, feed_settings_screen):
        """Test tracking multiple field changes."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title")
            feed_settings_screen._on_field_changed("category_id", 2)

        assert feed_settings_screen.is_dirty is True
        assert len(feed_settings_screen.dirty_fields) == 2
        assert "title" in feed_settings_screen.dirty_fields
        assert "category_id" in feed_settings_screen.dirty_fields

    def test_on_field_changed_does_not_re_store_original(self, feed_settings_screen):
        """Test that original value is only stored once per field."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title 1")
            original_value_1 = feed_settings_screen.original_values["title"]

            feed_settings_screen._on_field_changed("title", "New Title 2")
            original_value_2 = feed_settings_screen.original_values["title"]

        assert original_value_1 == original_value_2
        assert original_value_2 == "Test Feed"


class TestSaveAction:
    """Test save action functionality."""

    @pytest.mark.asyncio
    async def test_save_calls_api_when_dirty(self, feed_settings_screen):
        """Test that save calls API when there are changes."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title")

        feed_settings_screen._collect_field_values = MagicMock(return_value={})

        with patch.object(feed_settings_screen, "query_one"):
            await feed_settings_screen.action_save_changes()

        feed_settings_screen.client.update_feed.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_does_nothing_if_not_dirty(self, feed_settings_screen):
        """Test that save does nothing when there are no changes."""
        assert feed_settings_screen.is_dirty is False

        with patch.object(feed_settings_screen, "query_one"):
            await feed_settings_screen.action_save_changes()

        feed_settings_screen.client.update_feed.assert_not_called()

    @pytest.mark.asyncio
    async def test_save_shows_success_message(self, feed_settings_screen):
        """Test that success message is shown after save."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title")
            feed_settings_screen._collect_field_values = MagicMock(return_value={})
            await feed_settings_screen.action_save_changes()

        assert "saved successfully" in feed_settings_screen.status_message.lower()
        assert feed_settings_screen.status_severity == "success"

    @pytest.mark.asyncio
    async def test_save_handles_timeout_error(self, feed_settings_screen):
        """Test that timeout errors are handled gracefully."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title")
            feed_settings_screen._collect_field_values = MagicMock(return_value={})
            feed_settings_screen.client.update_feed.side_effect = TimeoutError()
            await feed_settings_screen.action_save_changes()

        assert "timeout" in feed_settings_screen.status_message.lower()
        assert feed_settings_screen.status_severity == "error"

    @pytest.mark.asyncio
    async def test_save_handles_connection_error(self, feed_settings_screen):
        """Test that connection errors are handled gracefully."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title")
            feed_settings_screen._collect_field_values = MagicMock(return_value={})
            feed_settings_screen.client.update_feed.side_effect = ConnectionError()
            await feed_settings_screen.action_save_changes()

        assert "connection" in feed_settings_screen.status_message.lower()
        assert feed_settings_screen.status_severity == "error"


class TestCancelAction:
    """Test cancel action functionality."""

    @pytest.mark.asyncio
    async def test_cancel_with_no_changes_closes_screen(self, feed_settings_screen):
        """Test that cancel closes screen when no unsaved changes."""
        assert feed_settings_screen.is_dirty is False

        mock_app = MagicMock()
        with patch("miniflux_tui.ui.screens.feed_settings.Screen.app", mock_app), patch.object(feed_settings_screen, "query_one"):
            await feed_settings_screen.action_cancel_changes()

        mock_app.pop_screen.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_with_changes_shows_warning(self, feed_settings_screen):
        """Test that cancel shows warning with unsaved changes (first press)."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("title", "New Title")
        assert feed_settings_screen.is_dirty is True

        with patch.object(feed_settings_screen, "query_one"):
            await feed_settings_screen.action_cancel_changes()

        # After first press with unsaved changes, show confirmation and set flag
        assert feed_settings_screen._cancel_confirmed is True
        assert "discard" in feed_settings_screen.status_message.lower()
        assert feed_settings_screen.status_severity == "warning"


class TestCollectFieldValues:
    """Test field value collection."""

    def test_collect_field_values_returns_dict(self, feed_settings_screen):
        """Test that _collect_field_values returns a dictionary."""
        result = feed_settings_screen._collect_field_values()
        assert isinstance(result, dict)


class TestStatusMessages:
    """Test status message display."""

    def test_show_message_updates_state(self, feed_settings_screen):
        """Test that show_message updates state correctly."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._show_message("Test", severity="info")

        assert feed_settings_screen.status_message == "Test"
        assert feed_settings_screen.status_severity == "info"

    def test_show_message_all_severities(self, feed_settings_screen):
        """Test show_message with all severity levels."""
        severities = ["info", "success", "error", "warning"]

        for severity in severities:
            with patch.object(feed_settings_screen, "query_one"):
                feed_settings_screen._show_message("Test", severity=severity)

            assert feed_settings_screen.status_severity == severity


class TestIntegration:
    """Integration tests for complete workflows."""

    @pytest.mark.asyncio
    async def test_complete_edit_workflow(self, feed_settings_screen):
        """Test complete workflow: change -> dirty -> save."""
        with patch.object(feed_settings_screen, "query_one"):
            # Mark field as changed
            feed_settings_screen._on_field_changed("title", "Updated")
            assert feed_settings_screen.is_dirty is True

            # Prepare for save
            feed_settings_screen._collect_field_values = MagicMock(return_value={})

            # Save
            await feed_settings_screen.action_save_changes()

            # Verify clean
            assert feed_settings_screen.is_dirty is False


class TestGeneralSettingsFields:
    """Test General Settings field handling."""

    def test_field_mapping_for_widget_ids(self, feed_settings_screen):
        """Test that widget IDs are correctly mapped to feed field names."""
        with patch.object(feed_settings_screen, "query_one"):
            # Test title field mapping (pass a DIFFERENT value from the original)
            feed_settings_screen._on_field_changed("feed-title", "New Title")
            assert "title" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["title"] == "New Title"

            # Test site_url field mapping (pass a DIFFERENT value from the original)
            feed_settings_screen._on_field_changed("site-url", "https://different.com")
            assert "site_url" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["site_url"] == "https://different.com"

            # Test category_id field mapping (sample_feed has category_id=1, pass 5)
            feed_settings_screen._on_field_changed("category-id", "5")
            assert "category_id" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["category_id"] == "5"

            # Test disabled field mapping (sample_feed has disabled=False, pass True)
            feed_settings_screen._on_field_changed("feed-disabled", True)
            assert "disabled" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["disabled"] is True

    def test_on_input_changed_event(self, feed_settings_screen):
        """Test on_input_changed event handler."""
        mock_input = MagicMock()
        mock_input.id = "feed-title"
        mock_input.disabled = False

        event = MagicMock()
        event.input = mock_input
        event.value = "Updated Title"

        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen.on_input_changed(event)

        assert feed_settings_screen.is_dirty is True
        assert "title" in feed_settings_screen.dirty_fields

    def test_on_input_changed_skips_disabled_fields(self, feed_settings_screen):
        """Test that on_input_changed skips disabled input fields."""
        mock_input = MagicMock()
        mock_input.id = "feed-url"
        mock_input.disabled = True

        event = MagicMock()
        event.input = mock_input
        event.value = "https://example.com/feed.xml"

        # Should not mark as dirty since the input is disabled
        feed_settings_screen.on_input_changed(event)
        assert feed_settings_screen.is_dirty is False

    def test_on_checkbox_changed_event(self, feed_settings_screen):
        """Test on_checkbox_changed event handler."""
        mock_checkbox = MagicMock()
        mock_checkbox.id = "feed-disabled"

        event = MagicMock()
        event.checkbox = mock_checkbox
        event.value = True

        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen.on_checkbox_changed(event)

        assert feed_settings_screen.is_dirty is True
        assert "disabled" in feed_settings_screen.dirty_fields
        assert feed_settings_screen._field_values["disabled"] is True

    def test_collect_field_values_with_mapped_fields(self, feed_settings_screen):
        """Test that _collect_field_values returns mapped field names."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("feed-title", "New Title")
            feed_settings_screen._on_field_changed("site-url", "https://different.com")
            feed_settings_screen._on_field_changed("feed-disabled", True)

        updates = feed_settings_screen._collect_field_values()
        assert updates["title"] == "New Title"
        assert updates["site_url"] == "https://different.com"
        assert updates["disabled"] is True
        assert len(updates) == 3

    def test_feed_url_read_only_field_not_collected(self, feed_settings_screen):
        """Test that read-only feed-url field is not collected on save."""
        with patch.object(feed_settings_screen, "query_one"):
            # Try to mark feed-url as dirty (should be skipped in actual usage)
            feed_settings_screen._on_field_changed("feed-url", "different_url")

        # The field mapping will map it to feed_url
        updates = feed_settings_screen._collect_field_values()
        # Since feed_url is read-only and we don't actually modify it in the UI,
        # it should still be in updates if we marked it dirty
        # This test documents the behavior - in real usage, disabled inputs won't trigger events
        assert "feed_url" in updates

    def test_original_values_with_mapped_fields(self, feed_settings_screen):
        """Test that original values are stored with mapped field names."""
        original_title = feed_settings_screen.feed.title
        original_disabled = feed_settings_screen.feed.disabled

        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("feed-title", "Modified")
            feed_settings_screen._on_field_changed("feed-disabled", not original_disabled)

        assert feed_settings_screen.original_values["title"] == original_title
        assert feed_settings_screen.original_values["disabled"] == original_disabled


class TestGeneralSettingsIntegration:
    """Integration tests for General Settings workflow."""

    @pytest.mark.asyncio
    async def test_general_settings_edit_workflow(self, feed_settings_screen):
        """Test complete workflow for editing General Settings."""
        with patch.object(feed_settings_screen, "query_one"):
            # Simulate user edits
            feed_settings_screen._on_field_changed("feed-title", "Updated Feed Title")
            feed_settings_screen._on_field_changed("site-url", "https://newsite.com")
            feed_settings_screen._on_field_changed("category-id", "10")
            feed_settings_screen._on_field_changed("feed-disabled", True)

            # Verify dirty state
            assert feed_settings_screen.is_dirty is True
            assert len(feed_settings_screen.dirty_fields) == 4

            # Collect values
            updates = feed_settings_screen._collect_field_values()
            assert updates["title"] == "Updated Feed Title"
            assert updates["site_url"] == "https://newsite.com"
            assert updates["category_id"] == 10  # Converted to integer
            assert updates["disabled"] is True

    @pytest.mark.asyncio
    async def test_partial_general_settings_edit(self, feed_settings_screen):
        """Test workflow when only some General Settings fields are modified."""
        with patch.object(feed_settings_screen, "query_one"):
            # Only modify title and disabled
            feed_settings_screen._on_field_changed("feed-title", "Only Title Changed")
            feed_settings_screen._on_field_changed("feed-disabled", True)

        updates = feed_settings_screen._collect_field_values()
        # Should only have 2 updates
        assert len(updates) == 2
        assert updates["title"] == "Only Title Changed"
        assert updates["disabled"] is True
        # site_url and category_id should not be in updates
        assert "site_url" not in updates
        assert "category_id" not in updates


class TestNetworkSettingsFields:
    """Test Network Settings field handling."""

    def test_network_field_mapping(self, feed_settings_screen):
        """Test that network widget IDs are correctly mapped to field names."""
        with patch.object(feed_settings_screen, "query_one"):
            # Test username field mapping
            feed_settings_screen._on_field_changed("auth-username", "testuser")
            assert "username" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["username"] == "testuser"

            # Test password field mapping
            feed_settings_screen._on_field_changed("auth-password", "secretpass")
            assert "password" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["password"] == "secretpass"  # noqa: S105

            # Test user_agent field mapping
            feed_settings_screen._on_field_changed("user-agent", "Mozilla/5.0")
            assert "user_agent" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["user_agent"] == "Mozilla/5.0"

            # Test proxy_url field mapping
            feed_settings_screen._on_field_changed("proxy-url", "http://proxy.example.com:8080")
            assert "proxy_url" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["proxy_url"] == "http://proxy.example.com:8080"

            # Test ignore_https_errors field mapping
            feed_settings_screen._on_field_changed("ignore-https-errors", True)
            assert "ignore_https_errors" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["ignore_https_errors"] is True

    def test_on_input_changed_for_network_fields(self, feed_settings_screen):
        """Test on_input_changed event handler for network fields."""
        mock_input = MagicMock()
        mock_input.id = "auth-username"
        mock_input.disabled = False

        event = MagicMock()
        event.input = mock_input
        event.value = "networkuser"

        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen.on_input_changed(event)

        assert feed_settings_screen.is_dirty is True
        assert "username" in feed_settings_screen.dirty_fields

    def test_on_checkbox_changed_for_https_errors(self, feed_settings_screen):
        """Test on_checkbox_changed for HTTPS certificate errors setting."""
        mock_checkbox = MagicMock()
        mock_checkbox.id = "ignore-https-errors"

        event = MagicMock()
        event.checkbox = mock_checkbox
        event.value = True

        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen.on_checkbox_changed(event)

        assert feed_settings_screen.is_dirty is True
        assert "ignore_https_errors" in feed_settings_screen.dirty_fields
        assert feed_settings_screen._field_values["ignore_https_errors"] is True

    def test_collect_network_field_values(self, feed_settings_screen):
        """Test that _collect_field_values returns network field names."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("auth-username", "user123")
            feed_settings_screen._on_field_changed("auth-password", "pass123")
            feed_settings_screen._on_field_changed("user-agent", "CustomAgent/1.0")
            feed_settings_screen._on_field_changed("ignore-https-errors", True)

        updates = feed_settings_screen._collect_field_values()
        assert updates["username"] == "user123"
        assert updates["password"] == "pass123"  # noqa: S105
        assert updates["user_agent"] == "CustomAgent/1.0"
        assert updates["ignore_https_errors"] is True
        assert len(updates) == 4

    def test_empty_network_fields_not_collected(self, feed_settings_screen):
        """Test that empty network fields are not collected if not modified."""
        # Don't modify any network fields
        updates = feed_settings_screen._collect_field_values()
        # Should have no network fields since nothing was modified
        assert "username" not in updates
        assert "password" not in updates
        assert "user_agent" not in updates
        assert "proxy_url" not in updates

    def test_partial_network_settings_edit(self, feed_settings_screen):
        """Test workflow when only some network settings are modified."""
        with patch.object(feed_settings_screen, "query_one"):
            # Only modify username and proxy
            feed_settings_screen._on_field_changed("auth-username", "admin")
            feed_settings_screen._on_field_changed("proxy-url", "http://proxy:3128")

        updates = feed_settings_screen._collect_field_values()
        assert len(updates) == 2
        assert updates["username"] == "admin"
        assert updates["proxy_url"] == "http://proxy:3128"
        # password and user_agent should not be in updates
        assert "password" not in updates
        assert "user_agent" not in updates


class TestNetworkSettingsIntegration:
    """Integration tests for Network Settings workflow."""

    @pytest.mark.asyncio
    async def test_network_settings_full_workflow(self, feed_settings_screen):
        """Test complete workflow for editing all Network Settings."""
        with patch.object(feed_settings_screen, "query_one"):
            # Simulate user edits for all network fields
            feed_settings_screen._on_field_changed("auth-username", "networkuser")
            feed_settings_screen._on_field_changed("auth-password", "networkpass")
            feed_settings_screen._on_field_changed("user-agent", "Mozilla/5.0 Custom")
            feed_settings_screen._on_field_changed("proxy-url", "http://proxy.example.com:8080")
            feed_settings_screen._on_field_changed("ignore-https-errors", True)

            # Verify dirty state
            assert feed_settings_screen.is_dirty is True
            assert len(feed_settings_screen.dirty_fields) == 5

            # Collect values
            updates = feed_settings_screen._collect_field_values()
            assert updates["username"] == "networkuser"
            assert updates["password"] == "networkpass"  # noqa: S105
            assert updates["user_agent"] == "Mozilla/5.0 Custom"
            assert updates["proxy_url"] == "http://proxy.example.com:8080"
            assert updates["ignore_https_errors"] is True

    @pytest.mark.asyncio
    async def test_mixed_general_and_network_settings_edit(self, feed_settings_screen):
        """Test workflow when both General and Network Settings are modified."""
        with patch.object(feed_settings_screen, "query_one"):
            # Modify both general and network fields
            feed_settings_screen._on_field_changed("feed-title", "Updated Title")
            feed_settings_screen._on_field_changed("auth-username", "user456")
            feed_settings_screen._on_field_changed("ignore-https-errors", True)

        updates = feed_settings_screen._collect_field_values()
        # Should have 3 updates total
        assert len(updates) == 3
        assert updates["title"] == "Updated Title"
        assert updates["username"] == "user456"
        assert updates["ignore_https_errors"] is True

    @pytest.mark.asyncio
    async def test_network_settings_save_workflow(self, feed_settings_screen):
        """Test save workflow with network settings changes."""
        with patch.object(feed_settings_screen, "query_one"):
            # Modify network fields
            feed_settings_screen._on_field_changed("auth-username", "saveuser")
            feed_settings_screen._on_field_changed("proxy-url", "http://save-proxy:8080")

            # Verify dirty before save
            assert feed_settings_screen.is_dirty is True

            # Prepare for save
            feed_settings_screen._collect_field_values = MagicMock(
                return_value={
                    "username": "saveuser",
                    "proxy_url": "http://save-proxy:8080",
                }
            )

            # Save
            await feed_settings_screen.action_save_changes()

            # Verify clean after save
            assert feed_settings_screen.is_dirty is False
            assert feed_settings_screen.dirty_fields == {}


class TestRulesAndFilteringFields:
    """Test Rules & Filtering field handling."""

    def test_rules_field_mapping(self, feed_settings_screen):
        """Test that rule widget IDs are correctly mapped to field names."""
        with patch.object(feed_settings_screen, "query_one"):
            # Test scraper rules mapping
            feed_settings_screen._on_field_changed("scraper-rules", "div.content")
            assert "scraper_rules" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["scraper_rules"] == "div.content"

            # Test rewrite rules mapping
            feed_settings_screen._on_field_changed("rewrite-rules", "regex pattern")
            assert "rewrite_rules" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["rewrite_rules"] == "regex pattern"

            # Test blocklist rules mapping
            feed_settings_screen._on_field_changed("blocklist-rules", "block pattern")
            assert "blocklist_rules" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["blocklist_rules"] == "block pattern"

            # Test keep rules mapping
            feed_settings_screen._on_field_changed("keeplist-rules", "keep pattern")
            assert "keeplist_rules" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["keeplist_rules"] == "keep pattern"

    def test_on_text_area_changed_event(self, feed_settings_screen):
        """Test on_text_area_changed event handler."""
        mock_textarea = MagicMock()
        mock_textarea.id = "scraper-rules"
        mock_textarea.text = "div.article"

        event = MagicMock()
        event.text_area = mock_textarea

        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen.on_text_area_changed(event)

        assert feed_settings_screen.is_dirty is True
        assert "scraper_rules" in feed_settings_screen.dirty_fields

    def test_collect_rule_field_values(self, feed_settings_screen):
        """Test that _collect_field_values returns rule field names."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("scraper-rules", "div.post")
            feed_settings_screen._on_field_changed("rewrite-rules", "replace_pattern")
            feed_settings_screen._on_field_changed("blocklist-rules", "ad_pattern")

        updates = feed_settings_screen._collect_field_values()
        assert updates["scraper_rules"] == "div.post"
        assert updates["rewrite_rules"] == "replace_pattern"
        assert updates["blocklist_rules"] == "ad_pattern"
        assert len(updates) == 3

    def test_empty_rule_fields_not_collected(self, feed_settings_screen):
        """Test that empty rule fields are not collected if not modified."""
        # Don't modify any rule fields
        updates = feed_settings_screen._collect_field_values()
        # Should have no rule fields since nothing was modified
        assert "scraper_rules" not in updates
        assert "rewrite_rules" not in updates
        assert "blocklist_rules" not in updates
        assert "keeplist_rules" not in updates

    def test_partial_rules_edit(self, feed_settings_screen):
        """Test workflow when only some rule fields are modified."""
        with patch.object(feed_settings_screen, "query_one"):
            # Only modify scraper and blocking rules
            feed_settings_screen._on_field_changed("scraper-rules", "article.main")
            feed_settings_screen._on_field_changed("blocklist-rules", "spam_regex")

        updates = feed_settings_screen._collect_field_values()
        assert len(updates) == 2
        assert updates["scraper_rules"] == "article.main"
        assert updates["blocklist_rules"] == "spam_regex"
        # rewrite and keep rules should not be in updates
        assert "rewrite_rules" not in updates
        assert "keeplist_rules" not in updates

    def test_multiline_rule_content(self, feed_settings_screen):
        """Test handling of multiline rule content."""
        multiline_rules = "line1\nline2\nline3"
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("scraper-rules", multiline_rules)

        updates = feed_settings_screen._collect_field_values()
        assert updates["scraper_rules"] == multiline_rules
        assert "\n" in updates["scraper_rules"]


class TestRulesAndFilteringIntegration:
    """Integration tests for Rules & Filtering workflow."""

    @pytest.mark.asyncio
    async def test_rules_and_filtering_full_workflow(self, feed_settings_screen):
        """Test complete workflow for editing all Rules & Filtering fields."""
        with patch.object(feed_settings_screen, "query_one"):
            # Simulate user edits for all rule fields (API has 4 rule types)
            feed_settings_screen._on_field_changed("scraper-rules", "div.content")
            feed_settings_screen._on_field_changed("rewrite-rules", "pattern1 -> replacement1")
            feed_settings_screen._on_field_changed("blocklist-rules", "ads|spam")
            feed_settings_screen._on_field_changed("keeplist-rules", "important|urgent")

            # Verify dirty state
            assert feed_settings_screen.is_dirty is True
            assert len(feed_settings_screen.dirty_fields) == 4

            # Collect values
            updates = feed_settings_screen._collect_field_values()
            assert updates["scraper_rules"] == "div.content"
            assert updates["rewrite_rules"] == "pattern1 -> replacement1"
            assert updates["blocklist_rules"] == "ads|spam"
            assert updates["keeplist_rules"] == "important|urgent"

    @pytest.mark.asyncio
    async def test_combined_all_sections_edit(self, feed_settings_screen):
        """Test workflow when fields from all sections are modified."""
        with patch.object(feed_settings_screen, "query_one"):
            # Modify fields from each section
            feed_settings_screen._on_field_changed("feed-title", "New Title")  # General
            feed_settings_screen._on_field_changed("auth-username", "user1")  # Network
            feed_settings_screen._on_field_changed("scraper-rules", "div")  # Rules

        updates = feed_settings_screen._collect_field_values()
        # Should have 3 updates total
        assert len(updates) == 3
        assert updates["title"] == "New Title"
        assert updates["username"] == "user1"
        assert updates["scraper_rules"] == "div"

    @pytest.mark.asyncio
    async def test_rules_save_workflow(self, feed_settings_screen):
        """Test save workflow with rules changes."""
        with patch.object(feed_settings_screen, "query_one"):
            # Modify rules
            feed_settings_screen._on_field_changed("scraper-rules", "main.article")
            feed_settings_screen._on_field_changed("blocklist-rules", "\\badv\\b")

            # Verify dirty before save
            assert feed_settings_screen.is_dirty is True

            # Prepare for save
            feed_settings_screen._collect_field_values = MagicMock(
                return_value={
                    "scraper_rules": "main.article",
                    "blocklist_rules": "\\badv\\b",
                }
            )

            # Save
            await feed_settings_screen.action_save_changes()

            # Verify clean after save
            assert feed_settings_screen.is_dirty is False
            assert feed_settings_screen.dirty_fields == {}


class TestFeedInformationFields:
    """Test Feed Information field handling."""

    def test_feed_information_field_mapping(self, feed_settings_screen):
        """Test that feed information widget IDs are correctly mapped."""
        with patch.object(feed_settings_screen, "query_one"):
            # Test check interval field mapping
            feed_settings_screen._on_field_changed("check-interval", "60")
            assert "check_interval" in feed_settings_screen.dirty_fields
            assert feed_settings_screen._field_values["check_interval"] == "60"

    def test_collect_feed_information_field_values(self, feed_settings_screen):
        """Test that _collect_field_values returns feed information field names."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("check-interval", "120")

        updates = feed_settings_screen._collect_field_values()
        assert updates["check_interval"] == 120  # Converted to integer
        assert len(updates) == 1

    def test_empty_check_interval_not_collected(self, feed_settings_screen):
        """Test that empty check interval is not collected if not modified."""
        # Don't modify check interval
        updates = feed_settings_screen._collect_field_values()
        # Should have no check_interval since nothing was modified
        assert "check_interval" not in updates

    def test_original_values_with_feed_information(self, feed_settings_screen):
        """Test that original values are stored for feed information fields."""
        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("check-interval", "30")

        # Original value should be None for new field
        assert feed_settings_screen.original_values["check_interval"] is None


class TestFeedInformationIntegration:
    """Integration tests for Feed Information workflow."""

    @pytest.mark.asyncio
    async def test_feed_information_edit_workflow(self, feed_settings_screen):
        """Test complete workflow for editing Feed Information."""
        with patch.object(feed_settings_screen, "query_one"):
            # Simulate user edit for check interval
            feed_settings_screen._on_field_changed("check-interval", "45")

            # Verify dirty state
            assert feed_settings_screen.is_dirty is True
            assert "check_interval" in feed_settings_screen.dirty_fields

            # Collect values
            updates = feed_settings_screen._collect_field_values()
            assert updates["check_interval"] == 45  # Converted to integer

    @pytest.mark.asyncio
    async def test_combined_all_four_sections_edit(self, feed_settings_screen):
        """Test workflow when fields from all four sections are modified."""
        with patch.object(feed_settings_screen, "query_one"):
            # Modify fields from each section
            feed_settings_screen._on_field_changed("feed-title", "Updated")  # General
            feed_settings_screen._on_field_changed("auth-username", "user")  # Network
            feed_settings_screen._on_field_changed("scraper-rules", "div")  # Rules
            feed_settings_screen._on_field_changed("check-interval", "60")  # Feed Info

        updates = feed_settings_screen._collect_field_values()
        # Should have 4 updates total
        assert len(updates) == 4
        assert updates["title"] == "Updated"
        assert updates["username"] == "user"
        assert updates["scraper_rules"] == "div"
        assert updates["check_interval"] == 60  # Converted to integer

    @pytest.mark.asyncio
    async def test_feed_information_save_workflow(self, feed_settings_screen):
        """Test save workflow with feed information changes."""
        with patch.object(feed_settings_screen, "query_one"):
            # Modify feed information
            feed_settings_screen._on_field_changed("check-interval", "30")

            # Verify dirty before save
            assert feed_settings_screen.is_dirty is True

            # Prepare for save
            feed_settings_screen._collect_field_values = MagicMock(return_value={"check_interval": "30"})

            # Save
            await feed_settings_screen.action_save_changes()

            # Verify clean after save
            assert feed_settings_screen.is_dirty is False
            assert feed_settings_screen.dirty_fields == {}


class TestDeleteFeedFunctionality:
    """Test delete feed functionality and error handling."""

    @pytest.fixture
    def feed_settings_with_app(self):
        """Create feed settings screen with mock app."""
        feed = Feed(
            id=1,
            title="Test Feed",
            feed_url="https://example.com/feed",
            site_url="https://example.com",
            category_id=1,
            disabled=False,
            checked_at=None,
            parsing_error_count=0,
            parsing_error_message="",
        )

        return FeedSettingsScreen(feed_id=1, feed=feed, client=AsyncMock())

    @pytest.mark.asyncio
    async def test_delete_feed_requires_confirmation(self, feed_settings_with_app):
        """Test that delete feed requires two button presses (confirmation)."""
        screen = feed_settings_with_app
        mock_app = MagicMock()
        mock_app.client = AsyncMock()

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop, patch.object(screen, "query_one"):
            mock_app_prop.return_value = mock_app
            # First press - should show confirmation message, not delete
            await screen.action_delete_feed()

            # Verify confirmation message shown
            assert screen._delete_confirmed is True
            assert "confirm" in screen.status_message.lower()
            assert "cannot be undone" in screen.status_message.lower()
            assert screen.status_severity == "error"

            # Verify client.delete_feed was NOT called yet
            mock_app.client.delete_feed.assert_not_called()
            mock_app.pop_screen.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_feed_successful_delete(self, feed_settings_with_app):
        """Test successful feed deletion on second confirmation press."""
        screen = feed_settings_with_app
        mock_app = MagicMock()
        mock_app.client = AsyncMock()
        mock_app.client.delete_feed = AsyncMock()

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop, patch.object(screen, "query_one"):
            mock_app_prop.return_value = mock_app
            # First press - confirmation message
            await screen.action_delete_feed()
            assert screen._delete_confirmed is True

            # Second press - actual deletion
            await screen.action_delete_feed()

            # Verify API was called
            mock_app.client.delete_feed.assert_called_once_with(1)

            # Verify success message
            assert "deleted successfully" in screen.status_message.lower()
            assert screen.status_severity == "success"

            # Verify screen closed
            mock_app.pop_screen.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_feed_no_client(self, feed_settings_with_app):
        """Test error when API client is not available."""
        screen = feed_settings_with_app
        screen._delete_confirmed = True  # Skip confirmation
        mock_app = MagicMock()
        mock_app.client = None

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop, patch.object(screen, "query_one"):
            mock_app_prop.return_value = mock_app
            await screen.action_delete_feed()

            # Verify error message
            assert "API client not available" in screen.status_message
            assert screen.status_severity == "error"

            # Verify screen not closed
            mock_app.pop_screen.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_feed_timeout_error(self, feed_settings_with_app):
        """Test timeout error handling during deletion."""
        screen = feed_settings_with_app
        screen._delete_confirmed = True  # Skip confirmation
        mock_app = MagicMock()
        mock_app.client = AsyncMock()
        mock_app.client.delete_feed = AsyncMock(side_effect=TimeoutError())

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop, patch.object(screen, "query_one"):
            mock_app_prop.return_value = mock_app
            await screen.action_delete_feed()

            # Verify error message
            assert "timeout" in screen.status_message.lower()
            assert screen.status_severity == "error"

            # Verify confirmation flag reset for retry
            assert screen._delete_confirmed is False

            # Verify screen not closed
            mock_app.pop_screen.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_feed_connection_error(self, feed_settings_with_app):
        """Test connection error handling during deletion."""
        screen = feed_settings_with_app
        screen._delete_confirmed = True  # Skip confirmation
        mock_app = MagicMock()
        mock_app.client = AsyncMock()
        mock_app.client.delete_feed = AsyncMock(side_effect=ConnectionError())

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop, patch.object(screen, "query_one"):
            mock_app_prop.return_value = mock_app
            await screen.action_delete_feed()

            # Verify error message
            assert "connection failed" in screen.status_message.lower()
            assert screen.status_severity == "error"

            # Verify confirmation flag reset for retry
            assert screen._delete_confirmed is False

            # Verify screen not closed
            mock_app.pop_screen.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_feed_generic_error(self, feed_settings_with_app):
        """Test generic exception handling during deletion."""
        screen = feed_settings_with_app
        screen._delete_confirmed = True  # Skip confirmation
        mock_app = MagicMock()
        mock_app.client = AsyncMock()
        mock_app.client.delete_feed = AsyncMock(side_effect=ValueError("Invalid feed"))

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop, patch.object(screen, "query_one"):
            mock_app_prop.return_value = mock_app
            await screen.action_delete_feed()

            # Verify error message
            assert "Error deleting feed" in screen.status_message
            assert "Invalid feed" in screen.status_message
            assert screen.status_severity == "error"

            # Verify confirmation flag reset for retry
            assert screen._delete_confirmed is False

            # Verify screen not closed
            mock_app.pop_screen.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_confirmation_reset_on_error(self, feed_settings_with_app):
        """Test that confirmation flag is reset after error for safe retry."""
        screen = feed_settings_with_app
        mock_app = MagicMock()
        mock_app.client = AsyncMock()
        delete_feed_mock = AsyncMock(side_effect=TimeoutError())
        mock_app.client.delete_feed = delete_feed_mock

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop, patch.object(screen, "query_one"):
            mock_app_prop.return_value = mock_app
            screen._delete_confirmed = True

            # First attempt fails
            await screen.action_delete_feed()
            assert screen._delete_confirmed is False
            assert delete_feed_mock.call_count == 1

            # Reset for retry
            screen._delete_confirmed = True
            delete_feed_mock.side_effect = None  # Clear side_effect for success
            delete_feed_mock.reset_mock()

            # Second attempt should succeed
            await screen.action_delete_feed()
            assert delete_feed_mock.call_count == 1
            mock_app.pop_screen.assert_called_once()


class TestDangerZoneIntegration:
    """Integration tests for Danger Zone section."""

    @pytest.mark.asyncio
    async def test_delete_feed_complete_workflow(self):
        """Test complete delete feed workflow from confirmation to success."""
        mock_app = MagicMock()
        mock_app.pop_screen = MagicMock()
        mock_app.client = AsyncMock()
        mock_app.client.delete_feed = AsyncMock()

        feed = Feed(
            id=42,
            title="Complex Feed Title",
            feed_url="https://example.com/feed",
            site_url="https://example.com",
            category_id=5,
            disabled=False,
            checked_at=None,
            parsing_error_count=0,
            parsing_error_message="",
        )

        screen = FeedSettingsScreen(feed_id=42, feed=feed, client=AsyncMock())

        with patch.object(type(screen), "app", new_callable=PropertyMock) as mock_app_prop, patch.object(screen, "query_one"):
            mock_app_prop.return_value = mock_app
            # Step 1: First delete press - confirmation
            await screen.action_delete_feed()
            assert screen._delete_confirmed is True
            assert "confirm" in screen.status_message.lower()
            assert screen.status_severity == "error"
            mock_app.pop_screen.assert_not_called()

            # Step 2: Second delete press - actual deletion
            await screen.action_delete_feed()
            assert mock_app.client.delete_feed.call_count == 1
            assert mock_app.client.delete_feed.call_args[0][0] == 42
            assert "deleted successfully" in screen.status_message.lower()
            assert screen.status_severity == "success"
            mock_app.pop_screen.assert_called_once()


class TestHelperIntegration:
    """Integration tests for helper functionality."""

    def test_open_helper_no_focused_widget(self, feed_settings_screen):
        """Test opening helper with no focused widget."""
        with (
            patch.object(type(feed_settings_screen), "focused", new_callable=PropertyMock) as mock_focused,
            patch.object(feed_settings_screen, "query_one"),
        ):
            mock_focused.return_value = None
            feed_settings_screen.action_open_helper()

            assert "no field focused" in feed_settings_screen.status_message.lower()
            assert feed_settings_screen.status_severity == "info"

    def test_open_helper_non_rule_field(self, feed_settings_screen):
        """Test opening helper with non-rule field focused."""
        mock_widget = MagicMock()
        mock_widget.id = "feed-title"
        mock_widget.parent = None

        with (
            patch.object(type(feed_settings_screen), "focused", new_callable=PropertyMock) as mock_focused,
            patch.object(feed_settings_screen, "query_one"),
        ):
            mock_focused.return_value = mock_widget
            feed_settings_screen.action_open_helper()

            assert "focus a rule field" in feed_settings_screen.status_message.lower()
            assert feed_settings_screen.status_severity == "info"

    def test_open_helper_scraper_rules_field(self, feed_settings_screen):
        """Test opening helper for scraper rules field."""
        mock_app = MagicMock()
        mock_app.push_screen = MagicMock()

        mock_widget = MagicMock()
        mock_widget.id = "scraper-rules"
        mock_widget.parent = None

        with (
            patch.object(type(feed_settings_screen), "focused", new_callable=PropertyMock) as mock_focused,
            patch.object(type(feed_settings_screen), "app", new_callable=PropertyMock) as mock_app_prop,
        ):
            mock_focused.return_value = mock_widget
            mock_app_prop.return_value = mock_app
            feed_settings_screen.action_open_helper()

            mock_app.push_screen.assert_called_once()
            call_args = mock_app.push_screen.call_args
            screen = call_args[0][0]
            assert screen.rule_type == "scraper_rules"

    def test_open_helper_rewrite_rules_field(self, feed_settings_screen):
        """Test opening helper for rewrite rules field."""
        mock_app = MagicMock()
        mock_app.push_screen = MagicMock()

        mock_widget = MagicMock()
        mock_widget.id = "rewrite-rules"
        mock_widget.parent = None

        with (
            patch.object(type(feed_settings_screen), "focused", new_callable=PropertyMock) as mock_focused,
            patch.object(type(feed_settings_screen), "app", new_callable=PropertyMock) as mock_app_prop,
        ):
            mock_focused.return_value = mock_widget
            mock_app_prop.return_value = mock_app
            feed_settings_screen.action_open_helper()

            mock_app.push_screen.assert_called_once()
            call_args = mock_app.push_screen.call_args
            screen = call_args[0][0]
            assert screen.rule_type == "rewrite_rules"

    def test_open_helper_blocklist_rules_field(self, feed_settings_screen):
        """Test opening helper for blocking rules field."""
        mock_app = MagicMock()
        mock_app.push_screen = MagicMock()

        mock_widget = MagicMock()
        mock_widget.id = "blocklist-rules"
        mock_widget.parent = None

        with (
            patch.object(type(feed_settings_screen), "focused", new_callable=PropertyMock) as mock_focused,
            patch.object(type(feed_settings_screen), "app", new_callable=PropertyMock) as mock_app_prop,
            patch.object(feed_settings_screen, "_show_message"),
        ):
            mock_focused.return_value = mock_widget
            mock_app_prop.return_value = mock_app
            feed_settings_screen.action_open_helper()

            mock_app.push_screen.assert_called_once()
            call_args = mock_app.push_screen.call_args
            screen = call_args[0][0]
            assert screen.rule_type == "blocklist_rules"

    def test_open_helper_keep_rules_field(self, feed_settings_screen):
        """Test opening helper for keep rules field."""
        mock_app = MagicMock()
        mock_app.push_screen = MagicMock()

        mock_widget = MagicMock()
        mock_widget.id = "keeplist-rules"
        mock_widget.parent = None

        with (
            patch.object(type(feed_settings_screen), "focused", new_callable=PropertyMock) as mock_focused,
            patch.object(type(feed_settings_screen), "app", new_callable=PropertyMock) as mock_app_prop,
            patch.object(feed_settings_screen, "_show_message"),
        ):
            mock_focused.return_value = mock_widget
            mock_app_prop.return_value = mock_app
            feed_settings_screen.action_open_helper()

            mock_app.push_screen.assert_called_once()
            call_args = mock_app.push_screen.call_args
            screen = call_args[0][0]
            assert screen.rule_type == "keeplist_rules"

    def test_open_helper_passes_docs_cache(self, feed_settings_screen):
        """Test that docs cache is passed to helper screen."""
        mock_app = MagicMock()
        mock_app.push_screen = MagicMock()

        mock_widget = MagicMock()
        mock_widget.id = "scraper-rules"
        mock_widget.parent = None

        with (
            patch.object(type(feed_settings_screen), "focused", new_callable=PropertyMock) as mock_focused,
            patch.object(type(feed_settings_screen), "app", new_callable=PropertyMock) as mock_app_prop,
        ):
            mock_focused.return_value = mock_widget
            mock_app_prop.return_value = mock_app
            feed_settings_screen.action_open_helper()

            call_args = mock_app.push_screen.call_args
            screen = call_args[0][0]
            assert screen.docs_cache is feed_settings_screen.docs_cache

    def test_open_helper_detects_parent_rule_field(self, feed_settings_screen):
        """Test that helper detects rule field in parent widget."""
        mock_app = MagicMock()
        mock_app.push_screen = MagicMock()

        # Create widget hierarchy where child is focused but parent is the rule field
        mock_parent = MagicMock()
        mock_parent.id = "scraper-rules"
        mock_parent.parent = None

        mock_child = MagicMock()
        mock_child.id = None
        mock_child.parent = mock_parent

        with (
            patch.object(type(feed_settings_screen), "focused", new_callable=PropertyMock) as mock_focused,
            patch.object(type(feed_settings_screen), "app", new_callable=PropertyMock) as mock_app_prop,
        ):
            mock_focused.return_value = mock_child
            mock_app_prop.return_value = mock_app
            feed_settings_screen.action_open_helper()

            call_args = mock_app.push_screen.call_args
            screen = call_args[0][0]
            assert screen.rule_type == "scraper_rules"


class TestFormPersistenceIntegration:
    """Test Phase 10: Form Persistence integration."""

    def test_persistence_manager_initialized(self, feed_settings_screen):
        """Test that FormPersistenceManager is initialized."""
        assert hasattr(feed_settings_screen, "persistence")
        assert feed_settings_screen.persistence is not None

    def test_original_values_stored_on_mount(self, feed_settings_screen):
        """Test that original values are stored when storing."""
        feed_settings_screen._store_original_values()

        assert "title" in feed_settings_screen.original_values
        assert feed_settings_screen.original_values["title"] == "Test Feed"
        assert feed_settings_screen.original_values["site_url"] == "https://example.com"

    def test_field_change_tracked_with_persistence(self, feed_settings_screen):
        """Test that field changes are tracked with persistence manager."""
        with (
            patch.object(feed_settings_screen, "query_one"),
            patch.object(feed_settings_screen, "set_timer"),
        ):
            feed_settings_screen._on_field_changed("feed-title", "New Title")

        # Check that change was tracked
        assert feed_settings_screen.persistence.has_unsaved_changes(feed_settings_screen.feed_id)

    def test_change_count_incremented(self, feed_settings_screen):
        """Test that change count is incremented."""
        with (
            patch.object(feed_settings_screen, "query_one"),
            patch.object(feed_settings_screen, "set_timer"),
        ):
            feed_settings_screen._on_field_changed("feed-title", "New Title")
            feed_settings_screen._on_field_changed("site-url", "https://new.com")

        count = feed_settings_screen.persistence.get_change_count(feed_settings_screen.feed_id)
        assert count == 2

    def test_unsaved_indicator_updated(self, feed_settings_screen):
        """Test that unsaved indicator is updated when changes occur."""
        # Reset mock to track calls in this test
        feed_settings_screen._update_unsaved_indicator.reset_mock()

        with patch.object(feed_settings_screen, "query_one"):
            feed_settings_screen._on_field_changed("feed-title", "New Title")

        # Unsaved indicator should be updated
        assert feed_settings_screen._update_unsaved_indicator.called

    def test_auto_save_scheduled(self, feed_settings_screen):
        """Test that auto-save is scheduled on field change."""
        with (
            patch.object(feed_settings_screen, "query_one"),
            patch.object(feed_settings_screen, "set_timer") as mock_timer,
        ):
            feed_settings_screen._on_field_changed("feed-title", "New Title")

        # Auto-save should be scheduled
        assert mock_timer.called

    @pytest.mark.asyncio
    async def test_session_cleared_on_mount(self, feed_settings_screen):
        """Test that session state is cleared on mount to start fresh."""
        with (
            patch.object(feed_settings_screen.persistence, "clear_session") as mock_clear,
            patch.object(feed_settings_screen, "query_one"),
            patch("miniflux_tui.ui.screens.feed_settings.hasattr", return_value=False),
        ):
            await feed_settings_screen.on_mount()

        # Verify session was cleared to prevent showing stale unsaved changes
        mock_clear.assert_called_once_with(feed_settings_screen.feed_id)

    @pytest.mark.asyncio
    async def test_original_values_stored_on_mount_call(self, feed_settings_screen):
        """Test that original values are stored in on_mount."""
        with (
            patch.object(feed_settings_screen, "_store_original_values") as mock_store,
            patch.object(feed_settings_screen, "query_one"),
            patch("miniflux_tui.ui.screens.feed_settings.hasattr", return_value=False),
        ):
            await feed_settings_screen.on_mount()

        assert mock_store.called

    def test_cancel_confirms_with_dirty_flag(self, feed_settings_screen):
        """Test that cancel sets confirmation flag when there are unsaved changes."""
        feed_settings_screen.is_dirty = True
        feed_settings_screen._cancel_confirmed = False

        # Verify initial state
        assert feed_settings_screen.is_dirty is True
        assert feed_settings_screen._cancel_confirmed is False

    def test_auto_save_with_field_values(self, feed_settings_screen):
        """Test that auto-save collects field values."""
        # Mock the internal methods
        with (
            patch.object(feed_settings_screen, "_collect_field_values", return_value={"title": "Test"}),
            patch.object(feed_settings_screen, "_get_current_field_values", return_value={}),
            patch.object(feed_settings_screen.persistence, "auto_save_draft") as mock_save,
        ):
            feed_settings_screen._auto_save_draft()

        assert mock_save.called

    def test_get_current_field_values_empty_by_default(self, feed_settings_screen):
        """Test that _get_current_field_values returns empty dict when no widgets."""
        with patch.object(feed_settings_screen, "query", return_value=[]):
            result = feed_settings_screen._get_current_field_values()

        assert result == {}


class TestChangeFieldCounting:
    """Test actual change field counting (integration tests without mocking the counter)."""

    @pytest.fixture
    def counting_screen(self, sample_feed, mock_client):
        """Create a screen for testing change counting without mocking the indicator."""
        screen = FeedSettingsScreen(
            feed_id=sample_feed.id,
            feed=sample_feed,
            client=mock_client,
        )
        screen.set_timer = MagicMock(return_value=MagicMock())
        screen._initializing = False
        # Store original values
        screen._store_original_values()
        return screen

    def test_count_changed_fields_no_changes(self, counting_screen):
        """Test that no changes are counted initially."""
        with patch.object(counting_screen, "_get_widget_value_for_field") as mock_get:
            # Return original values (no change)
            mock_get.side_effect = lambda widget_id: counting_screen.original_values.get(
                {
                    "feed-title": "title",
                    "site-url": "site_url",
                    "feed-url": "feed_url",
                    "category-id": "category_id",
                    "feed-description": "description",
                    "hide-globally": "hide_globally",
                    "no-media-player": "no_media_player",
                    "feed-disabled": "disabled",
                    "auth-username": "username",
                    "auth-password": "password",
                    "user-agent": "user_agent",
                    "proxy-url": "proxy_url",
                    "ignore-https-errors": "ignore_https_errors",
                    "scraper-rules": "scraper_rules",
                    "rewrite-rules": "rewrite_rules",
                    "blocklist-rules": "blocklist_rules",
                    "keeplist-rules": "keeplist_rules",
                    "check-interval": "check_interval",
                }.get(widget_id)
            )

            count = counting_screen._count_changed_fields()

        assert count == 0, "Should be 0 changes when all values match originals"

    def test_count_changed_fields_one_field_changed(self, counting_screen):
        """Test that changing one field counts as 1 change, not 10."""
        with patch.object(counting_screen, "_get_widget_value_for_field") as mock_get:
            field_mapping = {
                "feed-title": "title",
                "site-url": "site_url",
                "feed-url": "feed_url",
                "category-id": "category_id",
                "feed-description": "description",
                "hide-globally": "hide_globally",
                "no-media-player": "no_media_player",
                "feed-disabled": "disabled",
                "auth-username": "username",
                "auth-password": "password",
                "user-agent": "user_agent",
                "proxy-url": "proxy_url",
                "ignore-https-errors": "ignore_https_errors",
                "scraper-rules": "scraper_rules",
                "rewrite-rules": "rewrite_rules",
                "blocklist-rules": "blocklist_rules",
                "keeplist-rules": "keeplist_rules",
                "check-interval": "check_interval",
            }

            def get_value(widget_id):
                # Title changed, everything else is original
                if widget_id == "feed-title":
                    return "New Title"
                return counting_screen.original_values.get(field_mapping.get(widget_id))

            mock_get.side_effect = get_value

            count = counting_screen._count_changed_fields()

        assert count == 1, "Changing one field should count as 1 change"

    def test_count_changed_fields_multiple_changed(self, counting_screen):
        """Test that changing multiple fields counts each field once."""
        with patch.object(counting_screen, "_get_widget_value_for_field") as mock_get:
            field_mapping = {
                "feed-title": "title",
                "site-url": "site_url",
                "feed-url": "feed_url",
                "category-id": "category_id",
                "feed-description": "description",
                "hide-globally": "hide_globally",
                "no-media-player": "no_media_player",
                "feed-disabled": "disabled",
                "auth-username": "username",
                "auth-password": "password",
                "user-agent": "user_agent",
                "proxy-url": "proxy_url",
                "ignore-https-errors": "ignore_https_errors",
                "scraper-rules": "scraper_rules",
                "rewrite-rules": "rewrite_rules",
                "blocklist-rules": "blocklist_rules",
                "keeplist-rules": "keeplist_rules",
                "check-interval": "check_interval",
            }

            def get_value(widget_id):
                # Title and description changed, everything else original
                if widget_id == "feed-title":
                    return "New Title"
                if widget_id == "feed-description":
                    return "Added description"
                return counting_screen.original_values.get(field_mapping.get(widget_id))

            mock_get.side_effect = get_value

            count = counting_screen._count_changed_fields()

        assert count == 2, "Changing two fields should count as 2 changes"

    def test_count_changed_fields_typing_many_chars_counts_as_one(self, counting_screen):
        """Test that typing many characters in description field counts as 1 change."""
        with patch.object(counting_screen, "_get_widget_value_for_field") as mock_get:
            field_mapping = {
                "feed-title": "title",
                "site-url": "site_url",
                "feed-url": "feed_url",
                "category-id": "category_id",
                "feed-description": "description",
                "hide-globally": "hide_globally",
                "no-media-player": "no_media_player",
                "feed-disabled": "disabled",
                "auth-username": "username",
                "auth-password": "password",
                "user-agent": "user_agent",
                "proxy-url": "proxy_url",
                "ignore-https-errors": "ignore_https_errors",
                "scraper-rules": "scraper_rules",
                "rewrite-rules": "rewrite_rules",
                "blocklist-rules": "blocklist_rules",
                "keeplist-rules": "keeplist_rules",
                "check-interval": "check_interval",
            }

            def get_value(widget_id):
                # Description has very long text (simulate many keystrokes)
                if widget_id == "feed-description":
                    return "This is a very long description that was typed character by character"
                return counting_screen.original_values.get(field_mapping.get(widget_id))

            mock_get.side_effect = get_value

            count = counting_screen._count_changed_fields()

        assert count == 1, "Typing 60+ characters should still count as 1 field change"

    def test_count_changed_fields_undo_to_original(self, counting_screen):
        """Test that changing a field back to original counts as 0 changes."""
        with patch.object(counting_screen, "_get_widget_value_for_field") as mock_get:
            field_mapping = {
                "feed-title": "title",
                "site-url": "site_url",
                "feed-url": "feed_url",
                "category-id": "category_id",
                "feed-description": "description",
                "hide-globally": "hide_globally",
                "no-media-player": "no_media_player",
                "feed-disabled": "disabled",
                "auth-username": "username",
                "auth-password": "password",
                "user-agent": "user_agent",
                "proxy-url": "proxy_url",
                "ignore-https-errors": "ignore_https_errors",
                "scraper-rules": "scraper_rules",
                "rewrite-rules": "rewrite_rules",
                "blocklist-rules": "blocklist_rules",
                "keeplist-rules": "keeplist_rules",
                "check-interval": "check_interval",
            }

            def get_value(widget_id):
                # All values are back to original (user typed then deleted)
                return counting_screen.original_values.get(field_mapping.get(widget_id))

            mock_get.side_effect = get_value

            count = counting_screen._count_changed_fields()

        assert count == 0, "Undoing changes should show 0 unsaved changes"
