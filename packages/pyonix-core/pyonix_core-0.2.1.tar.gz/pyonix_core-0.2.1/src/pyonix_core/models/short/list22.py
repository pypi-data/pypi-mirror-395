from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List22(Enum):
    """
    Language role.

    Attributes:
        VALUE_01: Language of text
        VALUE_02: Original language of a translated text Where the text
            in the original language is NOT part of the current product
        VALUE_03: Language of abstracts Where different from language of
            text: used mainly for serials
        VALUE_06: Original language in a multilingual edition Where the
            text in the original language is part of a bilingual or
            multilingual product
        VALUE_07: Translated language in a multilingual edition Where
            the text in a translated language is part of a bilingual or
            multilingual product
        VALUE_08: Language of audio track For example, on an audiobook
            or video product. Use for the only available audio track, or
            where there are multiple tracks (eg on a DVD), for an
            alternate language audio track that is NOT the original. (In
            the latter case, use code 11 for the original language audio
            if it is included in the product, or code 10 to identify an
            original language that is not present in the product)
        VALUE_09: Language of subtitles For example, on a DVD or digital
            video with closed or open captions / subtitles
        VALUE_10: Language of original audio track Where the audio in
            the original language is NOT part of the current product
        VALUE_11: Original language audio track in a multilingual
            product Where the audio in the original language is part of
            a multilingual product with multiple audio tracks
        VALUE_12: Language of notes Use for the language of footnotes,
            endnotes, annotations or commentary, instructions or
            guidance for use etc, where it is different from the
            language of the main text
        VALUE_13: Language of introduction / end matter Use for the
            language of any introductory text, prologue, etc, or
            epilogue, end matter, etc, where it is different from the
            language of the main text. Only for use in ONIX 3.0 or later
        VALUE_14: Target language of teaching / learning Eg for the book
            ‘Ingles para latinos’, English. For phrasebooks and language
            teaching, learning or study material. Wherever possible, the
            language should also be listed as the subject of the book.
            Only for use in ONIX 3.0 or later
        VALUE_15: Additional vocabulary / text in this language Use of
            significant words, phrases, quotations or short passages
            from a language other than the main language of the text, as
            an integral part of the text. This does not include
            ‘loanwords’, academic Latin, etc. Only for use in ONIX 3.0
            or later
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
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
