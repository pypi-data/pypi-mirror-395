from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List15(Enum):
    """
    Title type.

    Attributes:
        VALUE_00: Undefined
        VALUE_01: Distinctive title (book); Cover title (serial); Title
            of content item, collection, or resource The full text of
            the distinctive title of the item, without abbreviation or
            abridgement. For books, generally taken from the title page
            (see codes 11–15 where an alternative title is provided on
            cover or spine). Where the item is an omnibus edition
            containing two or more works by the same author, and there
            is no separate combined title, a distinctive title may be
            constructed (by the sender) by concatenating the individual
            titles, with suitable punctuation, as in ‘Pride and
            prejudice / Sense and sensibility / Northanger Abbey’. Where
            the title alone is not distinctive, recipients may add
            elements taken from a collection title and part number etc
            to create a distinctive title – but these elements should be
            provided separately by the sender
        VALUE_02: ISSN key title of serial Serials only
        VALUE_03: Title in original language Where the subject of the
            ONIX record is a translated item
        VALUE_04: Title acronym or initialism For serials: an acronym or
            initialism of Title Type 01, eg ‘JAMA’, ‘JACM’
        VALUE_05: Abbreviated title An abbreviated form of Title Type 01
        VALUE_06: Title in other language A translation of Title Type 01
            or 03, or an independent title, used when the work is
            translated into another language, sometimes termed a
            ‘parallel title’
        VALUE_07: Thematic title of journal issue Serials only: when a
            journal issue is explicitly devoted to a specified topic
        VALUE_08: Former title Books or serials: when an item was
            previously published under another title
        VALUE_10: Distributor’s title For books: the title carried in a
            book distributor’s title file: frequently incomplete, and
            may include elements not properly part of the title. Usually
            limited in length and character set (eg to about 30 ASCII
            characters) for use on other e-commerce documentation
        VALUE_11: Alternative title on cover An alternative title that
            appears on the cover of a book
        VALUE_12: Alternative title on back An alternative title that
            appears on the back of a book
        VALUE_13: Expanded title An expanded form of the title, eg the
            title of a school text book with grade and type and other
            details added to make the title meaningful, where otherwise
            it would comprise only the curriculum subject. This title
            type is required for submissions to the Spanish ISBN Agency
        VALUE_14: Alternative title An alternative title that the book
            is widely known by, whether it appears on the book or not
            (including a title used in another market – but see code 06
            for translations – or a working title previously used in
            metadata but replaced before publication)
        VALUE_15: Alternative title on spine An alternative title that
            appears on the spine of a book. Only for use in ONIX 3.0 or
            later
        VALUE_16: Translated from title Where the subject of the ONIX
            record is a translated item, but has been translated via
            some intermediate language. Title type 16 is distinct from
            title type 03. Only for use in ONIX 3.0 or later
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
