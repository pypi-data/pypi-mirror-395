from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List46(Enum):
    """
    Sales rights type.

    Attributes:
        VALUE_00: Sales rights unknown or unstated for any reason May
            only be used with the &lt;ROWSalesRightsType&gt; element
        VALUE_01: For sale, based on publisher’s exclusive publishing
            rights in the specified territory
        VALUE_02: For sale, based on publisher’s non-exclusive
            publishing rights in the specified territory It is possible
            that a different publisher offers the same content under
            another ISBN
        VALUE_03: Not for sale in the specified territory (reason
            unspecified) Publisher may or may not hold publishing rights
            – use codes 04–06 instead to provide greater detail
        VALUE_04: Not for sale in the specified territory (but publisher
            holds exclusive publishing rights in that territory)
        VALUE_05: Not for sale in the specified territory (but publisher
            holds non-exclusive publishing rights in that territory)
        VALUE_06: Not for sale in the specified territory (because
            publisher does not hold publishing rights in that territory)
        VALUE_07: For sale with exclusive rights in the specified
            countries or territories (sales restriction applies) Only
            for use with ONIX 3.0. Deprecated
        VALUE_08: For sale with non-exclusive rights in the specified
            countries or territories (sales restriction applies) Only
            for use with ONIX 3.0. Deprecated
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
