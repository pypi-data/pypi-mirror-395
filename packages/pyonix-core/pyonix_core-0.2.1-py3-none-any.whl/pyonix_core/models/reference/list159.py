from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List159(Enum):
    """
    Resource mode.

    Attributes:
        VALUE_01: Application An executable together with data on which
            it operates
        VALUE_02: Audio A sound recording
        VALUE_03: Image A still image
        VALUE_04: Text Readable text, with or without associated images
            etc
        VALUE_05: Video Moving images, with or without accompanying
            sound
        VALUE_06: Multi-mode A website or other supporting resource
            delivering content in a variety of modes
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
