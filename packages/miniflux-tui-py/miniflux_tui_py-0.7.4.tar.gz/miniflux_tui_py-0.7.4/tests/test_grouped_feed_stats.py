# SPDX-License-Identifier: MIT
"""Tests for grouped feed statistics tracking during navigation."""

from datetime import UTC, datetime

import pytest

from miniflux_tui.api.models import Entry, Feed
from miniflux_tui.ui.screens.entry_reader import EntryReaderScreen


@pytest.fixture
def feed1():
    """Create first test feed."""
    return Feed(
        id=1,
        title="Feed One",
        site_url="http://localhost:8080/feed1",
        feed_url="http://localhost:8080/feed1.xml",
    )


@pytest.fixture
def feed2():
    """Create second test feed."""
    return Feed(
        id=2,
        title="Feed Two",
        site_url="http://localhost:8080/feed2",
        feed_url="http://localhost:8080/feed2.xml",
    )


@pytest.fixture
def grouped_entry_list(feed1, feed2):
    """Create entry list with entries from two different feeds for grouping tests."""
    return [
        # Feed 1 entries
        Entry(
            id=1,
            feed_id=1,
            title="Feed1 Entry 1",
            url="http://localhost:8080/1",
            content="<p>Feed 1 - Entry 1</p>",
            feed=feed1,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=2,
            feed_id=1,
            title="Feed1 Entry 2",
            url="http://localhost:8080/2",
            content="<p>Feed 1 - Entry 2</p>",
            feed=feed1,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 11, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=3,
            feed_id=1,
            title="Feed1 Entry 3",
            url="http://localhost:8080/3",
            content="<p>Feed 1 - Entry 3</p>",
            feed=feed1,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 12, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=4,
            feed_id=1,
            title="Feed1 Entry 4",
            url="http://localhost:8080/4",
            content="<p>Feed 1 - Entry 4</p>",
            feed=feed1,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 13, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=5,
            feed_id=1,
            title="Feed1 Entry 5",
            url="http://localhost:8080/5",
            content="<p>Feed 1 - Entry 5</p>",
            feed=feed1,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 14, 0, 0, tzinfo=UTC),
        ),
        # Feed 2 entries
        Entry(
            id=6,
            feed_id=2,
            title="Feed2 Entry 1",
            url="http://localhost:8080/6",
            content="<p>Feed 2 - Entry 1</p>",
            feed=feed2,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 24, 10, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=7,
            feed_id=2,
            title="Feed2 Entry 2",
            url="http://localhost:8080/7",
            content="<p>Feed 2 - Entry 2</p>",
            feed=feed2,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 24, 11, 0, 0, tzinfo=UTC),
        ),
        Entry(
            id=8,
            feed_id=2,
            title="Feed2 Entry 3",
            url="http://localhost:8080/8",
            content="<p>Feed 2 - Entry 3</p>",
            feed=feed2,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 24, 12, 0, 0, tzinfo=UTC),
        ),
    ]


