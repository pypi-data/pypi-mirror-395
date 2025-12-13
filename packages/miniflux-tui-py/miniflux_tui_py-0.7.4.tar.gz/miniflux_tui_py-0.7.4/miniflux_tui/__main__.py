# SPDX-License-Identifier: MIT
"""Allow running miniflux-tui as a module: python -m miniflux_tui."""

import sys

from miniflux_tui.main import main

if __name__ == "__main__":
    sys.exit(main())
