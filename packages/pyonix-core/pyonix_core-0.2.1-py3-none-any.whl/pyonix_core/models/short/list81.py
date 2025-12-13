from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List81(Enum):
    """
    Product content type.

    Attributes:
        VALUE_10: Text Readable text of the main content: this value is
            required, together with applicable &lt;ProductForm&gt; and
            &lt;ProductFormDetail&gt; values, to designate an e-book or
            other digital or physical product whose primary content is
            text. Note ‘text’ is ‘text-as-text’, not ‘text as an image’
            or images of text
        VALUE_15: Extensive links between internal content E-publication
            contains a significant number of actionable (clickable)
            cross-references, hyperlinked notes and annotations, or with
            other actionable links between largely textual elements (eg
            quiz/test questions, ‘choose your own ending’ etc)
        VALUE_14: Extensive links to external content E-publication
            contains a significant number of actionable (clickable) web
            links to external content, downloadable resources,
            supplementary material, etc
        VALUE_51: Links to external interactive content Publication
            contains actionable (clickable) links to external
            interactive content. Only for use in ONIX 3.0 or later
        VALUE_16: Additional text not part of main content Publication
            contains additional textual content such as an interview,
            feature article, essay, bibliography, quiz/test, other
            background material, or text that is not included in a
            primary or ‘unenhanced’ version. Note ‘text’ is ‘text-as-
            text’, not ‘text as an image’ or images of text
        VALUE_45: Text within images Including text-as-text embedded in
            diagrams, charts, or within images containing speech
            balloons, thought bubbles, captions etc. Note this does not
            include ‘text as an image’ or images of text (for which see
            code 49). Only for use in ONIX 3.0 or later
        VALUE_41: Additional eye-readable links to external content
            Publication contains a significant number of web links
            (printed URLs, QR codes etc). Only for use in ONIX 3.0 or
            later
        VALUE_17: Promotional text for other book product Publication
            contains supplementary text as promotional content such as,
            for example, a teaser chapter
        VALUE_11: Musical notation
        VALUE_07: Still images / graphics Includes any type of
            illustrations. Use only when no more detailed specification
            is provided
        VALUE_18: Photographs Whether in a plate section / insert, or
            not
        VALUE_19: Figures, diagrams, charts, graphs Including other
            ‘mechanical’ (ie non-photographic) illustrations
        VALUE_20: Additional images / graphics not part of main work
            Publication is enhanced with additional images or graphical
            content such as supplementary photographs that are not
            included in a primary or ‘unenhanced’ version
        VALUE_12: Maps and/or other cartographic content
        VALUE_47: Chemical content Indicates that the publication
            contains chemical notations, formulae. Only for use in ONIX
            3.0 or later
        VALUE_48: Mathematical content Indicates that the publication
            contains mathematical notation, equations, formulae. Only
            for use in ONIX 3.0 or later
        VALUE_46: Decorative images or graphics Publication contains
            visual content that is purely decorative and are not
            necessary to understanding of the content. Only for use in
            ONIX 3.0 or later
        VALUE_42: Assessment material eg Questions or student exercises,
            problems, quizzes or tests (as an integral part of the
            work). Only for use in ONIX 3.0 or later
        VALUE_01: Audiobook Audio recording of a reading of a book or
            other text
        VALUE_02: Performance – spoken word Audio recording of a drama
            or other spoken word performance
        VALUE_13: Other speech content eg an interview, speech, lecture
            or commentary / discussion, not a ‘reading’ or
            ‘performance’)
        VALUE_03: Music recording Audio recording of a music
            performance, including musical drama and opera
        VALUE_04: Other audio Audio recording of other sound, eg
            birdsong, sound effects, ASMR material
        VALUE_49: Images of text At least some text – including text
            within other images – is ‘text as an image’ (ie a picture of
            text). Only for use in ONIX 3.0 or later
        VALUE_21: Partial performance – spoken word Audio recording of a
            reading, performance or dramatization of part of the work
        VALUE_22: Additional audio content not part of main content
            Product includes additional pre-recorded audio of any
            supplementary material such as full or partial reading,
            lecture, performance, dramatization, interview, background
            documentary or other audio content not included in the
            primary or ‘unenhanced’ version
        VALUE_23: Promotional audio for other book product eg Reading of
            teaser chapter
        VALUE_06: Video Includes Film, video, animation etc. Use only
            when no more detailed specification is provided. Formerly
            ‘Moving images’
        VALUE_26: Video recording of a reading
        VALUE_50: Video content without audio Publication contains video
            material with no audio recording or narration (but may have
            music or textual subtitles) . Only for use in ONIX 3.0 or
            later
        VALUE_27: Performance – visual Video recording of a drama or
            other performance, including musical performance
        VALUE_24: Animated / interactive illustrations eg animated
            diagrams, charts, graphs or other illustrations (usually
            without sound)
        VALUE_25: Narrative animation eg cartoon, animatic or CGI
            animation (usually includes sound)
        VALUE_28: Other video Other video content eg interview, not a
            reading or performance
        VALUE_29: Partial performance – video Video recording of a
            reading, performance or dramatization of part of the work
        VALUE_30: Additional video content not part of main work
            E-publication is enhanced with video recording of full or
            partial reading, performance, dramatization, interview,
            background documentary or other content not included in the
            primary or ‘unenhanced’ version
        VALUE_31: Promotional video for other book product eg Book
            trailer
        VALUE_05: Game / Puzzle No multi-user functionality. Formerly
            just ‘Game’
        VALUE_32: Contest Includes some degree of multi-user
            functionality
        VALUE_08: Software Largely ‘content free’
        VALUE_09: Data Data files
        VALUE_33: Data set plus software
        VALUE_34: Blank pages or spaces Entire pages or blank spaces,
            forms, boxes, write-in pages etc, intended to be filled in
            by the reader
        VALUE_35: Advertising content Use only where type of advertising
            content is not stated
        VALUE_37: Advertising – first party ‘Back ads’ – promotional
            content for other books (that does not include sample
            content of those books, cf codes 17, 23)
        VALUE_36: Advertising – coupons Eg to obtain discounts on other
            products
        VALUE_38: Advertising – third party display
        VALUE_39: Advertising – third party textual
        VALUE_40: Scripting E-publication contains microprograms written
            (eg) in JavaScript and executed within the reading system.
            Only for use in ONIX 3.0 or later
        VALUE_43: Scripted pop-ups E-publication contains pop-ups or
            other functionality offering (eg) term definitions, cross-
            links or glossary entries [Note this should not include (eg)
            dictionary functionality that is part of the reading
            system.] Only for use in ONIX 3.0 or later
        VALUE_44: Sequential art Or pictorial narrative, usually panel-
            based. Images displayed in a specific order for the purpose
            of graphic storytelling or giving information (eg graphic
            novels, comics and manga). May include text integrated into
            the image (as speech and thought bubbles, textual ‘sound’
            effects, captions etc). Only for use in ONIX 3.0 or later
    """

    VALUE_10 = "10"
    VALUE_15 = "15"
    VALUE_14 = "14"
    VALUE_51 = "51"
    VALUE_16 = "16"
    VALUE_45 = "45"
    VALUE_41 = "41"
    VALUE_17 = "17"
    VALUE_11 = "11"
    VALUE_07 = "07"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_12 = "12"
    VALUE_47 = "47"
    VALUE_48 = "48"
    VALUE_46 = "46"
    VALUE_42 = "42"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_13 = "13"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_49 = "49"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_06 = "06"
    VALUE_26 = "26"
    VALUE_50 = "50"
    VALUE_27 = "27"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_05 = "05"
    VALUE_32 = "32"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_33 = "33"
    VALUE_34 = "34"
    VALUE_35 = "35"
    VALUE_37 = "37"
    VALUE_36 = "36"
    VALUE_38 = "38"
    VALUE_39 = "39"
    VALUE_40 = "40"
    VALUE_43 = "43"
    VALUE_44 = "44"
