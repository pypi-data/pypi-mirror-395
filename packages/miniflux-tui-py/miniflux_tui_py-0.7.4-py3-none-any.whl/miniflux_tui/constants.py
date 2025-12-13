# SPDX-License-Identifier: MIT
"""Application constants."""

# API Limits
DEFAULT_ENTRY_LIMIT = 100
DEFAULT_OFFSET = 0

# UI Constants
FEED_HEADER_FORMAT = "━━ {feed_title} ━━"
CONTENT_SEPARATOR = "─" * 80

# Sorting
SORT_MODES = ["date", "feed", "status"]
DEFAULT_SORT = "date"

# Display Icons
STAR_ICON_FILLED = "★"
STAR_ICON_EMPTY = "☆"
UNREAD_ICON = "●"
READ_ICON = "○"
FOLD_EXPANDED = "▼"
FOLD_COLLAPSED = "▶"

# Colors (defaults)
DEFAULT_UNREAD_COLOR = "cyan"
DEFAULT_READ_COLOR = "gray"

# Timeout settings
DEFAULT_TIMEOUT = 30.0

# Retry settings
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.0
