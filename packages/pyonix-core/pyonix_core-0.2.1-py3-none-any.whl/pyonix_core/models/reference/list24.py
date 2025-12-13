from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List24(Enum):
    """
    Extent unit.

    Attributes:
        VALUE_00: Physical pieces Unbound sheets or leaves, where
            ‘pages’ is not appropriate. For example a count of the
            individual number of cards in a pack. Only for use in ONIX
            3.0 or later. For number of pieces in eg a jigsaw, kit,
            board game, see &lt;ProductFormFeature&gt; and code 22 from
            list 79
        VALUE_01: Characters Approximate number of characters (including
            spaces) of natural language text. Only for use in ONIX 3.0
            or later
        VALUE_02: Words Approximate number of words of natural language
            text
        VALUE_03: Pages
        VALUE_04: Hours (integer and decimals)
        VALUE_05: Minutes (integer and decimals)
        VALUE_06: Seconds (integer only)
        VALUE_11: Tracks Of an audiobook on CD (or a similarly divided
            selection of audio files). Conventionally, each track is 3–6
            minutes of running time, and track counts are misleading and
            inappropriate if the average track duration is significantly
            more or less than this. Note that track breaks are not
            necessarily aligned with structural breaks in the text (eg
            chapter breaks)
        VALUE_12: Discs Of an audiobook on multiple Red Book audio CDs.
            Conventionally, each disc is 60–70 minutes of running time,
            and disc counts are misleading and inappropriate if the
            average disc duration is significantly more or less than
            this (for example if the discs are Yellow Book CDs
            containing mp3 files). Note that disc breaks are not
            necessarily aligned with structural breaks in the text (eg
            chapter breaks). Only for use in ONIX 3.0 or later
        VALUE_14: Hours HHH Fill with leading zeroes if any elements are
            missing
        VALUE_15: Hours and minutes HHHMM Fill with leading zeroes if
            any elements are missing
        VALUE_16: Hours minutes seconds HHHMMSS Fill with leading zeroes
            if any elements are missing. If centisecond precision is
            required, use HHHMMSScc. Only for use in ONIX 3.0 or later
        VALUE_17: Bytes
        VALUE_18: Kbytes
        VALUE_19: Mbytes
        VALUE_31: Chapters Number of chapters (or other similar
            subdivisions) of the content. Only for use in ONIX 3.0 or
            later
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_31 = "31"
