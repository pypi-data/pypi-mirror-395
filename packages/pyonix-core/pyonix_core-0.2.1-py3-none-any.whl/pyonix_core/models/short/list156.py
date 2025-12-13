from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List156(Enum):
    """
    Cited content type.

    Attributes:
        VALUE_01: Review The full text of a review in a third-party
            publication in any medium
        VALUE_02: Bestseller list
        VALUE_03: Media mention Other than a review
        VALUE_04: ‘One locality, one book’ program Inclusion in a
            program such as ‘Chicago Reads’, ‘Seattle Reads’, ‘Canada
            Reads’, ‘One Dublin, one book’
        VALUE_05: Curated list For example a ‘best books of the year’ or
            ‘25 books you should have read’ list, without regard to
            their bestseller status
        VALUE_06: Commentary / discussion For example a third party
            podcast episode, social media message, newsletter issue,
            other commentary (see also code 03 for very brief items)
        VALUE_07: Interview Interview, for example with a contributor,
            in a third-party publication in any medium
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
