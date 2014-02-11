import unittest

from marionette import Marionette

import environment
from environment import InProcessTestEnvironment


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
