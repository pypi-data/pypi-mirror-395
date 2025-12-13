# SPDX-License-Identifier: MIT
"""Tests for the ChangeTracker."""

from __future__ import annotations

from datetime import UTC, datetime

from miniflux_tui.change_tracker import (
    ChangeHistory,
    ChangeTracker,
    FieldChange,
)


class TestFieldChange:
    """Test the FieldChange dataclass."""

    def test_field_change_creation(self):
        """Test creating a field change."""
        change = FieldChange(
            field_id="title",
            field_name="Title",
            before_value="Old Title",
            after_value="New Title",
            timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC),
        )

        assert change.field_id == "title"
        assert change.field_name == "Title"
        assert change.before_value == "Old Title"
        assert change.after_value == "New Title"
        assert change.change_type == "modified"

    def test_field_change_is_modified(self):
        """Test identifying modified field."""
        change = FieldChange(
            field_id="url",
            field_name="URL",
            before_value="https://old.com",
            after_value="https://new.com",
            timestamp=datetime.now(tz=UTC),
            change_type="modified",
        )

        assert change.is_modified()
        assert not change.is_added()
        assert not change.is_removed()

    def test_field_change_is_added(self):
        """Test identifying added field."""
        change = FieldChange(
            field_id="description",
            field_name="Description",
            before_value=None,
            after_value="New description",
            timestamp=datetime.now(tz=UTC),
            change_type="added",
        )

        assert change.is_added()
        assert not change.is_modified()
        assert not change.is_removed()

    def test_field_change_is_removed(self):
        """Test identifying removed field."""
        change = FieldChange(
            field_id="notes",
            field_name="Notes",
            before_value="Old notes",
            after_value=None,
            timestamp=datetime.now(tz=UTC),
            change_type="removed",
        )

        assert change.is_removed()
        assert not change.is_modified()
        assert not change.is_added()

    def test_field_change_to_dict(self):
        """Test converting field change to dictionary."""
        change = FieldChange(
            field_id="title",
            field_name="Title",
            before_value="Old",
            after_value="New",
            timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC),
        )

        data = change.to_dict()

        assert data["field_id"] == "title"
        assert data["before_value"] == "Old"
        assert data["after_value"] == "New"
        assert data["timestamp"] == "2025-01-01T12:00:00+00:00"

    def test_field_change_from_dict(self):
        """Test creating field change from dictionary."""
        data = {
            "field_id": "url",
            "field_name": "URL",
            "before_value": "https://old.com",
            "after_value": "https://new.com",
            "timestamp": "2025-01-01T12:00:00+00:00",
            "change_type": "modified",
        }

        change = FieldChange.from_dict(data)

        assert change.field_id == "url"
        assert change.before_value == "https://old.com"
        assert change.after_value == "https://new.com"
        assert change.is_modified()


class TestChangeHistory:
    """Test the ChangeHistory dataclass."""

    def test_change_history_creation(self):
        """Test creating change history."""
        history = ChangeHistory(feed_id=1)

        assert history.feed_id == 1
        assert history.changes == []
        assert history.has_changes() is False

    def test_change_history_add_change(self):
        """Test adding a change to history."""
        history = ChangeHistory(feed_id=1)
        change = FieldChange(
            field_id="title",
            field_name="Title",
            before_value="Old",
            after_value="New",
            timestamp=datetime.now(tz=UTC),
        )

        history.add_change(change)

        assert len(history.changes) == 1
        assert history.has_changes() is True

    def test_change_history_get_field_changes(self):
        """Test retrieving changes for a specific field."""
        history = ChangeHistory(feed_id=1)
        change1 = FieldChange(
            field_id="title",
            field_name="Title",
            before_value="Old",
            after_value="New",
            timestamp=datetime.now(tz=UTC),
        )
        change2 = FieldChange(
            field_id="url",
            field_name="URL",
            before_value="old.com",
            after_value="new.com",
            timestamp=datetime.now(tz=UTC),
        )

        history.add_change(change1)
        history.add_change(change2)

        title_changes = history.get_field_changes("title")
        assert len(title_changes) == 1
        assert title_changes[0].field_id == "title"

    def test_change_history_get_changes_by_type(self):
        """Test retrieving changes by type."""
        history = ChangeHistory(feed_id=1)

        history.add_change(
            FieldChange(
                field_id="f1",
                field_name="F1",
                before_value=None,
                after_value="added",
                timestamp=datetime.now(tz=UTC),
                change_type="added",
            )
        )
        history.add_change(
            FieldChange(
                field_id="f2",
                field_name="F2",
                before_value="old",
                after_value="new",
                timestamp=datetime.now(tz=UTC),
                change_type="modified",
            )
        )
        history.add_change(
            FieldChange(
                field_id="f3",
                field_name="F3",
                before_value="removed",
                after_value=None,
                timestamp=datetime.now(tz=UTC),
                change_type="removed",
            )
        )

        added = history.get_added_fields()
        modified = history.get_modified_fields()
        removed = history.get_removed_fields()

        assert len(added) == 1
        assert len(modified) == 1
        assert len(removed) == 1

    def test_change_history_get_change_count(self):
        """Test getting change count."""
        history = ChangeHistory(feed_id=1)

        assert history.get_change_count() == 0

        history.add_change(
            FieldChange(
                field_id="f1",
                field_name="F1",
                before_value="old",
                after_value="new",
                timestamp=datetime.now(tz=UTC),
            )
        )

        assert history.get_change_count() == 1

    def test_change_history_to_dict(self):
        """Test converting history to dictionary."""
        history = ChangeHistory(feed_id=1)
        history.add_change(
            FieldChange(
                field_id="title",
                field_name="Title",
                before_value="Old",
                after_value="New",
                timestamp=datetime.now(tz=UTC),
            )
        )

        data = history.to_dict()

        assert data["feed_id"] == 1
        assert len(data["changes"]) == 1
        assert "created_at" in data
        assert "last_modified" in data

    def test_change_history_from_dict(self):
        """Test creating history from dictionary."""
        data = {
            "feed_id": 1,
            "changes": [
                {
                    "field_id": "title",
                    "field_name": "Title",
                    "before_value": "Old",
                    "after_value": "New",
                    "timestamp": datetime.now(tz=UTC).isoformat(),
                    "change_type": "modified",
                }
            ],
            "created_at": datetime.now(tz=UTC).isoformat(),
            "last_modified": datetime.now(tz=UTC).isoformat(),
        }

        history = ChangeHistory.from_dict(data)

        assert history.feed_id == 1
        assert len(history.changes) == 1
        assert history.changes[0].field_id == "title"


