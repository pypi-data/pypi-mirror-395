# SPDX-License-Identifier: MIT
"""Tests for HTML content analyzer."""

from miniflux_tui.scraping.analyzer import ContentAnalyzer

# Sample HTML for testing
SIMPLE_ARTICLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Test Article</title></head>
<body>
    <nav><a href="/">Home</a> <a href="/about">About</a></nav>
    <aside>Sidebar content</aside>
    <article class="post-content">
        <h1>Article Title</h1>
        <p>First paragraph of content.</p>
        <p>Second paragraph with more details.</p>
        <p>Third paragraph to make it substantial.</p>
    </article>
    <footer>Copyright 2025</footer>
</body>
</html>
"""

MAIN_TAG_HTML = """
<!DOCTYPE html>
<html>
<body>
    <header>Site Header</header>
    <main id="main-content">
        <h1>Main Content</h1>
        <p>This is the main content area.</p>
        <p>Multiple paragraphs here.</p>
    </main>
    <footer>Footer</footer>
</body>
</html>
"""

MULTIPLE_ARTICLES_HTML = """
<!DOCTYPE html>
<html>
<body>
    <article class="teaser">
        <h2>Teaser 1</h2>
        <p>Short teaser.</p>
    </article>
    <article class="full-content">
        <h1>Full Article</h1>
        <p>Paragraph one with substantial content.</p>
        <p>Paragraph two with even more content.</p>
        <p>Paragraph three continues the story.</p>
        <p>Paragraph four adds more detail.</p>
        <p>Paragraph five concludes.</p>
    </article>
    <article class="teaser">
        <h2>Teaser 2</h2>
        <p>Another short teaser.</p>
    </article>
</body>
</html>
"""

COMPLEX_HTML = """
<!DOCTYPE html>
<html>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
    </nav>
    <div id="content">
        <div class="article-content">
            <h1>Article Title</h1>
            <p>Introduction paragraph.</p>
            <p>Body paragraph one.</p>
            <p>Body paragraph two.</p>
            <h2>Subheading</h2>
            <p>More content here.</p>
            <blockquote>A relevant quote.</blockquote>
            <p>Final paragraph.</p>
        </div>
        <aside class="sidebar">
            <h3>Related Links</h3>
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
            <a href="/link3">Link 3</a>
        </aside>
    </div>
    <footer>Footer content</footer>
</body>
</html>
"""

NO_SEMANTIC_HTML = """
<!DOCTYPE html>
<html>
<body>
    <div class="wrapper">
        <div class="header">Header</div>
        <div class="content">
            <p>Some content here.</p>
            <p>More content.</p>
        </div>
        <div class="footer">Footer</div>
    </div>
