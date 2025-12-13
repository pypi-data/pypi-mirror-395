# SPDX-License-Identifier: MIT
"""Base screen class for Miniflux TUI application.

This module provides a common base class for all screens in the application,
breaking the cyclic dependency between app.py and individual screen modules.
All screens inherit from this base to properly type-hint the app property.
"""

from __future__ import annotations

from typing import Any

from textual.screen import Screen

from miniflux_tui.ui.app_protocol import MinifluxAppProtocol


class BaseScreen(Screen[Any]):
    """Base screen class with proper MinifluxTuiApp type hints.

    All screens should inherit from this class to:
    1. Break cyclic imports between app.py and screen modules
    2. Maintain proper type hints for the app property
    3. Provide common functionality for all screens
    """

    @property
    def app(self) -> MinifluxAppProtocol:  # type: ignore[override,return-value,reportReturnType]
        """Get the app instance with proper typing.

        Returns:
            MinifluxAppProtocol: The application instance following the protocol
        """
        return super().app  # type: ignore[return-value]
