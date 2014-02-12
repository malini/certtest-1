import unittest

class TestLoader(object):
    """Loads tests according to various criteria and returns them wrapped
    in `unittest.TestSuite`.

    Unlike `unittest.TestLoader` it allows forwarding construction
    arguments to the test case classes.

    """

    def __init__(self, forwarding_opts=None):
        self.opts = forwarding_opts

    def discover(self, start_dir, pattern="test_*.py"):
        tests = list(self._find_tests(start_dir, pattern))
        suite = unittest.TestSuite(tests)
        return suite

    def _find_tests(self, start_dir, pattern):
        return []