</body>
</html>
"""


class TestContentAnalyzer:
    """Test suite for ContentAnalyzer class."""

    def test_init(self):
        """Test analyzer initialization."""
        analyzer = ContentAnalyzer(SIMPLE_ARTICLE_HTML)
        assert analyzer.soup is not None
        assert isinstance(analyzer.ALLOWED_TAGS, list)
        assert isinstance(analyzer.ALLOWED_ATTRIBUTES, dict)

    def test_find_main_content_article_tag(self):
        """Test finding content in semantic <article> tag."""
        analyzer = ContentAnalyzer(SIMPLE_ARTICLE_HTML)
        candidates = analyzer.find_main_content()

        assert len(candidates) > 0

        # Best candidate should be the article
        best = candidates[0]
        assert "article" in best["selector"] or best["type"] == "article"
        assert best["score"] > 0
        assert "Article Title" in best["preview"]

    def test_find_main_content_main_tag(self):
        """Test finding content in <main> tag."""
        analyzer = ContentAnalyzer(MAIN_TAG_HTML)
        candidates = analyzer.find_main_content()

        assert len(candidates) > 0

        # Should find main tag
        main_candidates = [c for c in candidates if c["type"] == "main"]
        assert len(main_candidates) > 0
        assert "Main Content" in main_candidates[0]["preview"]

    def test_find_main_content_by_id(self):
        """Test finding content by semantic ID."""
        analyzer = ContentAnalyzer(MAIN_TAG_HTML)
        candidates = analyzer.find_main_content()

        # Should find #main-content
        id_candidates = [c for c in candidates if c["selector"].startswith("#")]
        assert len(id_candidates) > 0

    def test_find_main_content_by_class(self):
        """Test finding content by semantic class name."""
        analyzer = ContentAnalyzer(COMPLEX_HTML)
        candidates = analyzer.find_main_content()

        # Should find .article-content
        class_candidates = [c for c in candidates if "article-content" in c["selector"]]
        assert len(class_candidates) > 0

    def test_score_element_paragraphs(self):
        """Test scoring rewards paragraphs."""
        analyzer = ContentAnalyzer(SIMPLE_ARTICLE_HTML)
        article = analyzer.soup.find("article")

        score = analyzer._score_element(article)

        # Should have positive score due to paragraphs
        assert score > 0
        # Article tag bonus should be applied
        assert score >= 50  # Article tag gets +50 bonus

    def test_score_element_text_length(self):
        """Test scoring considers text length."""
        long_html = """<article><p>{}</p></article>""".format("word " * 1000)
        short_html = """<article><p>Short</p></article>"""

        analyzer_long = ContentAnalyzer(long_html)
        analyzer_short = ContentAnalyzer(short_html)

        long_article = analyzer_long.soup.find("article")
        short_article = analyzer_short.soup.find("article")

        score_long = analyzer_long._score_element(long_article)
        score_short = analyzer_short._score_element(short_article)

        # Longer content should score higher (but capped at 100 for text)
        assert score_long > score_short

    def test_score_element_penalizes_many_links(self):
        """Test scoring penalizes excessive links."""
        # Many links (likely navigation)
        nav_html = """
        <div>
            <p>Text</p>
            <a href="/1">Link</a>
            <a href="/2">Link</a>
            <a href="/3">Link</a>
            <a href="/4">Link</a>
            <a href="/5">Link</a>
        </div>
        """

        # Few links (likely article)
        article_html = """
        <div>
            <p>Paragraph one</p>
            <p>Paragraph two</p>
            <p>Paragraph three</p>
            <a href="/source">Source</a>
        </div>
        """

        analyzer_nav = ContentAnalyzer(nav_html)
        analyzer_article = ContentAnalyzer(article_html)

        nav_div = analyzer_nav.soup.find("div")
        article_div = analyzer_article.soup.find("div")

        score_nav = analyzer_nav._score_element(nav_div)
        score_article = analyzer_article._score_element(article_div)

        # Article should score higher than navigation
        assert score_article > score_nav

    def test_generate_selector_by_id(self):
        """Test selector generation prefers ID."""
        html = """<div id="main-content" class="content wrapper">Text</div>"""
        analyzer = ContentAnalyzer(html)
        elem = analyzer.soup.find("div")

        selector = analyzer._generate_selector(elem)

        assert selector == "#main-content"

    def test_generate_selector_by_class(self):
        """Test selector generation uses first class if no ID."""
        html = """<div class="post-content wrapper">Text</div>"""
        analyzer = ContentAnalyzer(html)
        elem = analyzer.soup.find("div")

        selector = analyzer._generate_selector(elem)

        assert selector == "div.post-content"

    def test_generate_selector_by_tag(self):
        """Test selector generation falls back to tag name."""
        html = """<article>Text</article>"""
        analyzer = ContentAnalyzer(html)
        elem = analyzer.soup.find("article")

        selector = analyzer._generate_selector(elem)

        assert selector == "article"

    def test_get_text_preview_truncation(self):
        """Test text preview is truncated."""
        long_text = "word " * 200  # > 500 chars
        html = f"""<div>{long_text}</div>"""
        analyzer = ContentAnalyzer(html)
        elem = analyzer.soup.find("div")

        preview = analyzer._get_text_preview(elem, max_len=100)

        assert len(preview) <= 103  # 100 + "..."
        assert preview.endswith("...")

    def test_extract_with_selector(self):
        """Test extracting content with CSS selector."""
        analyzer = ContentAnalyzer(SIMPLE_ARTICLE_HTML)

        # Extract article content
        extracted = analyzer.extract_with_selector("article")

        assert extracted
        assert "Article Title" in extracted
        assert "First paragraph" in extracted
        # Should be sanitized HTML
        assert "<h1>" in extracted or "Article Title" in extracted

    def test_extract_with_selector_no_match(self):
        """Test extracting with non-matching selector returns empty."""
        analyzer = ContentAnalyzer(SIMPLE_ARTICLE_HTML)

        extracted = analyzer.extract_with_selector(".nonexistent")

        assert extracted == ""

    def test_extract_with_selector_sanitization(self):
        """Test extracted content is sanitized."""
        dangerous_html = """
        <article>
            <p>Safe content</p>
            <script>dangerousCode()</script>
            <iframe src="evil.com"></iframe>
            <p>More safe content</p>
        </article>
        """
        analyzer = ContentAnalyzer(dangerous_html)

        extracted = analyzer.extract_with_selector("article")

        # Should contain safe content
        assert "Safe content" in extracted
        # Should NOT contain dangerous tags
        assert "<script>" not in extracted
        assert "<iframe>" not in extracted
        # The text content from script will be removed with strip=True in bleach
        assert "dangerousCode" not in extracted or "</script>" not in extracted

    def test_get_element_stats(self):
        """Test getting element statistics."""
        analyzer = ContentAnalyzer(COMPLEX_HTML)

        stats = analyzer.get_element_stats(".article-content")

        assert stats["count"] == 1
        assert stats["paragraphs"] > 0
        assert stats["links"] >= 0
        assert stats["images"] >= 0

    def test_get_element_stats_no_match(self):
        """Test stats for non-matching selector."""
        analyzer = ContentAnalyzer(SIMPLE_ARTICLE_HTML)

        stats = analyzer.get_element_stats(".nonexistent")

        assert stats["count"] == 0
        assert stats["paragraphs"] == 0
        assert stats["links"] == 0
        assert stats["images"] == 0

    def test_get_element_stats_multiple_elements(self):
        """Test stats aggregates across multiple matched elements."""
        analyzer = ContentAnalyzer(MULTIPLE_ARTICLES_HTML)

        stats = analyzer.get_element_stats("article")

        # Should find all 3 articles
        assert stats["count"] == 3
        # Total paragraphs across all articles
        assert stats["paragraphs"] > 3

    def test_find_main_content_returns_sorted_by_score(self):
        """Test candidates are sorted by score descending."""
        analyzer = ContentAnalyzer(MULTIPLE_ARTICLES_HTML)
        candidates = analyzer.find_main_content()

        # Scores should be in descending order
        for i in range(len(candidates) - 1):
            assert candidates[i]["score"] >= candidates[i + 1]["score"]

    def test_find_main_content_limits_results(self):
        """Test find_main_content returns at most 10 candidates."""
        # Create HTML with many potential candidates
        html = "<html><body>"
        for i in range(20):
            html += f'<div id="content{i}"><p>Content {i}</p></div>'
        html += "</body></html>"

        analyzer = ContentAnalyzer(html)
        candidates = analyzer.find_main_content()

        # Should return at most 10
        assert len(candidates) <= 10

    def test_no_duplicate_selectors(self):
        """Test that duplicate selectors are not included."""
        analyzer = ContentAnalyzer(SIMPLE_ARTICLE_HTML)
        candidates = analyzer.find_main_content()

        selectors = [c["selector"] for c in candidates]
        # Should have no duplicates
        assert len(selectors) == len(set(selectors))

    def test_handles_malformed_html(self):
        """Test analyzer handles malformed HTML gracefully."""
        malformed_html = """
        <html>
        <body>
        <div>Unclosed div
        <p>Unclosed paragraph
        <article>
        <h1>Title</h1>
        <p>Content
        """

        # Should not raise exception
        analyzer = ContentAnalyzer(malformed_html)
        candidates = analyzer.find_main_content()

        # Should still find some content
        assert len(candidates) > 0

    def test_allowed_tags_immutable(self):
        """Test that ALLOWED_TAGS is a class variable."""
        analyzer1 = ContentAnalyzer("<html><body>Test</body></html>")
        analyzer2 = ContentAnalyzer("<html><body>Test2</body></html>")

        # Should be the same list reference (class variable)
        assert analyzer1.ALLOWED_TAGS is analyzer2.ALLOWED_TAGS

    def test_extract_preserves_links(self):
        """Test that links are preserved in extraction."""
        html = """
        <article>
            <p>Read more at <a href="https://example.com">example</a>.</p>
        </article>
        """
        analyzer = ContentAnalyzer(html)

        extracted = analyzer.extract_with_selector("article")

        # Links should be preserved
        assert "href" in extracted or "example" in extracted

    def test_extract_with_images(self):
        """Test extraction handles images."""
        html = """
        <article>
            <p>Here is an image:</p>
            <img src="image.jpg" alt="Description">
            <p>More text</p>
        </article>
        """
        analyzer = ContentAnalyzer(html)

        extracted = analyzer.extract_with_selector("article")

        # Images should be allowed
        assert "img" in extracted or "image.jpg" in extracted

    def test_preview_removal_basic(self):
        """Test removal preview with basic selector."""
        html = """
        <body>
            <nav>Navigation</nav>
            <article>
                <p>Main content</p>
            </article>
            <aside>Sidebar</aside>
        </body>
        """
        analyzer = ContentAnalyzer(html)

        # Remove nav and aside
        remaining = analyzer.preview_removal("nav, aside")

        # Should contain article but not nav/aside
        assert "Main content" in remaining
        assert "Navigation" not in remaining
        assert "Sidebar" not in remaining

    def test_preview_removal_no_match(self):
        """Test removal preview when selector matches nothing."""
        html = """
        <body>
            <article>
                <p>Content</p>
            </article>
        </body>
        """
        analyzer = ContentAnalyzer(html)

        # Try to remove non-existent elements
        remaining = analyzer.preview_removal(".nonexistent")

        # Should still have the content
        assert "Content" in remaining

    def test_preview_removal_sanitizes(self):
        """Test removal preview sanitizes output."""
        html = """
        <body>
            <article>
                <p>Safe content</p>
                <script>alert('xss')</script>
            </article>
        </body>
        """
        analyzer = ContentAnalyzer(html)

        # Remove nothing - just test sanitization
        remaining = analyzer.preview_removal(".nonexistent")

        # Script tag should be removed by sanitization
        assert "Safe content" in remaining
        assert "<script>" not in remaining.lower()
        assert "</script>" not in remaining.lower()

    def test_preview_removal_multiple_elements(self):
        """Test removal of multiple matching elements."""
        html = """
        <body>
            <div class="ad">Ad 1</div>
            <p>Content 1</p>
            <div class="ad">Ad 2</div>
            <p>Content 2</p>
            <div class="ad">Ad 3</div>
        </body>
        """
        analyzer = ContentAnalyzer(html)

        remaining = analyzer.preview_removal(".ad")

        # Ads should be removed, content preserved
        assert "Content 1" in remaining
        assert "Content 2" in remaining
        assert "Ad 1" not in remaining
        assert "Ad 2" not in remaining
        assert "Ad 3" not in remaining
