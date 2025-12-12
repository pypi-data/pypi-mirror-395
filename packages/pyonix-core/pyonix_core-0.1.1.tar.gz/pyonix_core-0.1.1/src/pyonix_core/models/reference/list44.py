from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List44(Enum):
    """
    Name identifier type.

    Attributes:
        VALUE_01: Proprietary name ID scheme For example, a publisher’s
            own name, contributor or imprint ID scheme. Note that a
            distinctive &lt;IDTypeName&gt; is required with proprietary
            identifiers
        VALUE_02: Proprietary Deprecated – use code 01
        VALUE_03: DNB publisher identifier Deutsche Nationalbibliothek
            publisher identifier
        VALUE_04: Börsenverein Verkehrsnummer (de: Verkehrsnummer ded
            Börsenverein des deutschen Buchhandels)
        VALUE_05: German ISBN Agency publisher identifier (de: MVB-
            Kennnummer)
        VALUE_06: GLN GS1 global location number (formerly EAN location
            number)
        VALUE_07: SAN Book trade Standard Address Number – US, UK etc
        VALUE_08: MARC organization code MARC code list for
            organizations – see
            http://www.loc.gov/marc/organizations/orgshome.html
        VALUE_10: Centraal Boekhuis Relatie ID Trading party identifier
            used in the Netherlands
        VALUE_12: Distributeurscode Boekenbank Flemish supplier code.
            Only for use in ONIX 3.0 or later
        VALUE_13: Fondscode Boekenbank Flemish publisher code
        VALUE_15: Y-tunnus Business Identity Code (Finland). See
            http://www.ytj.fi/ (in Finnish)
        VALUE_16: ISNI International Standard Name Identifier. A sixteen
            digit number. Usually presented with spaces or hyphens
            dividing the number into four groups of four digits, but in
            ONIX the spaces or hyphens should be omitted. See
            https://isni.org/
        VALUE_17: PND Personennamendatei – person name authority file
            used by Deutsche Nationalbibliothek and in other German-
            speaking countries. See
            http://www.dnb.de/standardisierung/normdateien/pnd.htm
            (German) or
            http://www.dnb.de/eng/standardisierung/normdateien/pnd.htm
            (English). Deprecated in favor of the GND
        VALUE_18: NACO A control number assigned to a Library of
            Congress Control Number (LCCN) Name Authority / NACO record
        VALUE_19: Japanese Publisher identifier Publisher identifier
            administered by Japanese ISBN Agency
        VALUE_20: GKD Gemeinsame Körperschaftsdatei – Corporate Body
            Authority File in the German-speaking countries. See
            http://www.dnb.de/standardisierung/normdateien/gkd.htm
            (German) or
            http://www.dnb.de/eng/standardisierung/normdateien/gkd.htm
            (English). Deprecated in favor of the GND
        VALUE_21: ORCID Open Researcher and Contributor ID. A sixteen
            digit number. Usually presented with hyphens dividing the
            number into four groups of four digits, but in ONIX the
            hyphens should be omitted. See http://www.orcid.org/
        VALUE_22: GAPP Publisher Identifier Publisher identifier
            maintained by the Chinese ISBN Agency (GAPP)
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
        VALUE_24: JP Distribution Identifier 4-digit business
            organization identifier controlled by the Japanese
            Publication Wholesalers Association
        VALUE_25: GND Gemeinsame Normdatei – Joint Authority File in the
            German-speaking countries. See http://www.dnb.de/EN/gnd
            (English). Combines the PND, SWD and GKD into a single
            authority file, and should be used in preference
        VALUE_26: DUNS Dunn and Bradstreet Universal Numbering System,
            see http://www.dnb.co.uk/dandb-duns-number
        VALUE_27: Ringgold ID Ringgold organizational identifier, see
            http://www.ringgold.com/identify.html
        VALUE_28: Identifiant Editeur Electre French Electre publisher
            identifier
        VALUE_29: EIDR Party ID Entertainment Identifier Registry party
            identifier (a DOI beginning ‘10.5237/’ with a suffix of 8
            hexadecimal digits and one hyphen, and without the
            https://doi.org/ or the older http://dx.doi.org/), for
            example ‘10.5237/C9F6-F41F’ (Sam Raimi). See http://eidr.org
        VALUE_30: Identifiant Marque Electre French Electre imprint
            Identifier
        VALUE_31: VIAF ID Virtual Internet Authority File.
            &lt;IDValue&gt; should be a number. The URI form of the
            identifier can be created by prefixing the number with
            ‘https://viaf.org/viaf/’. See https://viaf.org
        VALUE_32: FundRef DOI DOI used in CrossRef’s Open Funder
            Registry list of academic research funding bodies, for
            example ‘10.13039/100010269’ (Wellcome Trust). Use of RORs
            for funder identifiers is now preferred. See
            https://www.crossref.org/services/funder-registry/
        VALUE_33: BNE CN Control number assigned to a Name Authority
            record by the Biblioteca Nacional de España
        VALUE_34: BNF Control Number Numéro de la notice de personne BNF
        VALUE_35: ARK Archival Resource Key, as a URL (including the
            address of the ARK resolver provided by eg a national
            library)
        VALUE_36: Nasjonalt autoritetsregister Nasjonalt
            autoritetsregister for navn – Norwegian national authority
            file for personal and corporate names. Only for use in ONIX
            3.0 or later
        VALUE_37: GRID Global Research Identifier Database ID (see
            https://www.grid.ac). Only for use in ONIX 3.0 or later.
            Deprecated – ROR is now generally preferred
        VALUE_38: IDRef Party ID from Identifiers and Standards for
            Higher Education and Research (fr: Identifiants et
            Référentiels pour l’enseignement supérieur et la recherche).
            Only for use in ONIX 3.0 or later. See https://www.idref.fr
        VALUE_39: IPI Party ID from CISAC’s proprietary Interested Party
            Information scheme, used primarily in rights and royalties
            administration. Only for use in ONIX 3.0 or later
        VALUE_40: ROR Research organization registry identifier (see
            https://ror.org), leading 0 followed by 8 alphanumeric
            characters (including 2-digit checksum). Only for use in
            ONIX 3.0 or later
        VALUE_41: EORI Economic Operators Registration and
            Identification, identifier for businesses that import into
            or export from the EU. Only for use in ONIX 3.0 or later
        VALUE_42: LEI Legal Entity Identifier, administered by the
            Global LEI Foundation, as 20 alphanumeric characters without
            spaces or hyphens. Only for use in ONIX 3.0 or later
        VALUE_43: SIREN French business identifier, issued by the
            National Institute of Statistics and Economic Studies
            (INSEE). 9 digits, without spaces. Only for use in ONIX 3.0
            or later
        VALUE_44: SIRET French business and location identifier, issued
            by the National Institute of Statistics and Economic Studies
            (INSEE). 14 digits (the SIREN plus a further five digits),
            without spaces, or occasionally an alphanumeric code. Only
            for use in ONIX 3.0 or later
        VALUE_45: Chinese Participant identifier Chinese Participant
            identifier on the Publishing and distribution public service
            platform. 12-digits (or 11 digits plus X), usually presented
            with a / and hyphens dividing the number into groups of
            three, four and four digits plus a check digit, but in ONIX
            the / and hyphens should be omitted. Only for use in ONIX
            3.0 or later
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_10 = "10"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_34 = "34"
    VALUE_35 = "35"
    VALUE_36 = "36"
    VALUE_37 = "37"
    VALUE_38 = "38"
    VALUE_39 = "39"
    VALUE_40 = "40"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_44 = "44"
    VALUE_45 = "45"
