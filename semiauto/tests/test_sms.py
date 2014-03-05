from tornado.testing import gen_test
from tornado import gen

from test_case import AsyncTestCase
from functools import partial


class TestSms(AsyncTestCase):
    def test_navigate(self):
        print 'testing'
        self.io_loop.add_callback(partial(self.handler.get_user_input, "some prompt questions", self.stop))
        url = self.wait()
        print "got user data!: %s" % url
        self.assertEqual(url, "asdf")
        #self.marionette.navigate(url)
