import time
import unittest
from unittest.mock import patch

from hyperpod_elastic_agent.util import retry


class TestRetryDecorator(unittest.TestCase):

    def test_retry_success_first_attempt(self):
        """Test retry decorator when function succeeds on first attempt"""
        @retry(exceptions=(ValueError,), max_retries=3, delay=0.1)
        def successful_function():
            return "success"
        
        result = successful_function()
        self.assertEqual(result, "success")

    def test_retry_success_after_failures(self):
        """Test retry decorator when function succeeds after some failures"""
        call_count = 0
        
        @retry(exceptions=(ValueError,), max_retries=3, delay=0.1)
        def function_with_retries():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"
        
        result = function_with_retries()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)

    def test_retry_max_retries_exceeded(self):
        """Test retry decorator when max retries are exceeded"""
        @retry(exceptions=(ValueError,), max_retries=2, delay=0.1)
        def always_failing_function():
            raise ValueError("Always fails")
        
        with self.assertRaises(ValueError):
            always_failing_function()

    def test_retry_with_backoff(self):
        """Test retry decorator with exponential backoff"""
        call_times = []
        
        @retry(exceptions=(ValueError,), max_retries=3, delay=0.1, backoff=2)
        def function_with_backoff():
            call_times.append(time.time())
            raise ValueError("Always fails")
        
        with self.assertRaises(ValueError):
            function_with_backoff()
        
        # Should have 3 attempts (initial + 2 retries)
        self.assertEqual(len(call_times), 3)

    def test_retry_different_exception_not_caught(self):
        """Test retry decorator doesn't catch exceptions not in the list"""
        @retry(exceptions=(ValueError,), max_retries=3, delay=0.1)
        def function_with_different_exception():
            raise RuntimeError("Different exception")
        
        with self.assertRaises(RuntimeError):
            function_with_different_exception()

    @patch('time.sleep')
    def test_retry_sleep_called(self, mock_sleep):
        """Test that sleep is called between retries"""
        call_count = 0
        
        @retry(exceptions=(ValueError,), max_retries=3, delay=0.5, backoff=2)
        def function_with_retries():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"
        
        result = function_with_retries()
        self.assertEqual(result, "success")
        
        # Should have called sleep twice (between 3 attempts)
        self.assertEqual(mock_sleep.call_count, 2)
        # Check exponential backoff: first sleep(0.5), then sleep(1.0)
        mock_sleep.assert_any_call(0.5)
        mock_sleep.assert_any_call(1.0)


if __name__ == '__main__':
    unittest.main()