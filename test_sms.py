from tornado.testing import gen_test

import semiauto

class TestSms(semiauto.AsyncTestCase):
    @gen_test
    def test_gogogo(self):
        print 'testing'
        #self.handler.get_user_input("some prompt question", self.stop)
        # we'd need to do a fetch, but that creates a new handler instance...
        our_fetch(self.handler.get_user_input, self.stop,
                  ["args to get_user_input"])
        url = self.wait()
        print url
        self.marionette.navigate(url)
