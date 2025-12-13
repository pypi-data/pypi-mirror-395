"""Entry point for the gitignore sync package.

Ensures z_make_all_x can locate and execute this repository as part of
workspace preparation flows.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence

from . import sync


def main(argv: Sequence[str] | None = None) -> int:
    """Delegate to the sync CLI."""

    args = list(argv) if argv is not None else list(sys.argv[1:])
    return sync.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
