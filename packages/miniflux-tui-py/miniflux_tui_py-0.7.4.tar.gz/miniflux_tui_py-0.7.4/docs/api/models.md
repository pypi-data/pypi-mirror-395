# Data Models Reference

## Entry

The `Entry` class represents a single RSS entry/article.

::: miniflux_tui.api.models.Entry
    options:
      docstring_style: google
      show_source: true

### Properties

- **id**: Unique identifier for the entry
- **title**: Entry title
- **content**: Entry HTML content
- **published_at**: Publication timestamp
- **is_read**: Whether the entry has been read
- **starred**: Whether the entry is starred/favorited
- **feed**: The Feed this entry belongs to

### Helper Methods

- **is_unread**: Property that returns `True` if not read
- **status**: Property that returns "read" or "unread"

## Feed

The `Feed` class represents an RSS feed.

::: miniflux_tui.api.models.Feed
    options:
      docstring_style: google
      show_source: true

### Feed Properties

- **id**: Unique feed identifier
- **title**: Feed title
- **url**: Feed URL
- **unread_count**: Number of unread entries in this feed

## EntryListItem

Internal widget class for rendering entries in the list.

## FeedHeaderItem

Internal widget class for rendering feed group headers in grouped mode.

## Usage Example

```python
from miniflux_tui.api.models import Entry, Feed

# Create a feed
feed = Feed(id=1, title="My Blog", url="https://example.com/feed")

# Create an entry
entry = Entry(
    id=123,
    title="My Article",
    content="<p>Article content</p>",
    published_at=1699564800,
    is_read=False,
    starred=False,
    feed=feed
)

# Check properties
print(f"Entry: {entry.title}")
print(f"Feed: {entry.feed.title}")
print(f"Status: {entry.status}")
print(f"Is unread: {entry.is_unread}")
```
