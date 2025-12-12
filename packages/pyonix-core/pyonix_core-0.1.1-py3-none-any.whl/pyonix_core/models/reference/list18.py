from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List18(Enum):
    """
    Person / organization name type.

    Attributes:
        VALUE_00: Unspecified Usually the name as it is presented on the
            book
        VALUE_01: Pseudonym May be used to give a well-known pseudonym,
            where the primary name is a ‘real’ name
        VALUE_02: Authority-controlled name
        VALUE_03: Earlier name Use only within &lt;AlternativeName&gt;
        VALUE_04: ‘Real’ name May be used to identify a well-known
            ‘real’ name, where the primary name is a pseudonym or is
            unnamed
        VALUE_05: Transliterated / translated form of primary name Use
            only within &lt;AlternativeName&gt;, when the primary name
            type is unspecified, for names in a different script or
            language
        VALUE_06: Later name Use only within &lt;AlternativeName&gt;
        VALUE_07: Fictional character name Use only within
            &lt;NameAsSubject&gt; to indicate the subject is fictional,
            or in &lt;AlternativeName&gt; alongside
            &lt;UnnamedPersons&gt; to indicate a human-like name for a
            synthetic voice or AI. Only for use in ONIX 3.0 or later
        VALUE_08: Acronym / initialism Use only within
            &lt;AlternativeName&gt; with a corporate name to indicate
            the name is an acronym, initialism or short abbreviation for
            the full name. Only for use in ONIX 3.0 or later
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
