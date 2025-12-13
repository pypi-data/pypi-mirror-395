import unittest
from unittest.mock import MagicMock
import time
from pyonix_core.integration.resilience import with_onyx_retries

class CustomTransientError(Exception):
    pass

class CustomAuthError(Exception):
    pass

class TestResilience(unittest.TestCase):
    def test_retries_and_backoff(self):
        calls = []
        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise CustomTransientError("transient")
            return "ok"

        wrapped = with_onyx_retries(exceptions=(CustomTransientError,), max_attempts=4, initial_delay=0.01, backoff_factor=1.0)(flaky)
        result = wrapped()
        self.assertEqual(result, "ok")
        self.assertEqual(len(calls), 3)

    def test_fail_fast_on_auth(self):
        def bad():
            raise CustomAuthError("auth")
        wrapped = with_onyx_retries(exceptions=(CustomTransientError,), fail_fast_exceptions=(CustomAuthError,))(bad)
        with self.assertRaises(CustomAuthError):
            wrapped()

if __name__ == '__main__':
    unittest.main()
