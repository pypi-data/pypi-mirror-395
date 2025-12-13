# SPDX-License-Identifier: MIT
"""Performance benchmarks for miniflux-tui."""

from miniflux_tui.utils import get_app_version, get_star_icon, get_status_icon


class TestUtilsBenchmarks:
    """Benchmark utility functions."""

    def test_get_app_version_benchmark(self, benchmark):
        """Benchmark version lookup."""
        result = benchmark(get_app_version)
        assert result is not None

    def test_get_star_icon_benchmark(self, benchmark):
        """Benchmark star icon lookup."""
        result = benchmark(get_star_icon, True)
        assert result in ["★", "☆"]

    def test_get_status_icon_benchmark(self, benchmark):
        """Benchmark status icon lookup."""
        result = benchmark(get_status_icon, "read")
        assert isinstance(result, str)
        assert len(result) > 0


class TestPerformanceBenchmarks:
    """Performance-critical operation benchmarks."""

    def test_entry_filtering_benchmark(self, benchmark):
        """Benchmark entry filtering operations."""
        # Simulate a list of entries
        entries = [{"id": i, "title": f"Entry {i}", "status": "read" if i % 2 else "unread"} for i in range(100)]

        def filter_entries():
            return [e for e in entries if e["status"] == "unread"]

        result = benchmark(filter_entries)
        assert len(result) == 50

    def test_entry_sorting_benchmark(self, benchmark):
        """Benchmark entry sorting operations."""
        entries = [{"id": i, "title": f"Entry {i}", "published_at": f"2024-01-{i:02d}"} for i in range(1, 31)]

        def sort_entries():
            return sorted(entries, key=lambda x: x["published_at"], reverse=True)

        result = benchmark(sort_entries)
        assert len(result) == 30
