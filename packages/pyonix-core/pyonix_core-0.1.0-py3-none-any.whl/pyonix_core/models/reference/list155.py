from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List155(Enum):
    """
    Content date role.

    Attributes:
        VALUE_01: Publication date Nominal date of publication (of the
            content item or supporting resource)
        VALUE_04: Broadcast date Date when a TV or radio program was /
            will be broadcast
        VALUE_14: From date Date from which a content item or supporting
            resource may be referenced or used. The content is embargoed
            until this date
        VALUE_15: Until date Date until which a content item or
            supporting resource may be referenced or used
        VALUE_17: Last updated Date when a resource was last changed or
            updated
        VALUE_24: From… until date Combines From date and Until date to
            define a period (both dates are inclusive). Use for example
            with dateformat 06
        VALUE_27: Available from Date from which a supporting resource
            is available for download. Note that this date also implies
            that it can be immediately displayed to the intended
            audience, unless a From date (code 14) is also supplied and
            is later than the Available from date
        VALUE_28: Available until Date until which a supporting resource
            is available for download. Note that this date does not
            imply it must be removed from display to the intended
            audience on this date – for this, use Until date (code 15)
        VALUE_31: Associated start date Start date referenced by the
            supporting resource, for example, the ‘earliest exam date’
            for an official recommendation
        VALUE_32: Associated end date End date referenced by the
            supporting resource, for example, the ‘latest exam date’ for
            an official recommendation
    """

    VALUE_01 = "01"
    VALUE_04 = "04"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_17 = "17"
    VALUE_24 = "24"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_31 = "31"
    VALUE_32 = "32"
