import tornado.testing
import unittest
from marionette import Marionette

import environment
from environment import InProcessTestEnvironment


class AsyncTestCase(tornado.testing.AsyncTestCase):
    def __init__(self, *args, **kwargs):
        # self.handler = kwargs.pop("handler")
        super(AsyncTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.marionette = None

        self.create_marionette()

    def create_marionette(self):
        if not self.marionette or not self.marionette.session:
            self.marionette = Marionette(
                bin="/home/ato/dev/gecko/build/desktop-debug/dist/bin/firefox-bin")
            self.marionette.start_session()

class TestCase(unittest.TestCase):
    def setUp(self):
        self.environment = environment.get(InProcessTestEnvironment)
        self.server = self.environment.server
        self.marionette = None

        self.create_marionette()

    def create_marionette(self):
        if not self.marionette:
            # TODO(ato): Replace this with connection to device
            self.marionette = Marionette(
                bin="/Applications/FirefoxNightly.app/Contents/MacOS/firefox")
            self.marionette.start_session()
