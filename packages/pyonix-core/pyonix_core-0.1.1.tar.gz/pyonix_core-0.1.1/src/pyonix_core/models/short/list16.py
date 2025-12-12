from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List16(Enum):
    """
    Work identifier type.

    Attributes:
        VALUE_01: Proprietary work ID scheme For example, a publisher’s
            own work ID scheme. Note that a distinctive
            &lt;IDTypeName&gt; is required with proprietary identifiers
        VALUE_02: ISBN-10 10-character ISBN of manifestation of work,
            when this is the only work identifier available – now
            Deprecated in ONIX for Books, except where providing
            historical information for compatibility with legacy
            systems. It should only be used in relation to products
            published before 2007 – when ISBN-13 superseded it – and
            should never be used as the ONLY identifier (it should
            always be accompanied by the correct GTIN-13 / ISBN-13 of
            the manifestation of the work)
        VALUE_06: DOI Digital Object Identifier (variable length and
            character set, beginning ‘10.’ and without https://doi.org/
            or the older http://dx.doi.org/)
        VALUE_11: ISTC International Standard Text Code (16 characters:
            numerals and letters A–F, unhyphenated). Deprecated: the
            ISTC was withdrawn as a standard in 2021
        VALUE_15: ISBN-13 13-character ISBN of a manifestation of work,
            when this is the only work identifier available (13 digits,
            without spaces or hyphens)
        VALUE_18: ISRC International Standard Recording Code
        VALUE_31: EIDR Content ID Entertainment Identifier Registry
            identifier for an audiovisual work, eg a movie, TV series (a
            DOI beginning ‘10.5240/’ with a suffix of 21 hexadecimal
            digits and five hyphens, and without https://doi.org/ or the
            older http://dx.doi.org/). See ui.eidr.org/search. Only for
            use in ONIX 3.0 or later
        VALUE_32: GLIMIR Global Library Manifestation Identifier, OCLC’s
            ‘manifestation cluster’ ID
        VALUE_33: OWI OCLC Work Identifier
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
    VALUE_02 = "02"
    VALUE_06 = "06"
    VALUE_11 = "11"
    VALUE_15 = "15"
    VALUE_18 = "18"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_39 = "39"
