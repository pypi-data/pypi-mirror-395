from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List141(Enum):
    """
    Barcode indicator.

    Attributes:
        VALUE_00: Not barcoded
        VALUE_01: Barcoded, scheme unspecified
        VALUE_02: GTIN-13 Barcode uses 13-digit EAN symbology (version
            NR without 5-digit extension). See (eg)
            https://bic.org.uk/wp-
            content/uploads/2022/11/2019.05.31-Bar-Coding-for-Books-
            rev-09.pdf or https://www.bisg.org/barcoding-guidelines-for-
            the-us-book-industry
        VALUE_03: GTIN-13+5 (US dollar price encoded) EAN symbology
            (version NK, first digit of 5-digit extension is 1–5)
        VALUE_04: GTIN-13+5 (CAN dollar price encoded) EAN symbology
            (version NK, first digit of 5-digit extension is 6)
        VALUE_05: GTIN-13+5 (no price encoded) EAN symbology (version
            NF, 5-digit extension is 90000–98999 for proprietary use –
            extension does not indicate a price)
        VALUE_06: UPC-12 (item-specific) AKA item/price
        VALUE_07: UPC-12+5 (item-specific) AKA item/price
        VALUE_08: UPC-12 (price-point) AKA price/item
        VALUE_09: UPC-12+5 (price-point) AKA price/item
        VALUE_10: GTIN-13+5 (UK Pound Sterling price encoded) EAN
            symbology (version NK, first digit of 5-digit extension is
            0)
        VALUE_11: GTIN-13+5 (other price encoded) EAN symbology (version
            NK, price currency by local agreement)
        VALUE_12: GTIN-13+2 EAN symbology (two-digit extension, normally
            indicating periodical issue number)
        VALUE_13: GTIN-13+5 EAN symbology (five-digit extension,
            normally indicating periodical issue number)
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
    VALUE_13 = "13"
