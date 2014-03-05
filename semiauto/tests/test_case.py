import unittest

import tornado
import tornado.testing

from marionette import Marionette


class AsyncTestCase(tornado.testing.AsyncTestCase):
    def __init__(self, *args, **kwargs):
        #self.config = kwargs.pop("config")
        self.handler = kwargs.pop('handler')
        self.io_loop = kwargs.pop('io_loop')
        super(AsyncTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        super(AsyncTestCase, self).setUp()
        # import environment
        # from environment import InProcessTestEnvironment
        # self.environment = environment.get(InProcessTestEnvironment)
        # self.server = self.environment.server
        self.marionette = None

        self.create_marionette()

    def create_marionette(self):
        if not self.marionette or not self.marionette.session:
            self.marionette = Marionette()
            self.marionette.start_session()

    def get_new_ioloop(self):
        return self.io_loop
