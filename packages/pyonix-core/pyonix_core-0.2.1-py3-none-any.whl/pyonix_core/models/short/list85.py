from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List85(Enum):
    """
    Bible purpose.

    Attributes:
        AW: Award A Bible (or selected Biblical text) designed for
            presentation from a religious organization
        BB: Baby A Bible (or selected Biblical text) designed to be a
            gift to commemorate a child’s birth
        BR: Bride A special gift Bible (or selected Biblical text)
            designed for the bride on her wedding day. Usually white
        CH: Children’s A text Bible (or selected Biblical text) designed
            in presentation and readability for a child
        CT: Christening / Baptism gift A Bible (or selected Biblical
            text) specifically intended as a gift or keepsake for a
            child’s Christening or baptism, often with personalization
            features like a presentation page, space to record
            milestones, and sometimes even illustrations or stories
            tailored for young children. Only for use in ONIX 3.0 or
            later
        CM: Compact A small Bible (or selected Biblical text) with a
            trim height of five inches or less
        CF: Confirmation A Bible (or selected Biblical text) designed to
            be used in the confirmation reading or as a gift to a
            confirmand
        CR: Cross-reference A Bible (or selected Biblical text) which
            includes text conveying cross-references to related
            scripture passages
        DR: Daily readings A Bible (or selected Biblical text) laid out
            to provide readings for each day of the year
        DV: Devotional A Bible (or selected Biblical text) containing
            devotional content together with the scripture
        FM: Family A Bible (or selected Biblical text) containing family
            record pages and / or additional study material for family
            devotion
        FC: First communion A Bible or (selected Biblical text)
            specifically intended as a gift or keepsake for a
            communicant’s first communion. Only for use in ONIX 3.0 or
            later
        GT: General / Text A standard Bible (or selected Biblical text)
            of any version with no distinguishing characteristics beyond
            the canonical text
        GF: Gift A Bible (or selected Biblical text) designed for gift
            or presentation, often including a presentation page
        JN: Journaling / notetaking A Bible (or selected Biblical text)
            designed with extra space in the margins or on dedicated
            pages for notes, personal reflections or creative
            expression. Only for use in ONIX 3.0 or later
        LP: Lectern / Pulpit A large Bible (or selected Biblical text)
            with large print designed for use in reading scriptures in
            public worship from either the pulpit or lectern. Usually in
            a fine binding and elaborately decorated
        MN: Men’s A Bible (or selected Biblical text) especially
            designed with helps and study guides oriented to the adult
            male
        OT: Outreach A Bible (or selected Biblical text) designed for
            distribution to those outside of the church, often at a
            lower cost or in a more accessible format. They are intended
            to be shared with people who may not already own a Bible,
            and frequently feature helpful resources like introductions
            to key concepts, guidance on common questions, and
            explanations of salvation for those exploring faith or new
            believers. Only for use in ONIX 3.0 or later
        PA: Pastoral A Bible (or selected Biblical text) intended as a
            practical resource for pastors, offering guidance and tools
            for various aspects of ministry. It typically includes
            additional articles, sermon outlines, and special service
            templates, alongside standard Biblical text. Only for use in
            ONIX 3.0 or later
        PW: Pew Usually inexpensive but sturdy, a Bible (or selected
            Biblical text) designed for use in church pews
        PR: Preaching A Bible (or selected Biblical text) specifically
            designed with features that are helpful for public speaking
            and delivering sermons, including a larger font size, wider
            margins for taking notes, and a layout that makes it easy to
            locate verses quickly. Smaller and le. Only for use in ONIX
            3.0 or laterss elaborately-decorated than a Pulpit Bible
        PS: Primary school A Bible (or selected Biblical text) designed
            for use in primary school
        RD: Reader’s A Bible (or selected Biblical text) laid out as
            single-column text, with no footnotes or verse numbers, like
            a ‘normal’ book. Only for use in ONIX 3.0 or later
        SC: Scholarly A Bible (or selected Biblical text) including
            texts in Greek and / or Hebrew and designed for scholarly
            study
        SL: Slimline
        ST: Student A Bible (or selected Biblical text) with study
            articles and helps especially for use in the classroom
        SU: Study A Bible (or selected Biblical text) with many extra
            features, e.g. book introductions, dictionary, concordance,
            references, maps, etc, to help readers better understand the
            scripture
        WG: Wedding gift A special gift Bible (or selected Biblical
            text) designed as a gift to the couple on their wedding day
        WM: Women’s A devotional or study Bible (or selected Biblical
            text) with helps targeted at the adult woman
        YT: Youth / Teen A Bible (or selected Biblical text) containing
            special study and devotional helps designed specifically for
            the needs of teenagers or young adults
    """

    AW = "AW"
    BB = "BB"
    BR = "BR"
    CH = "CH"
    CT = "CT"
    CM = "CM"
    CF = "CF"
    CR = "CR"
    DR = "DR"
    DV = "DV"
    FM = "FM"
    FC = "FC"
    GT = "GT"
    GF = "GF"
    JN = "JN"
    LP = "LP"
    MN = "MN"
    OT = "OT"
    PA = "PA"
    PW = "PW"
    PR = "PR"
    PS = "PS"
    RD = "RD"
    SC = "SC"
    SL = "SL"
    ST = "ST"
    SU = "SU"
    WG = "WG"
    WM = "WM"
    YT = "YT"
