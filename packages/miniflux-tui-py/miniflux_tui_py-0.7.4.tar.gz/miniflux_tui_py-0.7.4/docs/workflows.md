# Keyboard Workflows

miniflux-tui-py is designed to keep your hands on the keyboard. The shortcuts below
highlight the most common flows for staying in sync with your feeds and navigating
quickly between screens.

## Staying Updated

- Press `r` to refresh the selected feed directly from the entry list.
- Use `,` (comma) to refresh every feed when you want a full sync.
- While a refresh is running you’ll see notifications showing progress; the list
  automatically refreshes afterward.

## Sorting And Grouping

- Tap `s` to cycle through sort modes: date, feed, or status.
- Toggle feed grouping with `g`; press `l` / `h` (or the arrow keys) to expand or
  collapse the focused feed.
- When grouping is enabled, `Shift+G` expands every feed and `Shift+Z` collapses
  them.
- If categories are available, press `c` to toggle category grouping—feed
  grouping is disabled automatically to keep the hierarchy predictable.

## Filtering Your Reading Queue

- `u` filters to unread items, while `t` shows only starred entries.
- `Enter` opens the reader and `J` / `K` step through entries using the current
  sort order.
- Use `m` to toggle the read state and `*` to star or un-star an entry without
  leaving the list.

## Searching

- Hit `/` to activate search (or call `set_search_term()` from automation).
- Once a search term is set, results update live; press `/` again to clear the
  filter or use the “Search cleared” notification shortcut.

## Reader Actions

Inside the entry reader, the following shortcuts mirror the list view:

- `m` toggles read/unread, `*` toggles starred.
- `s` saves the entry using your configured third-party service.
- `o` opens the entry in your default browser.
- `f` fetches the original content from Miniflux if it’s available.
- `Esc` returns to the list without losing your place.

For the full reference, press `?` in the application to open the in-app help
screen. That view stays up to date with every release.
