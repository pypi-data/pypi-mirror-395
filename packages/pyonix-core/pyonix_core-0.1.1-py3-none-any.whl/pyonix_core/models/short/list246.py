from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List246(Enum):
    """
    Event status.

    Attributes:
        A: Announced
        C: Cancelled Abandoned after having previously been announced
    """

    A = "A"
    C = "C"
