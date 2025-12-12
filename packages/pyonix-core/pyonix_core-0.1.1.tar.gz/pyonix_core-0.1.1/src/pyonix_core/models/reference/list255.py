from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List255(Enum):
    """
    Insert point type.

    Attributes:
        ALP: Adjacent to logical page Insert appears after an even
            numbered or before an odd numbered logical page.
            &lt;InsertPointValue&gt; is an integer page number
        APP: Adjacent to physical page Insert appears after an even
            numbered or before an odd numbered printed page number.
            &lt;InsertPointValue&gt; is an integer page number
        ATC: At timecode Insert appears in the body at a specific
            timecode (hours, minutes, seconds, counted from the
            beginning of the product before any inserts are added).
            &lt;InsertPointValue&gt; is in the format HHHMMSS. Fill with
            leading zeroes if any elements are missing. If centisecond
            precision is required, use HHHMMSScc
        AHL: Adjacent to HTML label Insert appears before the block-
            level HTML element – &amp;lt;InsertPointValue&gt; is the
            value of the id or name attribute of the block-level element
            (which must be unique within the body of the product)
    """

    ALP = "ALP"
    APP = "APP"
    ATC = "ATC"
    AHL = "AHL"
