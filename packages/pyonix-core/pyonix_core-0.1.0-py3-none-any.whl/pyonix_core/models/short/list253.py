from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List253(Enum):
    """
    Resource file feature type.

    Attributes:
        VALUE_01: File format Resource File Feature Value carries a code
            from List 178
        VALUE_04: Filename Resource File Feature Value carries the
            filename of the supporting resource, necessary only when it
            is different from the last part of the path provided in
            &lt;ResourceFileLink&gt;
        VALUE_05: Approximate download file size in megabytes Resource
            File Feature Value carries a decimal number only, suggested
            no more than 2 or 3 significant digits (eg 1.7, not 1.7462
            or 1.75MB)
        VALUE_06: MD5 hash value MD5 hash value of the resource file.
            &lt;ResourceFileFeatureValue&gt; should contain the 128-bit
            digest value (as 32 hexadecimal digits). Can be used as a
            cryptographic check on the integrity of a resource after it
            has been retrieved
        VALUE_07: Exact download file size in bytes Resource File
            Feature Value carries a integer number only (eg 1831023)
        VALUE_08: SHA-256 hash value SHA-256 hash value of the resource
            file. &lt;ResourceFileFeatureValue&gt; should contain the
            256-bit digest value (as 64 hexadecimal digits). Can be used
            as a cryptographic check on the integrity of a resource
            after it has been retrieved
        VALUE_31: Audio loudness Resource File Feature Value is the
            loudness in LKFS (LUFS) used for audio normalization – see
            ITU-R BS.1770
    """

    VALUE_01 = "01"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_31 = "31"
