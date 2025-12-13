from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List100(Enum):
    """
    Discount code type.

    Attributes:
        VALUE_01: BIC discount group code UK publisher’s or
            distributor’s discount group code in a format specified by
            BIC to ensure uniqueness (a five-letter prefix allocated by
            BIC, plus one to three alphanumeric characters – normally
            digits – chosen by the supplier). See
            https://bic.org.uk/resources/discount-group-codes/
        VALUE_02: Proprietary discount code scheme A publisher’s or
            supplier’s own code which identifies a trade discount
            category. Note that a distinctive
            &lt;DiscountCodeTypeName&gt; is required with proprietary
            coding schemes. The actual discount for each code is set by
            trading partner agreement (applies to goods supplied on
            standard trade discounting terms)
        VALUE_03: Boeksoort Terms code used in the Netherlands book
            trade
        VALUE_04: German terms code Terms code used in German ONIX
            applications
        VALUE_05: Proprietary commission code scheme A publisher’s or
            supplier’s own code which identifies a commission rate
            category. Note that a distinctive
            &lt;DiscountCodeTypeName&gt; is required with proprietary
            coding schemes. The actual commission rate for each code is
            set by trading partner agreement (applies to goods supplied
            on agency terms)
        VALUE_06: BIC commission group code UK publisher’s or
            distributor’s commission group code in format specified by
            BIC to ensure uniqueness. Format is identical to BIC
            discount group code, but indicates a commission rather than
            a discount (applies to goods supplied on agency terms)
        VALUE_07: ISNI-based discount group code ISNI-based discount
            group scheme devised initially by the German IG
            ProduktMetadaten, in a format comprised of the supplier’s
            16-digit ISNI, followed by a hyphen and one to three
            alphanumeric characters – normally digits – chosen by the
            supplier. These characters are the index to a discount
            percentage in a table shared in advance by the supplier with
            individual customers. In this way, a supplier may maintain
            individual product-specific discount arrangements with each
            customer. Only for use in ONIX 3.0 or later
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
