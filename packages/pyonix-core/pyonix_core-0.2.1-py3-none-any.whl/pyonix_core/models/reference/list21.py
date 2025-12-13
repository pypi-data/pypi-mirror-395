from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List21(Enum):
    """
    Edition type.

    Attributes:
        ABR: Abridged edition Content has been shortened: use for
            abridged, shortened, concise, condensed
        ACT: Acting edition Version of a play or script intended for use
            of those directly involved in a production, usually
            including full stage directions in addition to the text of
            the script
        ADP: Adapted edition Content has been adapted to serve a
            different purpose or audience, or from one medium to
            another: use for dramatization, novelization etc. Use
            &lt;EditionStatement&gt; to describe the exact nature of the
            adaptation
        ALT: Alternate Do not use. Deprecated, but retained in the list
            for reasons of backwards compatibility. Not for use in ONIX
            3.0 or later
        ANN: Annotated edition Content is augmented by the addition of
            notes
        AVS: Anniversary edition Edition published to mark a special
            anniversary of first publication of the content. Use
            &lt;EditionStatement&gt; to describe the nature of the
            anniversary. Only for use in ONIX 3.0 or later
        BLL: Bilingual edition Both languages should be specified in the
            &lt;Language&gt; group. Use MLL for an edition in more than
            two languages
        BLP: Bilingual ‘facing page’ edition Use only where the two
            languages are presented in parallel on facing pages, or in
            parallel columns of text on a single page (otherwise use
            BLL). Both languages should be specified in the
            &lt;Language&gt; group
        BRL: Braille edition Braille edition
        BUD: Budget edition Product sold at lower price than other
            editions, usually with lower quality paper or binding to
            reduce production costs. Only for use in ONIX 3.0 or later
        CMB: Combined volume An edition in which two or more works also
            published separately are combined in a single volume; AKA
            ‘omnibus edition’ or occasionally ‘bind-up’, or in comic
            books a ‘trade paperback’ (fr: ‘intégrale’)
        CRI: Critical edition Content includes critical commentary on
            the text
        CSP: Coursepack Content was compiled for a specified educational
            course
        DGO: Digital original A digital product that, at the time of
            publication, has or had no physical counterpart and that is
            or was not expected to have a physical counterpart for a
            reasonable time (recommended at least 30 days following
            publication)
        ENH: Enhanced edition Use for e-publications that have been
            enhanced with additional text, speech, other audio, video,
            interactive or other content
        ENL: Enlarged edition Content has been enlarged or expanded from
            that of a previous edition, with significant additions to
            the original content – for example additional chapters. Do
            not use where the only additions are not a part of the
            original work (eg ‘teaser chapters’ from another work)
        ETR: Easy-to-read edition Book which uses highly simplified
            wording, clear page layout and typography to ensure the
            content can be understood by those with intellectual
            disabilities. See https://www.inclusion-europe.eu/easy-to-
            read for guidelines. See also SMP for editions with
            simplified language. Only for use in ONIX 3.0 or later
        EXP: Expurgated edition ‘Offensive’ content has been removed
        FAC: Facsimile edition Exact reproduction of the content and
            format of a previous edition
        FST: Festschrift A collection of writings published in honor of
            a person, an institution or a society
        HRE: High readability edition Edition optimized for high
            readability, typically featuring colored or tinted page
            backgrounds to reduce contrast, extra letter, word and line
            spacing to reduce crowding and isolate individual words,
            simplified page layouts and an open, sans serif font (or
            occasionally, an unusual font design) intended to aid
            readability. Sometimes labelled ‘dyslexia-friendly’. See
            also code SMP if the text itself is simplified, and codes
            LTE or ULP if the type size is significantly larger than
            normal. Only for use in ONIX 3.0 or later
        ILL: Illustrated edition Content includes extensive
            illustrations which are not part of other editions
        INT: International edition A product aimed specifically at
            markets other than the country of original publication,
            usually titled as an ‘International edition’ and with
            specification and/or content changes
        LTE: Large type / large print edition Large print edition, print
            sizes 14 to 19pt – see also ULP
        MCP: Microprint edition A printed edition in a type size too
            small to be read without a magnifying glass
        MDT: Media tie-in An edition published to coincide with the
            release of a film, TV program, or electronic game based on
            the same work. Use &lt;EditionStatement&gt; to describe the
            exact nature of the tie-in
        MLL: Multilingual edition All languages should be specified in
            the ‘Language’ group. Use BLL for a bilingual edition
        NED: New edition Where no other information is given, or no
            other coded type or edition numbering is applicable
        NUM: Edition with numbered copies A limited or collectors’
            edition in which each copy is individually numbered, and the
            actual number of copies is strictly limited. Note that the
            supplier may limit the number of orders fulfilled per retail
            outlet. Use &lt;EditionStatement&gt; to give details of the
            number of copies printed
        PBO: Paperback original A product published in any form of soft
            cover, that at the time of publication, has or had no
            counterpart in any other format, and that is or was not
            expected to have such a counterpart for a reasonable time
            (recommended at least 30 days following publication). Only
            for use in ONIX 3.0 or later
        PRB: Prebound edition Book that was previously bound, normally
            as a paperback, and has been rebound with, for example, a
            library-quality hardcover binding, or a lay-flat binding, by
            a supplier other than the original publisher. See also the
            &lt;Publisher&gt; and &lt;RelatedProduct&gt; composites for
            other aspects of the treatment of prebound editions in ONIX
        REV: Revised edition Content has been revised from that of a
            previous edition (often used when there has been no
            corresponding increment in the edition number, or no edition
            numbering is available)
        SCH: School edition An edition intended specifically for use in
            schools
        SIG: Signed edition Individually autographed by the author(s)
        SMP: Simplified language edition An edition that uses simplified
            language, usually for second or additional language
            learners. See ETR for highly simplified editions for readers
            with intellectual disabilities
        SPE: Special edition Use for anniversary, collectors’, de luxe,
            gift, limited, signed, commemorative or celebratory, tie-in,
            special variant cover or otherwise special editions, but
            prefer more specific codes AVS, FST, MDT, NUM, SIG, UNN
            whenever appropriate. Use &lt;EditionStatement&gt; to
            describe the exact nature of the special edition
        STU: Student edition Where a text is available in both student
            and teacher’s editions
        TCH: Teacher’s edition Where a text is available in both student
            and teacher’s editions; use also for instructor’s or
            leader’s editions, and for editions intended exclusively for
            educators where no specific student edition is available
        UBR: Unabridged edition Where a title has also been published in
            an abridged edition; also for audiobooks, regardless of
            whether an abridged audio version also exists
        ULP: Ultra large print edition For print sizes 20pt and above,
            and with typefaces designed for the visually impaired – see
            also LTE
        UNN: Edition with unnumbered copies A limited or collectors’
            edition in which each copy is not individually numbered –
            but where the actual number of copies is strictly limited.
            Note that the supplier may limit the number of orders
            fulfilled per retail outlet. Use &lt;EditionStatement&gt; to
            give details of the number of copies printed
        UXP: Unexpurgated edition Content previously considered
            ‘offensive’ has been restored
        VAR: Variorum edition Content includes notes by various
            commentators, and/or includes and compares several variant
            texts of the same work
        VOR: Vorlesebücher Readaloud edition – specifically intended and
            designed for reading aloud (to children). Only for use in
            ONIX 3.0 or later
    """

    ABR = "ABR"
    ACT = "ACT"
    ADP = "ADP"
    ALT = "ALT"
    ANN = "ANN"
    AVS = "AVS"
    BLL = "BLL"
    BLP = "BLP"
    BRL = "BRL"
    BUD = "BUD"
    CMB = "CMB"
    CRI = "CRI"
    CSP = "CSP"
    DGO = "DGO"
    ENH = "ENH"
    ENL = "ENL"
    ETR = "ETR"
    EXP = "EXP"
    FAC = "FAC"
    FST = "FST"
    HRE = "HRE"
    ILL = "ILL"
    INT = "INT"
    LTE = "LTE"
    MCP = "MCP"
    MDT = "MDT"
    MLL = "MLL"
    NED = "NED"
    NUM = "NUM"
    PBO = "PBO"
    PRB = "PRB"
    REV = "REV"
    SCH = "SCH"
    SIG = "SIG"
    SMP = "SMP"
    SPE = "SPE"
    STU = "STU"
    TCH = "TCH"
    UBR = "UBR"
    ULP = "ULP"
    UNN = "UNN"
    UXP = "UXP"
    VAR = "VAR"
    VOR = "VOR"
