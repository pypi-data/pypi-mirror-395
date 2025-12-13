from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List217(Enum):
    """
    Price identifier type.

    Attributes:
        VALUE_01: Proprietary price identifier scheme Note that a
            distinctive &lt;IDTypeName&gt; is required for proprietary
            price identifiers
        VALUE_02: Proprietary price point identifier scheme Proprietary
            identifier uniquely identifies price amount and currency.
            Two unrelated products with the same price amount carry the
            same identifier, though their price types may be different.
            Note that a distinctive &lt;IDTypeName&gt; is required for
            proprietary price identifiers
        VALUE_03: Proprietary price type identifier scheme Proprietary
            identifier uniquely identifies price type, qualifier and any
            constraints and conditions. Two unrelated products with the
            same price type carry the same identifier, though their
            price points may be different. Note that a distinctive
            &lt;IDTypeName&gt; is required for proprietary price
            identifiers
        VALUE_04: Proprietary price point and type identifier scheme
            Proprietary identifier identifies a unique combination of
            price point and type, though two unrelated products may
            carry the same identifier if all details of their prices are
            identical. Note that a distinctive &lt;IDTypeName&gt; is
            required for proprietary price identifiers
        VALUE_05: Proprietary unique price identifier scheme Proprietary
            identifier is unique to a single price point, price type and
            product. No two products can carry the same identifier, even
            if all details of their prices are identical. Note that a
            distinctive &lt;IDTypeName&gt; is required for proprietary
            price identifiers
        VALUE_06: Proprietary product price point identifier scheme
            Proprietary identifier uniquely identifies a specific
            combination of product, price amount and currency,
            independent of the price type. Note that a distinctive
            &lt;IDTypeName&gt; is required for proprietary price
            identifiers
        VALUE_07: Proprietary product price type identifier scheme
            Proprietary identifier uniquely identifies a specific
            combination of product, price type, qualifier and any
            constraints and conditions, independent of the price amount
            and currency. A product with the same product price type
            identifier may carry differing price amounts, currencies at
            different points in time. Note that a distinctive
            &lt;IDTypeName&gt; is required for proprietary price
            identifiers
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
