from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List162(Enum):
    """
    Resource version feature type.

    Attributes:
        VALUE_01: File format Resource Version Feature Value carries a
            code from List 178
        VALUE_02: Image height in pixels Resource Version Feature Value
            carries an integer
        VALUE_03: Image width in pixels Resource Version Feature Value
            carries an integer
        VALUE_04: Filename Resource Version Feature Value carries the
            filename of the supporting resource, necessary only when it
            is different from the last part of the path provided in
            &lt;ResourceLink&gt;
        VALUE_05: Approximate download file size in megabytes Resource
            Version Feature Value carries a decimal number only,
            suggested no more than 2 or 3 significant digits (eg 1.7,
            not 1.7462 or 1.75MB)
        VALUE_06: MD5 hash value MD5 hash value of the resource file.
            &lt;ResourceVersionFeatureValue&gt; should contain the
            128-bit digest value (as 32 hexadecimal digits). Can be used
            as a cryptographic check on the integrity of a resource
            after it has been retrieved
        VALUE_07: Exact download file size in bytes Resource Version
            Feature Value carries a integer number only (eg 1831023)
        VALUE_08: SHA-256 hash value SHA-256 hash value of the resource
            file. &lt;ResourceVersionFeatureValue&gt; should contain the
            256-bit digest value (as 64 hexadecimal digits). Can be used
            as a cryptographic check on the integrity of a resource
            after it has been retrieved
        VALUE_09: ISCC International Standard Content Code, a
            ‘similarity hash’ derived algorithmically from the resource
            content itself (see https://iscc.codes). &lt;IDValue&gt; is
            the ISCC-CODE generated from a digital manifestation of the
            work, as a variable-length case-insensitive alphanumeric
            string (or 55 characters including three hyphens if using
            ISCC v1.0, but this is deprecated). Note alphabetic
            characters in v1.x ISCCs use Base32 encoding and are
            conventionally upper case. The ‘ISCC:’ prefix is omitted
        VALUE_10: Previous filename &lt;ResourceVersionFeatureValue&gt;
            carries the previous filename of the supporting resource,
            necessary only when it is different from the last part of
            the path provided in &lt;ResourceLink&gt; and from the
            filename provided using &lt;ResourceVersionFeatureType&gt;
            code 04, and when the data sender suggests the recipient
            delete this old file. Note that the ‘trigger’ to update the
            resource and delete the old file is provided by the Resource
            version’s &lt;ContentDate&gt;
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_10 = "10"
