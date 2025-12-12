from lxml import etree
from pathlib import Path
from typing import Union, List

class OnixValidator:
    def __init__(self, xsd_path: Union[str, Path]):
        self.xsd_path = str(xsd_path)
        try:
            xml_schema_doc = etree.parse(self.xsd_path)
            self.schema = etree.XMLSchema(xml_schema_doc)
        except Exception as e:
            raise ValueError(f"Invalid XSD file: {e}")

    def validate(self, xml_path: Union[str, Path]) -> bool:
        """
        Validates an XML file against the loaded XSD.
        """
        try:
            doc = etree.parse(str(xml_path))
            return self.schema.validate(doc)
        except Exception:
            return False
        
    def get_errors(self, xml_path: Union[str, Path]) -> List[str]:
        """
        Returns a list of validation errors.
        """
        try:
            doc = etree.parse(str(xml_path))
            if not self.schema.validate(doc):
                return [str(error) for error in self.schema.error_log]
            return []
        except Exception as e:
            return [f"Parsing error: {e}"]
