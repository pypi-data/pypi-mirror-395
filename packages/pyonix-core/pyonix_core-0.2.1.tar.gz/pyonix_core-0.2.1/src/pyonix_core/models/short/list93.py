from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List93(Enum):
    """
    Supplier role.

    Attributes:
        VALUE_00: Unspecified Default
        VALUE_01: Publisher to resellers Publisher as supplier to retail
            trade outlets
        VALUE_02: Publisher’s exclusive distributor to resellers
        VALUE_03: Publisher’s non-exclusive distributor to resellers
        VALUE_04: Wholesaler to retailers Wholesaler supplying retail
            trade outlets
        VALUE_05: Sales agent Deprecated – use
            &lt;MarketRepresentation&gt; (ONIX 2.1) or
            &lt;MarketPublishingDetail&gt; (ONIX 3.0 or later) to
            specify a sales agent
        VALUE_06: Publisher’s distributor to retailers In a specified
            supply territory. Use only where exclusive/non-exclusive
            status is not known. Prefer 02 or 03 as appropriate, where
            possible
        VALUE_07: POD supplier Where a POD product is supplied to
            retailers and/or consumers direct from a POD source
        VALUE_08: Retailer
        VALUE_09: Publisher to end-customers Publisher as supplier
            direct to consumers and/or institutional customers
        VALUE_10: Exclusive distributor to end-customers Intermediary as
            exclusive distributor direct to consumers and/or
            institutional customers
        VALUE_11: Non-exclusive distributor to end-customers
            Intermediary as non-exclusive distributor direct to
            consumers and/or institutional customers
        VALUE_12: Distributor to end-customers Use only where
            exclusive/non-exclusive status is not known. Prefer 10 or 11
            as appropriate, where possible
        VALUE_13: Exclusive distributor to resellers and end-customers
            Intermediary as exclusive distributor to retailers and
            direct to consumers and/or institutional customers. Only for
            use in ONIX 3.0 or later
        VALUE_14: Non-exclusive distributor to resellers and end-
            customers Intermediary as non-exclusive distributor to
            retailers and direct to consumers and/or institutional
            customers. Only for use in ONIX 3.0 or later
        VALUE_15: Distributor to resellers and end-customers Use only
            where exclusive/non-exclusive status is not known. Prefer
            codes 13 or 14 as appropriate whenever possible. Only for
            use in ONIX 3.0 or later
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
    VALUE_14 = "14"
    VALUE_15 = "15"
