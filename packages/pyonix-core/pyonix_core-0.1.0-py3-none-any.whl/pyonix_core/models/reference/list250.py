from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List250(Enum):
    """
    Resource identifier type.

    Attributes:
        VALUE_01: Proprietary resource ID scheme For example, a
            publisher’s internal digital asset ID. Note that a
            distinctive &lt;IDTypeName&gt; is required with proprietary
            resource identifiers
        VALUE_09: ISCC International Standard Content Code, a
            ‘similarity hash’ derived algorithmically from the resource
            content itself (see https://iscc.codes). &lt;IDValue&gt; is
            the ISCC-CODE generated from a digital manifestation of the
            work, as a variable-length case-insensitive alphanumeric
            string (or 55 characters including three hyphens if using
            ISCC v1.0, but this is deprecated). Note alphabetic
            characters in v1.x ISCCs use Base32 encoding and are
            conventionally upper case. The ‘ISCC:’ prefix is omitted
    """

    VALUE_01 = "01"
    VALUE_09 = "09"
