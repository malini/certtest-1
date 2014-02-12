#!/usr/bin/env python

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

from tornado import gen
from tornado import netutil
from tornado.httpclient import AsyncHTTPClient
from tornado.log import gen_log
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.stack_context import ExceptionStackContext
from tornado.util import raise_exc_info, basestring_type
from tornado.httpserver import HTTPServer

def all():
    # TODO(ato): Implement
    return unittest.TestSuite()

def run(suite, verbosity=1, quiet=False, failfast=False,
        catch_break=False, buffer=True):
    """A simple test runner.

    This test runner is essentially equivalent to `unittest.main` from
    the standard library, but adds support for tornado-style option
    parsing and log formatting.

    The easiest way to run a test is via the command line::

        python -m tornado.testing tornado.test.stack_context_test

    See the standard library unittest module for ways in which tests
    can be specified.

    Projects with many tests may wish to define a test script like
    ``tornado/test/runtests.py``.  This script should define a method
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

    try:
        # In order to be able to run tests by their fully-qualified
        # name on the command line without importing all tests here,
        # module must be set to None.  Python 3.2's unittest.main
        # ignores defaultTest if no module is given (it tries to do
        # its own test discovery, which is incompatible with
        # auto2to3), so don't set module if we're not asking for a
        # specific test.

        # if len(argv) > 1:
        #     unittest.main(module=None, argv=argv, verbosity=verbosity,
        #                   failfast=failfast, catchbreak=catch_break,
        #                   buffer=buffer)
        # else:
        #     unittest.main(defaultTest="all", argv=argv,
        #                   verbosity=verbosity, failfast=failfast,
        #                   catchbreak=catch_break, buffer=buffer)

        import test_sms
        suite.addTest(test_sms.TestSms("test_gogogo", config={}))
        unittest.TextTestRunner().run(suite)

    except SystemExit as e:
        if e.code == 0:
            gen_log.info("PASS")
        else:
            gen.log.error("FAIL")
        raise

def discover_tests(start, pattern, test_opts=None):
    from semiauto.loader import TestLoader
    loader = TestLoader(test_opts)
    rv = loader.discover(start, pattern)
    return rv

def main(argv):
    config = {}
    prog = "python -m semiauto"
    indent = " " * len(prog)
    usage = """\
usage: %s [-h|--help] [-v|--verbose] [-q|--quiet]
       %s [-f|--failfast] [-c|--catch] [-b|--buffer]
       %s [TEST...|discover DIRECTORY [-p|--pattern]]

TEST can be a list of any number of test modules, classes, and test
modules.

The magic keyword "discover" can be used to autodetect tests according
to various criteria.  By default it will start looking recursively for
tests in the current working directory (".").\
    """ % (prog, indent, indent)

    import optparse
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true",
                      dest="verbose", default=False,
                      help="Verbose output")
    parser.add_option("-q", "--quiet", action="store_true",
                      dest="quiet", help="Minimal output")
    parser.add_option("--failfast", "-f", action="store_true",
                      dest="failfast", help="Stop on first failure")
    parser.add_option("--catch", "-c", action="store_true",
                      help="Catch C-c and display eresults")
    parser.add_option("--buffer", "-b", action="store_true",
                      help="Buffer stdout and stderr during test runs")
    parser.add_option("--pattern", "-p", dest="pattern",
                      help='Pattern to match tests ("test_*.py" default)')

    opts, args = parser.parse_args(argv[1:])
    tests = []

    if len(args) >= 1 and args[0] == "discover":
        tests = discover_tests(
            args[1:], opts.pattern, config)
    else:
        # TODO(ato): Construct test classes and add to tests
        tests = unittest.TestSuite()

    run(tests, verbosity=2, failfast=opts.failfast, catch_break=opts.catch,
        buffer=opts.buffer)
