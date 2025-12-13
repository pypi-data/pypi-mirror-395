# SPDX-License-Identifier: MIT
"""Recovery system for automatic draft detection and restoration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from miniflux_tui.draft_manager import Draft, DraftManager


@dataclass
class RecoveryInfo:
    """Information about an available recovery session.

    Attributes:
        feed_id: ID of the feed with available recovery
        draft: The Draft object with recovery data
        time_since_last_save: Human-readable time since last save
    """

    feed_id: int
    draft: Draft
    time_since_last_save: str

    @classmethod
    def from_draft(cls, draft: Draft) -> RecoveryInfo:
        """Create RecoveryInfo from a Draft.

        Args:
            draft: The Draft object

        Returns:
            RecoveryInfo instance
        """
        return cls(
            feed_id=draft.feed_id,
            draft=draft,
            time_since_last_save=_format_time_delta(draft.timestamp),
        )


class RecoveryManager:
    """Manages automatic recovery of unsaved feed settings.

    Detects crashes, provides recovery dialogs, and restores draft state.
    Integrates with DraftManager for persistent storage.

    Attributes:
        draft_manager: DraftManager instance for draft I/O
        last_recovery_prompt: Track what we've prompted about to avoid re-prompting
    """

    def __init__(self) -> None:
        """Initialize the recovery manager."""
        self.draft_manager = DraftManager()
        self.last_recovery_prompt: dict[int, datetime] = {}

    def check_for_recovery(self, feed_id: int) -> RecoveryInfo | None:
        """Check if a draft exists and needs recovery.

        Args:
            feed_id: ID of the feed to check

        Returns:
            RecoveryInfo if a draft exists, None otherwise
        """
        draft = self.draft_manager.load_draft(feed_id)
        if draft is None:
            return None

        return RecoveryInfo.from_draft(draft)

    def get_all_recoverable(self) -> list[RecoveryInfo]:
        """Get all available recovery sessions.

        Returns:
            List of RecoveryInfo for all available drafts
        """
        drafts = self.draft_manager.list_drafts()
        return [RecoveryInfo.from_draft(draft) for draft in drafts]

    def recover_draft(self, feed_id: int) -> dict[str, Any] | None:
        """Recover the field values from a draft.

        Args:
            feed_id: ID of the feed to recover

        Returns:
            Dictionary of field values, or None if recovery fails
        """
        draft = self.draft_manager.load_draft(feed_id)
        if draft is None:
            return None

        return draft.field_values

    def discard_recovery(self, feed_id: int) -> bool:
        """Discard a recovery draft without restoring.

        Args:
            feed_id: ID of the feed

        Returns:
            True if draft was discarded, False if not found
        """
        return self.draft_manager.delete_draft(feed_id)

    def auto_save_recovery(self, feed_id: int, field_values: dict[str, Any]) -> None:
        """Auto-save field values for recovery purposes.

        Args:
            feed_id: ID of the feed
            field_values: Dictionary of field values to save
        """
        self.draft_manager.save_draft(feed_id, field_values)

    def cleanup_old_recovery(self, days: int = 7) -> int:
        """Clean up recovery drafts older than specified days.

        Args:
            days: Number of days to keep drafts (default: 7)

        Returns:
            Number of drafts deleted
        """
        return self.draft_manager.cleanup_old_drafts(days=days)

    def should_prompt_recovery(self, feed_id: int) -> bool:
        """Determine if we should show a recovery prompt.

        Avoids showing multiple prompts for the same recovery session.

        Args:
            feed_id: ID of the feed

        Returns:
            True if we should prompt, False if we already have
        """
        now = datetime.now(tz=UTC)

        # If we haven't prompted about this feed yet, we should
        if feed_id not in self.last_recovery_prompt:
            return True

        # If it's been more than 5 minutes, prompt again
        last_prompt = self.last_recovery_prompt[feed_id]
        return (now - last_prompt).total_seconds() > 300

    def mark_recovery_prompted(self, feed_id: int) -> None:
        """Mark that we've prompted about recovery for a feed.

        Args:
            feed_id: ID of the feed
        """
        self.last_recovery_prompt[feed_id] = datetime.now(tz=UTC)

    def clear_recovery(self, feed_id: int) -> None:
        """Clear recovery data after successful save.

        Args:
            feed_id: ID of the feed
        """
        self.draft_manager.delete_draft(feed_id)
        if feed_id in self.last_recovery_prompt:
            del self.last_recovery_prompt[feed_id]


def _format_time_delta(timestamp: datetime) -> str:
    """Format a timestamp as human-readable time since.

    Args:
        timestamp: The timestamp to format

    Returns:
        Human-readable string like "2 hours ago" or "just now"
    """
    now = datetime.now(tz=UTC)
    delta = now - timestamp

    # Handle negative deltas or very recent saves
    if delta.total_seconds() < 60:
        return "just now"

    # Minutes
    if delta.total_seconds() < 3600:
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    # Hours
    if delta.total_seconds() < 86400:
        hours = int(delta.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    # Days
    days = delta.days
    return f"{days} day{'s' if days != 1 else ''} ago"
