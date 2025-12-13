from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List102(Enum):
    """
    Sales outlet identifier type.

    Attributes:
        VALUE_01: Proprietary sales outlet ID scheme Proprietary list of
            retail and other end-user sales outlet IDs. Note that a
            distinctive &lt;IDTypeName&gt; is required with proprietary
            identifiers
        VALUE_03: ONIX retail sales outlet ID code Use with ONIX retail
            and other end-user sales outlet IDs from List 139
        VALUE_04: Retail sales outlet GLN 13-digit GS1 global location
            number (formerly EAN location number). Only for use in ONIX
            3.0 or later
        VALUE_05: Retail sales outlet SAN 7-digit Book trade Standard
            Address Number (US, UK etc). Only for use in ONIX 3.0 or
            later
    """

    VALUE_01 = "01"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
