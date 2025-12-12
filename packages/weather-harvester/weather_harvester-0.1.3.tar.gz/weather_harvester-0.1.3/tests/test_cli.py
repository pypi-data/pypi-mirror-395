import unittest
from cli import get_args

class TestCLI(unittest.TestCase):

    def test_single_city(self):
        args = get_args(["-c", "Delhi"])
        self.assertEqual(args.cities, ["Delhi"])

    def test_multiple_cities(self):
        args = get_args(["-c", "Delhi", "-c", "Pune"])
        self.assertEqual(args.cities, ["Delhi", "Pune"])

    def test_alert_temp(self):
        args = get_args(["--alert-temp", "30"])
        self.assertEqual(args.alert_temp, 30)

    def test_log_level(self):
        args = get_args(["--log-level", "DEBUG"])
        self.assertEqual(args.log_level, "DEBUG")

if __name__ == "__main__":
    unittest.main()
