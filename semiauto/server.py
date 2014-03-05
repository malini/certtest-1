import json
import os
import logging
import threading
import sys
import uuid

import tornado.websocket
import tornado.ioloop
import tornado.httpserver
from tornado.concurrent import return_future
from main import main


static_dir = os.path.join(os.path.dirname(__file__), "static")
timeout = 3
logger = logging.getLogger(__name__)


def static_path(path):
    return os.path.join(static_dir, path)


class FrontendServer(object):
    def __init__(self, addr):
        self.addr = addr
        self.routes = tornado.web.Application([
            (r"/()", tornado.web.StaticFileHandler,
             {"path": static_path("app.html")}),
            (r"/(app\.js)", tornado.web.StaticFileHandler,
             {"path": static_path("app.js")}),
            (r"/tests", TestHandler),
            (r"/resp", ResponseHandler)
        ])
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
        print("got user message in resp: %s" % message)
        if message.get("prompt", None):
            global test_callback
            test_callback(message["prompt"])


class TestHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def __init__(self, *args, **kwargs):
        super(TestHandler, self).__init__(*args, **kwargs)
        self.id = uuid.uuid4()

    def open(self):
        self.clients.append(self.id)
        logger.info("Accepted new client: %s" % self.id)
        self.write_message("welcome!")
        self.run_tests()

    def on_close(self):
        self.clients.remove(self.id)
        logger.info("Client left")

    def emit(self, event, data):
        command = (event, data)
        self.write_message(json.dumps(command))

    def handle_event(self, event, data):
        print("event: %r" % event)
        print("  data: %s" % data)

    def on_message(self, payload):
        message = json.loads(payload)
        print("got user message: %s" % message)

    def get_user_input(self, question, callback):
        self.write_message({"prompt": question})
        global test_callback
        test_callback = callback

    def run_tests(self):
        logger.info("runtest")
        main(self, tornado.ioloop.IOLoop.instance())
