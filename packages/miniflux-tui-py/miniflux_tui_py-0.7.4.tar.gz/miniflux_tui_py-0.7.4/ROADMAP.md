# miniflux-tui-py Roadmap

This document outlines the planned features and improvements for the miniflux-tui-py project. Features are organized by category and priority.

## Legend

- 🚀 **High Priority** - Core features that significantly improve functionality
- ⭐ **Medium Priority** - Nice-to-have features that enhance UX
- 💡 **Low Priority** - Future improvements or nice-to-have additions
- ✅ **Completed** - Features already implemented
- 🔄 **In Progress** - Currently being worked on
- 📋 **Planned** - Scheduled for next release

## Version 0.5.0 - Feed Management & Categories ✅ RELEASED (2025-11-01)

**Release Status**: ✅ Completed and deployed

### Category Support (🚀 High Priority) ✅
- [x] Support categories in feed list display
- [x] Filter entries by category
- [x] Move/copy feeds between categories
- [x] Create/edit/delete categories
- [x] Category-based grouping option
- **Issue**: [#54](https://github.com/reuteras/miniflux-tui-py/issues/54)
- **Status**: ✅ Completed

### Feed Operations (🚀 High Priority) ✅
- [x] Implement `refresh_all_feeds()` with 'R' keybinding
- [x] Change refresh behavior:
  - [x] 'r' or ',' → `refresh_feed()` for current feed
  - [x] 'R' → `refresh_all_feeds()` for all feeds
- [x] Display feed sync status/progress (via notifications)
- [x] Show feed error indicators (bad certs, bot protection, etc.)
- **Issue**: [#55](https://github.com/reuteras/miniflux-tui-py/issues/55)
- **Status**: ✅ Completed

### Feed Management (⭐ Medium Priority) ✅
- [x] Create/discover new feeds
- [x] Edit feed settings:
  - Update fetch rules
  - Toggle full content fetching
  - Configure scraping rules
- [x] Display feed metadata (last update, item count, etc.)
- **Issue**: [#58](https://github.com/reuteras/miniflux-tui-py/issues/58)
- **Status**: ✅ Completed

### Feed Status Screen (⭐ Medium Priority) ✅
- [x] New "Status" screen showing problematic feeds
- [x] Display feeds with errors:
  - [x] SSL certificate issues
  - [x] Bot protection blocking
  - [x] Connection timeouts
  - [x] Other HTTP errors
- [x] Links to feed settings on web UI
- [x] Show server version and URL
- **Issue**: [#59](https://github.com/reuteras/miniflux-tui-py/issues/247) (Note: Issue #59 created as #247)
- **Status**: ✅ Completed

## Version 0.6.0 - User Settings & Advanced Features 🔄

### Entry History (⭐ Medium Priority) ✅
- [x] View history of last read entries
- [x] Search through reading history
- [x] Filter history by date range
- [x] Filter history by feed
- [ ] Restore entries from history
- **Issue**: [#56](https://github.com/reuteras/miniflux-tui-py/issues/56)
- **Status**: ✅ Completed (v0.5.0)

### User Settings Management (⭐ Medium Priority) ✅
- [x] View current user settings
- [x] View/edit global feed settings
- [x] Configuration screen in TUI:
  - Display current settings
  - Allow inline edits
  - Link to web UI for advanced settings
- [x] Display enabled integrations
  - Service name and status
  - Link to web UI for configuration
- [x] Settings persistence
- **Issue**: [#TBD](https://github.com/reuteras/miniflux-tui-py/issues)
- **Status**: ✅ Completed (v0.6.0)

### Application Info (💡 Low Priority)
- [ ] Display app version from pyproject.toml in help screen
- [ ] Show server version in status screen
- [ ] Display API version info
- [ ] Show connectivity status
- **Issue**: [#TBD](https://github.com/reuteras/miniflux-tui-py/issues)
- **Status**: 📋 Planned

## Version 0.7.0 - Themes & Performance ✅ RELEASED (2025-11-27)

**Release Status**: ✅ Completed and deployed

### UI/UX Improvements - Dark/Light Theme (🚀 High Priority) ✅
- [x] Dark theme preset with optimized colors (using Textual built-in themes)
- [x] Light theme preset with optimized colors (using Textual built-in themes)
- [x] Theme toggle keybinding ('T' key)
- [x] Theme preference persistence in config
- [x] Runtime theme switching without restart (dynamic CSS update)
- **Status**: ✅ Completed

### Performance & Optimization (💡 Low Priority) ✅
- [x] Incremental feed sync (dynamic add/remove entries without full reload)
- [x] Background refresh with notifications (non-blocking UI using run_worker)
- [x] Non-blocking sync operations (comma key syncs while UI remains responsive)
- [ ] Memory optimization for large feed lists
- **Status**: ✅ Mostly Completed

## Version 0.8.0 - Advanced Features (Planned)

### Search & Discovery (📋 Planned)
- [ ] Full-text search across all entries
- [ ] Search filters by date, category, feed
- [ ] Save search queries (current session only - in-memory)
- [ ] Search history (current session only)

### UI/UX Improvements (⭐ Medium Priority)
- [ ] Bookmark/clipboard integration
- [ ] Export entries to various formats
- [ ] Customizable keybindings (💡 Low Priority)

## Completed Features ✅

- ✅ Basic entry list with sorting (date, feed, status)
- ✅ Entry detail view with HTML to Markdown conversion
- ✅ Mark as read/unread
- ✅ Mark as starred/unstarred
- ✅ Save entries to third-party services
- ✅ Keyboard-driven navigation
- ✅ Feed grouping
- ✅ Unread/starred filtering
- ✅ Search functionality (v0.4.0)
- ✅ Theme configuration (v0.4.0)
- ✅ Entry history view (v0.5.0)
- ✅ Category support (v0.5.0)
- ✅ Feed management (v0.5.0)
- ✅ User settings management (v0.6.0)
- ✅ Runtime theme switching (v0.7.0)
- ✅ Incremental feed sync (v0.7.0)
- ✅ Non-blocking background operations (v0.7.0)

## Technical Considerations

### API Requirements
Features will leverage the [Miniflux Python client](https://github.com/miniflux/python-client):
- `get_categories()` - Category list
- `create_category()` - New categories
- `update_category()` - Edit categories
- `delete_category()` - Remove categories
- `refresh_all_feeds()` - Refresh all feeds
- `refresh_feed()` - Refresh single feed
- `create_feed()` - Add new feed
- `discover_feed()` - Auto-discover feeds
- `update_feed()` - Modify feed settings
- `get_feed_history()` - Last read entries
- `get_user()` - User settings
- `get_server_info()` - Server version

### API-Dependent Features (When Available)
These features are planned pending upstream Miniflux API support:

- **Disable HTTP/2 to avoid fingerprinting** - Not yet available in Miniflux API
  - Will be added to Feed Settings when the Miniflux server provides this option
  - UI component already prepared for future implementation

- **Entry Filtering Rules** - Internal support exists in Miniflux, not yet exposed via API
  - Entry Blocking Rules - Filter entries by date, title, URL, content, author, tags
  - Entry Allow Rules - Keep only entries matching specified criteria
  - Would support regex patterns for flexible filtering
  - Requires Miniflux API enhancement to expose feed-level entry filter configuration

- **URL Rewrite Rules** - Not yet available in Miniflux API
  - Separate from Content Rewrite Rules for manipulating entry URLs
  - Requires Miniflux API enhancement

### Data Model Updates
- Add `Category` model
- Extend `Feed` model with status/error info
- Add `History` model for read entries
- Add `UserSettings` model
- Add `Integration` model

### UI Components Needed
- Category selector/list
- Feed status indicator
- Settings view
- History browser
- Status dashboard

## Release Schedule

- **v0.4.0** ✅ Released - Search & Theme support
- **v0.5.0** ✅ Released (2025-11-01) - Categories & Feed Management
- **v0.6.0** ✅ Released (2025-11-14) - History & User Settings
- **v0.7.0** ✅ Released (2025-11-27) - Runtime Theme Switching & Non-blocking Sync
- **v0.8.0** 📋 Planned (Q2 2026) - Advanced Features (Search, Integrations)

## Contributing

To work on features from this roadmap:

1. Check if an Issue exists for the feature
2. Create one if needed with the roadmap label
3. Create a feature branch: `git checkout -b feat/feature-name`
4. Submit a PR with reference to the issue
5. Updates will be tracked on the GitHub Project board

## Feedback & Ideas

Have ideas for new features? Please:
1. Check existing issues to avoid duplicates
2. Create a new issue with the `enhancement` label
3. Describe the use case and expected behavior
4. Add to this roadmap if appropriate

---

**Last Updated**: November 27, 2025
**Current Version**: v0.7.3
**Next Milestone**: v0.8.0 (Advanced Features - Search & Integrations)
