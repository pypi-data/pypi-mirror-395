import unittest
from pyonix_core.utils.identifiers import ISBN

class TestISBN(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(ISBN.clean("978-1-23-456789-0"), "9781234567890")
        self.assertEqual(ISBN.clean("978 1 23 456789 0"), "9781234567890")
        self.assertEqual(ISBN.clean("0-123-45678-9"), "0123456789")
        self.assertEqual(ISBN.clean("0-123-45678-X"), "012345678X")

    def test_validate_isbn13(self):
        self.assertTrue(ISBN.validate("978-0-306-40615-7"))
        self.assertFalse(ISBN.validate("978-0-306-40615-8")) # Wrong check digit

    def test_validate_isbn10(self):
        self.assertTrue(ISBN.validate("0-306-40615-2"))
        self.assertFalse(ISBN.validate("0-306-40615-1")) # Wrong check digit
        self.assertTrue(ISBN.validate("0-8044-2957-X")) # X check digit

    def test_to_13(self):
        # 0-306-40615-2 -> 978-0-306-40615-7
        self.assertEqual(ISBN.to_13("0-306-40615-2"), "9780306406157")
        
        with self.assertRaises(ValueError):
            ISBN.to_13("123") # Invalid length

        with self.assertRaises(ValueError):
            ISBN.to_13("0-306-40615-1") # Invalid checksum

if __name__ == '__main__':
    unittest.main()
