from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List58(Enum):
    """
    Price type.

    Attributes:
        VALUE_01: RRP excluding tax Recommended Retail Price, excluding
            any sales tax or value-added tax. Price recommended by the
            publisher or supplier for retail sales to the consumer. Also
            termed the Suggested Retail Price (SRP) or Maximum Suggested
            Retail Price (MSRP) in some countries. The retailer may
            choose to use this recommended price, or may choose to sell
            to the consumer at a lower (or occasionally, a higher) price
            which is termed the Actual Selling Price (ASP) in sales
            reports. The net price charged to the retailer depends on
            the RRP minus a trade discount (which may be customer-
            specific). Relevant tax detail must be calculated by the
            data recipient
        VALUE_02: RRP including tax Recommended Retail Price, including
            sales or value-added tax where applicable. The net price
            charged to the retailer depends on the trade discount. Sales
            or value-added tax detail is usually supplied in the
            &lt;Tax&gt; composite
        VALUE_03: FRP excluding tax Fixed Retail Price, excluding any
            sales or value-added tax, used in countries where retail
            price maintenance applies (by law or via trade agreement) to
            certain products. Price fixed by the publisher or supplier
            for retail sales to the consumer. The retailer must use this
            price, or may vary the price only within certain legally-
            prescribed limits. The net price charged to the retailer
            depends on the FRP minus a customer-specific trade discount.
            Relevant tax detail must be calculated by the data recipient
        VALUE_04: FRP including tax Fixed Retail Price, including any
            sales or value-added tax where applicable, used in countries
            where retail price maintenance applies (by law or via trade
            agreement) to certain products. The net price charged to the
            retailer depends on the trade discount. Sales or value-added
            tax detail is usually supplied in the &lt;Tax&gt; composite
        VALUE_05: Supplier’s Net price excluding tax Net or wholesale
            price, excluding any sales or value-added tax. Unit price
            charged by supplier for business-to-business transactions,
            without any direct relationship to the price for retail
            sales to the consumer, but sometimes subject to a further
            customer-specific trade discount based on volume. Relevant
            tax detail must be calculated by the data recipient
        VALUE_06: Supplier’s Net price excluding tax: rental goods Unit
            price charged by supplier to reseller / rental outlet,
            excluding any sales tax or value-added tax: goods for rental
            (used for video and DVD)
        VALUE_07: Supplier’s Net price including tax Net or wholesale
            price, including any sales or value-added tax where
            applicable. Unit price charged by supplier for business-to-
            business transactions, without any direct relationship to
            the price for retail sales to the consumer, but sometimes
            subject to a further customer-specific trade discount based
            on volume. Sales or value-added tax detail is usually
            supplied in the &lt;Tax&gt; composite
        VALUE_08: Supplier’s alternative Net price excluding tax Net or
            wholesale price charged by supplier to a specified class of
            reseller, excluding any sales tax or value-added tax.
            Relevant tax detail must be calculated by the data
            recipient. (This value is for use only in countries, eg
            Finland, where trade practice requires two different Net
            prices to be listed for different classes of resellers, and
            where national guidelines specify how the code should be
            used)
        VALUE_09: Supplier’s alternative net price including tax Net or
            wholesale price charged by supplier to a specified class of
            reseller, including any sales tax or value-added tax. Sales
            or value-added tax detail is usually supplied in the
            &lt;Tax&gt; composite. (This value is for use only in
            countries, eg Finland, where trade practice requires two
            different Net prices to be listed for different classes of
            resellers, and where national guidelines specify how the
            code should be used)
        VALUE_11: Special sale RRP excluding tax Special sale RRP
            excluding any sales tax or value-added tax. Note ‘special
            sales’ are sales where terms and conditions are different
            from normal trade sales, when for example products that are
            normally sold on a sale-or-return basis are sold on firm-
            sale terms, where a particular product is tailored for a
            specific retail outlet (often termed a ‘premium’ product),
            or where other specific conditions or qualifications apply.
            Further details of the modified terms and conditions should
            be given in &lt;PriceTypeDescription&gt;
        VALUE_12: Special sale RRP including tax Special sale RRP
            including sales or value-added tax if applicable
        VALUE_13: Special sale fixed retail price excluding tax In
            countries where retail price maintenance applies by law to
            certain products: not used in USA
        VALUE_14: Special sale fixed retail price including tax In
            countries where retail price maintenance applies by law to
            certain products: not used in USA
        VALUE_15: Supplier’s net price for special sale excluding tax
            Unit price charged by supplier to reseller for special sale
            excluding any sales tax or value-added tax
        VALUE_17: Supplier’s net price for special sale including tax
            Unit price charged by supplier to reseller for special sale
            including any sales tax or value-added tax
        VALUE_21: Pre-publication RRP excluding tax Pre-publication RRP
            excluding any sales tax or value-added tax. Use where RRP
            for pre-orders is different from post-publication RRP
        VALUE_22: Pre-publication RRP including tax Pre-publication RRP
            including sales or value-added tax if applicable. Use where
            RRP for pre-orders is different from post-publication RRP
        VALUE_23: Pre-publication fixed retail price excluding tax In
            countries where retail price maintenance applies by law to
            certain products: not used in USA
        VALUE_24: Pre-publication fixed retail price including tax In
            countries where retail price maintenance applies by law to
            certain products: not used in USA
        VALUE_25: Supplier’s pre-publication net price excluding tax
            Unit price charged by supplier to reseller pre-publication
            excluding any sales tax or value-added tax
        VALUE_27: Supplier’s pre-publication net price including tax
            Unit price charged by supplier to reseller pre-publication
            including any sales tax or value-added tax
        VALUE_31: Freight-pass-through RRP excluding tax In the US,
            books are sometimes supplied on ‘freight-pass-through’
            terms, where a price that is different from the RRP is used
            as the basis for calculating the supplier’s charge to a
            reseller. To make it clear when such terms are being
            invoked, code 31 is used instead of code 01 to indicate the
            RRP. Code 32 is used for the ‘billing price’
        VALUE_32: Freight-pass-through billing price excluding tax When
            freight-pass-through terms apply, the price on which the
            supplier’s charge to a reseller is calculated, ie the price
            to which trade discount terms are applied. See also code 31
        VALUE_33: Importer’s Fixed retail price excluding tax In
            countries where retail price maintenance applies by law to
            certain products, but the price is set by the importer or
            local sales agent, not the foreign publisher. In France,
            ‘prix catalogue éditeur étranger’
        VALUE_34: Importer’s Fixed retail price including tax In
            countries where retail price maintenance applies by law to
            certain products, but the price is set by the importer or
            local sales agent, not the foreign publisher. In France,
            ‘prix catalogue éditeur étranger’
        VALUE_35: Nominal gratis copy value for customs purposes,
            excluding tax Nominal value of gratis copies (eg review,
            sample or evaluation copies) for international customs
            declarations only, when a ‘free of charge’ price cannot be
            used. Only for use in ONIX 3.0 or later
        VALUE_36: Nominal value for claims purposes, excluding tax
            Nominal value of copies for claims purposes only (eg to
            account for copies lost during distribution). Only for use
            in ONIX 3.0 or later
        VALUE_37: Nominal value for customs purposes, excluding tax
            Nominal value of copies (Declared Unit Value) for
            international customs declarations only. Only for use in
            ONIX 3.0 or later
        VALUE_41: Publishers retail price excluding tax For a product
            supplied on agency terms, the retail price set by the
            publisher, excluding any sales tax or value-added tax
        VALUE_42: Publishers retail price including tax For a product
            supplied on agency terms, the retail price set by the
            publisher, including sales or value-added tax if applicable
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_17 = "17"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_27 = "27"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_34 = "34"
    VALUE_35 = "35"
    VALUE_36 = "36"
    VALUE_37 = "37"
    VALUE_41 = "41"
    VALUE_42 = "42"
