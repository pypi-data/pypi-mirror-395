from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List165(Enum):
    """
    Supplier own code type.

    Attributes:
        VALUE_01: Supplier’s sales classification A rating applied by a
            supplier (typically a wholesaler) to indicate its assessment
            of the expected or actual sales performance of a product
        VALUE_02: Supplier’s bonus eligibility A supplier’s coding of
            the eligibility of a product for a bonus scheme on overall
            sales
        VALUE_03: Publisher’s sales classification A rating applied by
            the publisher to indicate a sales category (eg
            backlist/frontlist, core stock etc). Use only when the
            publisher is not the ‘supplier’
        VALUE_04: Supplier’s pricing restriction classification A
            classification applied by a supplier to a product sold on
            Agency terms, to indicate that retail price restrictions are
            applicable
        VALUE_05: Supplier’s sales expectation Code is the ISBN of
            another book that had sales (both in terms of copy numbers
            and customer profile) comparable to that the distributor or
            supplier estimates for the product.
            &lt;SupplierCodeValue&gt; must be an ISBN-13 or GTIN-13
        VALUE_06: Publisher’s sales expectation Code is the ISBN of
            another book that had sales (both in terms of copy numbers
            and customer profile) comparable to that the publisher
            estimates for the product. &lt;SupplierCodeValue&gt; must be
            an ISBN-13 or GTIN-13
        VALUE_07: Supplier’s order routing eligibility Code indicates
            whether an order can be placed with the supplier indirectly
            via an intermediary system. The code name type indicates the
            specific intermediate order aggregation/routing platform and
            the code indicates the eligibility
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
