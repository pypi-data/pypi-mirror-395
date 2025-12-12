from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List57(Enum):
    """
    Unpriced item type.

    Attributes:
        VALUE_01: Free of charge
        VALUE_02: Price to be announced
        VALUE_03: Not sold separately Not sold separately at retail
        VALUE_04: Contact supplier May be used for books that do not
            carry a recommended retail price; when goods can only be
            ordered ‘in person’ from a sales representative; when an
            ONIX file is ‘broadcast’ rather than sent one-to-one to a
            single trading partner; or for digital products offered on
            subscription or with pricing which is too complex to specify
            in ONIX
        VALUE_05: Not sold as set When a collection that is not sold as
            a set nevertheless has its own ONIX record
        VALUE_06: Revenue share Unpriced, but available via a pre-
            determined revenue share agreement
        VALUE_07: Calculated from contents Price calculated as sum of
            individual prices of components listed as Product parts.
            Only for use in ONIX 3.0 or later
        VALUE_08: Supplier does not supply The supplier does not
            operate, or does not offer this product, in this part of the
            market as indicated by &lt;Territory&gt;. Use when other
            prices apply in different parts of the market (eg when the
            market is global, but the particular supplier does not
            operate outside its domestic territory). Use code 04 when
            the supplier does supply but has not set a price for part of
            the market. Only for use in ONIX 3.0 or later
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
