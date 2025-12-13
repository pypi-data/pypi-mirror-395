from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List154(Enum):
    """
    Content audience.

    Attributes:
        VALUE_00: Unrestricted Any audience
        VALUE_01: Restricted Distribution by agreement between the
            parties to the ONIX exchange (this value is provided to
            cover applications where ONIX content includes material
            which is not for general distribution)
        VALUE_02: Booktrade Distributors, bookstores, publisher’s own
            staff etc
        VALUE_03: End-customers
        VALUE_04: Librarians
        VALUE_05: Teachers
        VALUE_06: Students
        VALUE_07: Press Press or other media
        VALUE_08: Shopping comparison service Where a specially
            formatted description is required for this audience
        VALUE_09: Search engine index Text not intended for display, but
            may be used (in addition to any less restricted text) for
            indexing and search
        VALUE_10: Bloggers (Including vloggers, influencers etc) Where
            this is distinct from end customers or the Press
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
