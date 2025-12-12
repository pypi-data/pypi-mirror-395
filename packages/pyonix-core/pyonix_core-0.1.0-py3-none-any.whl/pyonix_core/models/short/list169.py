from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List169(Enum):
    """
    Quantity unit.

    Attributes:
        VALUE_00: Units The quantity refers to a unit implied by the
            quantity type
        VALUE_07: Days
        VALUE_08: Weeks
        VALUE_09: Months
        VALUE_10: Years
        VALUE_20: Classes Multiple copies or units suitable for a class.
            A ‘class’ is a group of learners attending a specific course
            or lesson and generally taught as a group
    """

    VALUE_00 = "00"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_20 = "20"
