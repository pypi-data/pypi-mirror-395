import unittest
from unittest.mock import MagicMock
from pyonix_core.facade.assets import AssetHelper

class TestAssetHelper(unittest.TestCase):
    def test_get_cover_image_none(self):
        mock_product = MagicMock()
        mock_product.collateral_detail = None
        helper = AssetHelper(mock_product)
        self.assertIsNone(helper.get_cover_image())

    def test_get_cover_image_found(self):
        # Construct a mock structure that mimics the generated classes
        mock_product = MagicMock()
        
        # ResourceContent
        res_content = MagicMock()
        # Mocking the enum value or object
        res_content.resource_content_type = [MagicMock(value='01')] 
        
        # ResourceVersion
        res_version = MagicMock()
        link = MagicMock()
        link.value = "http://example.com/cover.jpg"
        res_version.resource_link = [link]
        
        res_content.resource_version = [res_version]
        
        mock_product.collateral_detail.supporting_resource = [res_content]
        
        helper = AssetHelper(mock_product)
        self.assertEqual(helper.get_cover_image(), "http://example.com/cover.jpg")

    def test_get_cover_image_wrong_type(self):
        mock_product = MagicMock()
        res_content = MagicMock()
        # Type 04 is Table of Contents, not Cover
        res_content.resource_content_type = [MagicMock(value='04')] 
        
        res_version = MagicMock()
        link = MagicMock()
        link.value = "http://example.com/toc.pdf"
        res_version.resource_link = [link]
        
        res_content.resource_version = [res_version]
        
        mock_product.collateral_detail.supporting_resource = [res_content]
        
        helper = AssetHelper(mock_product)
        self.assertIsNone(helper.get_cover_image())

if __name__ == '__main__':
    unittest.main()
