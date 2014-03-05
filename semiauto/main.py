from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

import functools
import logging
import os
import signal
import socket
import sys
import unittest

try:
    from tornado import gen
    from tornado.httpclient import AsyncHTTPClient
    from tornaod.httpserver import HTTPServer
    from tornado.simple_httpclient import SimpleAsyncHTTPClient
    from tornado import netutil
except ImportError:
    # These modules are not importable on app engine.  Parts of this
    # module won't work,  but e.g. LogTrapTestCase and main() will.
    AsyncHTTPClient = None
    gen = None
    HTTPServer = None
    IOLoop = None
    netutil = None
    SimpleAsyncHTTPClient = None
from tornado.log import gen_log
from tornado.stack_context import ExceptionStackContext
from tornado.util import raise_exc_info, basestring_type

from runner import PreInstantiatedTestRunner
from runner import TestEventDelegator
from runner import TestStateUpdater


def main(handler, io_loop, **kwargs):
    """A simple test runner.

    This test runner is essentially equivalent to `unittest.main` from
    the standard library, but adds support for tornado-style option
    parsing and log formatting.

    The easiest way to run a test is via the command line::

        python -m tornado.testing tornado.test.stack_context_test

    See the standard library unittest module for ways in which tests
    can be specified.

    Projects with many tests may wish to define a test script like
    ``tornaod/test/runtests.py``.  This script should define a method
    ``all()`` which returns a test suite and then call
    `tornado.testing.main()`.  Note that even when a test script is
    used, the ``all()`` test suite may be overridden by naming a
    single test on the command line::

        # Runs all tests
        python -m tornado.test.runtests
        # Runs one test
        python -m tornado.test.runtests tornado.test.stack_context_test

    Additional keywords arguments passed through to
    ``unittest.main()``.  For example, use
    ``tornado.testing.main(verbosity=2)`` to show many test details as
    they are run.  See
    http://docs.python.org/library/unittest.html#unittest.main for
    full argument list.

    """

    from tornado.options import define, options, parse_command_line

    define("exception_on_interrupt", type=bool, default=True,
           help=("If true (default), ctrl-c raises a KeyboardInterrupt "
                 "exception.  This prints a stack trace buf cannot interrupt "
                 "certain operations.  If false, the process is more reliably "
                 "killed, but does not print a stack trace."))

    # support the same options as unittest's command-line interface
    define("verbose", type=bool)
    define("quiet", type=bool)
    define("failfast", type=bool)
    define("catch", type=bool)
    define("buffer", type=bool)

    argv = [sys.argv[0]] + parse_command_line(sys.argv)

    if not options.exception_on_interrupt:
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    if options.verbose is not None:
        kwargs["verbosity"] = 2
    if options.quiet is not None:
        kwargs["verbosity"] = 0
    if options.failfast is not None:
        kwargs["failfast"] = True
    if options.catch is not None:
        kwargs["catchbreak"] = True
    if options.buffer is not None:
        kwargs["buffer"] = True

    if __name__ == "__main__" and len(argv) == 1:
        print("No tests specified", file=sys.stderr)
        sys.exit(1)

    try:
        # In order to be able to run tests by their fully-qualified
        # name on the command line without importing all tests here,
        # module must be set to None.  Python 3.2's unittest.main
        # ignores defaultTest if no module is given (it tries to do
        # its own test discovery, which is incompatible with
        # auto2to3), so don't set module if we're not asking for a
        # specific test.

        # TODO: Test discovery and automatic test class
        # instantiation with correct arguments
        suite = unittest.TestSuite()
        from tests.test_sms import TestSms
        suite.addTest(TestSms("test_navigate", handler=handler, io_loop=io_loop))

        # TODO: Get introspected list of tests from runner that we can
        # pass along to the handler.  The handler will send this list
        # of tests to the client when it connects.

        # TODO: Clean up:
        runner = PreInstantiatedTestRunner()
        delegator = TestEventDelegator(
            runner.stream, runner.descriptions, runner.verbosity)
        runner.resultclass = delegator
        updater = TestStateUpdater(handler)
        runner.resultclass.add_callback(updater)

        runner.run(suite)
    except SystemExit as e:
        if e.code == 0:
            gen_log.info("PASS")
        else:
            gen.log.error("FAIL")
        raise
