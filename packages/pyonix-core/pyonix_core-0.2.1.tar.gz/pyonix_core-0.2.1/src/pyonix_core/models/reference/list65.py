from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List65(Enum):
    """
    Product availability.

    Attributes:
        VALUE_01: Cancelled Product was announced, and subsequently
            abandoned by the publisher. No expected availability date
            should be included in &lt;SupplyDate&gt;
        VALUE_09: Not yet available, postponed indefinitely Product is
            not yet available from the supplier, and the publisher
            indicates that it has been postponed indefinitely. Should be
            used in preference to code 10 where the publisher has
            indicated that a previously-announced publication date is no
            longer correct, and no new date has yet been announced. No
            expected availability date should be included in
            &lt;SupplyDate&gt;. Only for use in ONIX 3.0 or later
        VALUE_10: Not yet available Product is not yet available
            (requires expected date, either as &lt;ExpectedShipDate&gt;
            (ONIX 2.1) or as &lt;SupplyDate&gt; with
            &lt;SupplyDateRole&gt; coded ‘08’ (ONIX 3.0 or later),
            except in exceptional circumstances where no date is known)
        VALUE_11: Awaiting stock Product is not yet available, but will
            be a stock item when available (requires expected date,
            either as &lt;ExpectedShipDate&gt; (ONIX 2.1) or as
            &lt;SupplyDate&gt; with &lt;SupplyDateRole&gt; coded ‘08’
            (ONIX 3.0 or later), except in exceptional circumstances
            where no date is known). Used particularly for imports which
            have been published in the country of origin but have not
            yet arrived in the importing country
        VALUE_12: Not yet available, will be POD Product is not yet
            available, to be published as print-on-demand only (requires
            expected date, either as &lt;ExpectedShipDate&gt; (ONIX 2.1)
            or as &lt;SupplyDate&gt; with &lt;SupplyDateRole&gt; coded
            ‘08’ (ONIX 3.0 or later), except in exceptional
            circumstances where no date is known). May apply either to a
            POD successor to an existing conventional edition, when the
            successor will be published under a different ISBN (normally
            because different trade terms apply); or to a title that is
            being published as a POD original
        VALUE_20: Available Product is available from the supplier (form
            of availability unspecified)
        VALUE_21: In stock Product is available from the supplier as a
            stock item
        VALUE_22: To order Product is available from the supplier as a
            non-stock item, by special order. Where possible, an
            &lt;OrderTime&gt; should be included
        VALUE_23: POD Product is available from the supplier by print-
            on-demand. If the fulfillment delay is likely to be more
            than 24 hours, an &lt;OrderTime&gt; should be included
        VALUE_30: Temporarily unavailable Product is temporarily
            unavailable: temporarily unavailable from the supplier
            (reason unspecified) (requires expected date, either as
            &lt;ExpectedShipDate&gt; (ONIX 2.1) or as &lt;SupplyDate&gt;
            with &lt;SupplyDateRole&gt; coded ‘08’ (ONIX 3.0 or later),
            except in exceptional circumstances where no date is known)
        VALUE_31: Out of stock Product is stock item, but is temporarily
            out of stock (requires expected date, either as
            &lt;ExpectedShipDate&gt; (ONIX 2.1) or as &lt;SupplyDate&gt;
            with &lt;SupplyDateRole&gt; coded ‘08’ (ONIX 3.0 or later),
            except in exceptional circumstances where no date is known)
        VALUE_32: Reprinting Product is temporarily unavailable, and is
            reprinting (requires expected date, either as
            &lt;ExpectedShipDate&gt; (ONIX 2.1) or as &lt;SupplyDate&gt;
            with &lt;SupplyDateRole&gt; coded ‘08’ (ONIX 3.0 or later),
            except in exceptional circumstances where no date is known)
        VALUE_33: Awaiting reissue Product is temporarily unavailable,
            awaiting reissue (requires expected date, either as
            &lt;ExpectedShipDate&gt; (ONIX 2.1) or as &lt;SupplyDate&gt;
            with &lt;SupplyDateRole&gt; coded ‘08’ (ONIX 3.0 or later),
            except in exceptional circumstances where no date is known)
        VALUE_34: Temporarily withdrawn from sale Product is temporarily
            withdrawn from sale, possibly for quality or technical
            reasons. Requires expected availability date, either as
            &lt;ExpectedShipDate&gt; (ONIX 2.1) or as &lt;SupplyDate&gt;
            with &lt;SupplyDateRole&gt; coded ‘08’ (ONIX 3.0 or later),
            except in exceptional circumstances where no date is known
        VALUE_40: Not available (reason unspecified) Product is not
            available from the supplier (for any reason)
        VALUE_41: Not available, replaced by new product Product is
            unavailable, but a successor product or edition is or will
            be available from the supplier (identify successor in
            &lt;RelatedProduct&gt;)
        VALUE_42: Not available, other format available Product is
            unavailable, but the same content is or will be available
            from the supplier in an alternative format (identify other
            format product in &lt;RelatedProduct&gt;)
        VALUE_43: No longer supplied by the supplier Product is no
            longer available from the supplier. Identify new supplier in
            &lt;NewSupplier&gt; if possible
        VALUE_44: Apply direct Product is not available to trade, apply
            direct to publisher
        VALUE_45: Not sold separately Product must be bought as part of
            a set or trade pack (identify set or pack in
            &lt;RelatedProduct&gt; using code 02). Individual copies of
            the product are not available from the supplier, but packs
            of copies are available, and individual copies of the
            product may typically be sold at retail
        VALUE_46: Withdrawn from sale Product is withdrawn from sale,
            possibly permanently. May be for legal reasons or to avoid
            giving offence
        VALUE_47: Remaindered Product has been remaindered and is no
            longer available from the supplier in the normal way, but
            may be available under different terms and conditions in
            order to dispose of excess stock
        VALUE_48: Not available, replaced by POD Product is out of
            print, but a print-on-demand edition is or will be available
            under a different ISBN. Use only when the POD successor has
            a different ISBN, normally because different trade terms
            apply
        VALUE_49: Recalled Product has been recalled, possibly for
            reasons of consumer safety
        VALUE_50: Not sold as set Contents of set or pack must be bought
            as individual items (identify contents of set or pack in
            &lt;RelatedProduct&gt; using code 01). Used when a
            collection that is not sold as a set nevertheless has its
            own ONIX record
        VALUE_51: Not available, publisher indicates OP Product is
            unavailable from the supplier, no successor product or
            alternative format is available or planned. Use this code
            only when the publisher has indicated the product is out of
            print
        VALUE_52: Not available, publisher no longer sells product in
            this market Product is unavailable from the supplier in this
            market, no successor product or alternative format is
            available or planned. Use this code when a publisher has
            indicated the product is permanently unavailable (in this
            market) while remaining available elsewhere
        VALUE_97: No recent update received Sender has not received any
            recent update for this product from the publisher or
            supplier (for use when the sender is a data aggregator). The
            definition of ‘recent’ must be specified by the aggregator,
            or by agreement between parties to an exchange
        VALUE_98: No longer receiving updates Sender is no longer
            receiving any updates from the publisher or supplier of this
            product (for use when the sender is a data aggregator)
        VALUE_99: Contact supplier Product availability not known to
            sender
    """

    VALUE_01 = "01"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_34 = "34"
    VALUE_40 = "40"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_44 = "44"
    VALUE_45 = "45"
    VALUE_46 = "46"
    VALUE_47 = "47"
    VALUE_48 = "48"
    VALUE_49 = "49"
    VALUE_50 = "50"
    VALUE_51 = "51"
    VALUE_52 = "52"
    VALUE_97 = "97"
    VALUE_98 = "98"
    VALUE_99 = "99"
