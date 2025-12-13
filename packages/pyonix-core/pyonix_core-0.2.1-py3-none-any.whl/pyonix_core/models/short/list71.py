from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List71(Enum):
    """
    Sales restriction type.

    Attributes:
        VALUE_00: Unspecified – see text Restriction must be described
            in &lt;SalesRestrictionDetail&gt; (ONIX 2.1) or
            &lt;SalesRestrictionNote&gt; (ONIX 3.0 or later)
        VALUE_01: Retailer exclusive / own brand Sales rights (or market
            distribution rights) apply to sales through designated
            retailer(s), which must be identified or named in an
            instance of the &lt;SalesOutlet&gt; composite. Use only when
            it is not possible to assign the more explicit codes 04 or
            05
        VALUE_02: Through office supplies outlets only Sales rights (or
            market distribution rights) apply to sales though office
            supplies channels. Specific outlet(s) may be identified or
            named in an instance of the &lt;SalesOutlet&gt; composite
        VALUE_03: Internal publisher use only: do not list For an ISBN
            that is assigned for a publisher’s internal purposes. Should
            not appear in ONIX messages sent externally, and if sent
            inadvertently, data recipients should not list the product
            in their catalogs
        VALUE_04: Retailer exclusive Sales rights (or market
            distribution rights) apply to sales (under the publisher’s
            brand / imprint) through the designated retailer(s), which
            must be identified or named in an instance of the
            &lt;SalesOutlet&gt; composite
        VALUE_05: Retailer own brand Sales rights (or market
            distribution rights) apply to sales (under the retailer’s
            own brand / imprint) through the designated retailer(s),
            which must be identified or named in an instance of the
            &lt;SalesOutlet&gt; composite
        VALUE_06: To libraries only Sales rights (or market distribution
            rights) apply to supplies to libraries (public and national
            libraries, libraries in educational institutions)
        VALUE_07: To schools only Sales rights (or market distribution
            rights) apply to supplies to schools (primary and secondary
            education)
        VALUE_08: Indiziert Indexed for the German market – in
            Deutschland indiziert
        VALUE_09: Except to libraries Sales rights (or market
            distribution rights) apply to supplies other than to
            libraries
        VALUE_10: Through news outlets only Sales rights (or market
            distribution rights) apply to sales though news outlet
            channels (newsstands / newsagents)
        VALUE_11: Retailer exception Sales rights (or market
            distribution rights) apply to sales other than through
            designated retailer(s), which must be identified or named in
            the &lt;SalesOutlet&gt; composite
        VALUE_12: Except to subscription services Sales rights (or
            market distribution rights) apply to supplies other than to
            organizations or services offering consumers subscription
            access to a catalog of books
        VALUE_13: To subscription services only Sales rights (or market
            distribution rights) apply to supplies to organizations or
            services offering consumers subscription access to a catalog
            of books
        VALUE_14: Except through online retail Sales rights (or market
            distribution rights) apply to sales other than through
            online retail channels
        VALUE_15: Through online retail only Sales rights (or market
            distribution rights) apply to sales through online retail
            channels
        VALUE_16: Except to schools Sales rights (or market distribution
            rights) apply to supplies other than to schools. Only for
            use in ONIX 3.0 or later
        VALUE_17: Through Inventoryless POD POD copies may be
            manufactured at any time, either to fulfill a customer order
            immediately or to replace a minimal stockholding (ie near-
            inventoryless). Only for use in ONIX 3.0 or later
        VALUE_18: Through Stock Protection POD POD copies may be
            manufactured only to fulfill a customer order immediately
            while out of stock and awaiting delivery of further stock
            from the supplier. Only for use in ONIX 3.0 or later
        VALUE_19: Except through POD Not eligible for POD. Only for use
            in ONIX 3.0 or later
        VALUE_20: Except to some subscription services Sales rights (or
            market distribution rights) apply to all supplies through
            retailers, and to the designated subscription services,
            which must be identified or named in an instance of the
            &lt;SalesOutlet&gt; composite. Only for use in ONIX 3.0 or
            later
        VALUE_21: Subscription service exclusive Sales rights (or market
            distribution rights) apply to supplies to the designated
            subscription service(s), which must be identified or named
            in an instance of the &lt;SalesOutlet&gt; composite. Only
            for use in ONIX 3.0 or later
        VALUE_22: To education only Sales rights (or market distribution
            rights) apply to supplies to educational institutions only
            (primary, secondary, tertiary, adult, vocational and
            professional etc). Only for use in ONIX 3.0 or later
        VALUE_23: Except to education Sales rights (or market
            distribution rights) apply to supplies other than to
            educational institutions. Only for use in ONIX 3.0 or later
        VALUE_99: No restrictions on sales Positive indication that no
            sales restrictions apply, for example to indicate the
            product may be sold both online and in bricks-and mortar
            retail, or to subscription services and non-subscription
            customers. Only for use in ONIX 3.0 or later
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
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_99 = "99"
