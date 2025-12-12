import unittest
from unittest.mock import patch
from pyonix_core.utils.text import clean_html, to_markdown

class TestTextUtils(unittest.TestCase):
    def test_clean_html_basic(self):
        # Assuming bleach is installed or mocked
        raw = "<p>Hello <script>alert('xss')</script> <b>World</b></p>"
        cleaned = clean_html(raw)
        self.assertNotIn("<script>", cleaned)
        self.assertIn("<b>World</b>", cleaned)
        self.assertIn("<p>", cleaned)

    def test_clean_html_empty(self):
        self.assertEqual(clean_html(None), "")
        self.assertEqual(clean_html(""), "")

    def test_to_markdown_basic(self):
        # Assuming html2text is installed
        raw = "<h1>Title</h1><p>Para</p>"
        md = to_markdown(raw)
        self.assertIn("# Title", md)
        self.assertIn("Para", md)

    def test_to_markdown_empty(self):
        self.assertEqual(to_markdown(None), "")
        self.assertEqual(to_markdown(""), "")

if __name__ == '__main__':
    unittest.main()
