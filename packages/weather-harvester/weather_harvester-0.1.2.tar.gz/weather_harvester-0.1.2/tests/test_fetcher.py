import unittest
from unittest.mock import patch, MagicMock
from fetcher import fetch_weather

class TestFetcher(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_fetch_weather_success(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.read.return_value = b'''
        {
            "current_weather": {
                "temperature": 25.5,
                "windspeed": 6.4,
                "winddirection": 120,
                "weathercode": 1
            }
        }
        '''
        mock_urlopen.return_value.__enter__.return_value = fake_response

        data = fetch_weather(28.6, 77.2)
        self.assertIn("temperature", data)
        self.assertEqual(data["temperature"], 25.5)

    @patch("urllib.request.urlopen")
    def test_fetch_weather_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Network error")

        data = fetch_weather(28.6, 77.2)
        self.assertIsNone(data)

if __name__ == "__main__":
    unittest.main()
