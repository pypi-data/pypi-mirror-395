from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List34(Enum):
    """
    Text format.

    Attributes:
        VALUE_02: HTML Other than XHTML
        VALUE_03: XML Other than XHTML
        VALUE_05: XHTML
        VALUE_06: Default text format Default: plain text containing no
            markup tags of any kind, except for the character entities
            &amp;amp; and &amp;lt; that XML insists must be used to
            represent ampersand and less-than characters in textual
            data, and in the encoding declared at the head of the
            message or in the XML default (UTF-8 or UTF-16) if there is
            no explicit declaration
        VALUE_07: Basic ASCII text Plain text containing no markup tags
            of any kind, except for the character entities &amp;amp; and
            &amp;lt; that XML insists must be used to represent
            ampersand and less-than characters in textual data, and with
            the character set limited to the ASCII range, i.e. valid
            characters whose Unicode character numbers lie between 32
            (space) and 126 (tilde)
    """

    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
