from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List3(Enum):
    """
    Record source type.

    Attributes:
        VALUE_00: Unspecified
        VALUE_01: Publisher
        VALUE_02: Publisher’s distributor Use to designate a distributor
            providing primary warehousing and fulfillment for a
            publisher or for a publisher’s sales agent, as distinct from
            a wholesaler
        VALUE_03: Wholesaler
        VALUE_04: Bibliographic agency Bibliographic data aggregator
        VALUE_05: Library bookseller Library supplier. Bookseller
            selling to libraries (including academic libraries)
        VALUE_06: Publisher’s sales agent Use for a publisher’s sales
            agent responsible for marketing the publisher’s products
            within a territory, as opposed to a publisher’s distributor
            who fulfills orders but does not market
        VALUE_07: Publisher’s conversion service provider Downstream
            provider of e-publication format conversion services (who
            might also be a distributor or retailer of the converted
            e-publication), supplying metadata on behalf of the
            publisher. The assigned ISBN is taken from the publisher’s
            ISBN prefix
        VALUE_08: Conversion service provider Downstream provider of
            e-publication format conversion services (who might also be
            a distributor or retailer of the converted e-publication),
            supplying metadata on behalf of the publisher. The assigned
            ISBN is taken from the service provider’s prefix (whether or
            not the service provider dedicates that prefix to a
            particular publisher)
        VALUE_09: ISBN Registration Agency
        VALUE_10: ISTC Registration Agency Deprecated: the ISTC was
            withdrawn as a standard in 2021
        VALUE_11: Retail bookseller Bookseller selling primarily to
            consumers
        VALUE_12: Education bookseller Bookseller selling primarily to
            educational institutions
        VALUE_13: Library Library service providing enhanced metadata to
            publishers or other parties
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
