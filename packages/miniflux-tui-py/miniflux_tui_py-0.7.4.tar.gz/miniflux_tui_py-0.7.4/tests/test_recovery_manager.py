# SPDX-License-Identifier: MIT
"""Tests for the RecoveryManager."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from miniflux_tui.draft_manager import Draft
from miniflux_tui.recovery_manager import (
    RecoveryInfo,
    RecoveryManager,
    _format_time_delta,
)


@pytest.fixture
def recovery_manager():
    """Create a RecoveryManager with mocked draft manager."""
    with patch("miniflux_tui.recovery_manager.DraftManager") as mock_dm:
        manager = RecoveryManager()
        manager.draft_manager = mock_dm.return_value
        yield manager


class TestRecoveryInfo:
    """Test the RecoveryInfo dataclass."""

    def test_recovery_info_creation(self):
        """Test creating RecoveryInfo."""
        draft = Draft(
            feed_id=1,
            timestamp=datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC),
            field_values={"title": "Test"},
        )
        info = RecoveryInfo.from_draft(draft)

        assert info.feed_id == 1
        assert info.draft == draft
        assert isinstance(info.time_since_last_save, str)

    def test_recovery_info_time_formatting(self):
        """Test that time_since_last_save is formatted."""
        draft = Draft(
            feed_id=1,
            timestamp=datetime.now(tz=UTC) - timedelta(hours=2),
            field_values={},
        )
        info = RecoveryInfo.from_draft(draft)

        assert "hour" in info.time_since_last_save or "ago" in info.time_since_last_save


class TestFormatTimeDelta:
    """Test the time delta formatting function."""

    def test_format_just_now(self):
        """Test formatting for very recent timestamps."""
        timestamp = datetime.now(tz=UTC) - timedelta(seconds=10)
        result = _format_time_delta(timestamp)
        assert result == "just now"

    def test_format_minutes_ago(self):
        """Test formatting for minutes."""
        timestamp = datetime.now(tz=UTC) - timedelta(minutes=5)
        result = _format_time_delta(timestamp)
        assert result == "5 minutes ago"

    def test_format_singular_minute(self):
        """Test singular minute formatting."""
        timestamp = datetime.now(tz=UTC) - timedelta(minutes=1)
        result = _format_time_delta(timestamp)
        assert result == "1 minute ago"

    def test_format_hours_ago(self):
        """Test formatting for hours."""
        timestamp = datetime.now(tz=UTC) - timedelta(hours=3)
        result = _format_time_delta(timestamp)
        assert result == "3 hours ago"

    def test_format_singular_hour(self):
        """Test singular hour formatting."""
        timestamp = datetime.now(tz=UTC) - timedelta(hours=1)
        result = _format_time_delta(timestamp)
        assert result == "1 hour ago"

    def test_format_days_ago(self):
        """Test formatting for days."""
        timestamp = datetime.now(tz=UTC) - timedelta(days=5)
        result = _format_time_delta(timestamp)
        assert result == "5 days ago"

    def test_format_singular_day(self):
        """Test singular day formatting."""
        timestamp = datetime.now(tz=UTC) - timedelta(days=1)
        result = _format_time_delta(timestamp)
        assert result == "1 day ago"


class TestRecoveryManagerInitialization:
    """Test RecoveryManager initialization."""

    def test_init(self, recovery_manager):
        """Test initialization."""
        assert recovery_manager.draft_manager is not None
        assert recovery_manager.last_recovery_prompt == {}

    def test_init_creates_draft_manager(self):
        """Test that initialization creates DraftManager."""
        with patch("miniflux_tui.recovery_manager.DraftManager") as mock_dm:
            RecoveryManager()
            mock_dm.assert_called_once()


class TestRecoveryManagerChecking:
    """Test recovery checking methods."""

    def test_check_for_recovery_exists(self, recovery_manager):
        """Test checking for recovery when draft exists."""
        draft = Draft(feed_id=1, timestamp=datetime.now(tz=UTC), field_values={})
        recovery_manager.draft_manager.load_draft.return_value = draft

        result = recovery_manager.check_for_recovery(1)

        assert result is not None
        assert result.feed_id == 1
        recovery_manager.draft_manager.load_draft.assert_called_once_with(1)

    def test_check_for_recovery_not_exists(self, recovery_manager):
        """Test checking for recovery when no draft exists."""
        recovery_manager.draft_manager.load_draft.return_value = None

        result = recovery_manager.check_for_recovery(1)

        assert result is None

    def test_get_all_recoverable_empty(self, recovery_manager):
        """Test getting all recoverable when none exist."""
        recovery_manager.draft_manager.list_drafts.return_value = []

        result = recovery_manager.get_all_recoverable()

        assert result == []

    def test_get_all_recoverable_multiple(self, recovery_manager):
        """Test getting multiple recoverable sessions."""
        drafts = [
            Draft(feed_id=1, timestamp=datetime.now(tz=UTC), field_values={}),
            Draft(feed_id=2, timestamp=datetime.now(tz=UTC), field_values={}),
            Draft(feed_id=3, timestamp=datetime.now(tz=UTC), field_values={}),
        ]
        recovery_manager.draft_manager.list_drafts.return_value = drafts

        result = recovery_manager.get_all_recoverable()

        assert len(result) == 3
        assert all(isinstance(info, RecoveryInfo) for info in result)
        assert [info.feed_id for info in result] == [1, 2, 3]


class TestRecoveryManagerRecovery:
    """Test recovery operations."""

    def test_recover_draft_exists(self, recovery_manager):
        """Test recovering a draft."""
        field_values = {"title": "Test Feed", "url": "https://example.com"}
        draft = Draft(feed_id=1, timestamp=datetime.now(tz=UTC), field_values=field_values)
        recovery_manager.draft_manager.load_draft.return_value = draft

        result = recovery_manager.recover_draft(1)

        assert result == field_values

    def test_recover_draft_not_exists(self, recovery_manager):
        """Test recovering when no draft exists."""
        recovery_manager.draft_manager.load_draft.return_value = None

        result = recovery_manager.recover_draft(1)

        assert result is None

    def test_discard_recovery_exists(self, recovery_manager):
        """Test discarding a recovery."""
        recovery_manager.draft_manager.delete_draft.return_value = True

        result = recovery_manager.discard_recovery(1)

        assert result is True
        recovery_manager.draft_manager.delete_draft.assert_called_once_with(1)

    def test_discard_recovery_not_exists(self, recovery_manager):
        """Test discarding when no draft exists."""
        recovery_manager.draft_manager.delete_draft.return_value = False

        result = recovery_manager.discard_recovery(1)

        assert result is False

    def test_auto_save_recovery(self, recovery_manager):
        """Test auto-saving for recovery."""
        field_values = {"title": "Test"}
        recovery_manager.draft_manager.save_draft.return_value = MagicMock()

        recovery_manager.auto_save_recovery(1, field_values)

        recovery_manager.draft_manager.save_draft.assert_called_once_with(1, field_values)

    def test_cleanup_old_recovery(self, recovery_manager):
        """Test cleaning up old recovery files."""
        recovery_manager.draft_manager.cleanup_old_drafts.return_value = 3

        result = recovery_manager.cleanup_old_recovery(days=7)

        assert result == 3
        recovery_manager.draft_manager.cleanup_old_drafts.assert_called_once_with(days=7)

    def test_cleanup_old_recovery_default_days(self, recovery_manager):
        """Test cleanup with default days."""
        recovery_manager.draft_manager.cleanup_old_drafts.return_value = 0

        recovery_manager.cleanup_old_recovery()

        recovery_manager.draft_manager.cleanup_old_drafts.assert_called_once_with(days=7)


class TestRecoveryManagerPrompting:
    """Test recovery prompting logic."""

    def test_should_prompt_recovery_first_time(self, recovery_manager):
        """Test that we should prompt on first recovery check."""
        assert recovery_manager.should_prompt_recovery(1) is True

    def test_should_prompt_recovery_recent(self, recovery_manager):
        """Test that we don't re-prompt within 5 minutes."""
        recovery_manager.last_recovery_prompt[1] = datetime.now(tz=UTC)

        assert recovery_manager.should_prompt_recovery(1) is False

    def test_should_prompt_recovery_after_timeout(self, recovery_manager):
        """Test that we re-prompt after 5 minute timeout."""
        recovery_manager.last_recovery_prompt[1] = datetime.now(tz=UTC) - timedelta(minutes=6)

        assert recovery_manager.should_prompt_recovery(1) is True

    def test_mark_recovery_prompted(self, recovery_manager):
        """Test marking that we've prompted."""
        before = datetime.now(tz=UTC)
        recovery_manager.mark_recovery_prompted(1)
        after = datetime.now(tz=UTC)

        assert 1 in recovery_manager.last_recovery_prompt
        assert before <= recovery_manager.last_recovery_prompt[1] <= after

    def test_clear_recovery_removes_prompt_tracking(self, recovery_manager):
        """Test that clearing recovery removes prompt tracking."""
        recovery_manager.last_recovery_prompt[1] = datetime.now(tz=UTC)
        recovery_manager.draft_manager.delete_draft.return_value = True

        recovery_manager.clear_recovery(1)

        assert 1 not in recovery_manager.last_recovery_prompt
        recovery_manager.draft_manager.delete_draft.assert_called_once_with(1)

    def test_clear_recovery_without_prompt_tracking(self, recovery_manager):
        """Test clearing recovery when no prompt tracking exists."""
        recovery_manager.draft_manager.delete_draft.return_value = True

        recovery_manager.clear_recovery(1)

        recovery_manager.draft_manager.delete_draft.assert_called_once_with(1)


