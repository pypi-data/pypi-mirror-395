from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List241(Enum):
    """
    AV Item Identifier type.

    Attributes:
        VALUE_01: Proprietary AV Item ID scheme For example, a
            publisher’s own identifier. Note that a distinctive
            &lt;IDTypeName&gt; is required with proprietary AV item
            identifiers
        VALUE_03: GTIN-13 Formerly known as the EAN-13 (unhyphenated)
        VALUE_06: DOI Digital Object Identifier (variable length and
            character set, beginning ‘10.’ and without https://doi.org/
            or the older http://dx.doi.org/)
        VALUE_12: IMDB Motion picture work identifier from the
            International Movie Database
        VALUE_18: ISRC International Standard Recording Code, 5
            alphanumeric characters plus 7 digits
        VALUE_19: ISAN International Standard Audiovisual Number (17 or
            26 characters – 16 or 24 hexadecimal digits, plus one or two
            alphanumeric check characters, and without spaces or
            hyphens)
        VALUE_31: EIDR Content ID Entertainment Identifier Registry
            identifier for an audiovisual work, eg a movie, TV series (a
            DOI beginning ‘10.5240/’ with a suffix of 21 hexadecimal
            digits and five hyphens, and without https://doi.org/ or the
            older http://dx.doi.org/). See ui.eidr.org/search
    """

    VALUE_01 = "01"
    VALUE_03 = "03"
    VALUE_06 = "06"
    VALUE_12 = "12"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_31 = "31"
