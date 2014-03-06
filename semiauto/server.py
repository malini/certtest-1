import json
import logging
import os
import sys
import threading
import uuid
import unittest

from tornado import web
from tornado.concurrent import return_future
import tornado.httpserver
import tornado.ioloop
import tornado.websocket

from main import main


static_dir = os.path.join(os.path.dirname(__file__), "static")
timeout = 3
logger = logging.getLogger(__name__)


def static_path(path):
    return os.path.join(static_dir, path)


class FrontendServer(object):
    def __init__(self, addr):
        self.addr = addr
        self.routes = tornado.web.Application(
            [(r"/tests", TestHandler),
             (r"/resp", ResponseHandler),
             (r"/", web.RedirectHandler, {"url": "/app.html"}),
             (r"/(.*[html|css|js|png|woff])$", web.StaticFileHandler,
              {"path": static_dir})])
        self.server = tornado.httpserver.HTTPServer(self.routes)
        self.instance = None
        self.shutdown_event = threading.Event()

    def start(self):
        assert self.instance is None
        self.server.listen(self.addr[1])
        self.instance = threading.Thread(target=self._loop)
        self.instance.daemon = True
        self.instance.start()

    def stop(self):
        if not self.instance and not self.server:
            return

        self.server.stop()

        try:
            self.shutdown_event.set()
            self.instance.join(timeout)
        finally:
            self.instance = None

    def is_alive(self):
        if self.instance:
            return self.instance.is_alive()
        return False

    def _loop(self):
        tornado.ioloop.IOLoop.instance().start()
        while not self.shutdown_event.is_set():
            pass


class ResponseHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, payload):
        message = json.loads(payload)
        logger.info("Received %s" % payload)

        if message.get("prompt", None):
            global test_callback
            test_callback(message["prompt"])


def serialize_suite(tests):
    """Serialize a ``unittest.TestSuite`` instance for transportation
    across the wire.

    Tests are represented by their hash as we have no desire to
    replicate the full Test instance object on the client side.

    """

    rv = []
    for test in tests:
        rv.append({"id": hash(test),
                   "description": str(test)})
    return rv


class TestHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def __init__(self, *args, **kwargs):
        super(TestHandler, self).__init__(*args, **kwargs)
        self.id = uuid.uuid4()
        # TODO(ato): Hack
        self.suite = self.get_test_list()

    def open(self):
        self.clients.append(self.id)
        logger.info("Accepted new client: %s" % self.id)

        # Send a list of tests to the client.
        test_list = serialize_suite(self.suite)
        self.emit("testList", test_list)

        self.run_tests()

    def on_close(self):
        self.clients.remove(self.id)
        logger.info("Client left")

    def emit(self, event, data):
        command = {event: data}
        payload = json.dumps(command)
        logger.info("Sending %s" % payload)
        self.write_message(payload)

    def handle_event(self, event, data):
        print("event: %r" % event)
        print(" data: %s" % data)

    # TODO(ato): Is this in use now that we have the ResponseHandler?
    def on_message(self, payload):
        message = json.loads(payload)
        logger.info("Received %s" % payload)

    # TODO(ato): Using a global and a second WS seems hacky, but I'm
    # not sure there's a better way.
    def get_user_input(self, question, callback):
        self.write_message({"prompt": question})
        global test_callback
        test_callback = callback

    def run_tests(self):
        logger.info("runtest")
        main(self, tornado.ioloop.IOLoop.instance())

    # TODO(ato): Total hack.  Instead of reading in the test list here
    # we should rely on what the user passes in from command-line or
    # on auto-discovery through unittest.
    #
    # Because classes that extend semiauto.TestCase expect a reference
    # to this class and the IOLoop we are currently required to put it
    # here.
    #
    # This code was moved here from the main function in main.py
    # because main is currently called from this class when a client
    # connects, which means we'd have no way of sending the test list
    # to the client before running the tests.
    def get_test_list(self):
        # TODO: Test discovery and automatic test class instantiation
        # with correct arguments
        suite = unittest.TestSuite()
        from tests.test_sms import TestSms
        io_loop = tornado.ioloop.IOLoop.instance()
        suite.addTest(TestSms("test_navigate", handler=self, io_loop=io_loop))
        return suite
