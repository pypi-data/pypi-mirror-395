from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List173(Enum):
    """
    Price date role.

    Attributes:
        VALUE_14: From date Date on which a price becomes effective
        VALUE_15: Until date Date on which a price ceases to be
            effective
        VALUE_24: From… until date Combines From date and Until date to
            define a period (both dates are inclusive). Use for example
            with dateformat 06
    """

    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_24 = "24"
