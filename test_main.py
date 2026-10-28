"""Simple tests for the sensor sanitization function."""
import unittest
from main import clean_sensor_readings


class CleanSensorReadingsTests(unittest.TestCase):
    def test_converts_filters_and_clips(self):
        self.assertEqual(
            clean_sensor_readings([25, "40.5", None, -10, "abc", 650, 100]),
            [25.0, 40.5, 500.0, 100.0],
        )

    def test_empty_list(self):
        self.assertEqual(clean_sensor_readings([]), [])

    def test_all_invalid(self):
        self.assertEqual(clean_sensor_readings([None, -1, "bad"]), [])


if __name__ == "__main__":
    unittest.main()
