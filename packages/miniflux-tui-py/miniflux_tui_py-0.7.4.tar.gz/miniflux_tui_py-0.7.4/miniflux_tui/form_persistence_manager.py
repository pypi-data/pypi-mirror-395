# SPDX-License-Identifier: MIT
"""Form persistence manager integrating draft, recovery, and change tracking."""

from __future__ import annotations

from typing import Any

from miniflux_tui.change_tracker import ChangeTracker
from miniflux_tui.draft_manager import DraftManager
from miniflux_tui.recovery_manager import RecoveryInfo, RecoveryManager


class FormPersistenceManager:
    """Unified interface for form persistence, recovery, and change tracking.

    Coordinates DraftManager, RecoveryManager, and ChangeTracker for
    comprehensive form state management.

    Attributes:
        draft_manager: Manages draft persistence
        recovery_manager: Handles automatic recovery
        change_tracker: Tracks field modifications
    """

    def __init__(self) -> None:
        """Initialize the form persistence manager."""
        self.draft_manager = DraftManager()
        self.recovery_manager = RecoveryManager()
        self.change_tracker = ChangeTracker()

    # Recovery Operations
    def check_for_recovery(self, feed_id: int) -> RecoveryInfo | None:
        """Check if a feed has available recovery.

        Args:
            feed_id: ID of the feed

        Returns:
            RecoveryInfo if recovery available, None otherwise
        """
        return self.recovery_manager.check_for_recovery(feed_id)

    def should_prompt_recovery(self, feed_id: int) -> bool:
        """Determine if we should show recovery prompt.

        Args:
            feed_id: ID of the feed

        Returns:
            True if we should prompt
        """
        return self.recovery_manager.should_prompt_recovery(feed_id)

    def recover_field_values(self, feed_id: int) -> dict[str, Any] | None:
        """Get field values from recovery draft.

        Args:
            feed_id: ID of the feed

        Returns:
            Dictionary of recovered field values, or None
        """
        return self.recovery_manager.recover_draft(feed_id)

    def discard_recovery(self, feed_id: int) -> bool:
        """Discard recovery draft without restoring.

        Args:
            feed_id: ID of the feed

        Returns:
            True if discarded successfully
        """
        return self.recovery_manager.discard_recovery(feed_id)

    def mark_recovery_handled(self, feed_id: int) -> None:
        """Mark that we've handled recovery for this feed.

        Args:
            feed_id: ID of the feed
        """
        self.recovery_manager.mark_recovery_prompted(feed_id)

    # Draft Persistence
    def auto_save_draft(self, feed_id: int, field_values: dict[str, Any]) -> None:
        """Auto-save current field values as draft.

        Args:
            feed_id: ID of the feed
            field_values: Current field values to save
        """
        self.recovery_manager.auto_save_recovery(feed_id, field_values)

    def clear_draft_after_save(self, feed_id: int) -> None:
        """Clear draft and recovery after successful save.

        Args:
            feed_id: ID of the feed
        """
        self.recovery_manager.clear_recovery(feed_id)

    # Change Tracking
    def track_field_change(
        self,
        feed_id: int,
        field_id: str,
        field_name: str,
        before_value: Any,
        after_value: Any,
    ) -> None:
        """Track a field modification.

        Args:
            feed_id: ID of the feed
            field_id: ID of the field
            field_name: Human-readable field name
            before_value: Value before change
            after_value: Value after change
        """
        self.change_tracker.track_change(feed_id, field_id, field_name, before_value, after_value)

    def get_field_change_summary(self, feed_id: int) -> dict[str, Any] | None:
        """Get summary of changes for a feed.

        Args:
            feed_id: ID of the feed

        Returns:
            Summary dictionary or None if no changes
        """
        return self.change_tracker.get_summary(feed_id)

    def get_field_diff(self, feed_id: int, field_id: str) -> dict[str, Any] | None:
        """Get before/after values for a field.

        Args:
            feed_id: ID of the feed
            field_id: ID of the field

        Returns:
            Diff dictionary with before/after, or None
        """
        return self.change_tracker.get_field_diff(feed_id, field_id)

    def has_unsaved_changes(self, feed_id: int) -> bool:
        """Check if a feed has unsaved changes.

        Args:
            feed_id: ID of the feed

        Returns:
            True if changes exist
        """
        return self.change_tracker.has_changes(feed_id)

    def get_change_count(self, feed_id: int) -> int:
        """Get count of unsaved changes.

        Args:
            feed_id: ID of the feed

        Returns:
            Number of changes tracked
        """
        summary = self.change_tracker.get_summary(feed_id)
        return summary["total_changes"] if summary else 0

    # Cleanup
    def clear_session(self, feed_id: int) -> None:
        """Clear all session state for a feed.

        Args:
            feed_id: ID of the feed
        """
        self.change_tracker.clear_history(feed_id)
        self.recovery_manager.clear_recovery(feed_id)

    def cleanup_old_sessions(self, days: int = 7) -> int:
        """Clean up old recovery sessions.

        Args:
            days: Number of days to keep drafts

        Returns:
            Number of sessions deleted
        """
        return self.recovery_manager.cleanup_old_recovery(days=days)

    # Batch Operations
    def save_all_state(self, feed_id: int, field_values: dict[str, Any]) -> None:
        """Save complete form state (draft + metadata).

        Args:
            feed_id: ID of the feed
            field_values: Current field values
        """
        # Save as recovery draft
        self.auto_save_draft(feed_id, field_values)

    def restore_all_state(self, feed_id: int) -> dict[str, Any] | None:
        """Restore complete form state from recovery.

        Args:
            feed_id: ID of the feed

        Returns:
            Restored field values or None
        """
        return self.recover_field_values(feed_id)

    def get_full_session_info(self, feed_id: int) -> dict[str, Any]:
        """Get complete information about a form session.

        Args:
            feed_id: ID of the feed

        Returns:
            Dictionary with recovery, changes, and metadata
        """
        recovery = self.check_for_recovery(feed_id)
        changes = self.get_field_change_summary(feed_id)

        return {
            "feed_id": feed_id,
            "has_recovery": recovery is not None,
            "recovery_info": recovery,
            "has_changes": changes is not None,
            "change_summary": changes,
            "change_count": self.get_change_count(feed_id),
        }
