from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List20(Enum):
    """
    Event role.

    Attributes:
        VALUE_01: Publication linked to conference For example an
            academic, professional or political conference
        VALUE_02: Complete proceedings of conference
        VALUE_03: Selected papers from conference
        VALUE_11: Publication linked to sporting event For example a
            competitive match, fixture series or championship
        VALUE_12: Programme or guide for sporting event
        VALUE_21: Publication linked to artistic event For example a
            theatrical or musical event or performance, a season of
            events or performances, or an exhibition of art
        VALUE_22: Programme or guide for artistic event
        VALUE_31: Publication linked to exposition For example a
            commercial exposition
        VALUE_32: Programme or guide for exposition
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_31 = "31"
    VALUE_32 = "32"
