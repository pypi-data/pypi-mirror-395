from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List252(Enum):
    """
    Resource file detail code.

    Attributes:
        A410: Mono Includes ‘stereo’ where channels are identical
        A411: 22.05kHz
        A412: 44.1kHz 44,100 samples per channel per second (CD-quality)
        A413: 48kHz
        A414: 88.2kHz
        A415: 96kHz
        A416: 16-bits per sample Bit depth, 16 bits per sample (CD-
            quality)
        A417: 20-bits per sample
        A418: 24-bits per sample
        A419: 32-bits per sample (FP)
        A420: Stereo Includes ‘joint stereo’
        A421: Stereo 2.1
        A422: ID3v1 Includes v1.1
        A423: ID3v2
        A441: Surround 4.1 Five-channel audio (including low-frequency
            channel)
        A451: Surround 5.1 Six-channel audio (including low-frequency
            channel)
        B001: With crop marks
        B002: Without crop marks If page size of the resource file is
            not equal to final trimmed page size of the product (in
            &lt;Measure&gt;, then text or image area should be centered
            on final pages. Note that content may not bleed to the
            trimmed page edge
        B003: Monochrome
        B004: Preseparated – 2 channels Two pages in the resource file
            represent a single page in the product
        B005: Preseparated – 3 channels
        B006: Preseparated – 4 channels For example, preseparated CMYK
        B010: Composite (CMYK)
        B011: Composite (RGB)
    """

    A410 = "A410"
    A411 = "A411"
    A412 = "A412"
    A413 = "A413"
    A414 = "A414"
    A415 = "A415"
    A416 = "A416"
    A417 = "A417"
    A418 = "A418"
    A419 = "A419"
    A420 = "A420"
    A421 = "A421"
    A422 = "A422"
    A423 = "A423"
    A441 = "A441"
    A451 = "A451"
    B001 = "B001"
    B002 = "B002"
    B003 = "B003"
    B004 = "B004"
    B005 = "B005"
    B006 = "B006"
    B010 = "B010"
    B011 = "B011"
