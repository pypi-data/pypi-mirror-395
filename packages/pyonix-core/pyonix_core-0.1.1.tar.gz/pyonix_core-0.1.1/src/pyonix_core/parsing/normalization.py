import pkgutil
from lxml import etree
from typing import BinaryIO, Optional
import io

class TagNormalizer:
    def __init__(self):
        # Load XSLT once upon instantiation to save overhead
        xslt_content = pkgutil.get_data("pyonix_core", "assets/ONIX3_ShortToReference_3.0.xslt")
        if xslt_content is None:
            raise FileNotFoundError("Could not find assets/ONIX3_ShortToReference_3.0.xslt")
        self.transform = etree.XSLT(etree.XML(xslt_content))

    def normalize_stream(self, input_source: BinaryIO) -> BinaryIO:
        """
        Takes a file-like object containing Short Tag ONIX.
        Returns a temporary file-like object containing Reference Tag ONIX.
        """
        # Parse the input stream
        # Note: For very large files, this loads the whole tree into memory.
        # Future optimization: Use a streaming approach or SAX filter.
        try:
            tree = etree.parse(input_source)
            result_tree = self.transform(tree)
            
            # Serialize the result to a bytes buffer
            output_buffer = io.BytesIO()
            result_tree.write(output_buffer, encoding='utf-8', xml_declaration=True)
            output_buffer.seek(0)
            return output_buffer
        except Exception as e:
            # In case of error, we might want to log it or re-raise
            raise RuntimeError(f"Failed to normalize ONIX stream: {e}") from e
