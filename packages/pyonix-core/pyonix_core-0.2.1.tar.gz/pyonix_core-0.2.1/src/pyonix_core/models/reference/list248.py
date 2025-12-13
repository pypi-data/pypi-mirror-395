from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List248(Enum):
    """
    Specification detail code.

    Attributes:
        A411: 22.05kHz
        A412: 44.1kHz 44,100 samples per channel per second (CD quality)
        A413: 48kHz
        A416: 16-bits per sample Bit depth, 16 bits per sample (CD-
            quality)
        A418: 24-bits per sample
        A424: ID3v1 Includes v1.1
        A425: ID3v2
        B001: Printed long grain Grain of paper parallel to spine
        B002: Printed short grain Grain of paper perpendicular to spine
        B003: Printed monochrome Usually B/W
        B004: Printed CMYK
        B005: Printed higher-quality CMYK Printed ‘premium’ or high-
            fidelity / high resolution CMYK (where different from
            ‘Printed CMYK’, and the manufacturer offers two quality
            settings)
        B006: Printed with bleed At least some content bleeds to or
            beyond trimmed page edge
        B007: Printed higher-quality monochrome Printed ‘premium’ or
            high-fidelity / high resolution monochrome (where different
            from ‘Printed monochrome’, and the manufacturer offers two
            quality settings)
    """

    A411 = "A411"
    A412 = "A412"
    A413 = "A413"
    A416 = "A416"
    A418 = "A418"
    A424 = "A424"
    A425 = "A425"
    B001 = "B001"
    B002 = "B002"
    B003 = "B003"
    B004 = "B004"
    B005 = "B005"
    B006 = "B006"
    B007 = "B007"
