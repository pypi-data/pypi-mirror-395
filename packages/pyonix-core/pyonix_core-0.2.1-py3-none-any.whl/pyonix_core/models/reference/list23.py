from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List23(Enum):
    """
    Extent type.

    Attributes:
        VALUE_00: Main content page count The highest-numbered page in a
            single numbered sequence of main content, usually the
            highest Arabic-numbered page in a book; or, for books
            without page numbers or (rarely) with multiple numbered
            sequences of main content, the total number of pages that
            carry the main content of the book. Note that this may
            include numbered but otherwise blank pages (eg pages
            inserted to ensure chapters start on a recto page) and may
            exclude unnumbered (but contentful) pages such as those in
            inserts/plate sections. It should exclude pages of back
            matter (eg any index) even when their numbering sequence
            continues from the main content. Either this or the Content
            Page count is the preferred page count for most books for
            the general reader. For books with substantial front and/or
            back matter, include also Front matter (03) and Back matter
            (04) page counts, or Total numbered pages (05). For books
            with inserts (plate sections), also include Total unnumbered
            insert page count whenever possible
        VALUE_02: Total text length Number of words or characters of
            natural language text
        VALUE_03: Front matter page count The total number of numbered
            (usually Roman-numbered) pages that precede the main content
            of a book. This usually consists of various title and
            imprint pages, table of contents, an introduction, preface,
            foreword, etc
        VALUE_04: Back matter page count The total number of numbered
            (often Roman-numbered) pages that follow the main content of
            a book. This usually consists of an afterword, appendices,
            endnotes, index, etc. It excludes extracts or ‘teaser’
            material from other works, and blank (or advertising) pages
            that are present only for convenience of printing and
            binding
        VALUE_05: Total numbered pages The sum of all Roman- and Arabic-
            numbered pages. Note that this may include numbered but
            otherwise blank pages (eg pages inserted to ensure chapters
            start on a recto page) and may exclude unnumbered (but
            contentful) pages such as those in inserts/plate sections.
            It is the sum of the main content (00), front matter (03)
            and back matter (04) page counts
        VALUE_06: Production page count The total number of pages in a
            book, including unnumbered pages, front matter, back matter,
            etc. This includes any extracts or ‘teaser’ material from
            other works, and blank pages at the back that carry no
            content and are present only for convenience of printing and
            binding
        VALUE_07: Absolute page count The total number of pages of the
            book counting the cover as page 1. This page count type
            should be used only for digital publications delivered with
            fixed pagination
        VALUE_08: Number of pages in print counterpart The total number
            of pages (equivalent to the Content page count, code 11) in
            the print counterpart of a digital product delivered without
            fixed pagination, or of an audio product
        VALUE_09: Duration Total duration in time, expressed in the
            specified extent unit. This is the ‘running time’ equivalent
            of code 11
        VALUE_10: Notional number of pages in digital product An
            estimate of the number of ‘pages’ in a digital product
            delivered without fixed pagination, and with no print
            counterpart, given as an indication of the size of the work.
            Equivalent to code 08, but exclusively for digital or audio
            products
        VALUE_11: Content page count The sum of all Roman- and Arabic-
            numbered and contentful unnumbered pages. Sum of page counts
            with codes 00, 03, 04 and 12, and also the sum of 05 and 12
        VALUE_12: Total unnumbered insert page count The total number of
            unnumbered pages with content inserted within the main
            content of a book – for example inserts/plate sections that
            are not numbered
        VALUE_13: Duration of introductory matter Duration in time,
            expressed in the specified extent units, of introductory
            matter. This is the ‘running time’ equivalent of code 03,
            and comprises any significant amount of running time
            represented by a musical intro, announcements, titles,
            introduction or other material prefacing the main content
        VALUE_14: Duration of main content Duration in time, expressed
            in the specified extent units, of the main content. This is
            the ‘running time’ equivalent of code 00, and excludes time
            represented by announcements, titles, introduction or other
            prefatory material or ‘back matter’
        VALUE_15: Duration of back matter Duration in time, expressed in
            the specified extent units, of any content that follows the
            main content of a book. This may consist of an afterword,
            appendices, endnotes, end music etc. It excludes extracts or
            ‘teaser’ material from other works. This is the ‘running
            time’ equivalent of code 04
        VALUE_16: Production duration Duration in time, expressed in the
            specified extent units, of the complete content of a book.
            This is the ‘running time’ equivalent of code 06, and
            includes time represented by musical themes, announcements,
            titles, introductory and other prefatory material, plus
            ‘back matter’ such as any afterword, appendices, plus any
            extracts or ‘teaser’ material from other works
        VALUE_17: Number of cards In a pack of educational flash cards,
            playing cards, postcards, greeting cards etc. Only for use
            in ONIX 3.0 or later
        VALUE_18: Number of write-in pages Count of the number of pages
            within the main content page count that are blank or
            substantially blank, intended for the reader to fill in (eg
            in a journal). Only for use in ONIX 3.0 or later
        VALUE_22: Filesize Approximate size of a digital file or package
            (in the form it is downloaded), expressed in the specified
            extent unit
        VALUE_23: Storage filesize Approximate size of storage space
            required for a digital file or package in the form in which
            it is usually stored for use on a device, where this is
            different from the download filesize (see code 22), and
            expressed in the specified extent unit. Only for use in ONIX
            3.0 or later
    """

    VALUE_00 = "00"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_22 = "22"
    VALUE_23 = "23"
