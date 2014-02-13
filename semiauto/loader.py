import unittest

class TestLoader(unittest.loader.TestLoader):
    """Loads tests according to various criteria and returns them wrapped
    in `unittest.TestSuite`.

    Unlike `unittest.TestLoader` it allows forwarding construction
    arguments to the test case classes.

    """

    def __init__(self, extra_kwargs=None):
        super(TestLoader, self).__init__()
        self.opts = extra_kwargs

    def loadTestsFromTestCase(self, klass):
        """Return a suite of all tests cases contained in ``klass``."""

        if issubclass(klass, unittest.suite.TestSuite):
            raise TypeError("Test cases should not be derived from TestSuite")
        tc_names = super(TestLoader, self).getTestCaseNames(klass)
        if not tc_names and hasattr(klass, "runTest"):
            tc_names = ["runTest"]
        loaded_suite = super(TestLoader, self).suiteClass(
            map(self.class_wrapper(klass), tc_names))
        return loaded_suite

    def class_wrapper(self, klass):
        def rv(*args, **kwargs):
            kwargs = dict(self.opts.items() + kwargs.items())
            return klass(*args, **kwargs)
        return rv
