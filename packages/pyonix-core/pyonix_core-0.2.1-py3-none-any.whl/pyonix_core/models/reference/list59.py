from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List59(Enum):
    """
    Price type qualifier.

    Attributes:
        VALUE_00: Unqualified price Price applies to all customers that
            do not fall within any other group with a specified group-
            specific qualified price
        VALUE_01: Member/subscriber price Price applies to a designated
            group membership
        VALUE_02: Export price Price applies to sales outside the
            territory in which the supplier is located
        VALUE_03: Reduced price applicable when the item is purchased as
            part of a set (or series, or collection) Use in cases where
            there is no combined price, but a lower price is offered for
            each part if the whole set / series / collection is
            purchased (either at one time, as part of a continuing
            commitment, or in a single purchase)
        VALUE_04: Voucher price In the Netherlands (or any other market
            where similar arrangements exist): a reduced fixed price
            available for a limited time on presentation of a voucher or
            coupon published in a specified medium, eg a newspaper.
            Should be accompanied by Price Type code 13 and additional
            detail in &lt;PriceTypeDescription&gt;, and by validity
            dates in &lt;PriceEffectiveFrom&gt; and
            &lt;PriceEffectiveUntil&gt; (ONIX 2.1) or in the
            &lt;PriceDate&gt; composite (ONIX 3.0 or later)
        VALUE_05: Consumer price Price for individual consumer sale only
        VALUE_06: Corporate / Library / Education price Price for sale
            to libraries or other corporate or institutional customers
        VALUE_07: Reservation order price Price valid for a specified
            period prior to publication. Orders placed prior to the end
            of the period are guaranteed to be delivered to the retailer
            before the nominal publication date. The price may or may
            not be different from the ‘normal’ price, which carries no
            such delivery guarantee. Must be accompanied by a
            &lt;PriceEffectiveUntil&gt; date (or equivalent
            &lt;PriceDate&gt; composite in ONIX 3.0 or later), and
            should also be accompanied by a ‘normal’ price
        VALUE_08: Promotional offer price Temporary ‘Special offer’
            price. Must be accompanied by &lt;PriceEffectiveFrom&gt; and
            &lt;PriceEffectiveUntil&gt; dates (or equivalent
            &lt;PriceDate&gt; composites in ONIX 3.0 or later), and may
            also be accompanied by a ‘normal’ price
        VALUE_09: Linked price Price requires purchase with, or proof of
            ownership of another product. Further details of purchase or
            ownership requirements must be given in
            &lt;PriceTypeDescription&gt;
        VALUE_10: Library price Price for sale only to libraries
            (including public, school and academic libraries)
        VALUE_11: Education price Price for sale only to educational
            institutions (including school and academic libraries),
            educational buying consortia, government and local
            government bodies purchasing for use in education
        VALUE_12: Corporate price Price for sale to corporate customers
            only
        VALUE_13: Subscription service price Price for sale to
            organizations or services offering consumers subscription
            access to a library of books
        VALUE_14: School library price Price for primary and secondary
            education
        VALUE_15: Academic library price Price for higher education and
            scholarly institutions
        VALUE_16: Public library price
        VALUE_17: Introductory price Initial ‘Introductory offer’ price.
            Must be accompanied by an Effective until date in a
            &lt;PriceDate&gt; composite in ONIX 3, and may also be
            accompanied by a ‘normal’ price valid after the introductory
            offer expires (Fr. Prix de lancement). Only for use in ONIX
            3.0 or later
        VALUE_18: Consortial price Price for library consortia. Only for
            use in ONIX 3.0 or later
        VALUE_19: Education price for alternative provision (fr: « prix
            pour l’education specialisée ») Only for use in ONIX 3.0 or
            later
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
