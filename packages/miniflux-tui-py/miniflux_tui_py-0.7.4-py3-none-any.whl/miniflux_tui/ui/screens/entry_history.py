# SPDX-License-Identifier: MIT
"""Entry history screen showing previously read entries."""

from miniflux_tui.ui.screens.entry_list import EntryListScreen


class EntryHistoryScreen(EntryListScreen):
    """Screen displaying previously read entries - extends EntryListScreen.

    Pressing Shift+H in this screen returns to the main entry list.
    """

    def __init__(self, **kwargs):
        """Initialize with empty entries list - will be populated on mount."""
        super().__init__(entries=[], **kwargs)
        # Update subtitle to indicate this is history view
        self.sub_title = "Reading History"

    def on_mount(self) -> None:
        """Called when screen is mounted - load history instead of normal entries."""
        super().on_mount()
        self.app.log("EntryHistoryScreen.on_mount called")
        self.run_worker(self._load_history, exclusive=True)

    async def _load_history(self) -> None:
        """Load history entries asynchronously."""
        if not hasattr(self.app, "client") or not self.app.client:
            self.app.notify("API client not available", severity="error")
            return

        try:
            # Show loading indicator
            self.app.notify("Loading history...")

            # Get read entries (limit to 200 for performance)
            history_entries = await self.app.client.get_read_entries(limit=200, offset=0)

            self.app.log(f"Loaded {len(history_entries)} history entries")

            if not history_entries:
                self.app.notify("No read entries found. Read some articles first!", severity="information")
                self.entries = []
                self._populate_list()
            else:
                self.app.notify(f"Loaded {len(history_entries)} entries", severity="information")
                # Set the entries and populate the list (inherited from EntryListScreen)
                self.entries = history_entries
                self._populate_list()

        except Exception as e:
            error_msg = f"Error loading history: {type(e).__name__}: {e}"
            self.app.log(error_msg)
            # Show actual error in notification so user knows what went wrong
            short_error = str(e)[:100]  # Limit to 100 chars for notification
            self.app.notify(f"Failed to load history: {short_error}", severity="error")
            self.entries = []
            self._populate_list()

    def action_show_history(self):
        """Return to main entry list (override parent method).

        In history view, pressing Shift+H returns to the main entry list
        instead of opening history again.
        """
        self.app.log("History screen: action_show_history - popping back to main list")
        self.app.pop_screen()
