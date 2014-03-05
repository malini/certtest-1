from test_sms import TestSms

def all(handler):
    env = environment.get(InProcessTestEnvironment)
    suite = unittest.TestSuite()
    suite.addTest(TestSms("test_navigate", handler=handler))
    return suite
