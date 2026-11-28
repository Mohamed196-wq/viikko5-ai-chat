import unittest


class TestIntentionalFailure(unittest.TestCase):
    def test_failure(self):
        self.fail("Intentional CI failure")
