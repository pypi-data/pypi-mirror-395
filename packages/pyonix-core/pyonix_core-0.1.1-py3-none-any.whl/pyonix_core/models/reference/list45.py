from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List45(Enum):
    """
    Publishing role.

    Attributes:
        VALUE_01: Publisher
        VALUE_02: Co-publisher Use where two or more publishers co-
            publish the exact same product, either under a single ISBN
            (in which case both publishers are co-publishers), or under
            different ISBNs (in which case the publisher of THIS ISBN is
            the publisher and the publishers of OTHER ISBNs are co-
            publishers. Note this is different from publication of ‘co-
            editions’
        VALUE_03: Sponsor
        VALUE_04: Publisher of original-language version Of a translated
            work
        VALUE_05: Host/distributor of electronic content
        VALUE_06: Published for/on behalf of
        VALUE_07: Published in association with Use also for ‘Published
            in cooperation with’
        VALUE_09: New or acquiring publisher When ownership of a product
            is transferred from one publisher to another
        VALUE_10: Publishing group The group to which a publisher
            (publishing role 01) belongs: use only if a publisher has
            been identified with role code 01
        VALUE_11: Publisher of facsimile original The publisher of the
            edition of which a product is a facsimile
        VALUE_12: Repackager of prebound edition The repackager of a
            prebound edition that has been assigned its own identifier.
            (In the US, a ‘prebound edition’ is a book that was
            previously bound, normally as a paperback, and has been
            rebound with a library-quality hardcover binding by a
            supplier other than the original publisher.) Required when
            the &lt;EditionType&gt; is coded PRB. The original publisher
            should be named as the ‘publisher’
        VALUE_13: Former publisher When ownership of a product is
            transferred from one publisher to another (complement of
            code 09)
        VALUE_14: Publication funder Body funding publication fees, if
            different from the body funding the underlying research.
            Intended primarily for use with open access publications
        VALUE_15: Research funder Body funding the research on which
            publication is based, if different from the body funding the
            publication. Intended primarily for use with open access
            publications
        VALUE_16: Funding body Body funding research and publication.
            Intended primarily for use with open access publications
        VALUE_17: Printer Organization responsible for printing a
            printed product. Supplied primarily to meet legal deposit
            requirements, and may apply only to the first impression.
            The organization may also be responsible for binding, when a
            separate binder is not specified
        VALUE_18: Binder Organization responsible for binding a printed
            product (where distinct from the printer). Supplied
            primarily to meet legal deposit requirements, and may apply
            only to the first impression
        VALUE_19: Manufacturer Organization primarily responsible for
            physical manufacture of a product, when neither Printer nor
            Binder is directly appropriate (for example, with disc or
            tape products, or digital products on a physical carrier)
        VALUE_21: Previous publisher Use for the publisher of earlier
            manifestations of the work. Only for use in ONIX 3.0 or
            later
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
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
    VALUE_21 = "21"
