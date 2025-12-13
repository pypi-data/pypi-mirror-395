from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List84(Enum):
    """
    Study Bible type.

    Attributes:
        CAM: Cambridge Annotated Contains the work of Howard Clark Kee
            including a summary of the development of the canon,
            introductions to the books, notes and cross references.
            Originally published in 1993, NRSV
        LIF: Life Application A project of Tyndale House Publishers and
            Zondervan intended to help readers apply the Bible to daily
            living. Living Bible, King James, New International, NASB
        MAC: Macarthur A King James version study Bible with notes by
            James Macarthur first published in 1997
        OXF: Oxford Annotated A study Bible originally published in the
            1960s and based on the RSV / NRSV
        NNT: Studiebibel, Det Nye testamentet Norwegian study Bible, New
            Testament
        NOX: New Oxford Annotated Published in 1991 and based on the New
            Revised Standard version
        NSB: Norsk studiebibel Norwegian study Bible
        RYR: Ryrie Based on the work of Charles C. Ryrie. King James,
            NI, NASB
        SCO: Scofield A study Bible based on the early 20th century work
            of C.I. Scofield. Based on the King James version
        SPR: Spirit Filled A transdenominational study Bible for persons
            from the Pentecostal/Charismatic traditions
    """

    CAM = "CAM"
    LIF = "LIF"
    MAC = "MAC"
    OXF = "OXF"
    NNT = "NNT"
    NOX = "NOX"
    NSB = "NSB"
    RYR = "RYR"
    SCO = "SCO"
    SPR = "SPR"
