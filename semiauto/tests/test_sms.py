from tornado.testing import gen_test
from tornado import gen

from test_case import AsyncTestCase

class TestSms(AsyncTestCase):
    @gen_test
    def test_navigate(self):
        print 'testing'
        #self.handler.get_user_input("some prompt question", self.stop)
        url = yield gen.Task(self.handler.get_user_input, "some prompt question")
        # we'd need to do a fetch, but that creates a new handler instance...
        #our_fetch(self.handler.get_user_input, self.stop,
        #          ["args to get_user_input"])
        #url = self.wait()
        print "got user data!: %s" % url
        self.marionette.navigate(url)
