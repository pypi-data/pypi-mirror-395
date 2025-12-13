# SPDX-License-Identifier: MIT
"""Feed settings screen for comprehensive feed configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Input, Select, Static, TextArea

from miniflux_tui.docs_cache import DocsCache
from miniflux_tui.form_persistence_manager import FormPersistenceManager
from miniflux_tui.ui.screens.rules_helper import RulesHelperScreen

if TYPE_CHECKING:
    from miniflux_tui.api.client import MinifluxClient
    from miniflux_tui.api.models import Category, Feed


class FeedSettingsScreen(Screen):
    """Full-screen scrollable feed settings interface.

    Provides centralized management of feed configuration including:
    - General settings (title, category, site URL, description)
    - Network settings (authentication, proxies, certificates)
    - Rules and filtering (scraper, rewrite, blocking rules)
    - Feed metadata (last check, next check, ETag, LastModified)
    - Feed management (delete)

    Attributes:
        feed_id: ID of the feed being configured
        feed: Current feed data
        client: Miniflux API client
        dirty_fields: Dictionary tracking which fields have been modified
        is_dirty: Boolean flag indicating if any changes have been made
    """

    BINDINGS: ClassVar = [
        Binding("tab", "focus_next", "Next Field"),
        Binding("shift+tab", "focus_previous", "Prev Field"),
        Binding("enter", "save_changes", "Save", key_display="Enter"),
        Binding("ctrl+s", "save_changes", "Save", key_display="Ctrl+S"),
        Binding("escape", "cancel_changes", "Cancel"),
        Binding("x", "open_helper", "Helper"),
    ]

    DEFAULT_CSS: ClassVar[str] = """
    FeedSettingsScreen {
        background: $surface;
        color: $text;
        layout: vertical;
        overflow: hidden;
    }

    FeedSettingsScreen > Header {
        dock: top;
    }

    FeedSettingsScreen > Footer {
        dock: bottom;
    }

    #content-wrapper {
        layout: vertical;
        height: 1fr;
        width: 100%;
        overflow: hidden hidden;
    }

    #content-wrapper > ScrollableContainer {
        height: 1fr;
        width: 100%;
        overflow-x: hidden;
        overflow-y: auto;
    }

    #content-wrapper > #bottom-section {
        height: auto;
        width: 100%;
        layout: vertical;
    }

    #bottom-section > #status-message {
        height: auto;
        width: 100%;
        padding: 1 2;
        border-top: solid $primary 30%;
    }

    #settings-header {
        width: 100%;
        height: auto;
        padding: 1 2;
        background: $boost;
        border-bottom: solid $primary 50%;
        content-align: left middle;
        text-style: bold;
        color: $text;
        overflow: hidden;
    }

    #unsaved-indicator {
        width: 100%;
        height: auto;
        padding: 0 2;
        margin-bottom: 0;
        color: $warning;
        text-style: dim;
        overflow: hidden;
    }

    .section {
        width: 100%;
        height: auto;
        padding: 1 2;
        margin-bottom: 1;
        border-bottom: solid $primary 30%;
        overflow: hidden;
    }

    .section-title {
        width: 100%;
        height: auto;
        padding: 1 0;
        padding-bottom: 0;
        text-style: bold;
        color: $accent;
        border-bottom: solid $primary 20%;
        margin-bottom: 1;
    }

    .field-group {
        width: 100%;
        height: auto;
        layout: horizontal;
        margin-bottom: 1;
        padding: 0 0;
    }

    .field-label {
        width: 100%;
        height: auto;
        margin-bottom: 1;
        color: $text-muted;
        text-style: dim;
    }

    .field-label-inline {
        height: auto;
        width: auto;
        margin-right: 1;
        color: $text-muted;
        text-style: dim;
    }

    .field-value {
        width: 100%;
        height: auto;
        margin: 0 0 1 0;
    }

    .field-value-inline {
        height: auto;
        width: 1fr;
    }

    .textarea-container {
        width: 100%;
        height: 8;
        border: solid $primary 50%;
    }

    TextArea {
        width: 100%;
        height: 100%;
        min-height: 8;
        overflow: hidden;
    }

    #status-message {
        width: 100%;
        height: auto;
        padding: 1 2;
        color: $text-muted;
        min-height: 1;
    }

    #status-message.success {
        color: $success;
        text-style: bold;
    }

    #status-message.error {
        color: $error;
        text-style: bold;
    }

    #status-message.warning {
        color: $warning;
        text-style: bold;
    }

    #status-message.info {
        color: $text;
    }

    .danger-button {
        background: $error;
        color: $text;
    }

    .danger-button:hover {
        background: $error 80%;
    }
    """

    def __init__(
        self,
        feed_id: int,
        feed: Feed,
        client: MinifluxClient,
        **kwargs,
    ):
        """Initialize the feed settings screen.

        Args:
            feed_id: ID of the feed to configure
            feed: Current feed data
            client: Miniflux API client for API calls
            **kwargs: Additional keyword arguments for Screen
        """
        super().__init__(**kwargs)
        self.feed_id = feed_id
        self.feed = feed
        self.client = client

        # Documentation cache for helper screens
        self.docs_cache = DocsCache()

        # Form persistence and auto-recovery
        self.persistence = FormPersistenceManager()

        # Dirty state tracking
        self.dirty_fields: dict[str, bool] = {}
        self.is_dirty = False

        # Store original values for cancel
        self.original_values: dict[str, Any] = {}

        # Status message
        self.status_message = ""
        self.status_severity = "info"  # "info", "success", "error", "warning"

        # Auto-save debounce timer
        self._auto_save_handle = None

        # Categories for dropdown
        self.categories: list[Category] = []

        # Initialization flag to prevent tracking changes during widget setup
        self._initializing = True

    def compose(self) -> ComposeResult:
        """Compose the feed settings screen layout.

        Yields:
            Composed widgets for the screen
        """
        yield Header()

        # Wrapper to manage layout: ScrollableContainer gets space after bottom-section is sized
        with Container(id="content-wrapper"):
            # ScrollableContainer for form content - only this should scroll
            with ScrollableContainer(id="settings-scroll"):
                # Settings header with unsaved indicator
                yield Static(
                    f"Feed Settings: {self.feed.title}",
                    id="settings-header",
                )
                yield Static("", id="unsaved-indicator", classes="field-label")

                # Yield each section
                yield from self._compose_general_settings()
                yield from self._compose_network_settings()
                yield from self._compose_rules_and_filtering()
                yield from self._compose_feed_information()
                yield from self._compose_danger_zone()

            # Bottom container for status message (stays fixed at bottom)
            with Static(id="bottom-section"):
                # Status message area
                yield Static(self.status_message, id="status-message")

        yield Footer()

    def _compose_general_settings(self) -> ComposeResult:
        """Compose the General Settings section."""
        yield Static("General", classes="section-title")
        with Static(classes="section"):
            # Feed Title
            yield Static("Title", classes="field-label")
            yield Input(
                value=self.feed.title,
                id="feed-title",
                classes="field-value",
            )

            # Site URL
            yield Static("Site URL", classes="field-label")
            yield Input(
                value=self.feed.site_url,
                id="site-url",
                classes="field-value",
            )

            # Feed URL (read-only)
            yield Static("Feed URL", classes="field-label")
            yield Input(
                value=self.feed.feed_url,
                id="feed-url",
                disabled=True,
                classes="field-value",
            )

            # Category (dropdown selector for available categories)
            yield Static("Category", classes="field-label")
            # Will be populated with categories in on_mount()
            yield Select(
                options=[("Loading...", "")],
                id="category-id",
                classes="field-value",
                allow_blank=True,
            )

            # Description (optional notes/description for this feed)
            yield Static("Description (optional)", classes="field-label")
            yield TextArea(
                text=self.feed.description,
                id="feed-description",
                classes="field-value",
            )

            # Feed behavior options (checkboxes without extra labels)
            yield Checkbox(
                label="Hide entries in global unread list",
                value=self.feed.hide_globally,
                id="hide-globally",
                classes="field-value",
            )

            yield Checkbox(
                label="No media player (audio/video)",
                value=self.feed.no_media_player,
                id="no-media-player",
                classes="field-value",
            )

            yield Checkbox(
                label="Do not refresh this feed",
                value=self.feed.disabled,
                id="feed-disabled",
                classes="field-value",
            )

    def _compose_network_settings(self) -> ComposeResult:
        """Compose the Network Settings section."""
        yield Static("Network Settings", classes="section-title")
        with Static(classes="section"):
            # Feed Username
            yield Static("Feed Username (optional)", classes="field-label")
            yield Input(
                value=self.feed.username or "",
                id="auth-username",
                classes="field-value",
            )

            # Feed Password
            yield Static("Feed Password (optional)", classes="field-label")
            yield Input(
                value=self.feed.password or "",
                id="auth-password",
                password=True,
                classes="field-value",
            )

            # Override Default User Agent
            yield Static("Override Default User Agent (optional)", classes="field-label")
            yield Input(
                value=self.feed.user_agent or "",
                id="user-agent",
                classes="field-value",
            )

            # Proxy URL
            yield Static("Proxy URL (optional)", classes="field-label")
            yield Input(
                value=self.feed.proxy_url or "",
                id="proxy-url",
                classes="field-value",
            )

            # Fetch original content
            yield Checkbox(
                label="Fetch original content",
                value=self.feed.crawler,
                id="crawler",
                classes="field-value",
            )

            # Ignore HTTP cache
            yield Checkbox(
                label="Ignore HTTP cache",
                value=self.feed.ignore_http_cache,
                id="ignore-http-cache",
                classes="field-value",
            )

            # Allow self-signed or invalid certificates
            yield Checkbox(
                label="Allow self-signed or invalid certificates",
                value=self.feed.ignore_https_errors,
                id="ignore-https-errors",
                classes="field-value",
            )

            # Note: Disable HTTP/2 field not available in current Miniflux API version
            # If you need this feature, please request it in Miniflux repository

    def _compose_rules_and_filtering(self) -> ComposeResult:
        """Compose the Rules section."""
        yield Static("Rules", classes="section-title")
        with Static(classes="section"):
            # Single-line rule fields
            # Scraper Rules
            yield Static("Scraper Rules (optional)", classes="field-label")
            yield Input(
                value=self.feed.scraper_rules or "",
                id="scraper-rules",
                classes="field-value",
            )

            # Content Rewrite Rules
            yield Static("Content Rewrite Rules (optional)", classes="field-label")
            yield Input(
                value=self.feed.rewrite_rules or "",
                id="rewrite-rules",
                classes="field-value",
            )

            # Regex-Based Blocking Filters
            yield Static("Regex-Based Blocking Filters (optional)", classes="field-label")
            yield Input(
                value=self.feed.blocklist_rules or "",
                id="blocklist-rules",
                classes="field-value",
            )

            # Regex-Based Keep Filters
            yield Static("Regex-Based Keep Filters (optional)", classes="field-label")
            yield Input(
                value=self.feed.keeplist_rules or "",
                id="keeplist-rules",
                classes="field-value",
            )

            # Note: Additional rule types not yet available in Miniflux API
            # When available in future versions:
            # - URL Rewrite Rules
            # - Entry Blocking Rules (multi-line)
            # - Entry Allow Rules (multi-line)

    def _compose_feed_information(self) -> ComposeResult:
        """Compose the Feed Information section."""
        yield Static("Feed Information", classes="section-title")
        with Static(classes="section"):
            # Last Checked (on one line)
            with Container(classes="field-group"):
                yield Static("Last Checked: ", classes="field-label-inline")
                yield Static(
                    self.feed.checked_at or "Never",
                    id="last-checked",
                    classes="field-value-inline",
                )

            # Parsing Error Count
            yield Static("Parsing Errors", classes="field-label")
            yield Static(
                f"{self.feed.parsing_error_count} error(s)",
                id="error-count",
                classes="field-value",
            )

            # Parsing Error Message (if present)
            if self.feed.parsing_error_message:
                yield Static("Error Message", classes="field-label")
                yield Static(
                    self.feed.parsing_error_message,
                    id="error-message",
                    classes="field-value",
                )

            # Check Interval
            yield Static("Check Interval (minutes, optional)", classes="field-label")
            yield Input(
                value=str(self.feed.check_interval or ""),
                id="check-interval",
                classes="field-value",
            )

            # Feed ID (on one line)
            with Container(classes="field-group"):
                yield Static("Feed ID: ", classes="field-label-inline")
                yield Static(
                    str(self.feed.id),
                    id="feed-id",
                    classes="field-value-inline",
                )

    def _compose_danger_zone(self) -> ComposeResult:
        """Compose the Danger Zone section."""
        yield Static("Danger Zone", classes="section-title")
        with Static(classes="section"):
            yield Static(
                "Delete this feed permanently. This action cannot be undone.",
                classes="field-label",
            )
            yield Button(
                "🗑️ Delete Feed",
                id="delete-feed-button",
                classes="danger-button",
            )

    async def on_mount(self) -> None:
        """Called when screen is mounted.

        Initialize screen state, load categories, and load feed data.
        """

        # Clear all session state from previous invocations
        # (change tracker, recovery drafts, etc.) to start fresh
        # This ensures we don't show stale unsaved changes if the server data changed
        self.persistence.clear_session(self.feed_id)

        # Store original field values for change tracking
        self._store_original_values()

        # Load categories from API
        try:
            if hasattr(self.app, "client") and self.app.client:  # type: ignore[attr-defined]
                self.categories = await self.app.client.get_categories()  # type: ignore[attr-defined]
                # Update the Select widget with loaded categories
                self._update_category_selector()
        except Exception:  # noqa: S110  # nosec: B110
            # If categories fail to load, just continue with empty list
            pass

        # Initialization complete - now track actual user changes
        self._initializing = False

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input field changes.

        Args:
            event: Input change event
        """
        if event.input.id and not event.input.disabled:
            self._on_field_changed(event.input.id, event.value)

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox state changes.

        Args:
            event: Checkbox change event
        """
        if event.checkbox.id:
            self._on_field_changed(event.checkbox.id, event.value)

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle text area content changes.

        Args:
            event: TextArea change event
        """
        if event.text_area.id:
            self._on_field_changed(event.text_area.id, event.text_area.text)

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle select/dropdown changes.

        Args:
            event: Select change event
        """
        if event.select.id:
            # Convert empty string to None for category_id
            value = event.value if event.value else None
            self._on_field_changed(event.select.id, value)

    async def action_focus_next(self) -> None:
        """Focus next focusable widget."""
        self.screen.focus_next()

    async def action_focus_previous(self) -> None:
        """Focus previous focusable widget."""
        self.screen.focus_previous()

    async def action_save_changes(self) -> None:
        """Save all changes to Miniflux API.

        This action:
        1. Collects all modified field values
        2. Shows loading indicator
        3. Calls the API to update the feed
        4. Clears persistence state on success
        5. Shows success/error message with visual feedback
        """

        if not self.is_dirty:
            self._show_message("No changes to save", severity="info")
            return

        # Show loading message
        self._show_message("💾 Saving feed settings...", severity="info")

        try:
            # Collect field values
            updates = self._collect_field_values()

            # Call API to update feed
            updated_feed = await self.client.update_feed(self.feed_id, **updates)

            # Update internal state and reset tracking
            self._handle_save_success(updated_feed)

        except TimeoutError:
            self._show_message("✗ Request timeout while saving", severity="error")
        except ConnectionError:
            self._show_message("✗ Connection failed while saving", severity="error")
        except ValueError as e:
            self._show_message(f"✗ Invalid input: {e}", severity="error")
        except Exception as e:
            self._show_message(f"✗ Error saving settings: {e}", severity="error")

    def _collect_original_values(self) -> dict[str, Any]:
        """Collect current UI widget values as original values.

        This is used after a successful save to reset the baseline for change detection.

        Returns:
            Dictionary mapping field names to their current UI values
        """
        # Map field names to their widget IDs and default values
        field_map = {
            "title": ("feed-title", ""),
            "site_url": ("site-url", ""),
            "feed_url": ("feed-url", ""),
            "category_id": ("category-id", ""),
            "description": ("feed-description", ""),
            "hide_globally": ("hide-globally", False),
            "no_media_player": ("no-media-player", False),
            "disabled": ("feed-disabled", False),
            "username": ("auth-username", ""),
            "password": ("auth-password", ""),
            "user_agent": ("user-agent", ""),
            "proxy_url": ("proxy-url", ""),
            "crawler": ("crawler", False),
            "ignore_http_cache": ("ignore-http-cache", False),
            "ignore_https_errors": ("ignore-https-errors", False),
            "scraper_rules": ("scraper-rules", ""),
            "rewrite_rules": ("rewrite-rules", ""),
            "blocklist_rules": ("blocklist-rules", ""),
            "keeplist_rules": ("keeplist-rules", ""),
            "check_interval": ("check-interval", ""),
        }

        return {name: self._get_widget_value_for_field(widget_id) or default for name, (widget_id, default) in field_map.items()}

    def _handle_save_success(self, updated_feed: Feed) -> None:
        """Handle successful feed settings save.

        Updates internal state, resets original values, and shows confirmation.

        Args:
            updated_feed: The updated feed object from the API
        """
        self.feed = updated_feed
        self.is_dirty = False
        self.dirty_fields.clear()

        # Reset original values to match current UI state
        # Use UI widget values, not API response, to avoid inconsistencies
        self.original_values = self._collect_original_values()

        # Clear persistence state after successful save
        self.persistence.clear_session(self.feed_id)

        # Clear unsaved indicator
        self._update_unsaved_indicator()

        # Show success message with confirmation
        self._show_message(
            "✓ Feed settings saved successfully",
            severity="success",
        )

    async def action_cancel_changes(self) -> None:
        """Cancel changes and close screen.

        If there are unsaved changes, show confirmation message.
        Otherwise, close immediately.
        """
        if self.is_dirty:
            # Show confirmation message
            if not hasattr(self, "_cancel_confirmed"):
                self._cancel_confirmed = False

            if not self._cancel_confirmed:
                # First press - show confirmation
                self._show_message(
                    "Press Escape again to discard unsaved changes",
                    severity="warning",
                )
                self._cancel_confirmed = True
                return

            # Second press - discard changes and close
            self.is_dirty = False
            self.dirty_fields.clear()
            self.persistence.discard_recovery(self.feed_id)
            self._cancel_confirmed = False
            self._update_unsaved_indicator()

        # Close the screen
        self.app.pop_screen()

    def action_open_helper(self) -> None:
        """Open helper screen for current field.

        This action opens appropriate helper screens based on
        which rule field is currently focused (if any).
        """
        # Map of rule field IDs to rule types
        rule_field_mapping = {
            "scraper-rules": "scraper_rules",
            "rewrite-rules": "rewrite_rules",
            "blocklist-rules": "blocklist_rules",
            "keeplist-rules": "keeplist_rules",
        }

        # Get currently focused widget
        focused = self.focused
        if focused is None:
            self._show_message(
                "No field focused. Focus a rule field and press 'x' for help.",
                severity="info",
            )
            return

        # Check if the focused widget or its parent is a rule field
        widget = focused
        rule_type = None

        # Check the focused widget itself
        if widget.id and widget.id in rule_field_mapping:
            rule_type = rule_field_mapping[widget.id]
        else:
            # Check parent widgets
            parent = widget.parent
            while parent and not rule_type:
                if parent.id and parent.id in rule_field_mapping:
                    rule_type = rule_field_mapping[parent.id]
                    break
                parent = parent.parent

        if not rule_type:
            self._show_message(
                "Focus a rule field to see help. Rule fields: Scraper, Rewrite, Blocklist, Keeplist.",
                severity="info",
            )
            return

        # Open the helper screen with the appropriate rule type
        helper_screen = RulesHelperScreen(
            rule_type=rule_type,
            docs_cache=self.docs_cache,
        )
        self.app.push_screen(helper_screen)

    async def action_delete_feed(self) -> None:
        """Delete the feed with confirmation and visual feedback.

        Shows a confirmation message before deleting.
        Requires pressing the button twice for safety.
        Provides visual feedback during deletion.
        """
        # Check if this is a confirmation press
        if not hasattr(self, "_delete_confirmed"):
            self._delete_confirmed = False

        if not self._delete_confirmed:
            # First press - show confirmation
            self._show_message(
                "⚠️  Press Delete Feed again to confirm. This action cannot be undone.",
                severity="error",
            )
            self._delete_confirmed = True
            return

        # Second press - proceed with deletion
        if not hasattr(self.app, "client") or not self.app.client:  # type: ignore[attr-defined]
            self._show_message("✗ Error: API client not available", severity="error")
            self._delete_confirmed = False
            return

        # Disable delete button and show loading message
        delete_button = self.query_one("Button#delete-feed-button", expect_type=Button)
        delete_button.disabled = True
        self._show_message("🗑️  Deleting feed...", severity="info")

        try:
            await self.app.client.delete_feed(self.feed_id)  # type: ignore[attr-defined]
            self._show_message(
                f"✓ Feed '{self.feed.title}' deleted successfully",
                severity="success",
            )
            # Close the screen after successful deletion
            self.app.pop_screen()
        except TimeoutError:
            self._show_message("✗ Request timeout while deleting feed", severity="error")
            self._delete_confirmed = False
            delete_button.disabled = False
        except ConnectionError:
            self._show_message("✗ Connection failed while deleting feed", severity="error")
            self._delete_confirmed = False
            delete_button.disabled = False
        except Exception as e:
            self._show_message(f"✗ Error deleting feed: {e}", severity="error")
            self._delete_confirmed = False
            delete_button.disabled = False

    def _on_field_changed(self, widget_id: str, new_value: Any) -> None:
        """Mark a field as dirty when its value changes.

        Args:
            widget_id: ID of the widget that changed
            new_value: New value of the widget
        """
        # Skip change tracking during initialization (widgets fire events during setup)
        if self._initializing:
            return

        # Map widget IDs to feed field names
        field_mapping = {
            # General Settings
            "feed-title": "title",
            "site-url": "site_url",
            "feed-url": "feed_url",
            "category-id": "category_id",
            "feed-description": "description",
            "hide-globally": "hide_globally",
            "no-media-player": "no_media_player",
            "feed-disabled": "disabled",
            # Network Settings
            "auth-username": "username",
            "auth-password": "password",
            "user-agent": "user_agent",
            "proxy-url": "proxy_url",
            "crawler": "crawler",
            "ignore-http-cache": "ignore_http_cache",
            "ignore-https-errors": "ignore_https_errors",
            # Rules & Filtering
            "scraper-rules": "scraper_rules",
            "rewrite-rules": "rewrite_rules",
            "blocklist-rules": "blocklist_rules",
            "keeplist-rules": "keeplist_rules",
            # Feed Information
            "check-interval": "check_interval",
        }

        field_name = field_mapping.get(widget_id, widget_id)

        # Store original value on first change (if not already stored)
        # This handles cases where _store_original_values() wasn't called yet
        if field_name not in self.original_values:
            self.original_values[field_name] = getattr(self.feed, field_name, None)

        # Get the original value for comparison
        original_value = self.original_values[field_name]

        # CRITICAL FIX: Only track if the value has actually changed
        # Convert new_value to the same type as original_value for comparison
        # This prevents false positives from widget initialization
        if original_value is not None:
            # Convert new_value to match original_value type for comparison
            if isinstance(original_value, str):
                new_value_cmp = str(new_value) if new_value is not None else ""
            elif isinstance(original_value, bool):
                new_value_cmp = new_value
            elif isinstance(original_value, int):
                try:
                    new_value_cmp = int(new_value) if new_value else None
                except (ValueError, TypeError):
                    new_value_cmp = new_value
            else:
                new_value_cmp = new_value
        else:
            new_value_cmp = new_value

        # If the value hasn't actually changed from the original, skip tracking
        if new_value_cmp == original_value:
            # CRITICAL: Still need to update the indicator because another field might have changed
            # We need to recount all fields to get accurate total
            self._update_unsaved_indicator()
            return

        # Store the new value for collection later
        if not hasattr(self, "_field_values"):
            self._field_values: dict[str, Any] = {}
        self._field_values[field_name] = new_value

        # Track change with persistence manager
        self.persistence.track_field_change(
            feed_id=self.feed_id,
            field_id=widget_id,
            field_name=field_name,
            before_value=original_value,
            after_value=new_value,
        )

        # Mark field as dirty
        self.dirty_fields[field_name] = True
        self.is_dirty = True

        # Update unsaved indicator
        self._update_unsaved_indicator()

        # Trigger auto-save with debouncing
        self._schedule_auto_save()

    def _collect_field_values(self) -> dict[str, Any]:
        """Collect all modified field values for API update.

        Handles type conversions for specific fields (e.g., check_interval to int).

        Returns:
            Dictionary of field_name: new_value for dirty fields
        """
        updates: dict[str, Any] = {}

        # Collect values for dirty fields
        if hasattr(self, "_field_values"):
            for field_name in self.dirty_fields:
                if self.dirty_fields[field_name] and field_name in self._field_values:
                    value = self._field_values[field_name]

                    # Type conversions for specific fields
                    if field_name in {"check_interval", "category_id"}:
                        # Convert to int or None
                        if value and str(value).strip():
                            try:
                                value = int(str(value).strip())
                            except ValueError:
                                # If not a valid integer, skip this update
                                continue
                        else:
                            value = None
                    elif field_name == "description" and isinstance(value, str) and value == "":
                        # Miniflux doesn't accept empty string for description
                        # Use single space as workaround to "clear" the description
                        value = " "

                    updates[field_name] = value

        return updates

    def _show_message(
        self,
        message: str,
        severity: str = "info",
    ) -> None:
        """Display a status message with styled appearance.

        Args:
            message: Message text to display
            severity: Message severity ("info", "success", "error", "warning")
        """
        self.status_message = message
        self.status_severity = severity

        # Update status display
        status_widget = self.query_one("#status-message", expect_type=Static)
        status_widget.update(message)

        # Remove all severity classes
        status_widget.remove_class("success")
        status_widget.remove_class("error")
        status_widget.remove_class("warning")
        status_widget.remove_class("info")

        # Add appropriate severity class and color
        if severity == "success":
            status_widget.add_class("success")
        elif severity == "error":
            status_widget.add_class("error")
        elif severity == "warning":
            status_widget.add_class("warning")
        else:
            status_widget.add_class("info")

    def _store_original_values(self) -> None:
        """Store original field values for change tracking.

        Note: Store values as they appear in widgets (strings for numeric fields)
        to ensure proper comparison when tracking changes.
        """

        self.original_values = {
            # General Settings
            "title": self.feed.title,
            "site_url": self.feed.site_url,
            "feed_url": self.feed.feed_url,
            # Convert category_id to string to match Select widget value type
            "category_id": str(self.feed.category_id) if self.feed.category_id else "",
            "description": self.feed.description or "",
            "hide_globally": self.feed.hide_globally,
            "no_media_player": self.feed.no_media_player,
            "disabled": self.feed.disabled,
            # Network Settings
            "username": self.feed.username or "",
            "password": self.feed.password or "",
            "user_agent": self.feed.user_agent or "",
            "proxy_url": self.feed.proxy_url or "",
            "crawler": self.feed.crawler,
            "ignore_http_cache": self.feed.ignore_http_cache,
            "ignore_https_errors": self.feed.ignore_https_errors,
            # Rules & Filtering
            "scraper_rules": self.feed.scraper_rules or "",
            "rewrite_rules": self.feed.rewrite_rules or "",
            "blocklist_rules": self.feed.blocklist_rules or "",
            "keeplist_rules": self.feed.keeplist_rules or "",
            # Feed Information
            # Convert check_interval to string to match Input widget value type
            "check_interval": str(self.feed.check_interval) if self.feed.check_interval else "",
        }

    def _update_category_selector(self) -> None:
        """Update the category Select widget with loaded categories."""
        try:
            # Build options list with (category_title, category_id)
            options: list[tuple[str, str]] = []

            # Add "No category" option
            options.append(("No category", ""))

            # Add loaded categories
            for category in self.categories:
                options.append((category.title, str(category.id)))

            # Get the Select widget and update its options
            category_select = self.query_one("#category-id", expect_type=Select)
            category_select.set_options(options)

            # Set the current value if feed has a category
            if self.feed.category_id:
                category_select.value = str(self.feed.category_id)
            else:
                category_select.value = ""
        except Exception:  # noqa: S110  # nosec: B110
            # If update fails, the Select widget will remain with its default options
            pass

    def _check_for_recovery(self) -> None:
        """Check and handle recovery from previous session."""
        if self.persistence.should_prompt_recovery(self.feed_id):
            recovery = self.persistence.check_for_recovery(self.feed_id)

            if recovery:
                self._show_recovery_dialog(recovery)
            else:
                # Mark that we prompted (even if no recovery)
                self.persistence.mark_recovery_handled(self.feed_id)

    def _show_recovery_dialog(self, recovery: Any) -> None:
        """Show recovery dialog with user options.

        Args:
            recovery: RecoveryInfo object with recovery data
        """
        message = (
            f"Found unsaved changes from {recovery.time_since_last_save}\n\n"
            f"Would you like to:\n"
            f"• (R)ecover: Restore unsaved changes\n"
            f"• (D)iscard: Start with current feed values\n"
            f"• (C)ancel: Cancel editing"
        )

        self._show_message(message, severity="warning")
        self._recovery_pending = recovery

    def _get_widget_value_for_field(self, widget_id: str) -> Any:
        """Get value from a widget, handling different widget types.

        Args:
            widget_id: ID of the widget

        Returns:
            Current value or None if widget not found
        """
        try:
            # Input widgets (title, URLs, usernames, intervals)
            input_widgets = {
                "feed-title",
                "site-url",
                "feed-url",
                "auth-username",
                "auth-password",
                "user-agent",
                "proxy-url",
                "check-interval",
            }
            if widget_id in input_widgets:
                return self.query_one(f"#{widget_id}", Input).value

            # Select widget (category)
            if widget_id == "category-id":
                select_widget = self.query_one("#category-id", Select)
                return str(select_widget.value) if select_widget.value else ""

            # TextArea widgets (description and rules)
            if widget_id == "feed-description" or widget_id.endswith("-rules"):
                return self.query_one(f"#{widget_id}", TextArea).text

            # Checkbox widgets (flags)
            checkbox_widgets = {
                "hide-globally",
                "no-media-player",
                "feed-disabled",
                "crawler",
                "ignore-http-cache",
                "ignore-https-errors",
            }
            if widget_id in checkbox_widgets:
                return self.query_one(f"#{widget_id}", Checkbox).value

        except Exception:  # noqa: S110 - Intentional: widget not found is non-critical  # nosec: B110
            pass

        return None

    def _count_changed_fields(self) -> int:
        """Count how many fields have actually changed from their original values.

        This counts FIELDS that have changed, not change EVENTS.
        Typing multiple characters in a field counts as 1 change, not N changes.

        Returns:
            Number of fields with changed values
        """
        changed_count = 0

        # Map widget IDs to field names (same mapping as _on_field_changed)
        field_mapping = {
            "feed-title": "title",
            "site-url": "site_url",
            "feed-url": "feed_url",
            "category-id": "category_id",
            "feed-description": "description",
            "hide-globally": "hide_globally",
            "no-media-player": "no_media_player",
            "feed-disabled": "disabled",
            "auth-username": "username",
            "auth-password": "password",
            "user-agent": "user_agent",
            "proxy-url": "proxy_url",
            "crawler": "crawler",
            "ignore-http-cache": "ignore_http_cache",
            "ignore-https-errors": "ignore_https_errors",
            "scraper-rules": "scraper_rules",
            "rewrite-rules": "rewrite_rules",
            "blocklist-rules": "blocklist_rules",
            "keeplist-rules": "keeplist_rules",
            "check-interval": "check_interval",
        }

        # Check each field for changes
        for widget_id, field_name in field_mapping.items():
            current_value = self._get_widget_value_for_field(widget_id)
            if current_value is None:
                # Widget not found, skip
                continue

            original_value = self.original_values.get(field_name)

            # Type-aware comparison (same logic as _on_field_changed)
            if original_value is not None:
                if isinstance(original_value, str):
                    current_cmp = str(current_value) if current_value is not None else ""
                elif isinstance(original_value, bool):
                    current_cmp = current_value
                elif isinstance(original_value, int):
                    try:
                        current_cmp = int(current_value) if current_value else None
                    except (ValueError, TypeError):
                        current_cmp = current_value
                else:
                    current_cmp = current_value
            else:
                current_cmp = current_value

            # If values differ, count this field as changed
            if current_cmp != original_value:
                changed_count += 1

        return changed_count

    def _update_unsaved_indicator(self) -> None:
        """Update the unsaved changes indicator in the header."""
        try:
            indicator = self.query_one("#unsaved-indicator", expect_type=Static)
            # Count fields with actual changes, not change events
            change_count = self._count_changed_fields()

            if change_count > 0:
                indicator.update(f"● Unsaved changes: {change_count} field(s)")
                indicator.styles.color = "yellow"
            else:
                indicator.update("")
                indicator.styles.color = "$text-muted"
        except Exception:  # noqa: S110 - Intentional: widget not found is non-critical  # nosec: B110
            pass

    def _schedule_auto_save(self) -> None:
        """Schedule auto-save with debouncing (1 second delay)."""
        # Cancel previous timer if exists
        if self._auto_save_handle:
            self._auto_save_handle.stop()

        # Schedule new auto-save (1 second debounce delay)
        self._auto_save_handle = self.set_timer(1.0, self._auto_save_draft)

    def _auto_save_draft(self) -> None:
        """Auto-save current field values as draft."""
        # Collect current field values from UI
        field_values = self._collect_field_values()

        if field_values:
            # Add current field values
            field_values.update(self._get_current_field_values())

            # Save as draft
            self.persistence.auto_save_draft(self.feed_id, field_values)

    def _get_current_field_values(self) -> dict[str, Any]:
        """Get current values from all UI fields.

        Returns:
            Dictionary of field_id: value for all fields
        """
        field_values: dict[str, Any] = {}

        try:
            # Collect from Input fields
            for input_field in self.query(Input):
                if input_field.id and not input_field.disabled:
                    field_values[input_field.id] = input_field.value

            # Collect from Checkbox fields
            for checkbox in self.query(Checkbox):
                if checkbox.id:
                    field_values[checkbox.id] = checkbox.value

            # Collect from TextArea fields
            for textarea in self.query(TextArea):
                if textarea.id:
                    field_values[textarea.id] = textarea.text

            # Collect from Select fields
            for select in self.query(Select):
                if select.id:
                    field_values[select.id] = select.value
        except Exception:  # noqa: S110  # nosec: B110
            pass

        return field_values