class TestRecoveryManagerIntegration:
    """Integration tests for RecoveryManager."""

    def test_full_recovery_flow(self):
        """Test complete recovery workflow without mocks."""
        with patch("miniflux_tui.recovery_manager.DraftManager") as mock_dm:
            # Setup mock to simulate a saved draft
            draft = Draft(
                feed_id=1,
                timestamp=datetime.now(tz=UTC),
                field_values={"title": "Recovered Feed"},
            )
            mock_dm.return_value.load_draft.return_value = draft
            mock_dm.return_value.delete_draft.return_value = True

            manager = RecoveryManager()

            # Check for recovery
            recovery = manager.check_for_recovery(1)
            assert recovery is not None

            # Prompt check
            assert manager.should_prompt_recovery(1) is True
            manager.mark_recovery_prompted(1)
            assert manager.should_prompt_recovery(1) is False

            # Recover draft
            field_values = manager.recover_draft(1)
            assert field_values["title"] == "Recovered Feed"

            # Clear recovery
            manager.clear_recovery(1)
            assert 1 not in manager.last_recovery_prompt

    def test_multiple_recovery_sessions(self):
        """Test managing multiple concurrent recovery sessions."""
        with patch("miniflux_tui.recovery_manager.DraftManager") as mock_dm:
            drafts = [
                Draft(feed_id=1, timestamp=datetime.now(tz=UTC), field_values={}),
                Draft(feed_id=2, timestamp=datetime.now(tz=UTC), field_values={}),
                Draft(feed_id=3, timestamp=datetime.now(tz=UTC), field_values={}),
            ]
            mock_dm.return_value.list_drafts.return_value = drafts

            manager = RecoveryManager()

            # Get all recoverable
            all_recoverable = manager.get_all_recoverable()
            assert len(all_recoverable) == 3

            # Prompt differently for each
            assert manager.should_prompt_recovery(1) is True
            manager.mark_recovery_prompted(1)
            assert manager.should_prompt_recovery(1) is False

            assert manager.should_prompt_recovery(2) is True
            manager.mark_recovery_prompted(2)
            assert manager.should_prompt_recovery(2) is False

            assert manager.should_prompt_recovery(3) is True


