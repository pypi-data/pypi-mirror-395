from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List60(Enum):
    """
    Unit of pricing.

    Attributes:
        VALUE_00: Per copy of whole product Default. Note where the
            product is a pack of multiple copies, the price is per
            multi-item product, not per individual copy within the pack
        VALUE_01: Per page for printed loose-leaf content only
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
