from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List43(Enum):
    """
    Text item identifier type.

    Attributes:
        VALUE_01: Proprietary text item ID scheme For example, a
            publisher’s own identifier scheme for a textual content
            item. Note that a distinctive &lt;IDTypeName&gt; is required
            with proprietary identifiers
        VALUE_03: GTIN-13 Formerly known as the EAN-13 (unhyphenated)
        VALUE_06: DOI Digital Object Identifier (variable length and
            character set, beginning ‘10.’ and without https://doi.org/
            or the older http://dx.doi.org/)
        VALUE_09: PII Publisher item identifier, 17 characters, without
            punctuation, beginning with B (for book) or S (for serial
            publications). Deprecated
        VALUE_10: SICI Serial Item and Contribution Identifier, for
            serial items only. Deprecated: the SICI was withdrawn as a
            standard in 2012
        VALUE_11: ISTC International Standard Text Code (16 characters:
            numerals and letters A–F, unhyphenated). Deprecated: the
            ISTC was withdrawn as a standard in 2021
        VALUE_15: ISBN-13 (Unhyphenated)
        VALUE_39: ISCC International Standard Content Code, a
            ‘similarity hash’ derived algorithmically from the content
            itself (see https://iscc.codes). &lt;IDValue&gt; is a
            sequence comprising the Meta-Code and Content-Code ISCC-
            UNITSs generated from a digital manifestation of the work,
            as a variable-length case-insensitive alphanumeric string
            (or 27 characters including one hyphen if using ISCC v1.0,
            but this is deprecated). Note alphabetic characters in v1.x
            ISCCs use Base32 encoding and are conventionally upper case.
            The ‘ISCC:’ prefix is omitted. Only for use in ONIX 3.0 or
            later
    """

    VALUE_01 = "01"
    VALUE_03 = "03"
    VALUE_06 = "06"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_15 = "15"
    VALUE_39 = "39"
