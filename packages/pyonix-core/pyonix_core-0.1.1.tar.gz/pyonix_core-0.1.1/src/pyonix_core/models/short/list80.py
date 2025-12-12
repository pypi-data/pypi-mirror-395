from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List80(Enum):
    """
    Product packaging type.

    Attributes:
        VALUE_00: No outer packaging No packaging, or all smaller items
            enclosed inside largest item
        VALUE_01: Slip-sleeve Thin card or soft plastic sleeve, much
            less rigid than a slip case
        VALUE_02: Clamshell Packaging consisting of formed plastic
            sealed around each side of the product. Not to be confused
            with single-sided Blister pack
        VALUE_03: Keep case Typical DVD-style packaging, sometimes known
            as an ‘Amaray’ case
        VALUE_05: Jewel case Typical CD-style packaging
        VALUE_06: Digipak Common CD-style packaging, a card folder with
            one or more panels incorporating a tray, hub or pocket to
            hold the disc(s)
        VALUE_08: Shrink-wrapped (biodegradable) Use for products or
            product bundles supplied for retail sale in shrink-wrapped
            packaging, where the shrink-wrap film is biodegradable. For
            non-degradable film, see code 21. Only for use in ONIX 3.0
            or later
        VALUE_09: In box (with lid) Individual item, items or set in
            card box with separate or hinged lid: not to be confused
            with the commonly-used ‘boxed set’ which is more likely to
            be packaged in a slip case
        VALUE_10: Slip-cased Slip-case for single item only (de:
            ‘Schuber’)
        VALUE_11: Slip-cased set Slip-case for multi-volume set, also
            commonly referred to as ‘boxed set’ (de: ‘Kassette’)
        VALUE_12: Tube Rolled in tube or cylinder: eg sheet map or
            poster
        VALUE_13: Binder Use for miscellaneous items such as slides,
            microfiche, when presented in a binder
        VALUE_14: In wallet or folder Use for miscellaneous items such
            as slides, microfiche, when presented in a wallet or folder
        VALUE_15: Long triangular package Long package with triangular
            cross-section used for rolled sheet maps, posters etc
        VALUE_16: Long square package Long package with square cross-
            section used for rolled sheet maps, posters, etc
        VALUE_17: Softbox (for DVD)
        VALUE_18: Pouch In pouch, eg teaching materials in a plastic bag
            or pouch
        VALUE_19: Rigid plastic case In duroplastic or other rigid
            plastic case, eg for a class set
        VALUE_20: Cardboard case In cardboard case, eg for a class set
        VALUE_21: Shrink-wrapped Use for products or product bundles
            supplied for retail sale in shrink-wrapped packaging. For
            biodegradable shrink-wrap film, prefer code 08. For shrink-
            wrapped packs of multiple products for trade supply only,
            see code XL in List 7
        VALUE_22: Blister pack A pack comprising a pre-formed plastic
            blister and a printed card with a heat-seal coating
        VALUE_23: Carry case A case with carrying handle, typically for
            a set of educational books and/or learning materials
        VALUE_24: In tin Individual item, items or set in metal box or
            can with separate or hinged lid
        VALUE_25: With browse-prevention tape (ja: koguchi tome)
            Peelable sticker or tape sealing the foredge of a book to
            prevent pre-purchase reading of the content. Only for use in
            ONIX 3.0 or later
    """

    VALUE_00 = "00"
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_05 = "05"
    VALUE_06 = "06"
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
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
