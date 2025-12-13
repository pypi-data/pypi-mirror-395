from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List92(Enum):
    """
    Supplier identifier type.

    Attributes:
        VALUE_01: Proprietary name ID scheme For example, a publisher’s
            own agent, suppier or location ID scheme. Note that a
            distinctive &lt;IDTypeName&gt; is required with proprietary
            identifiers
        VALUE_02: Proprietary Deprecated – use code 01
        VALUE_04: Börsenverein Verkehrsnummer
        VALUE_05: German ISBN Agency publisher identifier
        VALUE_06: GLN GS1 global location number (formerly EAN location
            number)
        VALUE_07: SAN Book trade Standard Address Number – US, UK etc
        VALUE_12: Distributeurscode Boekenbank Flemish supplier code
        VALUE_13: Fondscode Boekenbank Flemish publisher code
        VALUE_16: ISNI International Standard Name Identifier (used here
            to identify an organization). Only for use in ONIX 3.0 or
            later. See https://isni.org/
        VALUE_23: VAT Identity Number Identifier for a business
            organization for VAT purposes, eg within the EU’s VIES
            system. See
            http://ec.europa.eu/taxation_customs/vies/faqvies.do for EU
            VAT ID formats, which vary from country to country.
            Generally these consist of a two-letter country code
            followed by the 8–12 digits of the national VAT ID. Some
            countries include one or two letters within their VAT ID.
            See http://en.wikipedia.org/wiki/VAT_identification_number
            for non-EU countries that maintain similar identifiers.
            Spaces, dashes etc should be omitted
        VALUE_41: EORI Economic Operators Registration and
            Identification, identifier for businesses that import into
            or export from the EU. Only for use in ONIX 3.0 or later
        VALUE_45: Chinese participant identifier Chinese Participant
            identifier on the Publishing and distribution public service
            platform. 12-digits (or 11 digits plus X), usually presented
            with a / and hyphens dividing the number into groups of
            three, four and four digits plus a check digit, but in ONIX
            the / and hyphens should be omitted. Only for use in ONIX
            3.0 or later
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_16 = "16"
    VALUE_23 = "23"
    VALUE_41 = "41"
    VALUE_45 = "45"
