import unittest
from unittest.mock import MagicMock
from pyonix_core.integration.stream_wrapper import OnyxStreamWrapper

class FakeResp:
    def __init__(self, items=None, has_next=False, next_token=None):
        self.items = items or []
        self.has_next = has_next
        self.next_page_token = next_token

class TestStreamWrapper(unittest.TestCase):
    def test_basic_pagination_by_page(self):
        # function that returns FakeResp with 2 pages
        def func(page):
            if page == 1:
                return FakeResp(items=[1,2], has_next=True)
            elif page == 2:
                return FakeResp(items=[3], has_next=False)
            return FakeResp(items=[])

        wrapper = OnyxStreamWrapper(func, page_param='page')
        items = list(wrapper)
        self.assertEqual(items, [1,2,3])

    def test_empty_response_stops(self):
        def func(page):
            return FakeResp(items=[], has_next=False)
        wrapper = OnyxStreamWrapper(func)
        self.assertEqual(list(wrapper), [])

    def test_response_as_iterable(self):
        def func(page):
            return [10,11]
        wrapper = OnyxStreamWrapper(func)
        self.assertEqual(list(wrapper), [10,11])

    def test_max_items_cap(self):
        # Simulate pages that would be large; ensure max_items limits total yields
        def func(page):
            # Each page returns 1000 items for the sake of the test
            return list(range((page - 1) * 1000, page * 1000))

        # Cap at 1500 total items -- should stop after 1500 yields
        wrapper = OnyxStreamWrapper(func, max_items=1500, page_param='page')
        # Consume wrapper and ensure we got exactly 1500 items
        items = list(wrapper)
        self.assertEqual(len(items), 1500)
        # Basic sanity on first/last values
        self.assertEqual(items[0], 0)
        self.assertEqual(items[-1], 1499)

if __name__ == '__main__':
    unittest.main()
