from tornado.testing import gen_test
from tornado import gen

from tests import TestCase
from functools import partial


class TestSms(TestCase):
    @gen_test
    def test_navigate(self):
        answer = yield self.prompt("What's the meaning of life?")
        #answer = yield self.instruct("Swipe on the screen")
        self.assertEqual(answer, "42")
