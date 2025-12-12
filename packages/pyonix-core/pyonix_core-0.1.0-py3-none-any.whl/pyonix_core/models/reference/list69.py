from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List69(Enum):
    """
    Agent role.

    Attributes:
        VALUE_01: Publisher acts as own sales agent Normally omitted,
            but required in some countries to provide positive
            indication the publisher acts as its own sales agent (FR:
            auto-diffuseur) in a specified market. Only for use in ONIX
            3.0 or later
        VALUE_05: Exclusive sales agent Publisher’s exclusive sales
            agent in a specified territory
        VALUE_06: Non-exclusive sales agent Publisher’s non-exclusive
            sales agent in a specified territory
        VALUE_07: Local publisher Publisher for a specified territory
        VALUE_08: Sales agent Publisher’s sales agent in a specific
            territory. Use only where exclusive / non-exclusive status
            is not known. Prefer 05 or 06 as appropriate, where possible
    """

    VALUE_01 = "01"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
