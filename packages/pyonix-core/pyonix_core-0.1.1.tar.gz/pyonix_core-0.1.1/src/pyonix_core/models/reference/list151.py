from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List151(Enum):
    """
    Contributor place relator.

    Attributes:
        VALUE_00: Associated with To express unknown relationship types
            (for use when expressing legacy ONIX 2.1 data in ONIX 3.0)
        VALUE_01: Born in
        VALUE_02: Died in
        VALUE_03: Formerly resided in
        VALUE_04: Currently resides in
        VALUE_05: Educated in
        VALUE_06: Worked in
        VALUE_07: Flourished in (‘Floruit’)
        VALUE_08: Citizen of Or nationality. For use with country codes
            only
        VALUE_09: Registered in The place of legal registration of an
            organization
        VALUE_10: Operating from The place an organization or part of an
            organization is based or operates from
        VALUE_11: Eligible for geographical marketing programs
            Contributor is eligible for national, regional or local
            marketing support. Use with country code, region code or
            country/region plus location, as appropriate
        VALUE_12: Indigenous to (Indigenous geographies or
            territorialities) Use to indicate that an Indigenous
            contributor has chosen to be publicly identified as an
            Indigenous person associated with a particular territory or
            geography. Used with &lt;LocationName&gt; (in addition to
            country or region) to indicate an Indigenous territoriality
            or geography
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
