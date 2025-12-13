from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


class List166(Enum):
    """
    Supply date role.

    Attributes:
        VALUE_02: Sales embargo date If there is an embargo on retail
            sales (of copies from the supplier) before a certain date
            and this is later than any general or market-wide embargo
            date, the date from which the embargo is lifted and retail
            sales and fulfillment of pre-orders are permitted. Use code
            02 here ONLY in the exceptional case when the embargo is
            supplier-specific. More general market-wide or global sales
            embargos should be specified in &lt;MarketDate&gt; or
            &lt;PublishingDate&gt; codes. In the absence of any
            supplier-specific, market-wide or general embargo date,
            retail sales and pre-order fulfillment may begin as soon as
            stock is available to the retailer
        VALUE_08: Expected availability date The date on which physical
            stock is expected to be available to be shipped from the
            supplier to retailers, or a digital product is expected to
            be released by the publisher or digital asset distributor to
            retailers or their retail platform providers
        VALUE_18: Last date for returns Last date when returns will be
            accepted, generally for a product which is being remaindered
            or put out of print
        VALUE_25: Reservation order deadline Latest date on which an
            order may be placed for guaranteed delivery prior to the
            publication date. May or may not be linked to a special
            reservation or pre-publication price
        VALUE_29: Last redownload date Latest date on which existing
            owners or licensees may download or re-download a copy of
            the product. Existing users may continue to use their local
            copy of the product
        VALUE_30: Last TPM date Date on which any required technical
            protection measures (DRM) support will be withdrawn. DRM-
            protected products may not be usable after this date
        VALUE_34: Expected warehouse date The date on which physical
            stock is expected to be delivered to the supplier from the
            manufacturer or from a primary distributor. For the
            distributor or wholesaler (the supplier) this is the ‘goods
            in’ date, as contrasted with the Expected availability date,
            code 08, which is the ‘goods out’ date
        VALUE_50: New supplier start date First date on which the
            supplier specified in &lt;NewSupplier&gt; will accept
            orders. Note the first date would typically be the day after
            the old supplier end date, but they may overlap if there is
            an agreement to forward any orders between old and new
            supplier for fulfillment
        VALUE_51: Supplier end date Last date on which the supplier
            specified in &lt;Supplier&gt; will accept orders. New
            supplier should be specified where available. Note last date
            would typically be the day before the new supplier start
            date, but they may overlap if there is an agreement to
            forward any orders between old and new supplier for
            fulfillment
    """

    VALUE_02 = "02"
    VALUE_08 = "08"
    VALUE_18 = "18"
    VALUE_25 = "25"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_34 = "34"
    VALUE_50 = "50"
    VALUE_51 = "51"
