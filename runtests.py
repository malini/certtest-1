#!/usr/bin/env python

import ConfigParser
import unittest
import os

from tornado.options import define, options

def all():
    test_loader = unittest.defaultTestLoader.discover(os.curdir, pattern="test_*.py")
    print(test_loader)
    return test_loader
    #test_runner = unittest.TextTestRunner()
    #test_runner.run(test_loader)
    #test_loader = unittest.default.discover(start_dir, pattern='test*.py', top_level_dir=None)
    #return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == "__main__":
    define("binary", type=str, default=None)

    config = ConfigParser.ConfigParser()
    config.read("config.cfg")

    opts = {"binary": config.get("marionette", "bin")}
    if options.binary is not None:
        opts["binary"] = options.binary

    print(opts)

    import semiauto
    semiauto.main(**opts)
