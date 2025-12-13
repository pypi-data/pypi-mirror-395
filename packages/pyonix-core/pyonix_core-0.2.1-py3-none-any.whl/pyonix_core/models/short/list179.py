from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List179(Enum):
    """
    Price code type.

    Attributes:
        VALUE_01: Proprietary price coding scheme A publisher or
            retailer’s proprietary price code list, which identifies
            particular codes with particular price points, price tiers
            or bands. Note that a distinctive &lt;PriceCodeTypeName&gt;
            is required with proprietary coding schemes
        VALUE_02: Finnish Pocket Book price code Price Code scheme for
            Finnish Pocket Books (Pokkareiden hintaryhmä). Price codes
            expressed as letters A–J in &lt;PriceCode&gt;
        VALUE_03: Finnish Miki Book price code Price Code scheme for
            Finnish Miki Books (Miki-kirjojen hintaryhmä). Price codes
            expressed as an integer 1–n in &lt;PriceCode&gt;
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
