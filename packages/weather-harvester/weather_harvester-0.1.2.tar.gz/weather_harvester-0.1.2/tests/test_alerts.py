import unittest
from alerts import check_alert

class TestAlerts(unittest.TestCase):

    def test_alert_triggered(self):
        weather = {"temperature": 40}
        self.assertTrue(check_alert(weather, 35))

    def test_no_alert(self):
        weather = {"temperature": 20}
        self.assertFalse(check_alert(weather, 35))

    def test_alert_exact_threshold(self):
        weather = {"temperature": 35}
        self.assertTrue(check_alert(weather, 35))

if __name__ == "__main__":
    unittest.main()
