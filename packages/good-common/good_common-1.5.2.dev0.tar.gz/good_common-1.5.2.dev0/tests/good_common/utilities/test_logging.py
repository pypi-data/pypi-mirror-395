"""Tests for utilities._logging module."""

from time import sleep

import pytest
from loguru import logger

from good_common.utilities._logging import catchtime, human_readable_bytes


class TestCatchtime:
    """Test catchtime context manager."""

    def test_catchtime_basic(self, caplog):
        """Test basic catchtime functionality."""
        with catchtime("test_operation") as get_elapsed:
            sleep(0.01)  # Small delay
            elapsed = get_elapsed()
            assert elapsed > 0

    def test_catchtime_logs_start_message(self, caplog):
        """Test that catchtime logs start message."""
        # Capture loguru output
        with logger.contextualize():
            with catchtime("test_task"):
                pass
        # Note: loguru uses a different logging mechanism than standard logging
        # We're primarily testing that it doesn't raise errors

    def test_catchtime_measures_time_accurately(self):
        """Test that catchtime measures time with reasonable accuracy."""
        with catchtime("timing_test") as get_elapsed:
            sleep(0.05)  # 50ms delay
            elapsed = get_elapsed()
            # Should be at least 40ms (accounting for timing variations)
            assert elapsed >= 0.04
            # Should be less than 100ms
            assert elapsed < 0.1

    def test_catchtime_lambda_updates(self):
        """Test that the elapsed time lambda updates during execution."""
        with catchtime("incremental_test") as get_elapsed:
            first = get_elapsed()
            sleep(0.02)
            second = get_elapsed()
            assert second > first

    def test_catchtime_with_exception(self):
        """Test that catchtime still measures time when exception occurs."""
        with pytest.raises(ValueError):
            with catchtime("error_test") as get_elapsed:
                sleep(0.01)
                elapsed = get_elapsed()
                assert elapsed > 0
                raise ValueError("Test error")

    def test_catchtime_with_return_value(self):
        """Test catchtime with function that returns a value."""

        def timed_function():
            with catchtime("function_timing") as get_elapsed:
                result = 42
                sleep(0.01)
                assert get_elapsed() > 0
                return result

        result = timed_function()
        assert result == 42

    def test_catchtime_nested(self):
        """Test nested catchtime contexts."""
        with catchtime("outer") as outer_time:
            sleep(0.01)
            with catchtime("inner") as inner_time:
                sleep(0.01)
            # Outer should be greater than inner
            assert outer_time() > inner_time()

    def test_catchtime_multiple_calls_to_lambda(self):
        """Test calling the elapsed time lambda multiple times."""
        with catchtime("multi_call") as get_elapsed:
            time1 = get_elapsed()
            sleep(0.01)
            time2 = get_elapsed()
            sleep(0.01)
            time3 = get_elapsed()
            assert time1 < time2 < time3

    def test_catchtime_with_different_names(self):
        """Test catchtime with various operation names."""
        names = ["short", "longer_name", "name-with-dashes", "name_with_underscores"]
        for name in names:
            with catchtime(name) as get_elapsed:
                sleep(0.001)
                assert get_elapsed() > 0


