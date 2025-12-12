from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List87(Enum):
    """
    Bible reference location.

    Attributes:
        CCL: Center column References are printed in a narrow column in
            the center of the page between two columns of text
        PGE: Page end References are printed at the foot of the page
        SID: Side column References are printed in a column to the side
            of the scripture
        VER: Verse end References are printed at the end of the
            applicable verse
        UNK: Unknown The person creating the ONIX record does not know
            where the references are located
        ZZZ: Other Other locations not otherwise identified
    """

    CCL = "CCL"
    PGE = "PGE"
    SID = "SID"
    VER = "VER"
    UNK = "UNK"
    ZZZ = "ZZZ"
