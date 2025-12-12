from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List142(Enum):
    """
    Position on product.

    Attributes:
        VALUE_00: Unknown / unspecified Position unknown or unspecified
        VALUE_01: Cover 4 The back cover of a book (or book jacket) –
            the recommended position
        VALUE_02: Cover 3 The inside back cover of a book
        VALUE_03: Cover 2 The inside front cover of a book
        VALUE_04: Cover 1 The front cover of a book
        VALUE_05: On spine The spine of a book
        VALUE_06: On box Used only for boxed products
        VALUE_07: On tag Used only for products fitted with hanging tags
        VALUE_08: On bottom Not be used for books unless they are
            contained within outer packaging
        VALUE_09: On back Not be used for books unless they are
            contained within outer packaging
        VALUE_10: On outer sleeve / back Used only for products packaged
            in outer sleeves
        VALUE_11: On removable wrapping Used only for products packaged
            in shrink-wrap or other removable wrapping
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
