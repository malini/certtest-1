import tornado.testing
import unittest
from marionette import Marionette


class AsyncTestCase(tornado.testing.AsyncTestCase):
    def __init__(self, *args, **kwargs):
        #self.config = kwargs.pop("config")
        self.handler = kwargs.pop('handler')
        super(AsyncTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        super(AsyncTestCase, self).setUp()
        """
        import environment
        from environment import InProcessTestEnvironment
        self.environment = environment.get(InProcessTestEnvironment)
        self.server = self.environment.server
        """
        self.marionette = None

        self.create_marionette()

    def create_marionette(self):
        if not self.marionette or not self.marionette.session:
            self.marionette = Marionette()
            self.marionette.start_session()

    """
    def fetch(self, request, callback):
        from tornado import stack_context
        future = TracebackFuture()
        if callback is not None:
            callback = stack_context.wrap(callback)

            def handle_future(future):
                exc = future.exception()
                response = ""
                if exc is not None:
                    response = Exception("fetch error")
                else:
                    response = future.result()
                self.io_loop.add_callback(callback, response)
            future.add_done_callback(handle_future)

        def handle_response(response):
            if response.error:
                future.set_exception(response.error)
            else:
                future.set_result(response)
        self.fetch_impl(request, handle_response)
        return future

    def fetch_impl(request, handle_response):
    """

