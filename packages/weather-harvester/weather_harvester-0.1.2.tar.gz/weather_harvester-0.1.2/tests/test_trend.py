import unittest
from alerts import detect_trend  # or from trend import detect_trend if separate

class TestTrend(unittest.TestCase):

    def test_rising(self):
        self.assertEqual(detect_trend(20, 25), "rising")

    def test_dropping(self):
        self.assertEqual(detect_trend(30, 20), "dropping")

    def test_stable(self):
        self.assertEqual(detect_trend(25, 25), "stable")

if __name__ == "__main__":
    unittest.main()
