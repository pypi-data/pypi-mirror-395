from lxml import etree

def create_secure_parser() -> etree.XMLParser:
    """
    Creates a secure XML parser configuration to prevent XXE and other attacks.
    
    Returns:
        etree.XMLParser: A configured lxml XMLParser.
    """
    return etree.XMLParser(
        resolve_entities=False,  # Block XXE
        no_network=True,         # Block remote fetching
        load_dtd=False,          # Block DTD processing
        huge_tree=True,          # Allow large files (managed via iterparse)
        remove_comments=True,
        remove_pis=True,
        collect_ids=False,
    )
