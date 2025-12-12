from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List168(Enum):
    """
    Price condition quantity type.

    Attributes:
        VALUE_01: Time period The price condition quantity represents a
            time period
        VALUE_02: Number of updates The price condition quantity is a
            number of updates
        VALUE_03: Number of linked products Use with Price condition
            type 06 and a Quantity of units. Price is valid when
            purchased with a specific number of products from a list of
            product identifiers provided in the associated
            &lt;ProductIdentifier&gt; composites. Use for example when
            describing a price for this product which is valid if it is
            purchased along with any two from a list of other products
        VALUE_04: Number of copies of this product Use with Price
            condition type 06 and a Quantity of units. Meeting the Price
            condition qualifies for purchase of a specified number of
            copies of this product at this price. Use for example when
            describing a price that applies to the specified number of
            units of this product which is valid if they are purchased
            along with a number of copies of another product
        VALUE_05: Minimum number of linked products Use with Price
            condition type 06 and a Quantity of units. Price is valid
            when purchased with at least a specific number of products
            from a list of product identifiers provided in the
            associated &lt;ProductIdentifier&gt; composites. Use for
            example when describing a price for this product which is
            valid if it is purchased along with any two from a list of
            other products
        VALUE_06: Maximum number of copies of this product (at this
            price). Use with Price condition type 06 and a Quantity of
            units. Meeting the Price condition qualifies for purchase of
            up to the specified number of copies of this product at this
            price. Use for example when describing a price that applies
            to the specified number of units of this product which is
            valid if they are purchased along with a number of copies of
            another product
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
