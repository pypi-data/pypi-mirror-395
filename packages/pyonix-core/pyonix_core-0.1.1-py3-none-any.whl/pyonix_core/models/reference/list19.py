from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List19(Enum):
    """
    Unnamed person(s)

    Attributes:
        VALUE_01: Unknown
        VALUE_02: Anonymous Note that Anonymous can be interpreted as
            singular or plural. A real name can be provided using
            &lt;AlternativeName&gt; where it is generally known
        VALUE_03: et al And others. Use when some but not all
            contributors are listed individually, perhaps because the
            complete contributor list is impractically long
        VALUE_04: Various When there are multiple contributors, and none
            are listed individually. Use for example when the product is
            a pack of books by different authors
        VALUE_05: Synthesized voice – male Use for example with
            Contributor role code E07 ‘read by’ for audio books with
            digital narration having a male-inflected tone. ‘Brand name’
            of voice may be provided in &lt;AlternativeName&gt;
        VALUE_06: Synthesized voice – female Use for example with
            Contributor role code E07 ‘read by’ for audio books with
            digital narration having a female-inflected tone. ‘Brand
            name’ of voice may be provided in &lt;AlternativeName&gt;
        VALUE_07: Synthesized voice – unspecified Use for example with
            Contributor role code E07 ‘read by’ for audio books with
            digital narration
        VALUE_08: Synthesized voice – based on real voice actor
            Sometimes termed an ‘Authorized Voice Replica’. Use for
            example with Contributor role code E07 ‘read by’ for audio
            books with digital narration, and provide name of voice
            actor in &lt;AlternativeName&gt;. Only for use in ONIX 3.0
            or later
        VALUE_09: AI (Artificial intelligence) Use when the creator (of
            text, of images etc) is a generative AI model or technique.
            Note, can also be combined with the role ‘assisted by’. Only
            for use in ONIX 3.0 or later
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
