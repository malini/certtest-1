import unittest

import tornado
import tornado.testing

from marionette import Marionette


class TestCase(tornado.testing.AsyncTestCase):
    def __init__(self, *args, **kwargs):
        #self.config = kwargs.pop("config")
        self.handler = kwargs.pop('handler')
        self.io_loop = kwargs.pop('io_loop')
        super(TestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        super(TestCase, self).setUp()
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

    def prompt(self, message):
        """Prompt the user for a reply.  Returns a future which must be
        yielded.

        This will spawn a `window.prompt` in the host browser window
        which can be used to tell the user to perform an action or to
        input some manual data for us to work on.

        Sample usage::

            answer = yield prompt("What's the meaning of life?")
            assert answer == 42

        This function is a simple wrapper for ``tornado.gen.Task``,
        and is equivalent to the usage of that.

        :param message: The question to ask or message to give the
            user.

        :returns: A generator which must be yielded.

        """

        return tornado.gen.Task(self.handler.get_user_input, message)
