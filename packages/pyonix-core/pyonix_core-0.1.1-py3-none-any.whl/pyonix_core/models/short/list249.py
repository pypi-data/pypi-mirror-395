from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List249(Enum):
    """
    Specification feature type.

    Attributes:
        VALUE_04: Filename Specification Feature Value carries the
            filename of the final product
        VALUE_21: Audio loudness Specification Feature Value is the
            target loudness in LKFS (LUFS) used for audio normalization
            – see ITU-R BS.1770
        VALUE_41: Paper type Specification Feature Description is the
            paper or card type, eg Coated, uncoated
        VALUE_42: Paper weight Specification Feature Value is the paper
            or card weight in GSM
        VALUE_43: Paper color Specification Feature Value is the paper
            or card color code selected from List 257
        VALUE_44: Ink color(s) Specification Feature Description lists
            the ink color(s) required. Do not use if mono or
            conventional CMYK
        VALUE_45: Special finish Specification Feature Value lists a
            special finish required, from List 258
    """

    VALUE_04 = "04"
    VALUE_21 = "21"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_44 = "44"
    VALUE_45 = "45"
