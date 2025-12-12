from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List163(Enum):
    """
    Publishing date role.

    Attributes:
        VALUE_01: Publication date Nominal date of publication. This
            date is primarily used for planning, promotion and other
            business process purposes, and is not necessarily the first
            date for retail sales or fulfillment of pre-orders. In the
            absence of a sales embargo date, retail sales and pre-order
            fulfillment may begin as soon as stock is available to the
            retailer
        VALUE_02: Sales embargo date If there is an embargo on retail
            sales (in the market) before a certain date, the date from
            which the embargo is lifted and retail sales and fulfillment
            of pre-orders are permitted. (In some markets, this may be
            termed a ‘strict on-sale date’.) In the absence of an
            embargo date, retail sales and pre-order fulfillment may
            begin as soon as stock is available to the retailer
        VALUE_09: Public announcement date Date when a new product may
            be announced to the general public. Prior to the
            announcement date, the product data is intended for internal
            use by the recipient and supply chain partners only. After
            the announcement date, or in the absence of an announcement
            date, the planned product may be announced to the public as
            soon as metadata is available
        VALUE_10: Trade announcement date Date when a new product may be
            announced to the book trade only. Prior to the announcement
            date, the product information is intended for internal use
            by the recipient only. After the announcement date, or in
            the absence of a trade announcement date, the planned
            product may be announced to supply chain partners (but not
            necessarily made public – see the Public announcement date)
            as soon as metadata is available
        VALUE_11: Date of first publication Date when the work
            incorporated in a product was first published. For works in
            translation, see also Date of first publication in original
            language (code 20)
        VALUE_12: Latest reprint date Date when a product was most
            recently reprinted
        VALUE_13: Out-of-print / permanently withdrawn date Date when a
            product was (or will be) declared out-of-print, permanently
            withdrawn from sale or deleted
        VALUE_16: Latest reissue date Date when a product was most
            recently reissued
        VALUE_19: Publication date of print counterpart Date of
            publication of a printed book which is the direct print
            counterpart to a digital product. The counterpart product
            may be included in &lt;RelatedProduct&gt; using code 13
        VALUE_20: Date of first publication in original language Date
            when the original language version of work incorporated in a
            product was first published (note, use only on works in
            translation – see code 11 for first publication date in the
            translated language)
        VALUE_21: Forthcoming reissue date Date when a product will be
            reissued
        VALUE_22: Expected availability date after temporary withdrawal
            Date when a product that has been temporary withdrawn from
            sale or recalled for any reason is expected to become
            available again, eg after correction of quality or technical
            issues
        VALUE_23: Review embargo date Date from which reviews of a
            product may be published eg in newspapers and magazines or
            online. Provided to the book trade for information only:
            newspapers and magazines are not expected to be recipients
            of ONIX metadata
        VALUE_25: Publisher’s reservation order deadline Latest date on
            which an order may be placed with the publisher for
            guaranteed delivery prior to the publication date. May or
            may not be linked to a special reservation or pre-
            publication price
        VALUE_26: Forthcoming reprint date Date when a product will be
            reprinted
        VALUE_27: Preorder embargo date Earliest date a retail
            ‘preorder’ can be placed (in the market), where this is
            distinct from the public announcement date. In the absence
            of a preorder embargo, advance orders can be placed as soon
            as metadata is available to the consumer (this would be the
            public announcement date, or in the absence of a public
            announcement date, the earliest date metadata is available
            to the retailer)
        VALUE_28: Transfer date Date of acquisition of product by new
            publisher (use with publishing roles 09 and 13)
        VALUE_29: Date of production For an audiovisual work (eg on DVD)
        VALUE_30: Streaming embargo date For digital products that are
            available to end customers both as a download and streamed,
            the earliest date the product can be made available on a
            stream, where the streamed version becomes available later
            than the download. For the download, see code 02 if it is
            embargoed or code 01 if there is no embargo
        VALUE_31: Subscription embargo date For digital products that
            are available to end customers both as purchases and as part
            of a subscription package, the earliest date the product can
            be made available by subscription, where the product may not
            be included in a subscription package until some while after
            publication. For ordinary sales, see code 02 if there is a
            sales embargo or code 01 if there is no embargo
        VALUE_32: Download embargo date For digital products that are
            available to end customers both as a download and streamed,
            the earliest date the product can be made available via
            download, where the download version becomes available later
            than the stream. For any embargo on the stream, see code 02
        VALUE_33: Purchase embargo date For digital products that are
            available to end customers both as purchases and as part of
            a subscription package, the earliest date the product can be
            made available to purchase, where the product may not be
            purchased until some while after it becomes available via
            the subscription. For any embargo on the subscription, see
            code 02
        VALUE_35: CIP date Date by which CIP copy is required for
            inclusion in the product
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_09 = "09"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_16 = "16"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_35 = "35"
