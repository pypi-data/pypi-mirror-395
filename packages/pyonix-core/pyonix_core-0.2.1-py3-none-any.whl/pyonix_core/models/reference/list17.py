from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List17(Enum):
    """
    Contributor role code.

    Attributes:
        A01: By (author) Author of a textual work
        A02: With With or as told to: ‘ghost’ or secondary author of a
            literary work (for clarity, should not be used for true
            ‘ghost’ authors who are not credited on the book and whose
            existence is secret)
        A03: Screenplay by Writer of screenplay or script (film or
            video)
        A04: Libretto by Writer of libretto (opera): see also A31
        A05: Lyrics by Author of lyrics (song): see also A31
        A06: By (composer) Composer of music
        A07: By (artist) Visual artist when named as the primary creator
            of, eg, a book of reproductions of artworks
        A08: By (photographer) Photographer when named as the primary
            creator of, eg, a book of photographs
        A09: Created by For example of an editorial concept, of a board
            game, etc
        A10: From an idea by For example of a plot idea. Implies a less
            direct association or active participation than ‘created by’
        A11: Designed by Use for interior graphic design. See code A36
            for cover design, code A12, A35 for interior illustrations
            or drawings
        A12: Illustrated by Artist when named as the creator of artwork
            which illustrates a text, or the originator (sometimes
            ‘penciller’ for collaborative art) of the artwork of a
            graphic novel or comic book
        A13: Photographs by Photographer when named as the creator of
            photographs which illustrate a text
        A14: Text by Author of text which accompanies art reproductions
            or photographs, or which is part of a graphic novel or comic
            book
        A15: Preface by Author of preface
        A16: Prologue by Author of prologue
        A17: Summary by Author of summary
        A18: Supplement by Author of supplement
        A19: Afterword by Author of afterword
        A20: Notes by Author of notes or annotations: see also A29
        A21: Commentaries by Author of commentaries on the main text
        A22: Epilogue by Author of epilogue
        A23: Foreword by Author of foreword
        A24: Introduction by Author of introduction: see also A29
        A25: Footnotes by Author/compiler of footnotes
        A26: Memoir by Author of memoir accompanying main text
        A27: Experiments by Person who carried out experiments reported
            in the text
        A28: Interpreted through Use with narratives drawn from an oral
            tradition, where no ‘ownership’ of the narrative is claimed.
            See also B33. Only for use in ONIX 3.0 or later
        A29: Introduction and notes by Author of introduction and notes:
            see also A20 and A24
        A30: Software written by Writer of computer programs ancillary
            to the text
        A31: Book and lyrics by Author of the textual content of a
            musical drama: see also A04 and A05
        A32: Contributions by Author of additional contributions to the
            text
        A33: Appendix by Author of appendix
        A34: Index by Compiler of index
        A35: Drawings by
        A36: Cover design or artwork by Use also for the cover artist of
            a graphic novel or comic book if named separately
        A37: Preliminary work by Responsible for preliminary work on
            which the work is based
        A38: Original author Author of the first edition (usually of a
            standard work) who is not an author of the current edition
        A39: Maps by Maps drawn or otherwise contributed by
        A40: Inked or colored by Use for secondary creators when
            separate persons are named as having respectively drawn and
            inked/colored/finished artwork, eg for a graphic novel or
            comic book. Use with A12 for ‘drawn by’. Use A40 for
            ‘finished by’, but prefer more specific codes A46 to A48
            instead of A40 unless the more specific secondary roles are
            inappropriate, unclear or unavailable
        A41: Paper engineering by Designer or paper engineer of die-
            cuts, press-outs or of pop-ups in a pop-up book, who may be
            different from the illustrator
        A42: Continued by Use where a standard work is being continued
            by somebody other than the original author
        A43: Interviewer
        A44: Interviewee
        A45: Comic script by Writer of dialogue, captions in a comic
            book (following an outline by the primary writer)
        A46: Inker Renders final comic book line art based on work of
            the illustrator or penciller (code A12). Preferred to code
            A40
        A47: Colorist Provides comic book color art and effects.
            Preferred to code A40
        A48: Letterer Creates comic book text balloons and other text
            elements (where this is a distinct role from script writer
            and/or illustrator), or creates calligraphy in non-comic
            products
        A49: Cover inker Renders final comic book cover line art based
            on work of the cover designer (code A36), where different
            from the inker of the interior line art. Only for use in
            ONIX 3.0 or later
        A50: Cover colorist Provides comic book cover color art and
            effects, where different from the colorist of the interior
            art and effects. Only for use in ONIX 3.0 or later
        A51: Research by Person or organization responsible for
            performing research on which the work is based. Only for use
            in ONIX 3.0 or later
        A52: Original character design (for comic books). Only for use
            in ONIX 3.0 or later
        A99: Other primary creator Other type of primary creator not
            specified above
        B01: Edited by
        B02: Revised by
        B03: Retold by
        B04: Abridged by
        B05: Adapted by See also B22 (Dramatized by)
        B06: Translated by
        B07: As told by
        B08: Translated with commentary by This code applies where a
            translator has provided a commentary on issues relating to
            the translation. If the translator has also provided a
            commentary on the work itself, codes B06 and A21 should be
            used
        B09: Series edited by Name of a series editor when the product
            belongs to a series
        B10: Edited and translated by
        B11: Editor-in-chief
        B12: Guest editor
        B13: Volume editor
        B14: Editorial board member
        B15: Editorial coordination by
        B16: Managing editor
        B17: Founded by Usually the founder editor of a serial
            publication (de: Begruendet von)
        B18: Prepared for publication by
        B19: Associate editor
        B20: Consultant editor Use also for ‘advisory editor’, ‘series
            advisor’, ‘editorial consultant’ etc
        B21: General editor
        B22: Dramatized by See also B05 (Adapted by)
        B23: General rapporteur In Europe, an expert editor who takes
            responsibility for the legal content of a collaborative law
            volume
        B24: Literary editor Editor who is responsible for establishing
            the text used in an edition of a literary work, where this
            is recognized as a distinctive role (es: editor literario)
        B25: Arranged by (music)
        B26: Technical editor Responsible for the technical accuracy and
            language, may also be involved in coordinating and preparing
            technical material for publication
        B27: Thesis advisor or supervisor
        B28: Thesis examiner
        B29: Scientific editor Responsible overall for the scientific
            content of the publication
        B30: Historical advisor Only for use in ONIX 3.0 or later
        B31: Original editor Editor of the first edition (usually of a
            standard work) who is not an editor of the current edition.
            Only for use in ONIX 3.0 or later
        B32: Translation revised by Where possible, use with B06 for the
            original translator. Only for use in ONIX 3.0 or later
        B33: Transcribed by As told to. Use with narratives drawn from
            an oral tradition, and with B03 (Retold by), B07 (As told
            by) or A28 (Interpreted through). Only for use in ONIX 3.0
            or later
        B34: Sensitivity reader / editor Reader or editor responsible
            for ensuring the text is free of offensive, potentially
            offensive or insensitive language, is inclusive and free
            from bias, and avoids stereotypical characterization. Only
            for use in ONIX 3.0 or later
        B35: Image descriptions by Creator of alternative image
            descriptions for accessibility purposes. Only for use in
            ONIX 3.0 or later
        B36: Text modernized or updated by Use for modernization or
            minor updating of language, but not for original
            contributions to the text
        B99: Other adaptation by Other type of adaptation or editing not
            specified above
        C01: Compiled by For puzzles, directories, statistics, etc
        C02: Selected by For textual material (eg for an anthology)
        C03: Non-text material selected by Eg for a collection of
            photographs etc
        C04: Curated by Eg for an exhibition
        C99: Other compilation by Other type of compilation not
            specified above
        D01: Producer Of a film, of a theatrical or multimedia
            production, of dramatized audio etc
        D02: Director Of a film, of a theatrical or multimedia
            production, of dramatized audio etc
        D03: Conductor Conductor of a musical performance
        D04: Choreographer Of a dance performance. Only for use in ONIX
            3.0 or later
        D99: Other direction by Other type of direction not specified
            above
        E01: Actor Performer in a dramatized production (including a
            voice actor in an audio production)
        E02: Dancer
        E03: Narrator Where the narrator is a character in a dramatized
            production (including a voice actor in an audio production).
            For the ‘narrator’ of a non-dramatized audiobook, use code
            E07
        E04: Commentator
        E05: Vocal soloist Singer etc
        E06: Instrumental soloist
        E07: Read by Reader of recorded text, as in an audiobook
        E08: Performed by (orchestra, band, ensemble) Name of a musical
            group in a performing role
        E09: Speaker Of a speech, lecture etc
        E10: Presenter Introduces and links other contributors and
            material, eg within a documentary
        E11: Introduction read by Reader of recorded introduction (or
            other ‘front matter’) in an audiobook. Only for use in ONIX
            3.0 or later
        E99: Performed by Other type of performer not specified above:
            use for a recorded performance which does not fit a category
            above, eg a performance by a stand-up comedian
        F01: Filmed/photographed by Cinematographer, etc
        F02: Editor (film or video)
        F99: Other recording by Other type of recording not specified
            above
        Z01: Assisted by Contributor must follow another contributor
            with any contributor role, and placement should therefore be
            controlled by contributor sequence numbering to ensure the
            correct association
        Z02: Honored/dedicated to
        Z03: Enacting jurisdiction For publication of laws, regulations,
            rulings etc. Only for use in ONIX 3.0 or later
        Z04: Peer reviewed Use with &lt;UnnamedPersons&gt; code 02 as a
            ‘flag’ to indicate the publication is anonymously peer-
            reviewed. Only for use in ONIX 3.0 or later
        Z05: Posthumously completed by Contributor must follow another
            (posthumous) contributor with any contributor role, and
            placement should therefore be controlled by contributor
            sequence numbering to ensure the correct association. Only
            for use in ONIX 3.0 or later
        Z06: In association with Contributor must follow another
            contributor with any contributor role, and placement should
            therefore be controlled by contributor sequence numbering to
            ensure the correct association. See also ‘published in
            association with’ in List 45. Only for use in ONIX 3.0 or
            later
        Z98: (Various roles) For use ONLY with ‘et al’ or ‘Various’
            within &lt;UnnamedPersons&gt;, where the roles of the
            multiple contributors vary
        Z99: Other Other creative responsibility not falling within A to
            F above
    """

    A01 = "A01"
    A02 = "A02"
    A03 = "A03"
    A04 = "A04"
    A05 = "A05"
    A06 = "A06"
    A07 = "A07"
    A08 = "A08"
    A09 = "A09"
    A10 = "A10"
    A11 = "A11"
    A12 = "A12"
    A13 = "A13"
    A14 = "A14"
    A15 = "A15"
    A16 = "A16"
    A17 = "A17"
    A18 = "A18"
    A19 = "A19"
    A20 = "A20"
    A21 = "A21"
    A22 = "A22"
    A23 = "A23"
    A24 = "A24"
    A25 = "A25"
    A26 = "A26"
    A27 = "A27"
    A28 = "A28"
    A29 = "A29"
    A30 = "A30"
    A31 = "A31"
    A32 = "A32"
    A33 = "A33"
    A34 = "A34"
    A35 = "A35"
    A36 = "A36"
    A37 = "A37"
    A38 = "A38"
    A39 = "A39"
    A40 = "A40"
    A41 = "A41"
    A42 = "A42"
    A43 = "A43"
    A44 = "A44"
    A45 = "A45"
    A46 = "A46"
    A47 = "A47"
    A48 = "A48"
    A49 = "A49"
    A50 = "A50"
    A51 = "A51"
    A52 = "A52"
    A99 = "A99"
    B01 = "B01"
    B02 = "B02"
    B03 = "B03"
    B04 = "B04"
    B05 = "B05"
    B06 = "B06"
    B07 = "B07"
    B08 = "B08"
    B09 = "B09"
    B10 = "B10"
    B11 = "B11"
    B12 = "B12"
    B13 = "B13"
    B14 = "B14"
    B15 = "B15"
    B16 = "B16"
    B17 = "B17"
    B18 = "B18"
    B19 = "B19"
    B20 = "B20"
    B21 = "B21"
    B22 = "B22"
    B23 = "B23"
    B24 = "B24"
    B25 = "B25"
    B26 = "B26"
    B27 = "B27"
    B28 = "B28"
    B29 = "B29"
    B30 = "B30"
    B31 = "B31"
    B32 = "B32"
    B33 = "B33"
    B34 = "B34"
    B35 = "B35"
    B36 = "B36"
    B99 = "B99"
    C01 = "C01"
    C02 = "C02"
    C03 = "C03"
    C04 = "C04"
    C99 = "C99"
    D01 = "D01"
    D02 = "D02"
    D03 = "D03"
    D04 = "D04"
    D99 = "D99"
    E01 = "E01"
    E02 = "E02"
    E03 = "E03"
    E04 = "E04"
    E05 = "E05"
    E06 = "E06"
    E07 = "E07"
    E08 = "E08"
    E09 = "E09"
    E10 = "E10"
    E11 = "E11"
    E99 = "E99"
    F01 = "F01"
    F02 = "F02"
    F99 = "F99"
    Z01 = "Z01"
    Z02 = "Z02"
    Z03 = "Z03"
    Z04 = "Z04"
    Z05 = "Z05"
    Z06 = "Z06"
    Z98 = "Z98"
    Z99 = "Z99"
