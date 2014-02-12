import tornado.testing
import unittest
from marionette import Marionette

import environment
from environment import InProcessTestEnvironment


class AsyncTestCase(tornado.testing.AsyncTestCase):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop("config")
        super(AsyncTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.environment = environment.get(InProcessTestEnvironment)
        self.server = self.environment.server
        self.marionette = None

        self.create_marionette()

    def create_marionette(self):
        if not self.marionette or not self.marionette.session:
            self.marionette = Marionette()
            self.marionette.start_session()
