from typing import Optional
from datetime import date

def format_isbn13(isbn: str) -> str:
    """
    Formats an ISBN-13 with hyphens (naive implementation).
    For correct formatting, use a library like `isbnlib`.
    """
    if not isbn:
        return ""
    clean_isbn = isbn.replace("-", "").replace(" ", "")
    if len(clean_isbn) != 13:
        return isbn
    
    # Naive formatting: 978-X-XXXX-XXXX-X
    return f"{clean_isbn[:3]}-{clean_isbn[3]}-{clean_isbn[4:8]}-{clean_isbn[8:12]}-{clean_isbn[12]}"

def parse_onix_date(date_str: str) -> Optional[date]:
    """
    Parses an ONIX date string (YYYYMMDD) into a python date object.
    """
    if not date_str:
        return None
    
    try:
        # Handle YYYYMMDD
        if len(date_str) == 8:
            return date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))
        # Handle YYYYMM
        elif len(date_str) == 6:
            return date(int(date_str[:4]), int(date_str[4:6]), 1)
        # Handle YYYY
        elif len(date_str) == 4:
            return date(int(date_str[:4]), 1, 1)
    except ValueError:
        pass
        
    return None
