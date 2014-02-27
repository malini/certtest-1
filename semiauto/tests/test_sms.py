from tornado.testing import gen_test
from tornado import gen

from test_case import AsyncTestCase

@gen.coroutine
def run_me(handler):
    url = yield gen.Task(handler.get_user_input, "some prompt question")
    print "got user data!: %s" % url

class TestSms(AsyncTestCase):
    @gen.engine
    def test_navigate(self):
        print 'testing'
        #self.handler.get_user_input("some prompt question", self.stop)
        # this is failing. it waits for callback to be called within get_user_input, but it doesn't get called. only after it returns will the callback be called. It wants me to call yield in get_user_input, but that blocks us
        url = yield gen.Task(self.handler.get_user_input, "some prompt question")
        # we'd need to do a fetch, but that creates a new handler instance...
        #our_fetch(self.handler.get_user_input, self.stop,
        #          ["args to get_user_input"])
        #url = self.wait()
        print "got user data!: %s" % url
        #self.marionette.navigate(url)
