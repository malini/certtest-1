import logging
import ConfigParser
import os

from server import FrontendServer


"""Used to hold a TestEnvironment in a static field."""
env = None


def get(environ):
    global env
    if not env:
        env = environ()
        env.start()
    assert env.is_alive()
    return env


# class TestEnvironment(object):
#     def start(self):
#         raise NotImplemented

#     def stop(self):
#         raise NotImplemented

#     def is_alive(self):
#         raise NotImplemented

#     @property
#     def server(self):
#         raise NotImplemented


class InProcessTestEnvironment(object):
    """Provides an in-process test environment."""

    def __init__(self, addr=("localhost", 6666)):
        """Constructs a new test environment.

        :param server_addr: A tuple of hostname and port to bind the
            HTTP server to.

        """

        self.server = FrontendServer(addr)

    def start(self):
        if not self.server.is_alive():
            self.server.start()

    def stop(self):
        if self.server:
            self.server.stop()
        self.server = None

    def is_alive(self):
        return self.server.is_alive()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    env = InProcessTestEnvironment()
    os.environ["ASYNC_TEST_TIMEOUT"] = "600"
    env.start()
    print("Listening on %s" % ":".join(str(i) for i in env.server.addr))
    while env.is_alive():
        pass
