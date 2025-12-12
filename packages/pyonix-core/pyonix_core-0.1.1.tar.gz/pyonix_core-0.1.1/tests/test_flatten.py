import unittest
from unittest.mock import MagicMock
from pyonix_core.utils.flatten import ProductFlattener

class TestProductFlattener(unittest.TestCase):
    def test_flatten_default_schema(self):
        # Mock a ProductFacade
        mock_facade = MagicMock()
        mock_facade.get_isbn13.return_value = "9781234567890"
        mock_facade.get_main_title.return_value = "Test Title"
        mock_facade.get_primary_author.return_value = "John Doe"
        mock_facade.get_publisher_name.return_value = "Test Pub"
        mock_facade.get_publication_date.return_value = "20230101"
        mock_facade.get_price.return_value = 19.99
        mock_facade.get_publishing_status_code.return_value = "04"

        flattener = ProductFlattener()
        result = flattener.flatten(mock_facade)

        expected = {
            "isbn13": "9781234567890",
            "title": "Test Title",
            "author_primary": "John Doe",
            "publisher": "Test Pub",
            "pub_date": "20230101",
            "price_usd": 19.99,
            "status": "04"
        }
        self.assertEqual(result, expected)

    def test_flatten_custom_schema(self):
        schema = {
            "ID": "record_reference",
            "Title": "title"
        }
        flattener = ProductFlattener(schema=schema)
        
        mock_facade = MagicMock()
        mock_facade.record_reference = "REF001"
        mock_facade.title = "My Book"
        
        result = flattener.flatten(mock_facade)
        
        self.assertEqual(result, {"ID": "REF001", "Title": "My Book"})

    def test_flatten_list_handling(self):
        schema = {"authors": "contributors"}
        flattener = ProductFlattener(schema=schema, join_char="|")
        
        mock_facade = MagicMock()
        mock_facade.contributors = ["Author A", "Author B"]
        
        result = flattener.flatten(mock_facade)
        self.assertEqual(result, {"authors": "Author A|Author B"})

    def test_flatten_missing_method(self):
        schema = {"missing": "non_existent_method"}
        flattener = ProductFlattener(schema=schema)
        mock_facade = MagicMock()
        del mock_facade.non_existent_method # Ensure it doesn't exist
        
        result = flattener.flatten(mock_facade)
        self.assertIsNone(result["missing"])

if __name__ == '__main__':
    unittest.main()
