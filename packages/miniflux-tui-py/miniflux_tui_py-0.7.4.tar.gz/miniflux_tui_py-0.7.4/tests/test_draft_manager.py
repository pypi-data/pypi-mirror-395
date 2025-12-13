# SPDX-License-Identifier: MIT
"""Tests for the DraftManager."""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from miniflux_tui.draft_manager import Draft, DraftManager


@pytest.fixture
def mock_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def draft_manager(mock_config_dir):
    """Create a DraftManager with mocked config directory."""
    with patch("miniflux_tui.draft_manager.get_config_dir") as mock_get_dir:
        mock_get_dir.return_value = mock_config_dir
        manager = DraftManager()
        yield manager


class TestDraft:
    """Test the Draft dataclass."""

    def test_draft_creation(self):
        """Test creating a draft."""
        draft = Draft(
            feed_id=1,
            timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC),
            field_values={"title": "Test Feed"},
        )
        assert draft.feed_id == 1
        assert draft.field_values["title"] == "Test Feed"

    def test_draft_to_dict(self):
        """Test converting draft to dictionary."""
        draft = Draft(
            feed_id=1,
            timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC),
            field_values={"title": "Test Feed"},
        )
        data = draft.to_dict()

        assert data["feed_id"] == 1
        assert data["field_values"]["title"] == "Test Feed"
        assert data["timestamp"] == "2025-01-01T12:00:00+00:00"

    def test_draft_from_dict(self):
        """Test creating draft from dictionary."""
        data = {
            "feed_id": 1,
            "timestamp": "2025-01-01T12:00:00+00:00",
            "field_values": {"title": "Test Feed"},
        }
        draft = Draft.from_dict(data)

        assert draft.feed_id == 1
        assert draft.field_values["title"] == "Test Feed"
        assert draft.timestamp == datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)

    def test_draft_from_dict_missing_feed_id(self):
        """Test from_dict with missing feed_id."""
        data = {"timestamp": "2025-01-01T12:00:00"}
        with pytest.raises(ValueError, match="feed_id and timestamp"):
            Draft.from_dict(data)

    def test_draft_from_dict_missing_timestamp(self):
        """Test from_dict with missing timestamp."""
        data = {"feed_id": 1}
        with pytest.raises(ValueError, match="feed_id and timestamp"):
            Draft.from_dict(data)

    def test_draft_from_dict_datetime_object(self):
        """Test from_dict with datetime object instead of string."""
        now = datetime.now(tz=UTC)
        data = {
            "feed_id": 1,
            "timestamp": now,
            "field_values": {"title": "Test"},
        }
        draft = Draft.from_dict(data)
        assert draft.timestamp == now


class TestDraftManagerInitialization:
    """Test DraftManager initialization."""

    def test_init_creates_drafts_directory(self, draft_manager):
        """Test that initialization creates drafts directory."""
        assert draft_manager.drafts_dir.exists()

    def test_init_with_existing_drafts_dir(self, mock_config_dir):
        """Test initialization when drafts directory already exists."""
        drafts_dir = mock_config_dir / "drafts"
        drafts_dir.mkdir()

        with patch("miniflux_tui.draft_manager.get_config_dir") as mock_get_dir:
            mock_get_dir.return_value = mock_config_dir
            manager = DraftManager()
            assert manager.drafts_dir.exists()


