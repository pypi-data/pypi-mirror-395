from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List175(Enum):
    """
    Product form detail.

    Attributes:
        A101: CD standard audio format CD ‘red book’ format
        A102: SACD super audio format
        A103: MP3 format MPEG-1/2 Audio Layer III file
        A104: WAV format
        A105: Real Audio format
        A106: WMA Windows Media Audio format
        A107: AAC Advanced Audio Coding format
        A108: Ogg/Vorbis Vorbis audio format in the Ogg container
        A109: Audible Audio format proprietary to Audible.com
        A110: FLAC Free lossless audio codec
        A111: AIFF Audio Interchangeable File Format
        A112: ALAC Apple Lossless Audio Codec
        A113: W3C Audiobook format Audiobook package format
        A201: DAISY 2: full audio with title only (no navigation)
            Deprecated, as does not meet DAISY 2 standard. Use
            conventional audiobook codes instead
        A202: DAISY 2: full audio with navigation (no text)
        A203: DAISY 2: full audio with navigation and partial text
        A204: DAISY 2: full audio with navigation and full text
        A205: DAISY 2: full text with navigation and partial audio
            Reading systems may provide full audio via text-to-speech
        A206: DAISY 2: full text with navigation and no audio Reading
            systems may provide full audio via text-to-speech
        A207: DAISY 3: full audio with title only (no navigation)
            Deprecated, as does not meet DAISY 3 standard. Use
            conventional audiobook codes instead
        A208: DAISY 3: full audio with navigation (no text)
        A209: DAISY 3: full audio with navigation and partial text
        A210: DAISY 3: full audio with navigation and full text
        A211: DAISY 3: full text with navigation and partial audio
            Reading systems may provide full audio via text-to-speech
        A212: DAISY 3: full text with navigation and no audio Reading
            systems may provide full audio via text-to-speech
        A301: Standalone audio
        A302: Readalong audio Audio intended exclusively for use
            alongside a printed copy of the book. Most often a
            children’s product. Normally contains instructions such as
            ‘turn the page now’ and other references to the printed
            item, and is usually sold packaged together with a printed
            copy
        A303: Playalong audio Audio intended for musical accompaniment,
            eg ‘Music minus one’, etc, often used for music learning.
            Includes singalong backing audio for musical learning or for
            Karaoke-style entertainment
        A304: Speakalong audio Audio intended for language learning,
            which includes speech plus gaps intended to be filled by the
            listener
        A305: Synchronized audio Audio synchronized to text within an
            e-publication, for example an EPUB3 with audio overlay.
            Synchronization at least at paragraph level, and covering
            the full content
        A310: Sound effects Incidental sounds added to the audiobook
            narration (eg background environmental sounds)
        A311: Background music Incidental music added to the audiobook
            narration (eg to heighten atmosphere). Do not use where the
            music is a primary part of the audio
        A312: Without background sounds Pre-recorded audiobook narration
            does not contain any background sounds, including music,
            sound effects, etc, though music and effects may be present
            if isolated from the speech (ie the sounds do not overlap)
        A400: 64kbits/s Constant or average bit rate (eg of an mp3 or
            AAC audio file) 64kbits/second or more. Note the bit rate is
            the total across all channels, not a per channel rate
        A401: 128kbits/s Constant or average bit rate 128bbits/second or
            more
        A402: 192kbits/s
        A403: 256kbits/s
        A404: 320kbits/s
        A410: Mono Includes ‘stereo’ where channels are identical
        A420: Stereo Includes ‘joint stereo’
        A421: Stereo 2.1 Stereo plus low-frequency channel
        A441: Surround 4.1 Five-channel audio (including low-frequency
            channel)
        A451: Surround 5.1 Six-channel audio (including low-frequency
            channel)
        A471: Dolby Atmos Multi-channel ‘spatial’ audio (eg for 7.1.4
            speaker arrangements or processed for headphone delivery)
        B101: Mass market (rack) paperback In North America, a category
            of paperback characterized partly by page size (typically
            from 6¾ up to 7⅛ x 4¼ inches) and partly by target market
            and terms of trade. Use with Product Form code BC
        B102: Trade paperback (US) In North America, a category of
            paperback characterized partly by page size (larger than
            rack-sized) and partly by target market and terms of trade.
            AKA ‘quality paperback’, and including textbooks. Most
            paperback books sold in North America except ‘mass-market’
            (B101) and ‘tall rack’ (B107) are correctly described with
            this code. Use with Product Form code BC
        B103: Digest format paperback In North America, a category of
            paperback characterized by page size (typically 7 x 5
            inches) and generally used for children’s books; use with
            Product Form code BC. Note: was wrongly shown as B102
            (duplicate entry) in Issue 3
        B104: A-format paperback In UK and IE, a category of paperback
            characterized by page size (normally 178 x 111 mm approx);
            use with Product Form code BC
        B105: B-format paperback In UK and IE, a category of paperback
            characterized by page size (normally 198 x 129 mm approx);
            use with Product Form code BC
        B106: Trade paperback (UK) In UK and IE, a category of paperback
            characterized largely by size (usually in traditional
            hardback dimensions), and often used for paperback originals
            or retailer/travel/export-exclusives; use with Product Form
            code BC
        B107: Tall rack paperback (US) In North America, a category of
            paperback characterized partly by page size (typically 7½ x
            4¼ inches) and partly by target market and terms of trade;
            use with Product Form code BC
        B108: A5 size Tankobon Japanese A-series size, 210 x 148mm. A
            tankobon is a complete collected story originally published
            in serialized form (eg in a magazine)
        B109: JIS B5 size Tankobon Japanese B-series size, 257 x 182mm
        B110: JIS B6 size Tankobon Japanese B-series size, 182 x 128mm
        B111: A6 size Bunko Japanese A-series size, 148 x 105mm
        B112: B40-dori Shinsho Japanese format, 182x103mm or 173x105mm
        B113: Pocket (Sweden, Norway, France) A Swedish, Norwegian,
            French paperback format, of no particular fixed size. Use
            with Product Form Code BC
        B114: Storpocket (Sweden) A Swedish paperback format, use with
            Product Form Code BC. In Finnish, Jättipokkari
        B115: Kartonnage (Sweden) A Swedish hardback format, use with
            Product Form Code BB
        B116: Flexband (Sweden) A Swedish softback format, use with
            Product Form Code BC
        B117: Mook / Bookazine A softback book in the format of a
            magazine, usually sold like a book. Use with Product Form
            code BC
        B118: Dwarsligger Also called ‘Flipback’. A softback book in a
            specially compact proprietary format with pages printed in
            landscape on very thin paper and bound along the long (top)
            edge (ie parallel with the lines of text). Use with Product
            Form code BC – see www.dwarsligger.com
        B119: 46 size Japanese format, 188 x 127mm
        B120: 46-Henkei size Japanese format, approximately 188 x 127mm
        B121: A4 297 x 210mm
        B122: A4-Henkei size Japanese format, approximately 297 x 210mm
        B123: A5-Henkei size Japanese format, approximately 210 x 146mm
        B124: B5-Henkei size Japanese format, approximately 257 x 182mm
        B125: B6-Henkei size Japanese format, approximately 182 x 128mm
        B126: AB size 257 x 210mm
        B127: JIS B7 size Japanese B-series size, 128 x 91mm
        B128: Kiku size Japanese format, 218 x 152mm or 227 x 152mm
        B129: Kiku-Henkei size Japanese format
        B130: JIS B4 size Japanese B-series size, 364 x 257 mm
        B131: Paperback (DE) German large paperback format, greater than
            about 205mm high, with flaps. Use with Product form code BC
        B132: Libro de bolsillo Spanish pocket paperback. Use with
            Product form code BC
        B133: Pocket-sized Pocket-sized format, usually less than about
            205mm high, without necessarily implying a particular trade
            category (de: ,Taschenbuch‘; it: «Tascabile /
            Supertascabile»; es: «libro de bolsillo»; fr: « livre de
            poche » etc). Use with Product form code BB or BC. See also
            List 12 code 04
        B134: A5 210 x 148mm
        B135: Mass market max paperback In North America, a category of
            paperback characterized partly by page size (typically 7⅛ x
            4¾ inches) and partly by target market and terms of trade.
            Use with Product Form code BC
        B139: Comic book size (US) Standard 10.25 x 6.625in size approx
            (260 x 170mm)
        B140: Comic album size (Euro) Standard 240 x 320mm size approx
        B141: B4-Henkei size Japanese format, approximately 364 x 257 mm
        B201: Coloring / join-the-dot book
        B202: Lift-the-flap book
        B204: Miniature book
        B205: Moving picture / flicker book
        B206: Pop-up book
        B207: Scented / ‘smelly’ book
        B208: Sound story / ‘noisy’ book
        B209: Sticker book
        B210: Touch-and-feel book Sensory book. A book whose pages have
            a variety of textured inserts designed to stimulate tactile
            exploration: see also B214 and B215
        B212: Die-cut book A book which is cut into a distinctive non-
            rectilinear shape and/or in which holes or shapes have been
            cut internally. (‘Die-cut’ is used here as a convenient
            shorthand, and does not imply strict limitation to a
            particular production process)
        B213: Book-as-toy A book which is also a toy, or which
            incorporates a toy as an integral part. (Do not, however,
            use B213 for a multiple-item product which includes a book
            and a toy as separate items)
        B214: Soft-to-touch book A book whose cover has a soft textured
            finish, typically over board
        B215: Fuzzy-felt book A book with detachable felt pieces and
            textured pages on which they can be arranged
        B216: Press-out pieces A book containing pages with die-cut or
            press-out pieces that can be used as a jigsaw, as puzzle or
            game pieces, play pieces (eg paper dolls) etc
        B221: Picture book Picture book, generally for children though
            also occasionally for teens or adults, with few words per
            illustration: use with applicable Product form code
        B222: ‘Carousel’ book (aka ‘Star’ book). Tax treatment of
            products may differ from that of products with similar codes
            such as Book as toy or Pop-up book)
        B223: Pull-the-tab book A book with movable card ‘tabs’ within
            the pages. Pull a tab to reveal or animate part of a picture
            (distinct from a ‘lift-the-flap’ book, where flaps simply
            reveal hidden pictures, and not specifically a ‘pop-up’ book
            with 3D paper engineering – though when combined with code
            B206 indicates a pop-up book with tabs for moveable parts of
            3D ‘scenes’)
        B224: ‘Wordless’ book Picture book, generally for children
            though also used in augmentative and alternative education,
            or for teens and adults, without text in the body of the
            book. Also ‘silent books’, wordless graphic novels and comic
            books: use with applicable Product Form code
        B225: Cut-out pieces A book containing pages with pieces
            intended to be cut out (not pre-cut or press-out – see B216)
            that can be used as puzzle or game pieces, play pieces etc,
            but which may not be suitable for young children
        B301: Loose leaf or partwork – sheets / parts and binder /
            wallet Use with Product Form code BD, BN or PM
        B302: Loose leaf or partwork – binder / wallet only Use with
            Product Form code BD, BN or PM
        B303: Loose leaf or partwork – sheets / parts only Use with
            Product Form code BD, BN or PM
        B304: Sewn AKA stitched; for ‘saddle-sewn’, prefer code B310
        B305: Unsewn / adhesive bound Including ‘perfect bound’, ‘glued’
        B306: Library binding Strengthened cloth-over-boards binding
            intended for libraries: use with Product form code BB
        B307: Reinforced binding Strengthened binding, not specifically
            intended for libraries: use with Product form code BB or BC
        B308: Half bound Highest quality material used on spine and
            corners only. Must be accompanied by a code specifying a
            material, eg ‘half-bound real leather’
        B309: Quarter bound Highest quality material used on spine only.
            Must be accompanied by a code specifying a material, eg
            ‘quarter bound real leather’
        B310: Saddle-sewn AKA ‘saddle-stitched’ or ‘wire-stitched’
        B311: Comb bound Round or oval plastic forms in a clamp-like
            configuration: use with Product Form code BE
        B312: Wire-O Twin loop metal wire spine: use with Product Form
            code BE
        B313: Concealed wire Cased over Coiled or Wire-O binding: use
            with Product Form code BE and Product Form Detail code B312
            or B314
        B314: Coiled wire bound Spiral wire bound. Use with product form
            code BE. The default if a spiral binding type is not stated.
            Cf. Comb and Wire-O binding
        B315: Trade binding Hardcover binding intended for general
            consumers rather than libraries, use with Product form code
            BB. The default if a hardcover binding detail is not stated.
            cf. Library binding
        B316: Swiss binding Cover is attached to the book block along
            only one edge of the spine, allowing the cover to lay flat
        B317: Notched binding Refinement of perfect binding, with
            notches cut in the spine of the book block prior to glueing,
            to improve adhesion and durability
        B318: Lay-flat binding Hardcover or softcover where interior
            spreads lay flat across the spine
        B319: Flush cut binding Hardcover where the cover boards are
            trimmed flush with the trimmed book block
        B320: Rounded spine Hardcover where the spine is rounded during
            binding
        B321: Square spine Hardcover where the spine is straight
        B400: Self-covered Covers do not use a distinctive stock, but
            are the same as the body pages. Use for example with Product
            form BF, to indicate a pamphlet does not use a card or
            distinct paper cover. See also B416 (for card covers) and
            B418 (for distinct paper covers)
        B401: Cloth over boards Cotton, linen or other woven fabric over
            boards. Use with &lt;ProductForm&gt; BB
        B402: Paper over boards Cellulose-based or similar non-woven
            material, which may be printed and may be embossed with an
            artificial cloth or leather-like texture, over boards. Use
            with &lt;ProductForm&gt; BB
        B403: Leather, real Covered with leather created by tanning
            animal hide. May be ‘full-grain’ using the entire thickness
            of the hide, ‘top grain’ using the outer layer of the hide,
            or ‘split’ using the inner layers of the hide. Split leather
            may be embossed with an artificial grain or texture. Use
            with &lt;ProductForm&gt; BG, and if appropriate with codes
            B308 or B309 (otherwise ‘full-bound’ is implied)
        B404: Leather, imitation Covered with synthetic leather-like
            material – polymer or non-animal fibre over a textile
            backing, usually coated and embossed with an artificial
            grain or texture. Leatherette, pleather etc. Use with
            &lt;ProductForm&gt; BB (or BG if particularly high-quality),
            and if appropriate with codes B308 or B309 (otherwise ‘full-
            bound’ is implied)
        B405: Leather, bonded Covered with leather reconstituted from a
            pulp made from shredded animal hide, layered on a fibre or
            textile backing, coated and usually embossed with an
            artificial grain or texture. Use with &lt;ProductForm&gt;
            BG, and if appropriate with codes B308 or B309 (otherwise
            ‘full-bound’ is implied)
        B406: Vellum Pages made with prepared but untanned animal skin
            (usually calf, occasionally goat or sheep). Includes
            parchment, a thicker and less refined form of animal skin,
            but not ‘paper vellum’ or vegetable parchment made from
            synthetic or plant fibres
        B407: Head and tail bands Capital bands, either decorative or
            functional. Use &lt;ProductFormFeature&gt; to specify the
            color
        B419: Decorated page edges Colored, stained, gilded, patterned,
            abstract or illustrated sprayed edges. Use
            &lt;ProductFormFeature&gt; to specify the color, and
            optionally, use &lt;SupportingResource&gt; to provide an
            image of the decoration
        B408: Decorated endpapers Colored, patterned, printed, abstract
            or illustrated endpapers or of inside front and back covers.
            Use &lt;ProductFormFeature&gt; to specify the color, and
            optionally, use &lt;SupportingResource&gt; to provide an
            image of the decoration
        B409: Cloth Cloth, not necessarily over boards – cf B401
        B410: Imitation cloth Spanish ‘simil-tela’
        B411: Velvet
        B412: Flexible plastic / vinyl cover AKA ‘flexibound’: use with
            Product Form code BC
        B413: Plastic-covered Separate outer plastic cover, often
            transparent and allowing the cover to show through.
            Typically has pockets into which the cover tucks. See also
            B412, where the cover itself is plastic or vinyl
        B414: Vinyl-covered Separate outer vinyl cover. See also B412,
            where the cover itself is plastic or vinyl
        B415: Laminated cover Book, laminating material unspecified,
            often termed PLC or PPC (printed laminated case, printed
            paper case) when used with Product form BB. Use L101 for
            ‘whole product laminated’, eg a laminated sheet map or
            wallchart
        B416: Card cover With card cover (like a typical paperback). As
            distinct from a self-cover or more elaborate binding. Use
            for example with Product form BF, to indicate a pamphlet is
            bound within a card cover. See also B400 (for self-covers)
            and B418 (for distinct paper covers)
        B417: Duplex-printed cover Printed both inside and outside the
            front and/or back cover
        B418: Paper cover Cover uses a distinct, usually heavier
            (thicker) paper than the interior pages. Use for example
            with Product form BF, to indicate a pamphlet is bound within
            a paper cover. See also B400 (for self-covers) and B416 (for
            card covers)
        B420: Delicate cover / jacket finish Cover or jacket finish may
            merit special handling or packaging during distribution and
            fulfilment, for example because of gloss varnish which may
            hold fingerprints or matt laminate liable to scuffing
        B421: Embossed cover Embossing (or debossing) used on cover or
            jacket
        B422: Foil (on cover)
        B423: Foil (on jacket)
        B424: Temporary stickers on cover or jacket All types of
            promotional stickers, applied on behalf of the publisher,
            but easily removable by the reader without damage to the
            cover or jacket
        B425: Permanent stickers on cover or jacket All types of
            promotional stickers, applied on behalf of the publisher,
            but not capable of being removed easily without damage to
            the cover or jacket
        B426: Spine panorama Spine illustration combines with spines of
            other products in a collection to form a panoramic image.
            Sometimes termed a ‘spinescape’
        B501: With dust jacket Type unspecified
        B502: With printed dust jacket Used to distinguish from B503
        B503: With translucent dust cover With translucent paper or
            plastic protective cover
        B504: With flaps For paperback with flaps – sometimes known as
            gatefolds or French flaps (extensions of the cover that fold
            inside the front and back cover)
        B505: With thumb index
        B506: With ribbon marker(s) If the number of markers is
            significant, it can be stated as free text in
            &lt;ProductFormDescription&gt;. Use
            &lt;ProductFormFeature&gt; to specify the color
        B507: With zip fastener
        B508: With button snap fastener
        B509: With leather edge lining AKA yapp edge?
        B510: Rough front With edge trimming such that the front edge is
            ragged, not neatly and squarely trimmed: AKA deckle edge,
            feather edge, uncut edge, rough cut
        B511: Foldout With one or more gatefold or foldout sections
            bound into the book block
        B512: Wide margin Pages include extra-wide margin specifically
            intended for hand-written annotations
        B513: With fastening strap Book with attached loop for fixing to
            baby stroller, cot, chair etc
        B514: With perforated pages With one or more pages perforated
            and intended to be torn out for use
        B515: Acid-free paper Printed on acid-free or alkaline buffered
            paper conforming with ISO 9706
        B516: Archival paper Printed on acid-free or alkaline buffered
            paper with a high cotton content, conforming with ISO 11108
        B517: With elasticated strap Strap acts as closure or as page
            marker
        B518: With serialized authenticity token For example,
            holographic sticker such as the banderol used in the Turkish
            book trade
        B519: With dust jacket poster Jacket in the form of a pamphlet
            or poster, specifically intended to be removed and read or
            used separately from the book
        B520: Rounded corners Usually die-cut rounding to foredge
            corners of cover (and/or to foredge page corners). See B212
            for elaborate die-cutting
        B521: Splashproof Water-resistant or ‘waterproof’ cover and
            pages
        B522: Mineral paper Pages composed of ‘mineral paper’ comprised
            of HDPE plastic and ground calcium carbonate, eg Stonepaper
        B523: With accessibility claim ticket For example, cut-out claim
            form such as the ‘text data request ticket’ used in the
            Japanese book trade
        B524: Plastic paper Pages composed of microporous sheets
            comprised of non-woven HDPE or HDPP fibers, or of non-porous
            HDPP film, eg Tyvek or Yupo
        B525: With wraparound foredge flap For paperback with flaps (an
            extension of the cover that folds outside the front or back
            cover, covering the foredge). The other flap may be absent,
            conventional or may also wrap around the foredge
        B601: Turn-around book A book in which half the content is
            printed upside-down, to be read the other way round. Also
            known as a ‘flip-book’ or ‘tête-bêche’ (Fr) binding, it has
            two front covers and a single spine. Usually an omnibus of
            two works
        B602: Unflipped manga format Manga with pages and panels in the
            sequence of (right-to-left flowing) Japanese-style design
        B603: Back-to-back book A book in which half the content is
            printed so as to be read from the other cover. All content
            is printed the same way up. Also known as ‘dos-à-dos’ (Fr)
            binding, it has two front covers and two spines. Usually an
            omnibus of two works
        B604: Flipped manga format Manga with pages and panels in the
            sequence mirrored from Japanese-style design (thus flowing
            left-to-right)
        B605: Variant turn-around book A book in which half the content
            is read the other way round from ‘back’ to ‘front’. A
            variant on ‘flip-book’ or ‘tête-bêche’ (fr) binding where
            the text is in two languages with different page progression
            (eg English and Arabic) and neither needs to be upside down,
            it has two front covers and a single spine. Usually an
            omnibus of a work and a derived translated work
        B606: Page progression LTR Pages are ordered left to right (the
            left page in a spread is read before the right). Note this
            does not specifically mean text on the page is also read
            left to right
        B607: Page progression RTL Pages are ordered right to left
        B608: Page progression TTB Pages are ordered top to bottom, with
            the spine oriented horizontally. See also Dwarsligger (code
            B118), a proprietary variation of this format
        B609: Page progression other Pages are ordered bottom to top,
            with the spine oriented horizontally, or in a way for which
            there is no other code
        B610: Syllabification Text shows syllable breaks
        B611: Upper case only For bicameral scripts, body text is upper
            case only
        B701: UK Uncontracted Braille Single letters only. Was formerly
            identified as UK Braille Grade 1
        B702: UK Contracted Braille With some letter combinations. Was
            formerly identified as UK Braille Grade 2
        B703: US Braille For US Braille, prefer codes B704 and B705 as
            appropriate
        B704: US Uncontracted Braille
        B705: US Contracted Braille
        B706: Unified English Braille For UEB, prefer codes B708 and
            B709 as appropriate
        B707: Moon Moon embossed alphabet, used by some print-impaired
            readers who have difficulties with Braille
        B708: Unified English Uncontracted Braille
        B709: Unified English Contracted Braille
        B750: Tactile images Eg charts, diagrams, maps, or other tactile
            graphics or illustrations that are embossed or textured for
            accessibility purposes
        B751: Lenticular images Image-changing effect, ‘3D’ images,
            ‘tilt cards’, printed with tiny lenses
        B752: Anaglyph images Stereoscopic 3D effect (eg of images) as
            viewed through red/green filters
        C750: Raised 3D relief Physical 3D relief (eg of a map, globe)
            reflects height of terrain etc
        D101: Real Video format Proprietary RealNetworks format.
            Includes Real Video packaged within a .rm RealMedia
            container
        D102: Quicktime format
        D103: AVI format
        D104: Windows Media Video format
        D105: MPEG-4
        D201: MS-DOS Use with an applicable Product Form code D*; note
            that more detail of operating system requirements can be
            given in a Product Form Feature composite
        D202: Windows Use with an applicable Product Form code D*; see
            note on D201
        D203: Macintosh Use with an applicable Product Form code D*; see
            note on D201
        D204: UNIX / LINUX Use with an applicable Product Form code D*;
            see note on D201
        D205: Other operating system(s) Use with an applicable Product
            Form code D*; see note on D201
        D206: Palm OS Use with an applicable Product Form code D*; see
            note on D201
        D207: Windows Mobile Use with an applicable Product Form code
            D*; see note on D201
        D301: Microsoft XBox Use with Product Form code DB or DI as
            applicable
        D302: Nintendo Gameboy Color Use with Product Form code DE or DB
            as applicable
        D303: Nintendo Gameboy Advanced Use with Product Form code DE or
            DB as applicable
        D304: Nintendo Gameboy Use with Product Form code DE or DB as
            applicable
        D305: Nintendo Gamecube Use with Product Form code DE or DB as
            applicable
        D306: Nintendo 64 Use with Product Form code DE or DB as
            applicable
        D307: Sega Dreamcast Use with Product Form code DE or DB as
            applicable
        D308: Sega Genesis/Megadrive Use with Product Form code DE or DB
            as applicable
        D309: Sega Saturn Use with Product Form code DE or DB as
            applicable
        D310: Sony PlayStation 1 Use with Product Form code DB as
            applicable
        D311: Sony PlayStation 2 Use with Product Form code DB or DI as
            applicable
        D312: Nintendo Dual Screen Use with Product Form code DE as
            applicable
        D313: Sony PlayStation 3 Use with Product Form code DB, DI, DO
            or E* as applicable
        D314: Microsoft Xbox 360 Use with Product Form code DB, DI or VN
            as applicable
        D315: Nintendo Wii Use with Product Form code DA or E* as
            applicable
        D316: Sony PlayStation Portable (PSP) Use with Product Form code
            DL or VL as applicable
        D317: Sony PlayStation 3 Use with Product Form code DB, DI, DO
            or E* as applicable. Deprecated – use D313
        D318: Sony PlayStation 4 Use with Product Form code DB, DI, DO
            or E* as applicable
        D319: Sony PlayStation Vita Use with Product Form code DA or E*
            as applicable
        D320: Microsoft Xbox One Use with Product Form code DB, DI, DO
            or E* as applicable
        D321: Nintendo Switch Use with Product Form code DE or DB as
            applicable
        D322: Nintendo Wii U Use with Product Form code DE or DB as
            applicable
        D323: Sony PlayStation 5 Use with Product Form code DB, DI, DO
            or E* as applicable
        D324: Microsoft Xbox Series X / S Use with Product Form code DB,
            DI, DO or E* as applicable
        E100: Other No code allocated for this e-publication format yet
        E101: EPUB The Open Publication Structure / OPS Container Format
            standard of the International Digital Publishing Forum
            (IDPF) [File extension .epub]
        E102: OEB The Open EBook format of the IDPF, a predecessor of
            the full EPUB format, still (2008) supported as part of the
            latter [File extension .opf]. Includes EPUB format up to and
            including version 2 – but prefer code E101 for EPUB 2, and
            always use code E101 for EPUB 3
        E103: DOC Microsoft Word binary document format [File extension
            .doc]
        E104: DOCX Office Open XML / Microsoft Word XML document format
            (ISO/IEC 29500:2008) [File extension .docx]
        E105: HTML HyperText Mark-up Language [File extension .html,
            .htm]
        E106: ODF Open Document Format [File extension .odt]
        E107: PDF Portable Document Format (ISO 32000-1:2008) [File
            extension .pdf]
        E108: PDF/A PDF archiving format defined by ISO 19005-1:2005
            [File extension .pdf]
        E109: RTF Rich Text Format [File extension .rtf]
        E110: SGML Standard Generalized Mark-up Language
        E111: TCR A compressed text format mainly used on Psion handheld
            devices [File extension .tcr]
        E112: TXT Text file format [File extension .txt]. Typically
            ASCII or Unicode UTF-8/16
        E113: XHTML Extensible Hypertext Markup Language [File extension
            .xhtml, .xht, .xml, .html, .htm]
        E114: zTXT A compressed text format mainly used on Palm handheld
            devices [File extension .pdb – see also E121, E125, E130]
        E115: XPS XML Paper Specification format [File extension .xps]
        E116: Amazon Kindle A format proprietary to Amazon for use with
            its Kindle reading devices or software readers [File
            extensions .azw, .mobi, .prc etc]. Prefer code E148 for
            Print Replica files
        E117: BBeB A Sony proprietary format for use with the Sony
            Reader and LIBRIé reading devices [File extension .lrf]
        E118: DXReader A proprietary format for use with DXReader
            software
        E119: EBL A format proprietary to the Ebook Library service
        E120: Ebrary A format proprietary to the Ebrary service
        E121: eReader A proprietary format for use with eReader (AKA
            ‘Palm Reader’) software on various hardware platforms [File
            extension .pdb – see also E114, E125, E130]
        E122: Exebook A proprietary format with its own reading system
            for Windows platforms [File extension .exe]
        E123: Franklin eBookman A proprietary format for use with the
            Franklin eBookman reader
        E124: Gemstar Rocketbook A proprietary format for use with the
            Gemstar Rocketbook reader [File extension .rb]
        E125: iSilo A proprietary format for use with iSilo software on
            various hardware platforms [File extension .pdb – see also
            E114, E121, E130]
        E126: Microsoft Reader A proprietary format for use with
            Microsoft Reader software on Windows and Pocket PC platforms
            [File extension .lit]
        E127: Mobipocket A proprietary format for use with Mobipocket
            software on various hardware platforms [File extensions
            .mobi, .prc]. Includes Amazon Kindle formats up to and
            including version 7 – but prefer code E116 for version 7,
            and always use E116 for KF8
        E128: MyiLibrary A format proprietary to the MyiLibrary service
        E129: NetLibrary A format proprietary to the NetLibrary service
        E130: Plucker A proprietary format for use with Plucker reader
            software on Palm and other handheld devices [File extension
            .pdb – see also E114, E121, E125]
        E131: VitalBook A format proprietary to the VitalSource service
        E132: Vook A proprietary digital product combining text and
            video content and available to be used online or as a
            downloadable application for a mobile device – see
            www.vook.com
        E133: Google Edition An epublication made available by Google in
            association with a publisher; readable online on a browser-
            enabled device and offline on designated ebook readers
        E134: Book ‘app’ for iOS Epublication packaged as application
            for iOS (eg Apple iPhone, iPad etc), containing both
            executable code and content. Use &lt;ProductContentType&gt;
            to describe content, and &lt;ProductFormFeatureType&gt; to
            list detailed technical requirements
        E135: Book ‘app’ for Android Epublication packaged as
            application for Android (eg Android phone or tablet),
            containing both executable code and content. Use
            &lt;ProductContentType&gt; to describe content, and
            &lt;ProductFormFeatureType&gt; to list detailed technical
            requirements
        E136: Book ‘app’ for other operating system Epublication
            packaged as application, containing both executable code and
            content. Use where other ‘app’ codes are not applicable.
            Technical requirements such as target operating system
            and/or device should be provided eg in
            &lt;ProductFormFeatureType&gt;. Content type (text or text
            plus various ‘enhancements’) may be described with
            &lt;ProductContentType&gt;
        E139: CEB Founder Apabi’s proprietary basic e-book format
        E140: CEBX Founder Apabi’s proprietary XML e-book format
        E141: iBook Apple’s iBook format (a proprietary extension of
            EPUB), can only be read on Apple iOS devices
        E142: ePIB Proprietary format based on EPUB used by Barnes and
            Noble for fixed-format e-books, readable on NOOK devices and
            Nook reader software
        E143: SCORM Sharable Content Object Reference Model, standard
            content and packaging format for e-learning objects
        E144: EBP E-book Plus (proprietary Norwegian e-book format)
        E145: Page Perfect Proprietary format based on PDF used by
            Barnes and Noble for fixed-format e-books, readable on some
            NOOK devices and Nook reader software
        E146: BRF (Braille-ready file) Electronic Braille file
        E147: Erudit Proprietary XML format for articles, see for
            example https://www.cairn.info/services-aux-editeurs.php
        E148: Amazon Kindle Print Replica A format proprietary to Amazon
            for use with its Kindle reading devices or software readers.
            Essentially a PDF embedded within a KF8 format file
        E149: Comic Book Archive Format for comic books, consisting
            primarily of sequentially-named PNG or JPEG images in a zip
            container
        E150: EPUB/A
        E151: eBraille DAISY/APH Braille file standard based on ePUB
            (formerly known as eBRF)
        E200: Reflowable Use this and/or code E201 when a particular
            e-publication type (specified using codes E100 and upwards)
            is reflowable or has both fixed layout and reflowable
            sections or variants, to indicate which option is included
            in this product
        E201: Fixed format Use this and possibly code E200 when a
            particular e-publication type (specified using codes E100
            and upwards) is fixed layout or has both fixed layout and
            reflowable sections or variants, to indicate which option is
            included in this product
        E202: Readable offline All e-publication resources are included
            within the e-publication package
        E203: Requires network connection E-publication requires a
            network connection to access some resources (eg an enhanced
            e-book where video clips are not stored within the
            e-publication package itself, but are delivered via an
            internet connection)
        E204: Content removed Resources (eg images) present in other
            editions have been removed from this product, eg due to
            rights issues
        E205: Visible page numbering (Mostly fixed-format) e-publication
            contains visible page numbers. Use with List 196 code 19 if
            numbering has a print-equivalent
        E206: No preferred page progression For e-publications only,
            pages may be rendered LTR or RTL (see B606 to B609)
        E210: Landscape Use for fixed-format e-books optimized for
            landscape display. Also include an indication of the optimal
            screen aspect ratio
        E211: Portrait Use for fixed-format e-books optimized for
            portrait display. Also include an indication of the optimal
            screen aspect ratio
        E212: Square Use for fixed-format e-books optimized for a square
            display
        E213: Vertical scrolling Use for fixed-format e-publications
            optimized for vertical scrolling display (‘webtoon format’)
        E221: 5:4 (1.25:1) Use for fixed-format e-books optimized for
            displays with a 5:4 aspect ratio (eg 1280x1024 pixels etc,
            assuming square pixels). Note that aspect ratio codes are
            NOT specific to actual screen dimensions or pixel counts,
            but to the ratios between two dimensions or two pixel counts
        E222: 4:3 (1.33:1) Use for fixed-format e-books optimized for
            displays with a 4:3 aspect ratio (eg 800x600, 1024x768,
            2048x1536 pixels etc)
        E223: 3:2 (1.5:1) Use for fixed-format e-books optimized for
            displays with a 3:2 aspect ratio (eg 960x640, 3072x2048
            pixels etc)
        E224: 16:10 (1.6:1) Use for fixed-format e-books optimized for
            displays with a 16:10 aspect ratio (eg 1440x900, 2560x1600
            pixels etc)
        E225: 16:9 (1.77:1) Use for fixed-format e-books optimized for
            displays with a 16:9 aspect ratio (eg 1024x576, 1920x1080,
            2048x1152 pixels etc)
        E226: 18:9 (2:1) Use for fixed-format e-books optimized for
            displays with an 18:9 aspect ratio (eg 2160x1080, 2880x1440
            pixels etc)
        E227: 21:9 (2.37:1) Use for fixed-format e-books optimized for
            displays with an 21:9 (or 64:27) aspect ratio (eg 3840x1644
            pixels etc)
        L101: Laminated Whole product laminated (eg laminated map, fold-
            out chart, wallchart, etc): use B415 for book with laminated
            cover
        P091: Calendar with write-in space (de: Nutzkalendarium)
            Calendar or diary has spaces intended for entering
            birthdays, appointments, notes etc. Use with other calendar
            / diary type codes
        P092: Calendar without write-in space (de: Schmuckkalendarium)
            Calendar or diary has no spaces intended for entering
            birthdays, appointments, notes etc. Use with other calendar
            / diary type codes
        P096: Multiple months per page (de: Mehrmonatskalender) Calendar
            has multiple months (but not whole year) per page or view.
            Use with other calendar / diary type codes when the time
            period per sheet, page or view is not the expected
            arrangement
        P097: One month per page (de: Monatskalender) Calendar has one
            month per page or view
        P098: One week per page (de: Wochenkalender) Calendar has one
            week per page or view
        P099: One day per page (de: Tageskalender) Calendar has one day
            per page or view
        P101: Desk calendar or diary Large format, usually one week per
            page or view. Use with Product Form code PC or PF
        P102: Mini calendar or pocket diary Small format, usually one
            week per page or view. Use with Product Form code PC or PF
        P103: Engagement calendar or Appointment diary Day planner.
            Usually one day per page or view, with time-of-day
            subdivisions (rather than just days) or adequate space to
            add them. Use with Product Form code PC or PF
        P104: Day by day calendar Eg tear-off calendars (one day per
            sheet). Use with Product Form code PC
        P105: Poster calendar Large single-sheet calendar intended for
            hanging. Use with Product Form code PC or PK
        P106: Wall calendar Large calendar usually intended for hanging
            from the spine, typically one page per view and one month
            per view, with illustrations. See also P134. Use with
            Product Form code PC
        P107: Perpetual calendar or diary Usually undated. Use with
            Product Form code PC or PF, and can be combined with other
            calendar/diary type codes
        P108: Advent calendar Use with Product Form code PC, and can be
            combined with other calendar/diary type codes
        P109: Bookmark calendar Use with Product Form code PC or PT
        P110: Student or Academic calendar or diary Mid-year diary,
            start and end aligned with the academic year. Use with
            Product Form code PC or PF, and can be combined with other
            calendar/diary type codes
        P111: Project calendar Use with Product Form code PC
        P112: Almanac calendar Use with Product Form code PC
        P113: Other calendar, diary or organiser A calendar, diary or
            organiser that is not one of the types specified elsewhere:
            use with Product Form code PC, PF or PS
        P114: Other calendar or organiser product A product that is
            associated with or ancillary to a calendar or organiser, eg
            a deskstand for a calendar, or an insert for an organiser:
            use with Product Form code PC or PS
        P115: Family planner Wall or poster calendar with entries for
            each family member. Use with Product Form code PC or PK
        P116: Postcard calendar Calendar sheets detachable (usually
            perforated) and intended for mailing as postcards. Use with
            Product Form code PC
        P131: Blank calendar Wall calendar without illustrations,
            usually one page per month, intended to be used by adding
            your own images (de: Bastelkalender). Use with Product Form
            code PC
        P132: Panoramic calendar Very large wall calendar intended for
            hanging, usually one page per month, wide landscape
            orientation, with illustrations. Use with Product Form code
            PC
        P133: Columnar calendar Very large wall calendar intended for
            hanging, usually one page per month, narrow portrait
            orientation, with illustrations. Use with Product Form code
            PC
        P134: Square calendar (de: Broschurkalender) Wall calendar,
            usually intended for hanging from a page edge, typically two
            pages per view and one month per view, with illustrations.
            See also P106. Use with Product Form code PC
        P120: Picture story cards Kamishibai / Cantastoria cards
        P121: Flash cards For use to specify letter, word, image (etc)
            recognition cards for teaching reading or other classroom
            use. Use with Product form code PD
        P122: Reference cards Quick reference cards, revision cards,
            recipe cards etc. Use with Product form code PD
        P123: Recreation cards For use to specify cards and card decks
            for gaming, collecting and trading etc. Use also for
            divination cards. Use with Product form codes PD
        P124: Postcards And postcard packs / books. Use with Product
            form code PJ
        P125: Greeting cards And greeting card packs. Use with Product
            form code PJ
        P126: Gift cards Physical cards which carry an intrinsic value,
            or which are intended to have value added to them, that may
            be redeemed later. For example book token cards, gift cards.
            Note value additions and redemption may be in a physical
            store or online
        P127: Certificate cards Blank certificate, award or achievement
            cards, Use with Product form code PD
        P201: Hardback (stationery) Stationery item in hardback book
            format
        P202: Paperback / softback (stationery) Stationery item in
            paperback/softback book format
        P203: Spiral bound (stationery) Stationery item in spiral-bound
            book format
        P204: Leather / fine binding (stationery) Stationery item in
            leather-bound book format, or other fine binding
        P301: With hanging strips For wall map, poster, wallchart etc
        P305: Single-sided Content is printed single-sided (for
            wallcharts and hanging maps, calendars, etc)
        P306: Double-sided Content is printed double-sided (for
            wallcharts and hanging maps, calendars, etc, where double-
            sided may not always be expected)
        V201: PAL SD TV standard for video or DVD
        V202: NTSC SD TV standard for video or DVD
        V203: SECAM SD TV standard for video or DVD
        V205: HD Up to 2K resolution (1920 or 2048 pixels wide) eg for
            Blu-Ray
        V206: UHD Up to 4K resolution (3840 or 4096 pixels wide) eg for
            Ultra HD Blu-Ray
        V207: 3D video Eg for Blu-ray 3D
        V210: Closed captions Or subtitles, where visibility may be
            controlled by the viewer. Use &lt;Language&gt; for the
            language of the captions/subtitles
        V211: Open captions ‘Burnt-in’ or hard captions or subtitles.
            Use &lt;Language&gt; for the language of the
            captions/subtitles
        V212: Transcript Full transcript of audio and audiovisual
            content, supplied as a separate file (not as captions or
            subtitles) and included within the product. See also List
            158, where a transcript is a separate resource
        V213: Sign language interpretation Full signing of audio and
            audiovisual content included within the product
        V214: Textual description of audio Closed or open
            captions/subtitles include descriptions of non-dialogue
            audio (eg background sounds, music, speaker identification)
            in addition to dialogue. Use in combination with V210 or
            V211. Use V210, V211 alone for captions/subtitles that
            include only dialogue. In some markets, textual description
            of audio is termed ‘subtitles for the deaf and hard of
            hearing’ (SDH)
        V215: Audio description of video Also termed ‘described video’ –
            audio track describes the video content
        V220: Home use Licensed for use in domestic contexts only
        V221: Classroom use Licensed for use in education
        Z101: Wooden Primary material composition (eg of kit or puzzle
            pieces, of gameplay tokens or tiles) is wood or has wooden
            pieces/parts
        Z102: Plastic Plastic or plastic pieces/parts
        Z103: Board Card or board pieces/parts
        Z111: 3D puzzle Puzzle assembles into a 3D object
        Z112: Noisy kit / puzzle / toy Toy makes a noise. See B208 for
            noisy books
        Z113: Puppet Including finger / hand puppets, marionettes
        Z121: Extra large pieces Designed and sized for the very young,
            or those with visual impairments, limited motor skills,
            dementia etc
    """

    A101 = "A101"
    A102 = "A102"
    A103 = "A103"
    A104 = "A104"
    A105 = "A105"
    A106 = "A106"
    A107 = "A107"
    A108 = "A108"
    A109 = "A109"
    A110 = "A110"
    A111 = "A111"
    A112 = "A112"
    A113 = "A113"
    A201 = "A201"
    A202 = "A202"
    A203 = "A203"
    A204 = "A204"
    A205 = "A205"
    A206 = "A206"
    A207 = "A207"
    A208 = "A208"
    A209 = "A209"
    A210 = "A210"
    A211 = "A211"
    A212 = "A212"
    A301 = "A301"
    A302 = "A302"
    A303 = "A303"
    A304 = "A304"
    A305 = "A305"
    A310 = "A310"
    A311 = "A311"
    A312 = "A312"
    A400 = "A400"
    A401 = "A401"
    A402 = "A402"
    A403 = "A403"
    A404 = "A404"
    A410 = "A410"
    A420 = "A420"
    A421 = "A421"
    A441 = "A441"
    A451 = "A451"
    A471 = "A471"
    B101 = "B101"
    B102 = "B102"
    B103 = "B103"
    B104 = "B104"
    B105 = "B105"
    B106 = "B106"
    B107 = "B107"
    B108 = "B108"
    B109 = "B109"
    B110 = "B110"
    B111 = "B111"
    B112 = "B112"
    B113 = "B113"
    B114 = "B114"
    B115 = "B115"
    B116 = "B116"
    B117 = "B117"
    B118 = "B118"
    B119 = "B119"
    B120 = "B120"
    B121 = "B121"
    B122 = "B122"
    B123 = "B123"
    B124 = "B124"
    B125 = "B125"
    B126 = "B126"
    B127 = "B127"
    B128 = "B128"
    B129 = "B129"
    B130 = "B130"
    B131 = "B131"
    B132 = "B132"
    B133 = "B133"
    B134 = "B134"
    B135 = "B135"
    B139 = "B139"
    B140 = "B140"
    B141 = "B141"
    B201 = "B201"
    B202 = "B202"
    B204 = "B204"
    B205 = "B205"
    B206 = "B206"
    B207 = "B207"
    B208 = "B208"
    B209 = "B209"
    B210 = "B210"
    B212 = "B212"
    B213 = "B213"
    B214 = "B214"
    B215 = "B215"
    B216 = "B216"
    B221 = "B221"
    B222 = "B222"
    B223 = "B223"
    B224 = "B224"
    B225 = "B225"
    B301 = "B301"
    B302 = "B302"
    B303 = "B303"
    B304 = "B304"
    B305 = "B305"
    B306 = "B306"
    B307 = "B307"
    B308 = "B308"
    B309 = "B309"
    B310 = "B310"
    B311 = "B311"
    B312 = "B312"
    B313 = "B313"
    B314 = "B314"
    B315 = "B315"
    B316 = "B316"
    B317 = "B317"
    B318 = "B318"
    B319 = "B319"
    B320 = "B320"
    B321 = "B321"
    B400 = "B400"
    B401 = "B401"
    B402 = "B402"
    B403 = "B403"
    B404 = "B404"
    B405 = "B405"
    B406 = "B406"
    B407 = "B407"
    B419 = "B419"
    B408 = "B408"
    B409 = "B409"
    B410 = "B410"
    B411 = "B411"
    B412 = "B412"
    B413 = "B413"
    B414 = "B414"
    B415 = "B415"
    B416 = "B416"
    B417 = "B417"
    B418 = "B418"
    B420 = "B420"
    B421 = "B421"
    B422 = "B422"
    B423 = "B423"
    B424 = "B424"
    B425 = "B425"
    B426 = "B426"
    B501 = "B501"
    B502 = "B502"
    B503 = "B503"
    B504 = "B504"
    B505 = "B505"
    B506 = "B506"
    B507 = "B507"
    B508 = "B508"
    B509 = "B509"
    B510 = "B510"
    B511 = "B511"
    B512 = "B512"
    B513 = "B513"
    B514 = "B514"
    B515 = "B515"
    B516 = "B516"
    B517 = "B517"
    B518 = "B518"
    B519 = "B519"
    B520 = "B520"
    B521 = "B521"
    B522 = "B522"
    B523 = "B523"
    B524 = "B524"
    B525 = "B525"
    B601 = "B601"
    B602 = "B602"
    B603 = "B603"
    B604 = "B604"
    B605 = "B605"
    B606 = "B606"
    B607 = "B607"
    B608 = "B608"
    B609 = "B609"
    B610 = "B610"
    B611 = "B611"
    B701 = "B701"
    B702 = "B702"
    B703 = "B703"
    B704 = "B704"
    B705 = "B705"
    B706 = "B706"
    B707 = "B707"
    B708 = "B708"
    B709 = "B709"
    B750 = "B750"
    B751 = "B751"
    B752 = "B752"
    C750 = "C750"
    D101 = "D101"
    D102 = "D102"
    D103 = "D103"
    D104 = "D104"
    D105 = "D105"
    D201 = "D201"
    D202 = "D202"
    D203 = "D203"
    D204 = "D204"
    D205 = "D205"
    D206 = "D206"
    D207 = "D207"
    D301 = "D301"
    D302 = "D302"
    D303 = "D303"
    D304 = "D304"
    D305 = "D305"
    D306 = "D306"
    D307 = "D307"
    D308 = "D308"
    D309 = "D309"
    D310 = "D310"
    D311 = "D311"
    D312 = "D312"
    D313 = "D313"
    D314 = "D314"
    D315 = "D315"
    D316 = "D316"
    D317 = "D317"
    D318 = "D318"
    D319 = "D319"
    D320 = "D320"
    D321 = "D321"
    D322 = "D322"
    D323 = "D323"
    D324 = "D324"
    E100 = "E100"
    E101 = "E101"
    E102 = "E102"
    E103 = "E103"
    E104 = "E104"
    E105 = "E105"
    E106 = "E106"
    E107 = "E107"
    E108 = "E108"
    E109 = "E109"
    E110 = "E110"
    E111 = "E111"
    E112 = "E112"
    E113 = "E113"
    E114 = "E114"
    E115 = "E115"
    E116 = "E116"
    E117 = "E117"
    E118 = "E118"
    E119 = "E119"
    E120 = "E120"
    E121 = "E121"
    E122 = "E122"
    E123 = "E123"
    E124 = "E124"
    E125 = "E125"
    E126 = "E126"
    E127 = "E127"
    E128 = "E128"
    E129 = "E129"
    E130 = "E130"
    E131 = "E131"
    E132 = "E132"
    E133 = "E133"
    E134 = "E134"
    E135 = "E135"
    E136 = "E136"
    E139 = "E139"
    E140 = "E140"
    E141 = "E141"
    E142 = "E142"
    E143 = "E143"
    E144 = "E144"
    E145 = "E145"
    E146 = "E146"
    E147 = "E147"
    E148 = "E148"
    E149 = "E149"
    E150 = "E150"
    E151 = "E151"
    E200 = "E200"
    E201 = "E201"
    E202 = "E202"
    E203 = "E203"
    E204 = "E204"
    E205 = "E205"
    E206 = "E206"
    E210 = "E210"
    E211 = "E211"
    E212 = "E212"
    E213 = "E213"
    E221 = "E221"
    E222 = "E222"
    E223 = "E223"
    E224 = "E224"
    E225 = "E225"
    E226 = "E226"
    E227 = "E227"
    L101 = "L101"
    P091 = "P091"
    P092 = "P092"
    P096 = "P096"
    P097 = "P097"
    P098 = "P098"
    P099 = "P099"
    P101 = "P101"
    P102 = "P102"
    P103 = "P103"
    P104 = "P104"
    P105 = "P105"
    P106 = "P106"
    P107 = "P107"
    P108 = "P108"
    P109 = "P109"
    P110 = "P110"
    P111 = "P111"
    P112 = "P112"
    P113 = "P113"
    P114 = "P114"
    P115 = "P115"
    P116 = "P116"
    P131 = "P131"
    P132 = "P132"
    P133 = "P133"
    P134 = "P134"
    P120 = "P120"
    P121 = "P121"
    P122 = "P122"
    P123 = "P123"
    P124 = "P124"
    P125 = "P125"
    P126 = "P126"
    P127 = "P127"
    P201 = "P201"
    P202 = "P202"
    P203 = "P203"
    P204 = "P204"
    P301 = "P301"
    P305 = "P305"
    P306 = "P306"
    V201 = "V201"
    V202 = "V202"
    V203 = "V203"
    V205 = "V205"
    V206 = "V206"
    V207 = "V207"
    V210 = "V210"
    V211 = "V211"
    V212 = "V212"
    V213 = "V213"
    V214 = "V214"
    V215 = "V215"
    V220 = "V220"
    V221 = "V221"
    Z101 = "Z101"
    Z102 = "Z102"
    Z103 = "Z103"
    Z111 = "Z111"
    Z112 = "Z112"
    Z113 = "Z113"
    Z121 = "Z121"
