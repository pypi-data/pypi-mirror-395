from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List9(Enum):
    """
    Product classification type.

    Attributes:
        VALUE_01: WCO Harmonized System World Customs Organization
            Harmonized Commodity Coding and Description System, the
            basis of most other commodity code schemes. Use 6 digits,
            without punctuation. See
            https://www.wcoomd.org/en/topics/nomenclature/instrument-
            and-tools/hs-nomenclature-2022-edition.aspx and
            https://www.wcotradetools.org/en/harmonized-system
        VALUE_02: UNSPSC UN Standard Product and Service Classification,
            including national versions adopted without any additions or
            changes to the codes or their meaning. Use 8 (or
            occasionally 10) digits, without punctuation
        VALUE_03: HMRC UK Revenue and Customs classifications, based on
            the Harmonized System (8 or 10 digits, without punctuation,
            for exports from and imports into the UK respectively). See
            https://www.gov.uk/trade-tariff
        VALUE_04: Warenverzeichnis für die Außenhandelsstatistik German
            export trade classification, based on the Harmonised System
        VALUE_05: TARIC EU TARIC codes, an extended version of the
            Harmonized System primarily for imports into the EU. Use 10
            digits (very occasionally 11), without punctuation. See
            https://taxation-customs.ec.europa.eu/customs-4/calculation-
            customs-duties/customs-tariff/eu-customs-tariff-taric_en
        VALUE_06: Fondsgroep Centraal Boekhuis free classification field
            for publishers
        VALUE_07: Sender’s product category A product category (not a
            subject classification) assigned by the sender
        VALUE_08: GAPP Product Class Product classification maintained
            by the Chinese General Administration of Press and
            Publication (http://www.gapp.gov.cn)
        VALUE_09: CPA Statistical Classification of Products by Activity
            in the European Economic Community, see
            http://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_NOM_DTL&amp;StrNom=CPA_2008.
            Use 6 digits, without punctuation. For example, printed
            children’s books are ‘58.11.13’, but the periods are
            normally ommited in ONIX
        VALUE_10: NCM Mercosur/Mercosul Common Nomenclature, based on
            the Harmonised System. Use 8 digits, without punctuation
        VALUE_11: CPV Common Procurement Vocabulary (2008), used to
            describe products and services for public tendering and
            procurement within the EU. Code is a nine digit number
            (including the check digit), and may also include a space
            plus an alphanumeric code of two letters and three digits
            (including the supplementary check digit) from the
            Supplementary Vocabulary. See
            https://simap.ted.europa.eu/web/simap/cpv
        VALUE_12: PKWiU Polish Classification of Products and Services
            (2015). Use a single letter followed by 2 to 7 digits,
            without punctuation. Only for use in ONIX 3.0 or later
        VALUE_13: HTSUS US HTS (or HTSA) commodity codes for import of
            goods into USA (10 digits including the ‘statistical
            suffix’, and without punctuation). Only for use in ONIX 3.0
            or later. See https://hts.usitc.gov/current
        VALUE_14: US Schedule B US Schedule B commodity codes for export
            from USA (10 digits, without punctuation). Only for use in
            ONIX 3.0 or later. See http://uscensus.prod.3ceonline.com
        VALUE_15: Clave SAT Mexican SAT classification, based on UN SPSC
            with later modifications (8 digits, without punctuation).
            Only for use in ONIX 3.0 or later. See
            https://www.sat.gob.mx/consultas/53693/catalogo-de-
            productos-y-servicios
        VALUE_16: CN (EU Combined Nomenclature) EU Combined Nomenclature
            commodity codes, an extended version of the Harmonized
            System primarily for exports from the EU. Use 8 digits,
            without punctuation. Only for use in ONIX 3.0 or later. See
            https://trade.ec.europa.eu/access-to-
            markets/en/content/combined-nomenclature-0
        VALUE_17: CCT Canadian Customs Tariff scheme, 8 or 10 digits for
            imports into and exports from Canada. Only for use in ONIX
            3.0 or later. See https://www.cbsa-asfc.gc.ca/trade-
            commerce/tariff-tarif/menu-eng.html
        VALUE_18: CACT Australian ‘Working tariff’. Combined Australian
            Customs Tariff Nomenclature and Statistical Classification.
            Only for use in ONIX 3.0 or later. See
            https://www.abf.gov.au/importing-exporting-and-
            manufacturing/tariff-classification
        VALUE_19: NICO Mexican Número de Identificación Comercial, 10
            digits for imports into and exports from Mexico. Only for
            use in ONIX 3.0 or later. See
            https://www.snice.gob.mx/cs/avi/snice/nico.ligie.html
        VALUE_20: TARIC additional code EU TARIC Document codes, 4
            alphanumeric characters (usually 1 letter, 3 digits), eg
            Y129 (for goods outside the scope of EUDR). Only for use in
            ONIX 3.0 or later
        VALUE_21: HTSUS additional code HTSUS code for special
            classification provisions, or temporary legislation and
            restrictions, particularly from HTSUS chapters 98 and 99 (8
            digits, or 10 where a statistical suffix is appropriate),
            and without punctuation). Only for use in ONIX 3.0 or later.
            See https://hts.usitc.gov/current
        VALUE_22: CPPAP Commission paritaire des publications et agences
            de presse, identifier used in France (mostly for serial
            publications). 10 characters (4 digits, one letter, then
            five digits). The initial four digits indicate the month and
            year of expiry of the CPPAP registration. Only for use in
            ONIX 3.0 or later
        VALUE_50: Electre genre Typologie de marché géré par Electre
            (Market segment code maintained by Electre)
    """

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
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_50 = "50"
