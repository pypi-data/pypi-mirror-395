from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List147(Enum):
    """
    Unit of usage.

    Attributes:
        VALUE_01: Copies Maximum number of copies that may be made of a
            permitted extract
        VALUE_02: Characters Maximum number of characters in a permitted
            extract for a specified usage
        VALUE_03: Words Maximum number of words in a permitted extract
            for a specified usage
        VALUE_04: Pages Maximum number of pages in a permitted extract
            for a specified usage
        VALUE_05: Percentage Maximum percentage of total content in a
            permitted extract for a specified usage
        VALUE_06: Devices Maximum number of devices in ‘share group’
        VALUE_07: Concurrent users Maximum number of concurrent users.
            NB where the number of concurrent users is specifically not
            limited, set the number of concurrent users to zero
        VALUE_15: Users Maximum number of licensed individual users,
            independent of concurrency of use
        VALUE_19: Concurrent classes Maximum number of licensed
            concurrent classes of user. A ‘class’ is a group of learners
            attending a specific course or lesson and generally taught
            as a group
        VALUE_20: Classes Maximum number of licensed classes of
            learners, independent of concurrency of use and the number
            of users per class
        VALUE_31: Institutions Maximum number of licensed institutions,
            independent of concurrency of use and the number of classes
            or individuals per institution
        VALUE_08: Percentage per time period Maximum percentage of total
            content which may be used in a specified usage per time
            period; the time period being specified as another
            &lt;EpubUsageLimit&gt; Quantity
        VALUE_09: Days Maximum time period in days (beginning from
            product purchase or activation)
        VALUE_13: Weeks Maximum time period in weeks
        VALUE_14: Months Maximum time period in months
        VALUE_16: Hours minutes and seconds Maximum amount of time in
            hours, minutes and seconds allowed in a permitted extract
            for a specified usage, in the format HHHMMSS (7 digits, with
            leading zeros if necessary)
        VALUE_27: Days (fixed start) Maximum time period in days
            (beginning from the product publication date). In effect,
            this defines a fixed end date for the license independent of
            the purchase or activation date
        VALUE_28: Weeks (fixed start) Maximum time period in weeks
        VALUE_29: Months (fixed start) Maximum time period in months
        VALUE_10: Times Maximum number of times a specified usage event
            may occur (in the lifetime of the product)
        VALUE_22: Times per day Maximum frequency a specified usage
            event may occur (per day)
        VALUE_23: Times per month Maximum frequency a specified usage
            event may occur (per month)
        VALUE_24: Times per year Maximum frequency a specified usage
            event may occur (per year)
        VALUE_21: Dots per inch Maximum resolution of printed or
            copy/pasted extracts
        VALUE_26: Dots per cm Maximum resolution of printed or
            copy/pasted extracts
        VALUE_11: Allowed usage start page Page number where allowed
            usage begins. &lt;Quantity&gt; should contain an absolute
            page number, counting the cover as page 1. (This type of
            page numbering should not be used where the e-publication
            has no fixed pagination). Use with (max number of) Pages,
            Percentage of content, or End page to specify pages allowed
            in Preview
        VALUE_12: Allowed usage end page Page number at which allowed
            usage ends. &lt;Quantity&gt; should contain an absolute page
            number, counting the cover as page 1. (This type of page
            numbering should not be used where the e-publication has no
            fixed pagination). Use with Start page to specify pages
            allowed in a preview
        VALUE_17: Allowed usage start time Time at which allowed usage
            begins. &lt;Quantity&gt; should contain an absolute time,
            counting from the beginning of an audio or video product, in
            the format HHHMMSS or HHHMMSScc. Use with Time, Percentage
            of content, or End time to specify time-based extract
            allowed in Preview
        VALUE_18: Allowed usage end time Time at which allowed usage
            ends. &lt;Quantity&gt; should contain an absolute time,
            counting from the beginning of an audio or video product, in
            the format HHHMMSS or HHHMMSScc. Use with Start time to
            specify time-based extract allowed in Preview
        VALUE_98: Valid from The date from which the usage constraint
            applies. &lt;Quantity&gt; is in the format YYYYMMDD
        VALUE_99: Valid to The date until which the usage constraint
            applies. &lt;Quantity&gt; is in the format YYYYMMDD
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_15 = "15"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_31 = "31"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_16 = "16"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_10 = "10"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_21 = "21"
    VALUE_26 = "26"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_98 = "98"
    VALUE_99 = "99"
