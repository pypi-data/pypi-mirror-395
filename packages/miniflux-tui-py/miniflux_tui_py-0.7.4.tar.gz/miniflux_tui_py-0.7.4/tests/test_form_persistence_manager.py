# SPDX-License-Identifier: MIT
"""Tests for FormPersistenceManager."""

from __future__ import annotations

from miniflux_tui.form_persistence_manager import FormPersistenceManager


class TestFormPersistenceManagerInitialization:
    """Test manager initialization."""

    def test_init(self):
        """Test creating a FormPersistenceManager."""
        manager = FormPersistenceManager()

        assert manager is not None
        assert manager.draft_manager is not None
        assert manager.recovery_manager is not None
        assert manager.change_tracker is not None


class TestFormPersistenceManagerRecovery:
    """Test recovery-related operations."""

    def test_check_for_recovery_no_recovery(self):
        """Test checking for recovery when none exists."""
        manager = FormPersistenceManager()
        result = manager.check_for_recovery(999)

        assert result is None

    def test_should_prompt_recovery_first_time(self):
        """Test prompting on first recovery check."""
        manager = FormPersistenceManager()
        assert manager.should_prompt_recovery(1) is True

    def test_mark_recovery_handled(self):
        """Test marking recovery as handled."""
        manager = FormPersistenceManager()

        assert manager.should_prompt_recovery(1) is True
        manager.mark_recovery_handled(1)
        assert manager.should_prompt_recovery(1) is False


class TestFormPersistenceManagerTracking:
    """Test change tracking operations."""

    def test_has_no_changes_initially(self):
        """Test that no changes exist initially."""
        manager = FormPersistenceManager()
        assert manager.has_unsaved_changes(1) is False

    def test_track_field_change(self):
        """Test tracking a field change."""
        manager = FormPersistenceManager()

        manager.track_field_change(1, "title", "Title", "Old", "New")

        assert manager.has_unsaved_changes(1) is True
        assert manager.get_change_count(1) == 1

    def test_track_multiple_changes(self):
        """Test tracking multiple changes."""
        manager = FormPersistenceManager()

        manager.track_field_change(1, "title", "Title", "Old", "New")
        manager.track_field_change(1, "url", "URL", "old.com", "new.com")

        assert manager.get_change_count(1) == 2

    def test_get_field_change_summary(self):
        """Test getting change summary."""
        manager = FormPersistenceManager()

        manager.track_field_change(1, "title", "Title", "Old", "New")
        manager.track_field_change(1, "url", "URL", "old.com", "new.com")

        summary = manager.get_field_change_summary(1)
        assert summary is not None
        assert summary["total_changes"] == 2

    def test_get_field_diff(self):
        """Test getting before/after diff."""
        manager = FormPersistenceManager()

        manager.track_field_change(1, "title", "Title", "Old", "New")

        diff = manager.get_field_diff(1, "title")
        assert diff is not None
        assert diff["before"] == "Old"
        assert diff["after"] == "New"


class TestFormPersistenceManagerDrafts:
    """Test draft operations."""

    def test_auto_save_draft(self):
        """Test auto-saving draft."""
        manager = FormPersistenceManager()
        field_values = {"title": "Test Feed"}

        # Should not raise
        manager.auto_save_draft(1, field_values)

    def test_clear_draft_after_save(self):
        """Test clearing draft after save."""
        manager = FormPersistenceManager()

        # Should not raise
        manager.clear_draft_after_save(1)


class TestFormPersistenceManagerCleanup:
    """Test cleanup operations."""

    def test_clear_session(self):
        """Test clearing a session."""
        manager = FormPersistenceManager()

        manager.track_field_change(1, "title", "Title", "Old", "New")
        assert manager.has_unsaved_changes(1) is True

        manager.clear_session(1)
        assert manager.has_unsaved_changes(1) is False

    def test_cleanup_old_sessions(self):
        """Test cleanup of old sessions."""
        manager = FormPersistenceManager()

        # Should not raise and return count
        count = manager.cleanup_old_sessions(days=7)
        assert isinstance(count, int)


class TestFormPersistenceManagerBatch:
    """Test batch operations."""

    def test_save_all_state(self):
        """Test saving all state."""
        manager = FormPersistenceManager()
        field_values = {"title": "Feed", "url": "https://example.com"}

        # Should not raise
        manager.save_all_state(1, field_values)

    def test_restore_all_state_none(self):
        """Test restoring state when none exists."""
        manager = FormPersistenceManager()

        result = manager.restore_all_state(999)
        assert result is None

    def test_get_full_session_info(self):
        """Test getting full session information."""
        manager = FormPersistenceManager()

        info = manager.get_full_session_info(1)

        assert info["feed_id"] == 1
        assert "has_recovery" in info
        assert "has_changes" in info
        assert "change_count" in info


class TestFormPersistenceManagerWorkflow:
    """Integration workflow tests."""

    def test_complete_editing_workflow(self):
        """Test complete workflow: edit, track, save."""
        manager = FormPersistenceManager()
        feed_id = 1

        # Initial state: no changes
        assert manager.has_unsaved_changes(feed_id) is False
        assert manager.get_change_count(feed_id) == 0

        # Track changes as user edits
        manager.track_field_change(feed_id, "title", "Title", "Original", "Updated")
        manager.track_field_change(feed_id, "url", "URL", "old.com", "new.com")

        # Check state after editing
        assert manager.has_unsaved_changes(feed_id) is True
        assert manager.get_change_count(feed_id) == 2

        # Save state
        field_values = {"title": "Updated", "url": "new.com"}
        manager.save_all_state(feed_id, field_values)

        # Clear session after successful save
        manager.clear_session(feed_id)
        assert manager.has_unsaved_changes(feed_id) is False

    def test_multiple_independent_feeds(self):
        """Test managing multiple feeds independently."""
        manager = FormPersistenceManager()

        # Feed 1
        manager.track_field_change(1, "title", "Title", "F1Old", "F1New")

        # Feed 2
        manager.track_field_change(2, "title", "Title", "F2Old", "F2New")

        # Feed 3
        manager.track_field_change(3, "title", "Title", "F3Old", "F3New")

        # Check independence
        assert manager.has_unsaved_changes(1) is True
        assert manager.has_unsaved_changes(2) is True
        assert manager.has_unsaved_changes(3) is True

        # Clear feed 1
        manager.clear_session(1)

        assert manager.has_unsaved_changes(1) is False
        assert manager.has_unsaved_changes(2) is True
        assert manager.has_unsaved_changes(3) is True

    def test_recovery_and_changes_together(self):
        """Test recovery and change tracking together."""
        manager = FormPersistenceManager()
        feed_id = 1

        # Check for recovery (none yet)
        recovery = manager.check_for_recovery(feed_id)
        assert recovery is None

        # Track changes
        manager.track_field_change(feed_id, "title", "Title", "Old", "New")
        assert manager.has_unsaved_changes(feed_id) is True

        # Get session info
        info = manager.get_full_session_info(feed_id)
        assert info["change_count"] == 1
        assert info["has_recovery"] is False
