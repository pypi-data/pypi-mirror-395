from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List228(Enum):
    """
    Grant identifier type.

    Attributes:
        VALUE_01: Proprietary grant ID scheme Note that a distinctive
            &lt;IDTypeName&gt; is required with proprietary grant
            identifiers
        VALUE_06: DOI Digital Object Identifier (variable length and
            character set, beginning ‘10.’ and without https://doi.org/
            or the older http://dx.doi.org/)
    """

    VALUE_01 = "01"
    VALUE_06 = "06"
