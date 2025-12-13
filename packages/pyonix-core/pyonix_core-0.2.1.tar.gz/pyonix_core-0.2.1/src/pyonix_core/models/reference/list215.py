from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List215(Enum):
    """
    Proximity.

    Attributes:
        VALUE_01: Less than
        VALUE_02: Not more than
        VALUE_03: Exactly The supplier’s true figure, or at least a best
            estimate expected to be within 10% of the true figure (ie a
            quoted figure of 100 could in fact be anything between 91
            and 111)
        VALUE_04: Approximately Generally interpreted as within 25% of
            the true figure (ie a quoted figure of 100 could in fact be
            anything between 80 and 133). The supplier may introduce a
            deliberate approximation to reduce the commercial
            sensitivity of the figure
        VALUE_05: About Generally interpreted as within a factor of two
            of the true figure (ie a quoted figure of 100 could in fact
            be anything between 50 and 200). The supplier may introduce
            a deliberate approximation to reduce the commercial
            sensitivity of the figure
        VALUE_06: Not less than
        VALUE_07: More than
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
