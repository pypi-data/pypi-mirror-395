from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List167(Enum):
    """
    Price condition type.

    Attributes:
        VALUE_00: No conditions Allows positive indication that there
            are no conditions (the default if &lt;PriceCondition&gt; is
            omitted)
        VALUE_01: Includes updates Purchase at this price includes
            specified updates
        VALUE_02: Must also purchase updates Purchase at this price
            requires commitment to purchase specified updates, not
            included in price
        VALUE_03: Updates available Updates may be purchased separately,
            no minimum commitment required
        VALUE_04: Linked subsequent purchase price Use with
            &lt;PriceConditionQuantity&gt; and
            &lt;ProductIdentifier&gt;. Purchase at this price requires
            commitment to purchase the specified linked product, which
            is not included in the price
        VALUE_05: Linked prior purchase price Use with
            &lt;PriceConditionQuantity&gt; and
            &lt;ProductIdentifier&gt;. Purchase at this price requires
            prior purchase of the specified linked product
        VALUE_06: Linked price Use with &lt;PriceConditionQuantity&gt;
            and &lt;ProductIdentifier&gt;. Purchase at this price
            requires simultaneous purchase of the specified linked
            product, which is not included in the price
        VALUE_07: Auto-renewing The rental or subscription will
            automatically renew at the end of the period unless actively
            cancelled
        VALUE_08: Combined price Purchase at this price includes the
            price of the specified other product
        VALUE_10: Rental duration The duration of the rental to which
            the price applies. Deprecated, use &lt;PriceConstraint&gt;
            instead
        VALUE_11: Rental to purchase Purchase at this price requires
            prior rental of the product. &lt;PriceConditionQuantity&gt;
            gives minimum prior rental period, and
            &lt;ProductIdentifier&gt; may be used if rental uses a
            different product identifier
        VALUE_12: Rental extension Upgrade to longer rental duration.
            &lt;PriceConditionQuantity&gt; gives minimum prior rental
            duration, and &lt;ProductIdentifier&gt; may be used if
            rental uses a different product identifier. Separate price
            constraint with time limited license duration (code 07)
            specifies the new combined rental duration
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
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