class TestGroupedFeedStatistics:
    """Test grouped feed statistics tracking."""

    def test_calculate_group_info_single_feed(self, feed1):
        """Test group info calculation for a single feed."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Test Entry",
            url="http://localhost:8080/1",
            content="<p>Test</p>",
            feed=feed1,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )

        # Create entry list with 3 unread entries from same feed
        entry_list = [
            entry,
            Entry(
                id=2,
                feed_id=1,
                title="Entry 2",
                url="http://localhost:8080/2",
                content="<p>Test 2</p>",
                feed=feed1,
                status="unread",
                starred=False,
                published_at=datetime(2024, 10, 25, 11, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=3,
                feed_id=1,
                title="Entry 3",
                url="http://localhost:8080/3",
                content="<p>Test 3</p>",
                feed=feed1,
                status="unread",
                starred=False,
                published_at=datetime(2024, 10, 25, 12, 0, 0, tzinfo=UTC),
            ),
        ]

        screen = EntryReaderScreen(
            entry=entry,
            entry_list=entry_list,
            current_index=0,
            group_info={"mode": "feed", "name": "Test Feed", "total": 3, "unread": 3},
        )

        group_info = screen._calculate_group_info()
        assert group_info is not None
        assert group_info["mode"] == "feed"
        assert group_info["name"] == feed1.title
        assert group_info["total"] == 3
        assert group_info["unread"] == 3

    def test_grouped_stats_after_marking_entry_read(self, grouped_entry_list, feed1):
        """Test that group statistics are correct after marking an entry as read.

        This is the critical test for the bug:
        1. Start with 5 unread entries in Feed 1
        2. Open first entry (Feed 1 Entry 1)
        3. Mark it as read (simulating automatic read on open)
        4. Statistics should show 4 unread / 5 total for Feed 1
        """
        first_entry = grouped_entry_list[0]

        # Verify initial state: all Feed 1 entries are unread
        feed1_entries = [e for e in grouped_entry_list if e.feed.id == 1]
        assert all(e.is_unread for e in feed1_entries), "All Feed 1 entries should start as unread"
        assert len(feed1_entries) == 5

        screen = EntryReaderScreen(
            entry=first_entry,
            entry_list=grouped_entry_list,
            current_index=0,
            group_info={"mode": "feed", "name": feed1.title, "total": 5, "unread": 5},
        )

        # Simulate marking the first entry as read
        first_entry.status = "read"

        # Calculate group info - should show 4 unread / 5 total
        group_info = screen._calculate_group_info()
        assert group_info is not None
        assert group_info["mode"] == "feed"
        assert group_info["name"] == feed1.title
        assert group_info["total"] == 5
        assert group_info["unread"] == 4, f"Expected 4 unread after marking first entry as read, got {group_info['unread']}"

    def test_grouped_stats_navigation_between_feeds(self, grouped_entry_list, feed1, feed2):
        """Test group statistics when navigating between entries in different feeds.

        This reproduces the exact bug scenario:
        1. Start viewing Feed 1 Entry 1 (5 total, 5 unread initially)
        2. It gets marked as read → now 4 unread / 5 total
        3. Navigate to Feed 1 Entry 2 via J key
        4. Statistics for Feed 1 Entry 2 should still show 4 unread / 5 total, NOT 5/5
        5. Then navigate to Feed 2 Entry 1 via J key (across group boundary)
        6. Statistics should switch to Feed 2 (3 total, 3 unread)
        """
        # Start with first Feed 1 entry
        first_feed1_entry = grouped_entry_list[0]

        # Create screen in grouped mode
        screen = EntryReaderScreen(
            entry=first_feed1_entry,
            entry_list=grouped_entry_list,
            current_index=0,
            group_info={"mode": "feed", "name": feed1.title, "total": 5, "unread": 5},
        )

        # Step 1: Mark first entry as read (simulating automatic read)
        first_feed1_entry.status = "read"

        # Verify stats after marking first entry read
        stats = screen._calculate_group_info()
        assert stats["unread"] == 4, "After marking first entry read, should have 4 unread"
        assert stats["total"] == 5

        # Step 2: Simulate navigation to second Feed 1 entry with J key
        screen.entry = grouped_entry_list[1]  # Second Feed 1 entry
        screen.current_index = 1

        # Stats should still show 4 unread for Feed 1 (not 5/5!)
        stats = screen._calculate_group_info()
        assert stats["unread"] == 4, "After navigating to second Feed 1 entry, stats should show 4 unread, not 5"
        assert stats["total"] == 5
        assert stats["name"] == feed1.title

        # Step 3: Mark second entry as read
        grouped_entry_list[1].status = "read"

        stats = screen._calculate_group_info()
        assert stats["unread"] == 3, "After marking second entry read, should have 3 unread"

        # Step 4: Navigate to Feed 2 entry with J key
        screen.entry = grouped_entry_list[5]  # First Feed 2 entry (index 5)
        screen.current_index = 5
        # Update group_info to reflect Feed 2
        screen.group_info = {"mode": "feed", "name": feed2.title, "total": 3, "unread": 3}

        # Stats should now show Feed 2 stats
        stats = screen._calculate_group_info()
        assert stats["name"] == feed2.title
        assert stats["total"] == 3, f"Feed 2 should have 3 total entries, got {stats['total']}"
        assert stats["unread"] == 3, f"Feed 2 should have 3 unread, got {stats['unread']}"
        # Verify Feed 1 entry 1 being marked as read doesn't affect Feed 2 count
        assert stats["unread"] == 3, "Feed 2 unread count should not be affected by Feed 1 changes"

    def test_group_stats_text_formatting(self, feed1):
        """Test that group stats are formatted correctly for display."""
        entry = Entry(
            id=1,
            feed_id=1,
            title="Test Entry",
            url="http://localhost:8080/1",
            content="<p>Test</p>",
            feed=feed1,
            status="unread",
            starred=False,
            published_at=datetime(2024, 10, 25, 10, 0, 0, tzinfo=UTC),
        )

        entry_list = [
            entry,
            Entry(
                id=2,
                feed_id=1,
                title="Entry 2",
                url="http://localhost:8080/2",
                content="<p>Test 2</p>",
                feed=feed1,
                status="read",
                starred=False,
                published_at=datetime(2024, 10, 25, 11, 0, 0, tzinfo=UTC),
            ),
            Entry(
                id=3,
                feed_id=1,
                title="Entry 3",
                url="http://localhost:8080/3",
                content="<p>Test 3</p>",
                feed=feed1,
                status="unread",
                starred=False,
                published_at=datetime(2024, 10, 25, 12, 0, 0, tzinfo=UTC),
            ),
        ]

        screen = EntryReaderScreen(
            entry=entry,
            entry_list=entry_list,
            current_index=0,
            group_info={"mode": "feed", "name": feed1.title, "total": 3, "unread": 2},
        )

        stats_text = screen._get_group_stats_text()
        assert "Feed:" in stats_text
        assert "2 unread" in stats_text
        assert "3 total" in stats_text

    def test_entry_list_reference_sharing(self, grouped_entry_list, feed1):
        """Test that entry_list passed to EntryReaderScreen uses shared references.

        This test verifies that when entry objects are modified in the entry_list,
        changes are reflected in both the entry_reader and the original list.
        """
        # Create entry list copy like entry_list screen does
        sorted_entries = grouped_entry_list.copy()

        # Pass the copied list to entry reader
        screen = EntryReaderScreen(
            entry=sorted_entries[0],
            entry_list=sorted_entries,
            current_index=0,
            group_info={"mode": "feed", "name": feed1.title, "total": 5, "unread": 5},
        )

        # Modify an entry's status
        sorted_entries[0].status = "read"

        # The entry in the entry_reader should also be updated (shared reference)
        assert screen.entry_list[0].is_read, "Entry list should show entry as read"

        # Stats should reflect the change
        group_info = screen._calculate_group_info()
        assert group_info["unread"] == 4, "Should have 4 unread after marking first entry as read"
