from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List170(Enum):
    """
    Discount type.

    Attributes:
        VALUE_01: Rising discount Discount applied to all units in a
            qualifying order. The default if no &lt;DiscountType&gt; is
            specified
        VALUE_02: Rising discount (cumulative) Additional discount may
            be applied retrospectively, based on number of units ordered
            over a specific period
        VALUE_03: Progressive discount Discount applied to marginal
            units in a qualifying order
        VALUE_04: Progressive discount (cumulative) Previous orders
            within a specific time period are counted when calculating a
            progressive discount
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
