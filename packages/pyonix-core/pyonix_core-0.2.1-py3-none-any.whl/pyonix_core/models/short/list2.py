from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List2(Enum):
    """
    Product composition.

    Attributes:
        VALUE_00: Single-component retail product
        VALUE_01: Single-component, not available separately Used only
            when an ONIX record is required for a component-as-an-item,
            even though it is not currently available as such
        VALUE_10: Multiple-component retail product Multiple-component
            product retailed as a whole
        VALUE_11: Multiple-item collection, retailed as separate parts
            Used only when an ONIX record is required for a collection-
            as-a-whole, even though it is not currently retailed as such
        VALUE_20: Trade-only product Product available to the book
            trade, but not for retail sale, and not carrying retail
            items, eg empty dumpbin, empty counterpack, promotional
            material
        VALUE_30: Multiple-item trade-only pack Product available to the
            book trade, but not for general retail sale as a whole. It
            carries multiple components for retailing as separate items,
            eg shrink-wrapped trade pack, filled dumpbin, filled
            counterpack
        VALUE_31: Multiple-item pack Carrying multiple components,
            primarily for retailing as separate items. The pack may be
            split and retailed as separate items OR retailed as a single
            item. Use instead of Multiple-item trade-only pack (code 30)
            if the data provider specifically wishes to make explicit
            that the pack may optionally be retailed as a whole
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_20 = "20"
    VALUE_30 = "30"
    VALUE_31 = "31"
