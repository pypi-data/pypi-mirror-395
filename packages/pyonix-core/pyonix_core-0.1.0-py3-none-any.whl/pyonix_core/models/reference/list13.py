from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List13(Enum):
    """
    Collection identifier type.

    Attributes:
        VALUE_01: Proprietary collection ID scheme For example,
            publisher’s own series ID scheme. Note that a distinctive
            &lt;IDTypeName&gt; is required with proprietary identifiers
        VALUE_02: ISSN International Standard Serial Number,
            unhyphenated, 8 digits
        VALUE_03: German National Bibliography series ID Maintained by
            the Deutsche Nationalbibliothek
        VALUE_04: German Books in Print series ID Maintained by VLB
        VALUE_05: Electre series ID Maintained by Electre Information,
            France
        VALUE_06: DOI Digital Object Identifier (variable length and
            character set, beginning ‘10.’ and without https://doi.org/
            or the older http://dx.doi.org/)
        VALUE_15: ISBN-13 Use only where the collection (series or set)
            is available as a single product
        VALUE_22: URN Uniform Resource Name using full URN syntax, eg
            urn:issn:1476-4687 – though where a specific code for the
            identifier type is available, use of that code (ie code 02
            for ISSN) is preferred
        VALUE_27: JP Magazine ID Japanese magazine identifier, similar
            in scope to ISSN. Five digits to identify the periodical,
            without any hyphen or two digit extension. Only for use in
            ONIX 3.0 or later
        VALUE_29: BNF Control number French National Bibliography series
            ID. Identifiant des publications en série maintenu par la
            Bibliothèque Nationale de France
        VALUE_35: ARK Archival Resource Key, as a URL (including the
            address of the ARK resolver provided by eg a national
            library)
        VALUE_38: ISSN-L International Standard Serial Number ‘linking
            ISSN’, used when distinct from the serial ISSN.
            Unhyphenated, 8 digits. Only for use in ONIX 3.0 or later
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_15 = "15"
    VALUE_22 = "22"
    VALUE_27 = "27"
    VALUE_29 = "29"
    VALUE_35 = "35"
    VALUE_38 = "38"
