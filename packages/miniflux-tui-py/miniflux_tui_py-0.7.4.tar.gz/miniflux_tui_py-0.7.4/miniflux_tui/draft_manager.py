# SPDX-License-Identifier: MIT
"""Draft management system for feed settings persistence and auto-recovery."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from miniflux_tui.config import get_config_dir


@dataclass
class Draft:
    """Represents a saved draft of feed settings.

    Attributes:
        feed_id: ID of the feed being edited
        timestamp: When the draft was created/updated
        field_values: Dictionary of field IDs to their values
        metadata: Optional metadata about the draft
    """

    feed_id: int
    timestamp: datetime
    field_values: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert draft to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the draft
        """
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Draft:
        """Create a Draft from a dictionary.

        Args:
            data: Dictionary containing draft data

        Returns:
            Draft instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        if "feed_id" not in data or "timestamp" not in data:
            msg = "Draft must have feed_id and timestamp"
            raise ValueError(msg)

        timestamp = datetime.fromisoformat(data["timestamp"]) if isinstance(data["timestamp"], str) else data["timestamp"]

        return cls(
            feed_id=int(data["feed_id"]),
            timestamp=timestamp,
            field_values=data.get("field_values", {}),
            metadata=data.get("metadata", {}),
        )


class DraftManager:
    """Manages draft persistence for feed settings.

    Handles saving, loading, listing, and cleaning up drafts.
    Stores drafts in the config directory under a 'drafts' subdirectory.

    Attributes:
        drafts_dir: Path to the directory where drafts are stored
    """

    def __init__(self) -> None:
        """Initialize the draft manager.

        Creates the drafts directory if it doesn't exist.
        """
        config_dir = Path(get_config_dir())
        self.drafts_dir = config_dir / "drafts"
        self.drafts_dir.mkdir(parents=True, exist_ok=True)

    def save_draft(self, feed_id: int, field_values: dict[str, Any]) -> Draft:
        """Save a draft of feed settings.

        Args:
            feed_id: ID of the feed being edited
            field_values: Dictionary of field IDs to their values

        Returns:
            The saved Draft object

        Raises:
            IOError: If draft file cannot be written
        """
        draft = Draft(
            feed_id=feed_id,
            timestamp=datetime.now(tz=UTC),
            field_values=field_values,
            metadata={"version": 1},
        )

        draft_file = self._get_draft_file(feed_id)
        try:
            draft_file.write_text(json.dumps(draft.to_dict(), indent=2), encoding="utf-8")
            return draft
        except OSError as e:
            msg = f"Failed to save draft for feed {feed_id}: {e}"
            raise OSError(msg) from e

    def load_draft(self, feed_id: int) -> Draft | None:
        """Load the most recent draft for a feed.

        Args:
            feed_id: ID of the feed

        Returns:
            Draft object if found, None otherwise
        """
        draft_file = self._get_draft_file(feed_id)
        if not draft_file.exists():
            return None

        try:
            data = json.loads(draft_file.read_text(encoding="utf-8"))
            return Draft.from_dict(data)
        except (OSError, json.JSONDecodeError, ValueError):
            return None

    def has_draft(self, feed_id: int) -> bool:
        """Check if a draft exists for a feed.

        Args:
            feed_id: ID of the feed

        Returns:
            True if a draft exists, False otherwise
        """
        return self._get_draft_file(feed_id).exists()

    def get_draft_timestamp(self, feed_id: int) -> datetime | None:
        """Get the timestamp of the most recent draft.

        Args:
            feed_id: ID of the feed

        Returns:
            Datetime of the draft, or None if no draft exists
        """
        draft = self.load_draft(feed_id)
        return draft.timestamp if draft else None

    def list_drafts(self) -> list[Draft]:
        """List all available drafts.

        Returns:
            List of Draft objects, sorted by timestamp (newest first)
        """
        drafts = []
        for draft_file in self.drafts_dir.glob("draft_*.json"):
            try:
                data = json.loads(draft_file.read_text(encoding="utf-8"))
                draft = Draft.from_dict(data)
                drafts.append(draft)
            except (OSError, json.JSONDecodeError, ValueError):
                continue

        drafts.sort(key=lambda d: d.timestamp, reverse=True)
        return drafts

    def delete_draft(self, feed_id: int) -> bool:
        """Delete the draft for a feed.

        Args:
            feed_id: ID of the feed

        Returns:
            True if draft was deleted, False if it didn't exist
        """
        draft_file = self._get_draft_file(feed_id)
        if not draft_file.exists():
            return False

        try:
            draft_file.unlink()
            return True
        except OSError:
            return False

    def cleanup_old_drafts(self, days: int = 7) -> int:
        """Delete drafts older than specified number of days.

        Args:
            days: Number of days to keep drafts (default: 7)

        Returns:
            Number of drafts deleted
        """
        cutoff = datetime.now(tz=UTC) - timedelta(days=days)
        deleted_count = 0

        for draft_file in self.drafts_dir.glob("draft_*.json"):
            try:
                data = json.loads(draft_file.read_text(encoding="utf-8"))
                draft = Draft.from_dict(data)
                if draft.timestamp < cutoff:
                    draft_file.unlink()
                    deleted_count += 1
            except (OSError, json.JSONDecodeError, ValueError):
                continue

        return deleted_count

    def clear_all_drafts(self) -> int:
        """Delete all drafts.

        Returns:
            Number of drafts deleted
        """
        deleted_count = 0
        for draft_file in self.drafts_dir.glob("draft_*.json"):
            try:
                draft_file.unlink()
                deleted_count += 1
            except OSError:
                continue

        return deleted_count

    def _get_draft_file(self, feed_id: int) -> Path:
        """Get the file path for a draft.

        Args:
            feed_id: ID of the feed

        Returns:
            Path to the draft file
        """
        return self.drafts_dir / f"draft_{feed_id}.json"
