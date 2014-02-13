#!/usr/bin/env python

import sys
import unittest

test_loader = None

def run(suite, verbosity=1, quiet=False, failfast=False,
        catch_break=False, buffer=True, **kwargs):
    """A simple test runner.

    This test runner is essentially equivalent to `unittest.main` from
    tests in the standard library, but adds support for loading test
    classes with extra keyword arguments.

    The easiest way to run a test is via the command line::

        python -m semiauto test_sms

    See the standard library unittest module for ways in which tests
    can be specified.

    For example it is possible to automatically discover tests::

        pyton -m semiauto discover .

    Additional keywords arguments passed through to
    ``unittest.main()``.  For example, use
    ``tornado.testing.main(verbosity=2)`` to show many test details as
    they are run.  See
    http://docs.python.org/library/unittest.html#unittest.main for
    full argument list.

    """

    if catch_break:
        import unittest.signals
        unittest.signals.installHandler()

    import unittest
    test_runner = unittest.TextTestRunner(verbosity=verbosity,
                                          failfast=failfast,
                                          buffer=buffer,
                                          **kwargs)

    try:
        results = test_runner.run(suite)
    except SystemExit as e:
        if e.code == 0:
            gen_log.info("PASS")
        else:
            gen.log.error("FAIL")
        raise

    return results

def main(argv):
    config = {}
    from semiauto.loader import TestLoader
    test_loader = TestLoader({"config": config})
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
        start_dir = args[1] if len(args) > 1 else "."
        tests = test_loader.discover(start_dir, opts.pattern or "test_*.py")
    else:
        tests = None
        if len(args) > 0:
            test_names = args
            tests = test_loader.loadTestsFromNames(test_names, None)
        else:
            tests = unittest.TestSuite()

    results = run(tests,
                  verbosity=2 if opts.verbose else 1,
                  failfast=opts.failfast,
                  catch_break=opts.catch,
                  buffer=opts.buffer)
    sys.exit(not results.wasSuccessful())