class TestChangeTrackerTracking:
    """Test tracking functionality."""

    def test_track_modified_change(self):
        """Test tracking a modified field."""
        tracker = ChangeTracker()

        tracker.track_change(
            feed_id=1,
            field_id="title",
            field_name="Title",
            before_value="Old",
            after_value="New",
        )

        assert tracker.has_changes(1) is True
        history = tracker.get_history(1)
        assert history is not None
        assert len(history.changes) == 1
        assert history.changes[0].is_modified()

    def test_track_added_change(self):
        """Test tracking an added field."""
        tracker = ChangeTracker()

        tracker.track_change(
            feed_id=1,
            field_id="desc",
            field_name="Description",
            before_value=None,
            after_value="New description",
        )

        history = tracker.get_history(1)
        assert history.changes[0].is_added()

    def test_track_removed_change(self):
        """Test tracking a removed field."""
        tracker = ChangeTracker()

        tracker.track_change(
            feed_id=1,
            field_id="notes",
            field_name="Notes",
            before_value="Old notes",
            after_value=None,
        )

        history = tracker.get_history(1)
        assert history.changes[0].is_removed()

    def test_track_multiple_changes(self):
        """Test tracking multiple changes."""
        tracker = ChangeTracker()

        tracker.track_change(1, "title", "Title", "Old", "New")
        tracker.track_change(1, "url", "URL", "old.com", "new.com")
        tracker.track_change(1, "desc", "Description", None, "Added")

        history = tracker.get_history(1)
        assert history.get_change_count() == 3

    def test_track_changes_for_multiple_feeds(self):
        """Test tracking changes for different feeds."""
        tracker = ChangeTracker()

        tracker.track_change(1, "title", "Title", "Old1", "New1")
        tracker.track_change(2, "title", "Title", "Old2", "New2")
        tracker.track_change(3, "title", "Title", "Old3", "New3")

        assert tracker.has_changes(1)
        assert tracker.has_changes(2)
        assert tracker.has_changes(3)
        assert tracker.get_history(1).get_change_count() == 1
        assert tracker.get_history(2).get_change_count() == 1
        assert tracker.get_history(3).get_change_count() == 1


