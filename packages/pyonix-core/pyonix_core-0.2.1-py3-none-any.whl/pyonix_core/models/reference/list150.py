from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List150(Enum):
    """
    Product form.

    Attributes:
        VALUE_00: Undefined
        AA: Audio Audio recording – detail unspecified. Use only when
            the form is unknown and no further detail can be provided.
            Prefer AZ plus &lt;ProductFormDescription&gt; if detail is
            available but no other A* code applies
        AB: Audio cassette Audio cassette (analogue)
        AC: CD-Audio Audio compact disc: use for ‘Red book’ discs
            (conventional audio CD) and SACD, and use coding in
            &lt;ProductFormDetail&gt; to specify the format, if required
        AD: DAT Digital audio tape cassette
        AE: Audio disc Audio disc (excluding CD-Audio): use for ‘Yellow
            book’ (CD-Rom-style) discs, including for example mp3 CDs,
            and use coding in &lt;ProductFormDetail&gt; to specify the
            format of the data on the disc
        AF: Audio tape Audio tape (analogue open reel tape)
        AG: MiniDisc Sony MiniDisc format
        AH: CD-Extra Audio compact disc with part CD-ROM content, also
            termed CD-Plus or Enhanced-CD: use for ‘Blue book’ and
            ‘Yellow/Red book’ two-session discs
        AI: DVD Audio
        AJ: Downloadable audio file Digital audio recording downloadable
            to the purchaser’s own device(s)
        AK: Pre-recorded digital audio player For example, Playaway
            audiobook and player: use coding in
            &lt;ProductFormDetail&gt; to specify the recording format,
            if required
        AL: Pre-recorded SD card For example, Audiofy audiobook chip
        AM: LP ‘Long player’. Vinyl disc (analogue), typically 12 inches
            diameter and played at 33⅓rpm
        AN: Downloadable and online audio file Digital audio recording
            available both by download to the purchaser’s own device(s)
            and by online (eg streamed) access
        AO: Online audio file Digital audio recording available online
            (eg streamed), not downloadable to the purchaser’s own
            device(s)
        AZ: Other audio format Other audio format not specified by AB to
            AO. Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        BA: Book Book – detail unspecified. Use only when the form is
            unknown and no further detail can be provided. Prefer BZ
            plus &lt;ProductFormDescription&gt; if detail is available
            but no other B* code applies
        BB: Hardback Hardback or cased book
        BC: Paperback / softback Paperback or other softback book
        BD: Loose-leaf Loose-leaf book
        BE: Spiral bound Spiral, comb or coil bound book
        BF: Pamphlet Pamphlet, stapled (de: ‘geheftet’). Includes low-
            extent wire-stitched books bound without a distinct spine
            (eg many comic book ‘floppies’)
        BG: Leather / fine binding Use &lt;ProductFormDetail&gt; to
            provide additional description
        BH: Board book Child’s book with all pages printed on board
        BI: Rag book Child’s book with all pages printed on textile
        BJ: Bath book Child’s book printed on waterproof material
        BK: Novelty book A book whose novelty consists wholly or partly
            in a format which cannot be described by any other available
            code – a ‘conventional’ format code is always to be
            preferred; one or more Product Form Detail codes, eg from
            the B2nn group, should be used whenever possible to provide
            additional description
        BL: Slide bound Slide bound book
        BM: Big book Extra-large format for teaching etc; this format
            and terminology may be specifically UK; required as a top-
            level differentiator
        BN: Part-work (fascículo) A part-work issued with its own ISBN
            and intended to be collected and bound into a complete book
        BO: Fold-out book or chart Concertina-folded booklet or chart,
            designed to fold to pocket or regular page size, and usually
            bound within distinct board or card covers (de: ‘Leporello’)
        BP: Foam book A children’s book whose cover and pages are made
            of foam
        BZ: Other book format Other book format or binding not specified
            by BB to BP. Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        CA: Sheet map Sheet map – detail unspecified. Use only when the
            form is unknown and no further detail can be provided.
            Prefer CZ plus &lt;ProductFormDescription&gt; if detail is
            available but no other C* code applies
        CB: Sheet map, folded
        CC: Sheet map, flat
        CD: Sheet map, rolled See &lt;ProductPackaging&gt; and Codelist
            80 for ‘rolled in tube’
        CE: Globe Globe or planisphere
        CZ: Other cartographic Other cartographic format not specified
            by CB to CE. Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        DA: Digital (on physical carrier) Digital content delivered on a
            physical carrier (detail unspecified). Use only when the
            form is unknown and no further detail can be provided.
            Prefer DZ plus &lt;ProductFormDescription&gt; if detail is
            available but no other D* code applies
        DB: CD-ROM
        DC: CD-I CD interactive: use for ‘Green book’ discs
        DE: Game cartridge
        DF: Diskette AKA ‘floppy disc’
        DI: DVD-ROM
        DJ: Secure Digital (SD) Memory Card
        DK: Compact Flash Memory Card
        DL: Memory Stick Memory Card
        DM: USB Flash Drive
        DN: Double-sided CD/DVD Double-sided disc, one side Audio CD/CD-
            ROM, other side DVD
        DO: BR-ROM (Blu Ray ROM)
        DZ: Other digital carrier Other carrier of digital content not
            specified by DB to DO. Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        EA: Digital (delivered electronically) Digital content delivered
            electronically (delivery method unspecified). Use only when
            the form and delivery method is unknown, or when no other E*
            code applies and the delivery method is described in
            &lt;ProductFormDescription&gt;. Note, use
            &lt;ProductFormDetail&gt; to specify file format
        EB: Digital download and online Digital content available both
            by download and by online access
        EC: Digital online Digital content accessed online only (eg
            streamed), not downloadable to the purchaser’s own device(s)
        ED: Digital download Digital content delivered by download only
        FA: Film or transparency Film or transparency – detail
            unspecified. Use only when the form is unknown and no
            further detail can be provided. Prefer FZ plus
            &lt;ProductFormDescription&gt; if detail is available but no
            other F* code applies
        FC: Slides Photographic transparencies mounted for projection
        FD: OHP transparencies Transparencies for overhead projector
        FE: Filmstrip Photographic transparencies, unmounted but cut
            into short multi-frame strips
        FF: Film Continuous movie film as opposed to filmstrip
        FZ: Other film or transparency format Other film or transparency
            format not specified by FB to FF. Further detail is expected
            in &lt;ProductFormDescription&gt;, as
            &lt;ProductFormDetail&gt; and &lt;ProductFormFeature&gt; are
            unlikely to be sufficient
        LA: Digital product license Digital product license (delivery
            method unspecified). Use only when the form is unknown, or
            when no other L* code applies and the delivery method is
            described in &lt;ProductFormDescription&gt;
        LB: Digital product license key Digital product license
            delivered through the retail supply chain as a physical
            ‘key’, typically a card or booklet containing a code
            enabling the purchaser to download the associated product
        LC: Digital product license code Digital product license
            delivered by email or other electronic distribution,
            typically providing a code enabling the purchaser to
            activate, upgrade or extend the license supplied with the
            associated product
        MA: Microform Microform – detail unspecified. Use only when the
            form is unknown and no further detail can be provided.
            Prefer MZ plus &lt;ProductFormDescription&gt; if detail is
            available but no other M* code applies
        MB: Microfiche
        MC: Microfilm Roll microfilm
        MZ: Other microform Other microform not specified by MB or MC.
            Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        PA: Miscellaneous print Miscellaneous printed material – detail
            unspecified. Use only when the form is unknown and no
            further detail can be provided. Prefer PZ plus
            &lt;ProductFormDescription&gt; if detail is available but no
            other P* code applies
        PB: Address book May use &lt;ProductFormDetail&gt; codes P201 to
            P204 to specify binding
        PC: Calendar
        PD: Cards Cards, flash cards (eg for teaching reading), revision
            cards, divination, playing or trading cards
        PE: Copymasters Copymasters, photocopiable sheets
        PF: Diary or journal May use &lt;ProductFormDetail&gt; codes
            P201 to P204 to specify binding
        PG: Frieze Narrow strip-shaped printed sheet used mostly for
            education or children’s products (eg depicting alphabet,
            number line, procession of illustrated characters etc).
            Usually intended for horizontal display
        PH: Kit Parts for post-purchase assembly, including card, wood
            or plastic parts or model components, interlocking
            construction blocks, beads and other crafting materials etc
        PI: Sheet music May use &lt;ProductFormDetail&gt; codes P201 to
            P204 to specify binding
        PJ: Postcard book or pack Including greeting cards and packs.
            For bound books (usually with perforated sheets to remove
            cards), may use &lt;ProductFormDetail&gt; codes P201 to P204
            to specify binding
        PK: Poster Poster for retail sale – see also XF
        PL: Record book Record book (eg ‘birthday book’, ‘baby book’):
            binding unspecified; may use &lt;ProductFormDetail&gt; codes
            P201 to P204 to specify binding
        PM: Wallet or folder Wallet, folder or box (containing loose
            sheets etc, or empty): it is preferable to code the contents
            and treat ‘wallet’ (or folder / box) as packaging in
            &lt;ProductPackaging&gt; with Codelist 80, but if this is
            not possible (eg where the product is empty and intended for
            storing other loose items) the product as a whole may be
            coded as a ‘wallet’. For binders intended for loose leaf or
            partwork publications intended to be updateable, see codes
            BD, BN
        PN: Pictures or photographs
        PO: Wallchart
        PP: Stickers
        PQ: Plate (lámina) A book-sized (as opposed to poster-sized)
            sheet, usually in color or high quality print
        PR: Notebook / blank book A book with all pages blank for the
            buyer’s own use; may use &lt;ProductFormDetail&gt; codes
            P201 to P204 to specify binding
        PS: Organizer May use &lt;ProductFormDetail&gt; codes P201 to
            P204 to specify binding
        PT: Bookmark
        PU: Leaflet Folded but unbound
        PV: Book plates Ex libris’ book labels and packs
        PZ: Other printed item Other printed item not specified by PB to
            PQ. Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        SA: Multiple-component retail product Presentation unspecified:
            format of product components must be given in
            &lt;ProductPart&gt;. Use only when the packaging of the
            product is unknown, or when no other S* code applies and the
            presentation is described in &lt;ProductFormDescription&gt;
        SB: Multiple-component retail product, boxed Format of product
            components must be given in &lt;ProductPart&gt;
        SC: Multiple-component retail product, slip-cased Format of
            product components must be given in &lt;ProductPart&gt;
        SD: Multiple-component retail product, shrink-wrapped Format of
            product components must be given in &lt;ProductPart&gt;. Use
            code XL for a shrink-wrapped pack for trade supply, where
            the retail items it contains are intended for sale
            individually
        SE: Multiple-component retail product, loose Format of product
            components must be given in &lt;ProductPart&gt;
        SF: Multiple-component retail product, part(s) enclosed Multiple
            component product where subsidiary product part(s) is/are
            supplied as enclosures to the primary part, eg a book with a
            CD packaged in a sleeve glued within the back cover. Format
            of product components must be given in &lt;ProductPart&gt;
        SG: Multiple-component retail product, entirely digital Multiple
            component product where all parts are digital, and delivered
            as separate files, eg a group of individual EPUB files, an
            EPUB with a PDF, an e-book with a license to access a range
            of online resources, etc. Format of product components must
            be given in &lt;ProductPart&gt;
        VA: Video Video – detail unspecified. Use only when the form is
            unknown and no further detail can be provided. Prefer VZ
            plus &lt;ProductFormDescription&gt; if detail is available
            but no other V* code applies
        VF: Videodisc eg Laserdisc
        VI: DVD video DVD video: specify TV standard in
            &lt;ProductFormDetail&gt;
        VJ: VHS video VHS videotape: specify TV standard in
            &lt;ProductFormDetail&gt;
        VK: Betamax video Betamax videotape: specify TV standard in
            &lt;ProductFormDetail&gt;
        VL: VCD VideoCD
        VM: SVCD Super VideoCD
        VN: HD DVD High definition DVD disc, Toshiba HD DVD format
        VO: Blu-ray High definition DVD disc, Sony Blu-ray format
        VP: UMD Video Sony Universal Media disc
        VQ: CBHD China Blue High-Definition, derivative of HD-DVD
        VZ: Other video format Other video format not specified by VB to
            VQ. Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        XA: Trade-only material Trade-only material (unspecified). Use
            only when the form is unknown and no further detail can be
            provided. Prefer XZ plus &lt;ProductFormDescription&gt; if
            detail is available but no other X* code applies
        XB: Dumpbin – empty
        XC: Dumpbin – filled Dumpbin with contents. ISBN (where
            applicable) and format of contained items must be given in
            &lt;ProductPart&gt;
        XD: Counterpack – empty
        XE: Counterpack – filled Counterpack with contents. ISBN (where
            applicable) and format of contained items must be given in
            &lt;ProductPart&gt;
        XF: Poster, promotional Promotional poster for display, not for
            sale – see also PK
        XG: Shelf strip
        XH: Window piece Promotional piece for shop window display
        XI: Streamer
        XJ: Spinner – empty
        XK: Large book display Large scale facsimile of book for
            promotional display
        XL: Shrink-wrapped pack A quantity pack with its own product
            code, usually for trade supply only: the retail items it
            contains are intended for sale individually. ISBN (where
            applicable) and format of contained items must be given in
            &lt;ProductPart&gt;. For products or product bundles
            supplied individually shrink-wrapped for retail sale, use
            code SD
        XM: Boxed pack A quantity pack with its own product code,
            usually for trade supply only: the retail items it contains
            are intended for sale individually. ISBN (where applicable)
            and format of contained items must be given in
            &lt;ProductPart&gt;. For products or product bundles boxed
            individually for retail sale, use code SB
        XN: Pack (outer packaging unspecified) A quantity pack with its
            own product code, usually for trade supply only: the retail
            items it contains are intended for sale individually. ISBN
            (where applicable) and format of contained items must be
            given in &lt;ProductPart&gt;. Use only when the pack is
            neither shrinp-wrapped nor boxed
        XO: Spinner – filled Spinner with contents. ISBN(s) (where
            applicable) and detail of contained items must be given in
            &lt;ProductPart&gt;
        XY: Other point of sale – including retail product Other point
            of sale material not specified by XB to XO, supplied with
            included product(s) for retail sale. The retail product(s)
            must be described in &lt;ProductPart&gt;. Further detail of
            the POS material is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        XZ: Other point of sale Other point of sale material not
            specified by XB to XY, promotional or decorative. Further
            detail is expected in &lt;ProductFormDescription&gt;, as
            &lt;ProductFormDetail&gt; and &lt;ProductFormFeature&gt; are
            unlikely to be sufficient
        ZA: General merchandise General merchandise, book accessories
            and non-book products – unspecified. Use only when the form
            is unknown and no further detail can be provided. Prefer ZX,
            ZY or ZZ, plus &lt;ProductFormDescription&gt; if detail is
            available but no other Z* code applies
        ZB: Doll or figure Including action figures, figurines
        ZC: Soft toy Soft or plush toy
        ZD: Toy Including educational toys (where no other code is
            relevant)
        ZE: Game Board game, or other game (except computer game: see DE
            and other D* codes)
        ZF: T-shirt
        ZG: E-book reader Dedicated e-book reading device, typically
            with mono screen
        ZH: Tablet computer General purpose tablet computer, typically
            with color screen
        ZI: Audiobook player Dedicated audiobook player device,
            typically including book-related features like bookmarking
        ZJ: Jigsaw Jigsaw or similar ‘shapes’ puzzle
        ZK: Mug For example, branded, promotional or tie-in drinking
            mug, cup etc
        ZL: Tote bag For example, branded, promotional or tie-in bag
        ZM: Tableware For example, branded, promotional or tie-in
            plates, bowls etc (note for mugs and cups, use code ZK)
        ZN: Umbrella For example, branded, promotional or tie-in
            umbrella
        ZO: Paints, crayons, pencils Coloring set, including pens,
            chalks, etc
        ZP: Handicraft kit Handicraft kit or set, eg sewing, crochet,
            weaving, basketry, beadwork, leather, wood or metalworking,
            pottery and glassworking, candlemaking etc
        ZX: Other toy/game accessories Other toy, game and puzzle items
            not specified by ZB to ZQ, generally accessories to other
            products etc. Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        ZY: Other apparel Other apparel items not specified by ZB to ZQ,
            including branded, promotional or tie-in scarves, caps,
            aprons, dress-up costumes etc. Further detail is expected in
            &lt;ProductFormDescription&gt;, as &lt;ProductFormDetail&gt;
            and &lt;ProductFormFeature&gt; are unlikely to be sufficient
        ZZ: Other merchandise Other branded, promotional or tie-in
            merchandise not specified by ZB to ZY. Further detail is
            expected in &lt;ProductFormDescription&gt;, as
            &lt;ProductFormDetail&gt; and &lt;ProductFormFeature&gt; are
            unlikely to be sufficient
    """

    VALUE_00 = "00"
    AA = "AA"
    AB = "AB"
    AC = "AC"
    AD = "AD"
    AE = "AE"
    AF = "AF"
    AG = "AG"
    AH = "AH"
    AI = "AI"
    AJ = "AJ"
    AK = "AK"
    AL = "AL"
    AM = "AM"
    AN = "AN"
    AO = "AO"
    AZ = "AZ"
    BA = "BA"
    BB = "BB"
    BC = "BC"
    BD = "BD"
    BE = "BE"
    BF = "BF"
    BG = "BG"
    BH = "BH"
    BI = "BI"
    BJ = "BJ"
    BK = "BK"
    BL = "BL"
    BM = "BM"
    BN = "BN"
    BO = "BO"
    BP = "BP"
    BZ = "BZ"
    CA = "CA"
    CB = "CB"
    CC = "CC"
    CD = "CD"
    CE = "CE"
    CZ = "CZ"
    DA = "DA"
    DB = "DB"
    DC = "DC"
    DE = "DE"
    DF = "DF"
    DI = "DI"
    DJ = "DJ"
    DK = "DK"
    DL = "DL"
    DM = "DM"
    DN = "DN"
    DO = "DO"
    DZ = "DZ"
    EA = "EA"
    EB = "EB"
    EC = "EC"
    ED = "ED"
    FA = "FA"
    FC = "FC"
    FD = "FD"
    FE = "FE"
    FF = "FF"
    FZ = "FZ"
    LA = "LA"
    LB = "LB"
    LC = "LC"
    MA = "MA"
    MB = "MB"
    MC = "MC"
    MZ = "MZ"
    PA = "PA"
    PB = "PB"
    PC = "PC"
    PD = "PD"
    PE = "PE"
    PF = "PF"
    PG = "PG"
    PH = "PH"
    PI = "PI"
    PJ = "PJ"
    PK = "PK"
    PL = "PL"
    PM = "PM"
    PN = "PN"
    PO = "PO"
    PP = "PP"
    PQ = "PQ"
    PR = "PR"
    PS = "PS"
    PT = "PT"
    PU = "PU"
    PV = "PV"
    PZ = "PZ"
    SA = "SA"
    SB = "SB"
    SC = "SC"
    SD = "SD"
    SE = "SE"
    SF = "SF"
    SG = "SG"
    VA = "VA"
    VF = "VF"
    VI = "VI"
    VJ = "VJ"
    VK = "VK"
    VL = "VL"
    VM = "VM"
    VN = "VN"
    VO = "VO"
    VP = "VP"
    VQ = "VQ"
    VZ = "VZ"
    XA = "XA"
    XB = "XB"
    XC = "XC"
    XD = "XD"
    XE = "XE"
    XF = "XF"
    XG = "XG"
    XH = "XH"
    XI = "XI"
    XJ = "XJ"
    XK = "XK"
    XL = "XL"
    XM = "XM"
    XN = "XN"
    XO = "XO"
    XY = "XY"
    XZ = "XZ"
    ZA = "ZA"
    ZB = "ZB"
    ZC = "ZC"
    ZD = "ZD"
    ZE = "ZE"
    ZF = "ZF"
    ZG = "ZG"
    ZH = "ZH"
    ZI = "ZI"
    ZJ = "ZJ"
    ZK = "ZK"
    ZL = "ZL"
    ZM = "ZM"
    ZN = "ZN"
    ZO = "ZO"
    ZP = "ZP"
    ZX = "ZX"
    ZY = "ZY"
    ZZ = "ZZ"