class TestDraftManagerSaveLoad:
    """Test saving and loading drafts."""

    def test_save_draft(self, draft_manager):
        """Test saving a draft."""
        field_values = {
            "feed-title": "Test Feed",
            "site-url": "https://example.com",
        }
        draft = draft_manager.save_draft(1, field_values)

        assert draft.feed_id == 1
        assert draft.field_values == field_values
        assert (draft_manager.drafts_dir / "draft_1.json").exists()

    def test_save_draft_overwrites_existing(self, draft_manager):
        """Test that saving a draft overwrites existing one."""
        draft_manager.save_draft(1, {"field1": "value1"})
        draft_manager.save_draft(1, {"field2": "value2"})

        draft = draft_manager.load_draft(1)
        assert draft.field_values == {"field2": "value2"}

    def test_load_draft(self, draft_manager):
        """Test loading a draft."""
        original = draft_manager.save_draft(1, {"title": "Test"})
        loaded = draft_manager.load_draft(1)

        assert loaded is not None
        assert loaded.feed_id == original.feed_id
        assert loaded.field_values == original.field_values

    def test_load_nonexistent_draft(self, draft_manager):
        """Test loading a draft that doesn't exist."""
        draft = draft_manager.load_draft(999)
        assert draft is None

    def test_load_corrupted_draft(self, draft_manager):
        """Test loading a corrupted draft file."""
        draft_file = draft_manager.drafts_dir / "draft_1.json"
        draft_file.write_text("invalid json {")

        draft = draft_manager.load_draft(1)
        assert draft is None

    def test_draft_with_empty_field_values(self, draft_manager):
        """Test saving and loading draft with no field values."""
        draft = draft_manager.save_draft(1, {})
        loaded = draft_manager.load_draft(1)

        # Verify the saved draft matches the loaded draft
        assert draft is not None
        assert draft.feed_id == loaded.feed_id
        assert loaded is not None
        assert loaded.field_values == {}

    def test_draft_with_complex_field_values(self, draft_manager):
        """Test saving draft with complex field values."""
        field_values = {
            "title": "Test",
            "number": 42,
            "list": [1, 2, 3],
            "nested": {"key": "value"},
            "null_value": None,
        }
        draft_manager.save_draft(1, field_values)
        loaded = draft_manager.load_draft(1)

        assert loaded.field_values == field_values


class TestDraftManagerQueries:
    """Test draft query methods."""

    def test_has_draft_exists(self, draft_manager):
        """Test checking if draft exists."""
        draft_manager.save_draft(1, {"field": "value"})
        assert draft_manager.has_draft(1)

    def test_has_draft_not_exists(self, draft_manager):
        """Test checking if draft doesn't exist."""
        assert not draft_manager.has_draft(999)

    def test_get_draft_timestamp(self, draft_manager):
        """Test getting draft timestamp."""
        now = datetime.now(tz=UTC)
        draft_manager.save_draft(1, {"field": "value"})
        timestamp = draft_manager.get_draft_timestamp(1)

        assert timestamp is not None
        assert abs((timestamp - now).total_seconds()) < 1

    def test_get_draft_timestamp_nonexistent(self, draft_manager):
        """Test getting timestamp for nonexistent draft."""
        timestamp = draft_manager.get_draft_timestamp(999)
        assert timestamp is None

    def test_list_drafts_empty(self, draft_manager):
        """Test listing drafts when none exist."""
        drafts = draft_manager.list_drafts()
        assert drafts == []

    def test_list_drafts_multiple(self, draft_manager):
        """Test listing multiple drafts."""
        draft_manager.save_draft(1, {"field": "value1"})
        draft_manager.save_draft(2, {"field": "value2"})
        draft_manager.save_draft(3, {"field": "value3"})

        drafts = draft_manager.list_drafts()
        assert len(drafts) == 3

    def test_list_drafts_sorted_by_timestamp(self, draft_manager):
        """Test that drafts are sorted by timestamp (newest first)."""
        # Save drafts with a delay between them to ensure different timestamps
        # (save_draft creates new Draft with current timestamp)
        draft_manager.save_draft(1, {"old": True})
        time.sleep(0.01)  # 10ms delay to ensure timestamp difference
        draft_manager.save_draft(2, {"new": True})

        drafts = draft_manager.list_drafts()
        assert drafts[0].feed_id == 2  # Newest first
        assert drafts[1].feed_id == 1


