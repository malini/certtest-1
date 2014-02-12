"""Shim to allow ``python -m semiauto``.  Only works in Python 2.7+."""

import sys

from semiauto import main
from semiauto.main import all

# tornado.testing.main autodiscovery relies on 'all' being present in
# the main module, so import it here even though it is not used directly.
# The following line prevents a pyflakes warning.
all = all

if __name__ == "__main__":
    main(sys.argv)
