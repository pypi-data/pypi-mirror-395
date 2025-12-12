try:
    import bleach
except ImportError:
    bleach = None

try:
    import html2text
except ImportError:
    html2text = None

ALLOWED_TAGS = ['b', 'i', 'em', 'strong', 'p', 'br', 'ul', 'li']
ALLOWED_ATTRS = {}  # No style attributes allowed

def clean_html(raw_html: str) -> str:
    """Removes script tags, iframes, and dangerous attributes."""
    if not raw_html: 
        return ""
    
    if bleach is None:
        # Fallback or warning if bleach is not installed?
        # For now, we'll just return the raw html or raise a warning.
        # Ideally, we should raise an ImportError if the user explicitly asked for cleaning 
        # but didn't install the dependencies. However, this function might be called implicitly.
        # Let's raise an ImportError to be safe.
        raise ImportError("Install 'pyonix-core[text]' to use html sanitization.")

    return bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)

def to_markdown(raw_html: str) -> str:
    """Converts HTML description to Markdown."""
    if not raw_html:
        return ""

    if html2text is None:
        raise ImportError("Install 'pyonix-core[text]' to use markdown conversion.")
    
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(raw_html)
