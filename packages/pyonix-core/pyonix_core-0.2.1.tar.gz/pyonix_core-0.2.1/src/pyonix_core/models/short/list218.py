from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List218(Enum):
    """
    License expression type.

    Attributes:
        VALUE_01: Human readable Document (eg Word file, PDF or web
            page) intended for the lay reader
        VALUE_02: Professional readable Document (eg Word file, PDF or
            web page) intended for the legal specialist reader
        VALUE_03: Human readable additional license Document (eg Word
            file, PDF or web page) intended for the lay reader,
            expressing an additional license that may be separately
            obtained covering uses of the content that are not granted
            by the intrinsic product license (the license expressed by
            code 01)
        VALUE_04: Professional readable additional license Document (eg
            Word file, PDF or web page) intended for the legal
            specialist reader, expressing an additional license that may
            be separately obtained covering uses of the content that are
            not granted by the intrinsic product license (the license
            expressed by code 02)
        VALUE_10: ONIX-PL
        VALUE_20: ODRL Open Digital Rights Language (ODRL) in JSON-LD
            format. Used for example to express TDM licenses using the
            W3C TDM Reservation Protocol
        VALUE_21: ODRL additional license Open Digital Rights Language
            (ODRL) in JSON-LD format. Used for example to express
            additional TDM licenses that may be separately obtained
            covering uses of the content that are not granted by the
            intrinsic product license (the license expressed by code
            20), using the W3C TDM Reservation Protocol
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_10 = "10"
    VALUE_20 = "20"
    VALUE_21 = "21"
