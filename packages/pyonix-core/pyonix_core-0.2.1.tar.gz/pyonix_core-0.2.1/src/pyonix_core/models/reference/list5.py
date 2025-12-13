from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List5(Enum):
    """
    Product identifier type.

    Attributes:
        VALUE_01: Proprietary product ID scheme For example, a
            publisher’s or wholesaler’s product number or SKU. Note that
            a distinctive &lt;IDTypeName&gt; is required with
            proprietary identifiers
        VALUE_02: ISBN-10 International Standard Book Number, pre-2007
            (10 digits, or 9 digits plus X, without spaces or hyphens) –
            now Deprecated in ONIX for Books, except where providing
            historical information for compatibility with legacy
            systems. It should only be used in relation to products
            published before 2007 – when ISBN-13 superseded it – and
            should never be used as the ONLY identifier (it should
            always be accompanied by the correct GTIN-13 / ISBN-13)
        VALUE_03: GTIN-13 GS1 Global Trade Item Number, formerly known
            as EAN article number (13 digits, without spaces or hyphens)
        VALUE_04: UPC UPC product number (12 digits, without spaces or
            hyphens)
        VALUE_05: ISMN-10 International Standard Music Number, pre-2008
            (M plus nine digits, without spaces or hyphens) – now
            Deprecated in ONIX for Books, except where providing
            historical information for compatibility with legacy
            systems. It should only be used in relation to products
            published before 2008 – when ISMN-13 superseded it – and
            should never be used as the ONLY identifier (it should
            always be accompanied by the correct GTIN-12 / ISMN-13)
        VALUE_06: DOI Digital Object Identifier (variable length and
            character set, beginning ‘10.’ and without https://doi.org/
            or the older http://dx.doi.org/)
        VALUE_13: LCCN Library of Congress Control Number in normalized
            form (up to 12 characters, alphanumeric)
        VALUE_14: GTIN-14 GS1 Global Trade Item Number (14 digits,
            without spaces or hyphens)
        VALUE_15: ISBN-13 International Standard Book Number, from 2007
            (13 digits starting 978 or 9791–9799, without spaces or
            hyphens)
        VALUE_17: Legal deposit number The number assigned to a
            publication as part of a national legal deposit process
        VALUE_22: URN Uniform Resource Name: note that in trade
            applications an ISBN must be sent as a GTIN-13 and, where
            required, as an ISBN-13 – it should not be sent as a URN
        VALUE_23: OCLC number A unique number assigned to a
            bibliographic item by OCLC
        VALUE_24: Co-publisher’s ISBN-13 An ISBN-13 assigned by a co-
            publisher. The ‘main’ ISBN sent with &lt;ProductIDType&gt;
            codes 03 and/or 15 should always be the ISBN that is used
            for ordering from the supplier identified in
            &lt;SupplyDetail&gt;. However, ISBN rules allow a co-
            published title to carry more than one ISBN. The co-
            publisher should be identified in an instance of the
            &lt;Publisher&gt; composite, with the applicable
            &lt;PublishingRole&gt; code
        VALUE_25: ISMN-13 International Standard Music Number, from 2008
            (13-digit number starting 9790, without spaces or hyphens)
        VALUE_26: ISBN-A Actionable ISBN, in fact a special DOI
            incorporating the ISBN-13 within the DOI syntax. Begins
            ‘10.978.’ or ‘10.979.’ and includes a / character between
            the registrant element (publisher prefix) and publication
            element of the ISBN, eg 10.978.000/1234567. Note the ISBN-A
            should always be accompanied by the ISBN itself, using
            &lt;ProductIDType&gt; codes 03 and/or 15
        VALUE_27: JP e-code E-publication identifier controlled by
            JPOIID’s Committee for Research and Management of Electronic
            Publishing Codes. 20 alphanumeric characters, without
            spaces, beginning with the ISBN ‘registrant element’
        VALUE_28: OLCC number Unique number assigned by the Chinese
            Online Library Cataloging Center (see
            http://olcc.nlc.gov.cn)
        VALUE_29: JP Magazine ID Japanese magazine identifier, similar
            in scope to ISSN but identifying a specific issue of a
            serial publication. Five digits to identify the periodical,
            plus a hyphen and two digits to identify the issue
        VALUE_30: UPC-12+5 Used only with comic books and other products
            which use the UPC extension to identify individual issues or
            products. Do not use where the UPC-12 itself identifies the
            specific product, irrespective of any 5-digit extension –
            use code 04 instead
        VALUE_31: BNF Control number Numéro de la notice bibliographique
            BNF
        VALUE_34: ISSN-13 International Standard Serial Number expressed
            as a GTIN-13, with optional 2- or 5-digit barcode extension
            (ie 13, 15 or 18 digits starting 977, without spaces or
            hyphens, with &lt;BarcodeType&gt; codes 02, 12 or 05), and
            only when the extended ISSN is used specifically as a
            product identifier (ie when the two publisher-defined
            ‘variant’ digits within the ISSN-13 itself and/or the 2- or
            5-digit barcode extension are used to identify a single
            issue of a serial publication for separate sale). Only for
            use in ONIX 3.0 or later
        VALUE_35: ARK Archival Resource Key, as a URL (including the
            address of the ARK resolver provided by eg a national
            library)
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_17 = "17"
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
    VALUE_34 = "34"
    VALUE_35 = "35"
