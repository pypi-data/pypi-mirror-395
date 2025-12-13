from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List31(Enum):
    """
    Audience range precision.

    Attributes:
        VALUE_01: Exact May only be used in Audience range precision
            (1), and when no Audience range precision (2) is present
        VALUE_03: From May only be used in Audience range precision (1)
        VALUE_04: To May be used in Audience range precision (1) when no
            Audience range precision (2) is present, or in Audience
            range precision (2) when Audience range precision (1) is
            code 03
    """

    VALUE_01 = "01"
    VALUE_03 = "03"
    VALUE_04 = "04"
