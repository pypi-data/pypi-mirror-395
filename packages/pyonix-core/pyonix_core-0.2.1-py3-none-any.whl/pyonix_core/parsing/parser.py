from contextlib import contextmanager
from typing import Iterator, Union, BinaryIO, Type
from pathlib import Path
from lxml import etree
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext

from pyonix_core.models.short.product import Product as ProductShort
from pyonix_core.models.reference.product import Product as ProductRef
from pyonix_core.parsing.security import create_secure_parser

# Namespaces
NS_SHORT = "http://ns.editeur.org/onix/3.0/short"
NS_REF = "http://ns.editeur.org/onix/3.0/reference"

@contextmanager
def file_input(source: Union[str, Path, BinaryIO]) -> Iterator[BinaryIO]:
    if isinstance(source, (str, Path)):
        with open(source, "rb") as f:
            yield f
    else:
        yield source

def parse_onix_stream(source: Union[str, Path, BinaryIO]) -> Iterator[Union[ProductShort, ProductRef]]:
    """
    Parses an ONIX 3.0 stream and yields Product objects.
    Automatically detects Reference vs Short tags based on namespace.
    """
    context = XmlContext()
    parser = XmlParser(context=context)
    
    secure_parser_config = create_secure_parser()
    
    # We need to detect the namespace first.
    # We can peek at the start of the file or just handle both in iterparse.
    
    target_class: Type = ProductShort # Default
    
    with file_input(source) as f:
        # We listen for 'start-ns' to detect namespace, and 'end' for Product
        # iterparse accepts XMLParser arguments directly
        events = etree.iterparse(
            f, 
            events=("start-ns", "end"), 
            tag=["{*}Product", "{*}product"],
            resolve_entities=False,  # Block XXE
            no_network=True,         # Block remote fetching
            load_dtd=False,          # Block DTD processing
            huge_tree=True,          # Allow large files
            remove_comments=True,
            remove_pis=True,
            collect_ids=False
        )
        
        for event, element in events:
            if event == "start-ns":
                prefix, url = element
                if url == NS_REF:
                    target_class = ProductRef
                elif url == NS_SHORT:
                    target_class = ProductShort
                continue
            
            if event == "end":
                # Check if it is a Product element
                # Localname should be 'Product' (Ref) or 'product' (Short)
                localname = etree.QName(element).localname
                if localname.lower() == "product":
                    try:
                        obj = parser.parse(element, target_class)
                        yield obj
                    finally:
                        element.clear()
                        # Clear ancestors to free memory
                        # We need to be careful not to clear the root element too early if we need it,
                        # but for streaming products, we usually want to clear everything processed.
                        while element.getprevious() is not None:
                            del element.getparent()[0]