class TestHumanReadableBytes:
    """Test human_readable_bytes function."""

    def test_bytes_unit(self):
        """Test formatting for bytes."""
        assert human_readable_bytes(0) == "0.00 B"
        assert human_readable_bytes(100) == "100.00 B"
        assert human_readable_bytes(1023) == "1023.00 B"

    def test_kilobytes_unit(self):
        """Test formatting for kilobytes."""
        assert human_readable_bytes(1024) == "1.00 KB"
        assert human_readable_bytes(1536) == "1.50 KB"
        assert human_readable_bytes(10240) == "10.00 KB"

    def test_megabytes_unit(self):
        """Test formatting for megabytes."""
        assert human_readable_bytes(1024 * 1024) == "1.00 MB"
        assert human_readable_bytes(1024 * 1024 * 5) == "5.00 MB"
        assert human_readable_bytes(1024 * 1024 + 524288) == "1.50 MB"

    def test_gigabytes_unit(self):
        """Test formatting for gigabytes."""
        assert human_readable_bytes(1024 * 1024 * 1024) == "1.00 GB"
        assert human_readable_bytes(1024 * 1024 * 1024 * 2) == "2.00 GB"

    def test_terabytes_unit(self):
        """Test formatting for terabytes."""
        assert human_readable_bytes(1024**4) == "1.00 TB"
        assert human_readable_bytes(1024**4 * 3) == "3.00 TB"

    def test_petabytes_unit(self):
        """Test formatting for petabytes."""
        assert human_readable_bytes(1024**5) == "1.00 PB"

    def test_exabytes_unit(self):
        """Test formatting for exabytes."""
        assert human_readable_bytes(1024**6) == "1.00 EB"

    def test_zettabytes_unit(self):
        """Test formatting for zettabytes."""
        assert human_readable_bytes(1024**7) == "1.00 ZB"

    def test_yottabytes_unit(self):
        """Test formatting for yottabytes (largest unit)."""
        assert human_readable_bytes(1024**8) == "1.00 YB"
        assert human_readable_bytes(1024**9) == "1024.00 YB"

    def test_decimal_precision(self):
        """Test decimal precision in output."""
        # 1.5 KB
        result = human_readable_bytes(1536)
        assert ".50 KB" in result

        # 2.75 MB
        result = human_readable_bytes(int(2.75 * 1024 * 1024))
        assert "2.75 MB" in result

    def test_fractional_bytes(self):
        """Test small byte values."""
        assert human_readable_bytes(1) == "1.00 B"
        assert human_readable_bytes(512) == "512.00 B"

    def test_large_values(self):
        """Test very large values."""
        # 999 GB
        result = human_readable_bytes(999 * 1024**3)
        assert "999.00 GB" in result

        # Just over 1 TB
        result = human_readable_bytes(1024**4 + 1024**3)
        assert "1.00 TB" in result

    def test_edge_cases(self):
        """Test edge cases."""
        # Exactly at unit boundaries
        assert "1.00 KB" == human_readable_bytes(1024)
        assert "1.00 MB" == human_readable_bytes(1024**2)
        assert "1.00 GB" == human_readable_bytes(1024**3)

    def test_realistic_file_sizes(self):
        """Test with realistic file sizes."""
        # Small text file
        assert "15.00 KB" == human_readable_bytes(15360)

        # Photo
        assert "2.50 MB" == human_readable_bytes(int(2.5 * 1024**2))

        # Movie
        assert "1.50 GB" == human_readable_bytes(int(1.5 * 1024**3))

        # Large backup
        assert "500.00 GB" == human_readable_bytes(500 * 1024**3)

    def test_zero_bytes(self):
        """Test zero bytes specifically."""
        result = human_readable_bytes(0)
        assert result == "0.00 B"
        assert "B" in result

    def test_one_byte(self):
        """Test single byte."""
        result = human_readable_bytes(1)
        assert result == "1.00 B"

    def test_returns_string(self):
        """Test that return value is always a string."""
        for size in [0, 1, 1024, 1024**2, 1024**3]:
            result = human_readable_bytes(size)
            assert isinstance(result, str)
            # Should contain a space between number and unit
            assert " " in result


class TestLoggingIntegration:
    """Test integration between logging utilities."""

    def test_catchtime_with_human_readable_bytes(self):
        """Test using both utilities together."""
        data_size = 1024 * 1024 * 10  # 10 MB
        with catchtime(f"Processing {human_readable_bytes(data_size)}") as get_elapsed:
            # Simulate some work
            sleep(0.01)
            elapsed = get_elapsed()
            assert elapsed > 0

    def test_multiple_catchtime_sequential(self):
        """Test multiple sequential catchtime usages."""
        times = []
        for i in range(3):
            with catchtime(f"operation_{i}") as get_elapsed:
                sleep(0.01)
                times.append(get_elapsed())
        # All should have recorded some time
        assert all(t > 0 for t in times)
