import unittest
import io
from lxml import etree
from pyonix_core.parsing.normalization import TagNormalizer

class TestTagNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = TagNormalizer()

    def test_normalize_stream_basic(self):
        # Our dummy XSLT maps <product> to <Product>
        input_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<ONIXMessage release="3.0">
    <product>
        <RecordReference>REF123</RecordReference>
    </product>
</ONIXMessage>
"""
        input_stream = io.BytesIO(input_xml)
        
        output_stream = self.normalizer.normalize_stream(input_stream)
        output_xml = output_stream.read()
        
        # Parse output to verify transformation
        tree = etree.fromstring(output_xml)
        
        # Check for namespace which XSLT adds
        ns = {'onix': 'http://ns.editeur.org/onix/3.0/reference'}
        
        # The dummy XSLT transforms <product> to <Product> in the reference namespace
        products = tree.xpath('//onix:Product', namespaces=ns)
        self.assertEqual(len(products), 1)
        
    def test_normalize_stream_mixed_content(self):
        # Test that other content is preserved (Identity transform in XSLT)
        input_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<ONIXMessage>
    <Header>
        <Sender>Test</Sender>
    </Header>
    <product>
        <id>1</id>
    </product>
</ONIXMessage>
"""
        input_stream = io.BytesIO(input_xml)
        output_stream = self.normalizer.normalize_stream(input_stream)
        output_xml = output_stream.read()
        
        tree = etree.fromstring(output_xml)
        # Header should still be there
        self.assertTrue(tree.xpath('//Header'))
        # Sender should be there
        self.assertEqual(tree.xpath('//Sender')[0].text, 'Test')

if __name__ == '__main__':
    unittest.main()
