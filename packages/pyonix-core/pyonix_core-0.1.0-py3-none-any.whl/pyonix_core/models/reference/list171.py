from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List171(Enum):
    """
    Tax type.

    Attributes:
        VALUE_01: VAT (Value-added tax) TVA, IVA, MwSt, GST etc, levied
            incrementally at all parts of the supply chain
        VALUE_02: GST (Sales tax) General sales tax, levied on retail
            sales
        VALUE_03: ECO ‘Green’ or eco-tax, levied to encourage
            responsible production or disposal, used only where this is
            identified separately from value-added or sales taxes
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
