from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List229(Enum):
    """
    Gender – based on ISO 5218.

    Attributes:
        U: Unknown or unspecified Provides positive indication that the
            gender is not known or is not specified by the sender for
            any reason
        F: Female
        M: Male
    """

    U = "u"
    F = "f"
    M = "m"
