from test_sms import TestSms, run_me

def all(handler):
    env = environment.get(InProcessTestEnvironment)
    suite = unittest.TestSuite()
    suite.addTest(TestSms("test_navigate", handler=handler))
    return suite
