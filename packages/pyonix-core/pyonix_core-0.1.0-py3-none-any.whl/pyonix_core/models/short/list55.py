from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List55(Enum):
    """
    Date format.

    Attributes:
        VALUE_00: YYYYMMDD Common Era year, month and day (default for
            most dates)
        VALUE_01: YYYYMM Year and month
        VALUE_02: YYYYWW Year and week number
        VALUE_03: YYYYQ Year and quarter (Q = 1, 2, 3, 4, with 1 = Jan
            to Mar)
        VALUE_04: YYYYS Year and season (S = 1, 2, 3, 4, with 1 =
            ‘Spring’)
        VALUE_05: YYYY Year (default for some dates)
        VALUE_06: YYYYMMDDYYYYMMDD Spread of exact dates
        VALUE_07: YYYYMMYYYYMM Spread of months
        VALUE_08: YYYYWWYYYYWW Spread of week numbers
        VALUE_09: YYYYQYYYYQ Spread of quarters
        VALUE_10: YYYYSYYYYS Spread of seasons
        VALUE_11: YYYYYYYY Spread of years
        VALUE_12: Text string For complex, approximate or uncertain
            dates, or dates BCE. Suggested maximum length 100 characters
        VALUE_13: YYYYMMDDThhmm Exact time. Use ONLY when exact times
            with hour/minute precision are relevant. By default, time is
            local. Alternatively, the time may be suffixed with an
            optional ‘Z’ for UTC times, or with ‘+’ or ‘-’ and an hhmm
            timezone offset from UTC. Times without a timezone are
            ‘rolling’ local times, times qualified with a timezone
            (using Z, + or -) specify a particular instant in time
        VALUE_14: YYYYMMDDThhmmss Exact time. Use ONLY when exact times
            with second precision are relevant. By default, time is
            local. Alternatively, the time may be suffixed with an
            optional ‘Z’ for UTC times, or with ‘+’ or ‘-’ and an hhmm
            timezone offset from UTC. Times without a timezone are
            ‘rolling’ local times, times qualified with a timezone
            (using Z, + or -) specify a particular instant in time
        VALUE_20: YYYYMMDD (H) Year month day (Hijri calendar)
        VALUE_21: YYYYMM (H) Year and month (Hijri calendar)
        VALUE_25: YYYY (H) Year (Hijri calendar)
        VALUE_32: Text string (H) For complex, approximate or uncertain
            dates (Hijri calendar), text would usually be in Arabic
            script. Suggested maximum length 100 characters
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
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_25 = "25"
    VALUE_32 = "32"
