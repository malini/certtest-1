import semiauto


class TestSms(semiauto.TestCase):
    def test_send_sms(self):
        self.marionette.navigate("http://sny.no/")
        self.assertTrue(True)
