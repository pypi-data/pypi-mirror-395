from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List247(Enum):
    """
    Event occurrence date role.

    Attributes:
        VALUE_01: Date of occurrence Date and (with the default
            dateformat) time the event occurrence begins
        VALUE_02: Date of occurrence end Date and (with the default
            dateformat) time the event occurrence ends
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