class TestChangeTrackerQueries:
    """Test query functionality."""

    def test_get_history_nonexistent(self):
        """Test getting history for feed with no changes."""
        tracker = ChangeTracker()
        history = tracker.get_history(999)
        assert history is None

    def test_has_changes_nonexistent(self):
        """Test checking changes for feed with none."""
        tracker = ChangeTracker()
        assert tracker.has_changes(999) is False

    def test_get_field_changes(self):
        """Test getting all changes for a field."""
        tracker = ChangeTracker()

        # Track multiple changes to same field
        tracker.track_change(1, "title", "Title", "V1", "V2")
        # Add another change (overwriting same field)
        tracker.track_change(1, "title", "Title", "V2", "V3")

        changes = tracker.get_field_changes(1, "title")
        assert len(changes) == 2

    def test_get_last_change(self):
        """Test getting most recent change for a field."""
        tracker = ChangeTracker()

        tracker.track_change(1, "title", "Title", "Old", "Middle")
        tracker.track_change(1, "title", "Title", "Middle", "New")

        last = tracker.get_last_change(1, "title")
        assert last is not None
        assert last.after_value == "New"

    def test_get_field_diff(self):
        """Test getting before/after diff for a field."""
        tracker = ChangeTracker()

        tracker.track_change(1, "url", "URL", "https://old.com", "https://new.com")

        diff = tracker.get_field_diff(1, "url")
        assert diff is not None
        assert diff["before"] == "https://old.com"
        assert diff["after"] == "https://new.com"

    def test_get_summary(self):
        """Test getting summary of all changes."""
        tracker = ChangeTracker()

        tracker.track_change(1, "f1", "F1", "old", "new")
        tracker.track_change(1, "f2", "F2", None, "added")
        tracker.track_change(1, "f3", "F3", "removed", None)

        summary = tracker.get_summary(1)
        assert summary is not None
        assert summary["total_changes"] == 3
        assert summary["modified_count"] == 1
        assert summary["added_count"] == 1
        assert summary["removed_count"] == 1


class TestChangeTrackerCleanup:
    """Test cleanup functionality."""

    def test_clear_history(self):
        """Test clearing history for a feed."""
        tracker = ChangeTracker()

        tracker.track_change(1, "title", "Title", "Old", "New")
        assert tracker.has_changes(1)

        tracker.clear_history(1)
        assert tracker.has_changes(1) is False

    def test_clear_all_history(self):
        """Test clearing all tracked history."""
        tracker = ChangeTracker()

        tracker.track_change(1, "title", "Title", "Old", "New")
        tracker.track_change(2, "title", "Title", "Old", "New")

        assert tracker.has_changes(1)
        assert tracker.has_changes(2)

        tracker.clear_all_history()

        assert tracker.has_changes(1) is False
        assert tracker.has_changes(2) is False


class TestChangeTrackerComplexValues:
    """Test handling complex field values."""

    def test_track_list_values(self):
        """Test tracking changes with list values."""
        tracker = ChangeTracker()

        tracker.track_change(1, "tags", "Tags", ["old1", "old2"], ["new1", "new2", "new3"])

        diff = tracker.get_field_diff(1, "tags")
        assert diff["before"] == ["old1", "old2"]
        assert diff["after"] == ["new1", "new2", "new3"]

    def test_track_dict_values(self):
        """Test tracking changes with dict values."""
        tracker = ChangeTracker()

        before = {"name": "Old", "value": 1}
        after = {"name": "New", "value": 2}

        tracker.track_change(1, "config", "Config", before, after)

        diff = tracker.get_field_diff(1, "config")
        assert diff["before"] == before
        assert diff["after"] == after

    def test_track_null_values(self):
        """Test tracking changes with null/None values."""
        tracker = ChangeTracker()

        tracker.track_change(1, "field", "Field", None, "value")
        tracker.track_change(1, "other", "Other", "value", None)

        assert tracker.get_last_change(1, "field").is_added()
        assert tracker.get_last_change(1, "other").is_removed()


class TestChangeTrackerIntegration:
    """Integration tests."""

    def test_full_tracking_workflow(self):
        """Test complete tracking workflow."""
        tracker = ChangeTracker()

        # Track multiple changes
        tracker.track_change(1, "title", "Title", "Original", "Updated")
        tracker.track_change(1, "url", "URL", "old.com", "new.com")
        tracker.track_change(1, "desc", "Description", None, "New desc")

        # Verify history
        history = tracker.get_history(1)
        assert history.get_change_count() == 3

        # Get summary
        summary = tracker.get_summary(1)
        assert summary["total_changes"] == 3
        assert summary["modified_count"] == 2
        assert summary["added_count"] == 1

        # Get specific diffs
        title_diff = tracker.get_field_diff(1, "title")
        assert title_diff["before"] == "Original"
        assert title_diff["after"] == "Updated"

        # Clear and verify
        tracker.clear_history(1)
        assert tracker.get_summary(1) is None

    def test_multiple_feeds_independent_tracking(self):
        """Test that different feeds have independent change histories."""
        tracker = ChangeTracker()

        tracker.track_change(1, "title", "Title", "Feed1Old", "Feed1New")
        tracker.track_change(2, "title", "Title", "Feed2Old", "Feed2New")
        tracker.track_change(3, "title", "Title", "Feed3Old", "Feed3New")

        # Verify independence
        diff1 = tracker.get_field_diff(1, "title")
        diff2 = tracker.get_field_diff(2, "title")
        diff3 = tracker.get_field_diff(3, "title")

        assert diff1["after"] == "Feed1New"
        assert diff2["after"] == "Feed2New"
        assert diff3["after"] == "Feed3New"

        # Clear one feed
        tracker.clear_history(1)
        assert tracker.get_history(1) is None
        assert tracker.get_history(2) is not None
        assert tracker.get_history(3) is not None
