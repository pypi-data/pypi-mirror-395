import unittest
from tests.test_parsing import TestParsing

# This file serves as a suite runner for regression tests.
# It imports the existing TestParsing class which covers the core functionality.
# We can add more regression scenarios here if needed.

class TestRegression(TestParsing):
    """
    Inherits from TestParsing to run all existing tests.
    We can add specific regression checks for new features interacting with old code here.
    """
    
    def test_facade_backward_compatibility(self):
        """
        Ensure that the ProductFacade still behaves as expected for basic properties
        even with the new mixins and helpers attached.
        """
        # We can reuse the logic from test_parse_short_tags but explicitly check
        # that accessing new properties doesn't crash on old data
        from pathlib import Path
        from pyonix_core.parsing.parser import parse_onix_stream
        from pyonix_core.facade.product import ProductFacade
        
        xml_path = Path(__file__).parent / "sample_short.xml"
        products = list(parse_onix_stream(xml_path))
        product = products[0]
        facade = ProductFacade(product)
        
        # Old properties
        self.assertEqual(facade.record_reference, "REF001")
        
        # New properties should be safe to access (might be None or empty, but no crash)
        self.assertIsNotNone(facade.helper)
        # description_html might be empty string if no text content
        self.assertIsInstance(facade.description_html, str) 
        
        # to_dict should work
        flat = facade.to_dict()
        self.assertIsInstance(flat, dict)
        self.assertEqual(flat['isbn13'], "9781234567890")

if __name__ == '__main__':
    unittest.main()
