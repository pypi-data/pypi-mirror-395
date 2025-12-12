from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List70(Enum):
    """
    Stock quantity code type.

    Attributes:
        VALUE_01: Proprietary stock quantity coding scheme Note that a
            distinctive &lt;StockQuantityCodeTypeName&gt; is required
            with proprietary coding schemes
        VALUE_02: APA stock quantity code Code scheme defined by the
            Australian Publishers Association. Deprecated
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
