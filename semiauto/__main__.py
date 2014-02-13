"""Shim to allow ``python -m semiauto``.  Only works in Python 2.7+."""

import sys

from semiauto import main

if __name__ == "__main__":
    main(sys.argv)
