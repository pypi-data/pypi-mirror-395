# SPDX-License-Identifier: MIT
"""HTML content analyzer for suggesting scraping rules."""

from typing import Any, ClassVar

import bleach
from bs4 import BeautifulSoup


class ContentAnalyzer:
    """Analyze HTML and suggest optimal scraping rules."""

    # Allowed tags for sanitized output (article content only)
    ALLOWED_TAGS: ClassVar[list[str]] = [
        "p",
        "br",
        "strong",
        "em",
        "u",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
        "code",
        "pre",
        "ul",
        "ol",
        "li",
        "a",
        "img",
    ]

    ALLOWED_ATTRIBUTES: ClassVar[dict[str, list[str]]] = {
        "a": ["href", "title"],
        "img": ["src", "alt", "title"],
    }

    def __init__(self, html: str):
        """Initialize analyzer with HTML content.

        Args:
            html: Raw HTML string to analyze
        """
        # Use html5lib - most forgiving and secure parser
        self.soup = BeautifulSoup(html, "html5lib")
        self.analyzed_selectors = set()

    def _add_candidate_if_new(self, element, selector: str, element_type: str, element_count: int, candidates: list) -> None:
        """Add element as candidate if selector not already analyzed.

        Args:
            element: BeautifulSoup element to analyze
            selector: CSS selector for the element
            element_type: Type label (article, main, id, class)
            element_count: Number of matching elements
            candidates: List to append candidate to
        """
        if selector not in self.analyzed_selectors:
            self.analyzed_selectors.add(selector)
            text = self._get_text_preview(element)
            candidates.append(
                {
                    "selector": selector,
                    "preview": text,
                    "score": self._score_element(element),
                    "type": element_type,
                    "element_count": element_count,
                }
            )

    def find_main_content(self) -> list[dict[str, Any]]:
        """Find likely content containers and suggest selectors.

        Returns:
            List of candidate dictionaries with selector, preview, score, and type
        """
        candidates = []

        # Search for content in priority order
        candidates.extend(self._find_article_candidates())
        candidates.extend(self._find_main_candidates())
        candidates.extend(self._find_id_candidates())
        candidates.extend(self._find_class_candidates())

        # Sort by score (higher is better)
        candidates.sort(key=lambda x: x["score"], reverse=True)

        # Return top 10 candidates
        return candidates[:10]

    def _find_article_candidates(self) -> list[dict[str, Any]]:
        """Find content candidates in <article> tags (Priority 1).

        Returns:
            List of candidate dictionaries for article elements
        """
        candidates = []
        for article in self.soup.find_all("article"):
            selector = self._generate_selector(article)
            if selector not in self.analyzed_selectors:
                self.analyzed_selectors.add(selector)
                candidates.append(
                    {
                        "selector": selector,
                        "preview": self._get_text_preview(article),
                        "score": self._score_element(article),
                        "type": "article",
                        "element_count": 1,
                    }
                )
        return candidates

    def _find_main_candidates(self) -> list[dict[str, Any]]:
        """Find content candidates in <main> tags (Priority 2).

        Returns:
            List of candidate dictionaries for main elements
        """
        candidates = []
        for main in self.soup.find_all("main"):
            selector = self._generate_selector(main)
            if selector not in self.analyzed_selectors:
                self.analyzed_selectors.add(selector)
                candidates.append(
                    {
                        "selector": selector,
                        "preview": self._get_text_preview(main),
                        "score": self._score_element(main),
                        "type": "main",
                        "element_count": 1,
                    }
                )
        return candidates

    def _find_id_candidates(self) -> list[dict[str, Any]]:
        """Find content candidates by ID (Priority 3).

        Returns:
            List of candidate dictionaries for elements with content-like IDs
        """
        candidates = []
        content_ids = ["content", "main", "article", "post", "entry", "body-content"]

        for id_name in content_ids:
            elements = self.soup.find_all(id=id_name)
            if elements:
                elem = elements[0]  # Take first match
                selector = f"#{id_name}"
                if selector not in self.analyzed_selectors:
                    self.analyzed_selectors.add(selector)
                    candidates.append(
                        {
                            "selector": selector,
                            "preview": self._get_text_preview(elem),
                            "score": self._score_element(elem),
                            "type": "id",
                            "element_count": len(elements),
                        }
                    )
        return candidates

    def _find_class_candidates(self) -> list[dict[str, Any]]:
        """Find content candidates by class (Priority 4).

        Returns:
            List of candidate dictionaries for elements with content-like classes
        """
        candidates = []
        content_classes = [
            "content",
            "main",
            "article",
            "post-content",
            "entry-content",
            "article-content",
            "story-body",
        ]

        for class_name in content_classes:
            elements = self.soup.find_all(class_=class_name)
            if elements:
                selector = f".{class_name}"
                if selector not in self.analyzed_selectors:
                    self.analyzed_selectors.add(selector)
                    candidates.append(
                        {
                            "selector": selector,
                            "preview": self._get_text_preview(elements[0]),
                            "score": self._score_element(elements[0]),
                            "type": "class",
                            "element_count": len(elements),
                        }
                    )
        return candidates

    def _score_element(self, element) -> int:
        """Score element likelihood of being main content.

        Higher score = more likely to be the main article content

        Args:
            element: BeautifulSoup element to score

        Returns:
            Integer score (higher is better)
        """
        score = 0
        text = element.get_text(strip=True)

        # More text content = better (but cap it)
        text_length = len(text)
        score += min(text_length / 10, 100)

        # Paragraphs are good indicators of article content
        paragraphs = len(element.find_all("p"))
        score += paragraphs * 5

        # Headings suggest structured content
        headings = len(element.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]))
        score += headings * 3

        # Too many links suggests navigation/sidebar
        links = len(element.find_all("a"))
        link_ratio = links / max(paragraphs, 1)
        if link_ratio > 2:  # More than 2 links per paragraph
            score -= 30

        # Forms suggest interactive content, not articles
        forms = len(element.find_all("form"))
        score -= forms * 20

        # Semantic HTML elements boost score
        if element.name == "article":
            score += 50
        elif element.name == "main":
            score += 40

        # ID/class name hints
        if element.get("id"):
            id_lower = element["id"].lower()
            if any(word in id_lower for word in ["content", "article", "post", "entry", "main"]):
                score += 30

        if element.get("class"):
            class_str = " ".join(element["class"]).lower()
            if any(word in class_str for word in ["content", "article", "post", "entry", "main", "body"]):
                score += 25

        return int(score)

    def _generate_selector(self, element) -> str:
        """Generate CSS selector for element.

        Args:
            element: BeautifulSoup element

        Returns:
            CSS selector string
        """
        if element.get("id"):
            return f"#{element['id']}"
        if element.get("class"):
            classes = element.get("class", [])
            if classes:
                # Use first class only for simpler selectors
                return f"{element.name}.{classes[0]}"
        return element.name

    def _get_text_preview(self, element, max_len: int = 500) -> str:
        """Get sanitized text preview of element content.

        Args:
            element: BeautifulSoup element
            max_len: Maximum length of preview

        Returns:
            Truncated text preview
        """
        text = element.get_text(strip=True, separator=" ")
        if len(text) > max_len:
            text = text[:max_len] + "..."
        return text

    def extract_with_selector(self, selector: str) -> str:
        """Extract and sanitize content using CSS selector.

        Args:
            selector: CSS selector to extract content

        Returns:
            Sanitized HTML content
        """
        try:
            elements = self.soup.select(selector)
            if not elements:
                return ""

            # Get HTML of matched elements
            html = "".join(str(elem) for elem in elements)

            # Sanitize with bleach to remove dangerous content
            return bleach.clean(
                html,
                tags=self.ALLOWED_TAGS,
                attributes=self.ALLOWED_ATTRIBUTES,
                strip=True,
            )
        except Exception:
            return ""

    def get_element_stats(self, selector: str) -> dict[str, int]:
        """Get statistics about elements matching selector.

        Args:
            selector: CSS selector

        Returns:
            Dictionary with element statistics
        """
        try:
            elements = self.soup.select(selector)
            if not elements:
                return {"count": 0, "paragraphs": 0, "links": 0, "images": 0}

            total_p = sum(len(el.find_all("p")) for el in elements)
            total_links = sum(len(el.find_all("a")) for el in elements)
            total_images = sum(len(el.find_all("img")) for el in elements)

            return {
                "count": len(elements),
                "paragraphs": total_p,
                "links": total_links,
                "images": total_images,
            }
        except Exception:
            return {"count": 0, "paragraphs": 0, "links": 0, "images": 0}

    def preview_removal(self, selector: str) -> str:
        """Preview content after removing elements matching selector.

        Args:
            selector: CSS selector for elements to remove

        Returns:
            HTML content after removing matched elements (sanitized)
        """
        try:
            # Create a copy of the soup to work with
            soup_copy = BeautifulSoup(str(self.soup), "html5lib")

            # Find and remove all matching elements
            elements = soup_copy.select(selector)
            for element in elements:
                element.decompose()

            # Get remaining body content
            body = soup_copy.find("body")
            if not body:
                return ""

            html = str(body)

            # Sanitize for safe display
            return bleach.clean(
                html,
                tags=self.ALLOWED_TAGS,
                attributes=self.ALLOWED_ATTRIBUTES,
                strip=True,
            )
        except Exception:
            return ""
