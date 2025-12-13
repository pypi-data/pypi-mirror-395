# SPDX-License-Identifier: MIT
"""Change tracking system for feed settings modifications."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from miniflux_tui.draft_manager import DraftManager


@dataclass
class FieldChange:
    """Represents a single field modification.

    Attributes:
        field_id: ID of the field that changed
        field_name: Human-readable name of the field
        before_value: Value before the change
        after_value: Value after the change
        timestamp: When the change occurred
        change_type: Type of change ('added', 'modified', 'removed')
    """

    field_id: str
    field_name: str
    before_value: Any
    after_value: Any
    timestamp: datetime
    change_type: str = "modified"  # 'added', 'modified', 'removed'

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation of the change
        """
        return {
            "field_id": self.field_id,
            "field_name": self.field_name,
            "before_value": self.before_value,
            "after_value": self.after_value,
            "timestamp": self.timestamp.isoformat(),
            "change_type": self.change_type,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FieldChange:
        """Create FieldChange from dictionary.

        Args:
            data: Dictionary containing change data

        Returns:
            FieldChange instance
        """
        timestamp = datetime.fromisoformat(data["timestamp"]) if isinstance(data["timestamp"], str) else data["timestamp"]

        return cls(
            field_id=data["field_id"],
            field_name=data["field_name"],
            before_value=data["before_value"],
            after_value=data["after_value"],
            timestamp=timestamp,
            change_type=data.get("change_type", "modified"),
        )

    def is_added(self) -> bool:
        """Check if this is an added field.

        Returns:
            True if field was added
        """
        return self.change_type == "added"

    def is_removed(self) -> bool:
        """Check if this is a removed field.

        Returns:
            True if field was removed
        """
        return self.change_type == "removed"

    def is_modified(self) -> bool:
        """Check if this is a modified field.

        Returns:
            True if field was modified
        """
        return self.change_type == "modified"


@dataclass
class ChangeHistory:
    """Complete change history for a feed's settings.

    Attributes:
        feed_id: ID of the feed
        changes: List of field changes
        created_at: When the history was created
        last_modified: When it was last updated
    """

    feed_id: int
    changes: list[FieldChange] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    last_modified: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def add_change(self, change: FieldChange) -> None:
        """Add a change to the history.

        Args:
            change: The FieldChange to add
        """
        self.changes.append(change)
        self.last_modified = datetime.now(tz=UTC)

    def get_field_changes(self, field_id: str) -> list[FieldChange]:
        """Get all changes for a specific field.

        Args:
            field_id: ID of the field

        Returns:
            List of changes for that field
        """
        return [c for c in self.changes if c.field_id == field_id]

    def get_changes_by_type(self, change_type: str) -> list[FieldChange]:
        """Get all changes of a specific type.

        Args:
            change_type: Type of change ('added', 'modified', 'removed')

        Returns:
            List of changes of that type
        """
        return [c for c in self.changes if c.change_type == change_type]

    def get_added_fields(self) -> list[FieldChange]:
        """Get all added fields.

        Returns:
            List of added field changes
        """
        return self.get_changes_by_type("added")

    def get_modified_fields(self) -> list[FieldChange]:
        """Get all modified fields.

        Returns:
            List of modified field changes
        """
        return self.get_changes_by_type("modified")

    def get_removed_fields(self) -> list[FieldChange]:
        """Get all removed fields.

        Returns:
            List of removed field changes
        """
        return self.get_changes_by_type("removed")

    def has_changes(self) -> bool:
        """Check if there are any tracked changes.

        Returns:
            True if changes exist
        """
        return len(self.changes) > 0

    def get_change_count(self) -> int:
        """Get total number of changes.

        Returns:
            Number of tracked changes
        """
        return len(self.changes)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "feed_id": self.feed_id,
            "changes": [c.to_dict() for c in self.changes],
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChangeHistory:
        """Create ChangeHistory from dictionary.

        Args:
            data: Dictionary containing history data

        Returns:
            ChangeHistory instance
        """
        created_at = datetime.fromisoformat(data["created_at"]) if isinstance(data["created_at"], str) else data["created_at"]
        last_modified = datetime.fromisoformat(data["last_modified"]) if isinstance(data["last_modified"], str) else data["last_modified"]

        history = cls(
            feed_id=data["feed_id"],
            created_at=created_at,
            last_modified=last_modified,
        )

        for change_data in data.get("changes", []):
            history.add_change(FieldChange.from_dict(change_data))

        return history


class ChangeTracker:
    """Tracks changes to feed settings fields.

    Monitors field modifications and maintains complete change history.
    Enables before/after comparisons and field-level revert capabilities.

    Attributes:
        draft_manager: DraftManager for persisting changes
    """

    def __init__(self) -> None:
        """Initialize the change tracker."""
        self.draft_manager = DraftManager()
        self._current_history: dict[int, ChangeHistory] = {}

    def track_change(
        self,
        feed_id: int,
        field_id: str,
        field_name: str,
        before_value: Any,
        after_value: Any,
    ) -> None:
        """Track a field change.

        Args:
            feed_id: ID of the feed being edited
            field_id: ID of the field that changed
            field_name: Human-readable name of the field
            before_value: Value before the change
            after_value: Value after the change
        """
        if feed_id not in self._current_history:
            self._current_history[feed_id] = ChangeHistory(feed_id=feed_id)

        # Determine change type
        if before_value is None and after_value is not None:
            change_type = "added"
        elif before_value is not None and after_value is None:
            change_type = "removed"
        else:
            change_type = "modified"

        change = FieldChange(
            field_id=field_id,
            field_name=field_name,
            before_value=before_value,
            after_value=after_value,
            timestamp=datetime.now(tz=UTC),
            change_type=change_type,
        )

        self._current_history[feed_id].add_change(change)

    def get_history(self, feed_id: int) -> ChangeHistory | None:
        """Get change history for a feed.

        Args:
            feed_id: ID of the feed

        Returns:
            ChangeHistory if exists, None otherwise
        """
        return self._current_history.get(feed_id)

    def has_changes(self, feed_id: int) -> bool:
        """Check if a feed has tracked changes.

        Args:
            feed_id: ID of the feed

        Returns:
            True if changes have been tracked
        """
        return feed_id in self._current_history

    def get_field_changes(self, feed_id: int, field_id: str) -> list[FieldChange]:
        """Get all changes for a specific field.

        Args:
            feed_id: ID of the feed
            field_id: ID of the field

        Returns:
            List of changes for that field, empty list if none
        """
        history = self.get_history(feed_id)
        return history.get_field_changes(field_id) if history else []

    def get_last_change(self, feed_id: int, field_id: str) -> FieldChange | None:
        """Get the most recent change for a field.

        Args:
            feed_id: ID of the feed
            field_id: ID of the field

        Returns:
            Most recent FieldChange, or None if no changes
        """
        changes = self.get_field_changes(feed_id, field_id)
        return changes[-1] if changes else None

    def get_field_diff(self, feed_id: int, field_id: str) -> dict[str, Any] | None:
        """Get before/after values for a field.

        Args:
            feed_id: ID of the feed
            field_id: ID of the field

        Returns:
            Dictionary with 'before' and 'after' keys, or None if no changes
        """
        change = self.get_last_change(feed_id, field_id)
        if change is None:
            return None

        return {
            "field_id": change.field_id,
            "field_name": change.field_name,
            "before": change.before_value,
            "after": change.after_value,
            "change_type": change.change_type,
            "timestamp": change.timestamp,
        }

    def get_summary(self, feed_id: int) -> dict[str, Any] | None:
        """Get summary of all changes for a feed.

        Args:
            feed_id: ID of the feed

        Returns:
            Dictionary with change counts and summary, or None if no history
        """
        history = self.get_history(feed_id)
        if not history or not history.has_changes():
            return None

        return {
            "feed_id": feed_id,
            "total_changes": history.get_change_count(),
            "added_count": len(history.get_added_fields()),
            "modified_count": len(history.get_modified_fields()),
            "removed_count": len(history.get_removed_fields()),
            "created_at": history.created_at,
            "last_modified": history.last_modified,
        }

    def clear_history(self, feed_id: int) -> None:
        """Clear all tracked changes for a feed.

        Args:
            feed_id: ID of the feed
        """
        if feed_id in self._current_history:
            del self._current_history[feed_id]

    def clear_all_history(self) -> None:
        """Clear all tracked changes."""
        self._current_history.clear()