class TestRecoveryManagerErrorHandling:
    """Test error handling in RecoveryManager."""

    def test_check_for_recovery_handles_exception(self, recovery_manager):
        """Test that check_for_recovery handles exceptions gracefully."""
        recovery_manager.draft_manager.load_draft.side_effect = OSError("File error")

        # Should raise since we're not catching in the manager
        with pytest.raises(OSError, match="File error"):
            recovery_manager.check_for_recovery(1)

    def test_recover_draft_with_empty_values(self, recovery_manager):
        """Test recovering a draft with empty field values."""
        draft = Draft(feed_id=1, timestamp=datetime.now(tz=UTC), field_values={})
        recovery_manager.draft_manager.load_draft.return_value = draft

        result = recovery_manager.recover_draft(1)

        assert result == {}

    def test_recover_draft_with_complex_values(self, recovery_manager):
        """Test recovering a draft with complex field values."""
        complex_values = {
            "title": "Test",
            "number": 42,
            "list": [1, 2, 3],
            "nested": {"key": "value"},
            "null": None,
        }
        draft = Draft(feed_id=1, timestamp=datetime.now(tz=UTC), field_values=complex_values)
        recovery_manager.draft_manager.load_draft.return_value = draft

        result = recovery_manager.recover_draft(1)

        assert result == complex_values
