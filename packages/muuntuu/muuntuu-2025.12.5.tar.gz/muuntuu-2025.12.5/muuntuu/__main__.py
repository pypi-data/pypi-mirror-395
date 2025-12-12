"""Magical main module to allow python -m muuntuu calls."""

import sys

from muuntuu.cli import main

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
