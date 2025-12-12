from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List68(Enum):
    """
    Market publishing status.

    Attributes:
        VALUE_00: Unspecified Status is not specified (as distinct from
            unknown): the default if the &lt;MarketPublishingStatus&gt;
            element is not sent
        VALUE_01: Cancelled The product was announced for publication in
            this market, and subsequently abandoned. A market
            publication date must not be sent
        VALUE_02: Forthcoming Not yet published in this market, should
            be accompanied by expected local publication date
        VALUE_03: Postponed indefinitely The product was announced for
            publication in this market, and subsequently postponed with
            no expected local publication date. A market publication
            date must not be sent
        VALUE_04: Active The product was published in this market, and
            is still active in the sense that the publisher will accept
            orders for it, though it may or may not be immediately
            available, for which see &lt;SupplyDetail&gt;
        VALUE_05: No longer our product Responsibility for the product
            in this market has been transferred elsewhere (with details
            of acquiring publisher representative in this market if
            possible in PR.25 (in ONIX 2.1) OR P.25 (in ONIX 3.0 or
            later))
        VALUE_06: Out of stock indefinitely The product was active in
            this market, but is now inactive in the sense that (a) the
            publisher representative (local publisher or sales agent)
            cannot fulfill orders for it, though stock may still be
            available elsewhere in the supply chain, and (b) there are
            no current plans to bring it back into stock in this market.
            Code 06 does not specifically imply that returns are or are
            not still accepted
        VALUE_07: Out of print The product was active in this market,
            but is now permanently inactive in this market in the sense
            that (a) the publisher representative (local publisher or
            sales agent) will not accept orders for it, though stock may
            still be available elsewhere in the supply chain, and (b)
            the product will not be made available again in this market
            under the same ISBN. Code 07 normally implies that the
            publisher will not accept returns beyond a specified date
        VALUE_08: Inactive The product was active in this market, but is
            now permanently or indefinitely inactive in the sense that
            the publisher representative (local publisher or sales
            agent) will not accept orders for it, though stock may still
            be available elsewhere in the supply chain. Code 08 covers
            both of codes 06 and 07, and may be used where the
            distinction between those values is either unnecessary or
            meaningless
        VALUE_09: Unknown The sender of the ONIX record does not know
            the current publishing status in this market
        VALUE_10: Remaindered The product is no longer available in this
            market from the publisher representative (local publisher or
            sales agent), under the current ISBN, at the current price.
            It may be available to be traded through another channel,
            usually at a reduced price
        VALUE_11: Withdrawn from sale Withdrawn from sale in this
            market, typically for legal reasons or to avoid giving
            offence
        VALUE_12: Not available in this market Either no rights are held
            for the product in this market, or for other reasons the
            publisher has decided not to make it available in this
            market
        VALUE_13: Active, but not sold separately The product is
            published and active in this market but, as a publishing
            decision, its constituent parts are not sold separately –
            only in an assembly or as part of a pack, eg with Product
            composition code 01. Also use with Product composition codes
            30, 31 where depending on product composition and pricing,
            items in the pack may be saleable separately at retail
        VALUE_14: Active, with market restrictions The product is
            published in this market and active, but is not available to
            all customer types, typically because the market is split
            between exclusive sales agents for different market
            segments. In ONIX 2.1, should be accompanied by a free-text
            statement in &lt;MarketRestrictionDetail&gt; describing the
            nature of the restriction. In ONIX 3.0 or later, the
            &lt;SalesRestriction&gt; composite in Group P.24 should be
            used
        VALUE_15: Recalled Recalled in this market for reasons of
            consumer safety
        VALUE_16: Temporarily withdrawn from sale Temporarily withdrawn
            from sale in this market, typically for quality or technical
            reasons. In ONIX 3.0 or later, must be accompanied by
            expected availability date coded ‘22’ within the
            &lt;MarketDate&gt; composite, except in exceptional
            circumstances where no date is known
        VALUE_17: Permanently withdrawn from sale Withdrawn permanently
            from sale in this market. Effectively synonymous with ‘Out
            of print’ (code 07), but specific to downloadable and online
            digital products (where no ‘stock’ would remain in the
            supply chain). Only for use in ONIX 3.0 or later
        VALUE_18: Active, but not sold as set The various constituent
            parts of a product are published and active in this market
            but, as a publishing decision, they are not sold together as
            a single product – eg with Product composition code 11 – and
            are only available as a number of individual items. Only for
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
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
