from typing import Any, Dict, Union, Tuple, Optional

DEFAULT_FLAT_SCHEMA = {
    "isbn13": "get_isbn13",
    "title": "get_main_title",
    "author_primary": "get_primary_author",
    "publisher": "get_publisher_name",
    "pub_date": "get_publication_date",
    "price_usd": ("get_price", {"currency": "USD"}),
    "status": "get_publishing_status_code"
}

class ProductFlattener:
    def __init__(self, schema: Optional[Dict[str, Union[str, Tuple[str, Dict[str, Any]]]]] = None, join_char: str = "; "):
        self.schema = schema or DEFAULT_FLAT_SCHEMA
        self.join_char = join_char

    def flatten(self, product_facade) -> Dict[str, Any]:
        row = {}
        for col_name, method_def in self.schema.items():
            val = self._resolve(product_facade, method_def)
            row[col_name] = val
        return row

    def _resolve(self, obj: Any, method_def: Union[str, Tuple[str, Dict[str, Any]]]) -> Any:
        method_name = ""
        kwargs = {}

        if isinstance(method_def, tuple):
            method_name = method_def[0]
            kwargs = method_def[1]
        else:
            method_name = method_def
        
        if not hasattr(obj, method_name):
            return None
        
        attr = getattr(obj, method_name)
        
        if callable(attr):
            try:
                val = attr(**kwargs)
            except Exception:
                # If the method fails (e.g. missing data), return None
                return None
        else:
            val = attr

        if isinstance(val, list):
            return self.join_char.join(str(v) for v in val)
        
        return val
