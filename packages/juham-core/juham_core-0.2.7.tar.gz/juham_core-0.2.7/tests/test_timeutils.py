import unittest
import time
import datetime
import pytz

from juham_core.timeutils import (
    quantize,
    epoc2utc,
    timestampstr,
    timestamp,
    timestamp_hour,
    timestamp_hour_local,
    is_time_between,
    is_hour_within_schedule,
    elapsed_seconds_in_interval,
    elapsed_seconds_in_hour,
    elapsed_seconds_in_day,
)

class TestTimeUtils(unittest.TestCase):

    def test_quantize(self):
        self.assertEqual(quantize(5, 12), 10)
        self.assertEqual(quantize(3600, 3661), 3600)
        self.assertEqual(quantize(1, 0.999), 0.0)
        self.assertEqual(quantize(1.5, 3.7), 3.0)

    def test_epoc2utc(self):
        ts = 0  # Epoch start
        self.assertEqual(epoc2utc(ts), "1970-01-01T00:00:00Z")
        ts = 1609459200  # 2021-01-01T00:00:00Z
        self.assertEqual(epoc2utc(ts), "2021-01-01T00:00:00Z")

    def test_timestampstr(self):
        ts = 1609459200  # 2021-01-01 00:00:00
        self.assertEqual(timestampstr(ts), "2021-01-01 00:00:00")

    def test_timestamp(self):
        now = timestamp()
        self.assertTrue(isinstance(now, float))
        self.assertAlmostEqual(now, time.time(), delta=2)

    def test_timestamp_hour(self):
        dt = datetime.datetime(2024, 1, 1, 14, 30)
        ts = dt.timestamp()
        self.assertEqual(timestamp_hour(ts), 14)

    def test_timestamp_hour_local(self):
        dt = datetime.datetime(2024, 1, 1, 12, 0, tzinfo=pytz.utc)
        ts = dt.timestamp()
        hour_est = timestamp_hour_local(ts, "US/Eastern")
        self.assertEqual(hour_est, 7)  # UTC-5
        hour_utc = timestamp_hour_local(ts, "UTC")
        self.assertEqual(hour_utc, 12)

    def test_is_time_between(self):
        start = time.time() - 10
        end = time.time() + 10
        self.assertTrue(is_time_between(start, end))
        self.assertFalse(is_time_between(start, start - 1, check_time=start - 0.5))
        # Test crossing midnight
        begin = 23*3600
        end = 1*3600
        self.assertTrue(is_time_between(begin, end, check_time=0))
        self.assertTrue(is_time_between(begin, end, check_time=23.5*3600))
        self.assertFalse(is_time_between(begin, end, check_time=12*3600))

    def test_is_hour_within_schedule(self):
        # normal range
        self.assertTrue(is_hour_within_schedule(10, 8, 12))
        self.assertFalse(is_hour_within_schedule(7, 8, 12))
        # crossing midnight
        self.assertTrue(is_hour_within_schedule(23, 22, 2))
        self.assertTrue(is_hour_within_schedule(1, 22, 2))
        self.assertFalse(is_hour_within_schedule(3, 22, 2))
        # null schedule
        self.assertTrue(is_hour_within_schedule(10, 8, 8))
        self.assertTrue(is_hour_within_schedule(0, 5, 5))

    def test_elapsed_seconds_in_interval(self):
        ts = 3605  # 1 hour and 5 seconds since epoch
        self.assertEqual(elapsed_seconds_in_interval(ts, 3600), 5)
        self.assertEqual(elapsed_seconds_in_interval(ts, 60), 5)
        self.assertEqual(elapsed_seconds_in_interval(ts, 86400), 3605)

    def test_elapsed_seconds_in_hour_day(self):
        ts = 3661  # 1 hour, 1 minute, 1 second
        self.assertEqual(elapsed_seconds_in_hour(ts), 61)  # 1 min 1 s
        self.assertEqual(elapsed_seconds_in_day(ts), 3661)

if __name__ == "__main__":
    unittest.main()
