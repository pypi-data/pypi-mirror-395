import unittest
import logging
from unittest.mock import MagicMock
from pyonix_core.integration.adapter import OnyxSourceAdapter

# Enable debug logging for adapter tests to help trace hangs/crashes
logging.basicConfig(level=logging.DEBUG)

class TestAdapter(unittest.TestCase):
    def test_extract_uses_stream_wrapper(self):
        # Mock client and method
        client = MagicMock()
        def list_method(page):
            class R:
                def __init__(self, items, has_next):
                    self.items = items
                    self.has_next = has_next
            if page == 1:
                return R(["a"], True)
            if page == 2:
                return R(["b"], False)
            return R([], False)

        adapter = OnyxSourceAdapter(client, list_method)
        gen = adapter.extract()
        self.assertEqual(list(gen), ["a","b"])

    def test_cleanup_closes_client(self):
        client = MagicMock()
        adapter = OnyxSourceAdapter(client, lambda page: [])
        adapter.cleanup()
        # Adapter.cleanup should call client's close() if available
        client.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