class TestDraftManagerDeletion:
    """Test draft deletion methods."""

    def test_delete_draft_exists(self, draft_manager):
        """Test deleting an existing draft."""
        draft_manager.save_draft(1, {"field": "value"})
        assert draft_manager.delete_draft(1)
        assert not draft_manager.has_draft(1)

    def test_delete_draft_not_exists(self, draft_manager):
        """Test deleting a nonexistent draft."""
        assert not draft_manager.delete_draft(999)

    def test_cleanup_old_drafts(self, draft_manager):
        """Test cleaning up old drafts."""
        # Create old draft
        old_draft_file = draft_manager.drafts_dir / "draft_1.json"
        old_draft = Draft(
            feed_id=1,
            timestamp=datetime.now(tz=UTC) - timedelta(days=10),
            field_values={},
        )
        old_draft_file.write_text(json.dumps(old_draft.to_dict()))

        # Create recent draft
        draft_manager.save_draft(2, {"field": "value"})

        # Cleanup drafts older than 7 days
        deleted = draft_manager.cleanup_old_drafts(days=7)

        assert deleted == 1
        assert not draft_manager.has_draft(1)
        assert draft_manager.has_draft(2)

    def test_cleanup_old_drafts_none_to_delete(self, draft_manager):
        """Test cleanup when no old drafts exist."""
        draft_manager.save_draft(1, {"field": "value"})
        deleted = draft_manager.cleanup_old_drafts(days=7)
        assert deleted == 0

    def test_clear_all_drafts(self, draft_manager):
        """Test clearing all drafts."""
        draft_manager.save_draft(1, {"field": "value1"})
        draft_manager.save_draft(2, {"field": "value2"})
        draft_manager.save_draft(3, {"field": "value3"})

        deleted = draft_manager.clear_all_drafts()
        assert deleted == 3
        assert draft_manager.list_drafts() == []

    def test_clear_all_drafts_empty(self, draft_manager):
        """Test clearing when no drafts exist."""
        deleted = draft_manager.clear_all_drafts()
        assert deleted == 0


class TestDraftManagerErrorHandling:
    """Test error handling in DraftManager."""

    def test_save_draft_io_error(self, draft_manager):
        """Test handling IO error when saving draft."""
        # Mock the drafts_dir to raise OSError when writing (cross-platform approach)
        with patch.object(draft_manager, "drafts_dir") as mock_drafts_dir:
            mock_file = mock_drafts_dir / "draft_1.json"
            mock_file.write_text.side_effect = OSError("Permission denied")

            with pytest.raises(OSError, match="Failed to save draft"):
                draft_manager.save_draft(1, {"field": "value"})

    def test_load_invalid_feed_id(self, draft_manager):
        """Test loading with invalid feed ID."""
        # Manually create a malformed draft file
        bad_draft_file = draft_manager.drafts_dir / "draft_bad.json"
        bad_draft_file.write_text('{"timestamp": "2025-01-01T12:00:00"}')

        # This should not crash
        draft = draft_manager.load_draft(999)
        assert draft is None

    def test_list_drafts_with_corrupted_file(self, draft_manager):
        """Test listing drafts when one is corrupted."""
        draft_manager.save_draft(1, {"field": "value"})
        draft_manager.save_draft(2, {"field": "value"})

        # Corrupt one draft
        (draft_manager.drafts_dir / "draft_1.json").write_text("invalid")

        drafts = draft_manager.list_drafts()
        # Should still load the valid one
        assert len(drafts) == 1
        assert drafts[0].feed_id == 2


class TestDraftManagerIntegration:
    """Integration tests for DraftManager."""

    def test_full_workflow(self, draft_manager):
        """Test complete workflow: save, load, modify, delete."""
        # Save initial draft
        initial_values = {"title": "Original Title"}
        draft_manager.save_draft(1, initial_values)

        # Load and verify
        loaded = draft_manager.load_draft(1)
        assert loaded.field_values == initial_values

        # Update draft
        updated_values = {"title": "Updated Title", "url": "https://example.com"}
        draft_manager.save_draft(1, updated_values)

        # Load and verify update
        reloaded = draft_manager.load_draft(1)
        assert reloaded.field_values == updated_values

        # Delete
        draft_manager.delete_draft(1)
        assert draft_manager.load_draft(1) is None

    def test_multiple_feeds_drafts(self, draft_manager):
        """Test managing drafts for multiple feeds."""
        # Create drafts for multiple feeds
        for feed_id in range(1, 6):
            draft_manager.save_draft(feed_id, {"feed_id": feed_id})

        # Verify all exist
        assert len(draft_manager.list_drafts()) == 5

        # Delete one
        draft_manager.delete_draft(3)

        # Verify count
        assert len(draft_manager.list_drafts()) == 4

    def test_draft_metadata(self, draft_manager):
        """Test draft metadata handling."""
        draft = draft_manager.save_draft(1, {"field": "value"})
        assert "version" in draft.metadata
        assert draft.metadata["version"] == 1

        loaded = draft_manager.load_draft(1)
        assert loaded.metadata["version"] == 1
