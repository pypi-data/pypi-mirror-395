from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List51(Enum):
    """
    Product relation.

    Attributes:
        VALUE_00: Unspecified &lt;Product&gt; is related to
            &lt;RelatedProduct&gt; in a way that cannot be specified by
            another code value
        VALUE_01: Includes &lt;Product&gt; includes
            &lt;RelatedProduct&gt; (inverse of code 02)
        VALUE_02: Is part of &lt;Product&gt; is part of
            &lt;RelatedProduct&gt;: use for ‘also available as part of’
            (inverse of code 01)
        VALUE_03: Replaces &lt;Product&gt; replaces, or is new edition
            of, &lt;RelatedProduct&gt; (inverse of code 05)
        VALUE_04: Has companion product &lt;Product&gt; and
            &lt;RelatedProduct&gt; are companion products, intended to
            be used, or are usable, together (is own inverse). Only for
            use in ONIX 3.0 or later
        VALUE_05: Replaced by &lt;Product&gt; is replaced by, or has new
            edition, &lt;RelatedProduct&gt; (inverse of code 03)
        VALUE_06: Alternative format &lt;Product&gt; is available in an
            alternative format as &lt;RelatedProduct&gt; – indicates an
            alternative format of the same content which is or may be
            available (is own inverse)
        VALUE_07: Has ancillary product &lt;Product&gt; has an ancillary
            or supplementary product &lt;RelatedProduct&gt; (inverse of
            code 08)
        VALUE_08: Is ancillary to &lt;Product&gt; is ancillary or
            supplementary to &lt;RelatedProduct&gt; (inverse of code 07)
        VALUE_09: Is remaindered as &lt;Product&gt; is remaindered as
            &lt;RelatedProduct&gt;, when a remainder merchant assigns
            its own identifier to the product (inverse of code 10)
        VALUE_10: Is remainder of &lt;Product&gt; was originally sold as
            &lt;RelatedProduct&gt;, indicating the publisher’s original
            identifier for a title which is offered as a remainder under
            a different identifier (inverse of code 09)
        VALUE_11: Is other-language version of &lt;Product&gt; is an
            other-language version of &lt;RelatedProduct&gt; (is own
            inverse)
        VALUE_12: Publisher’s suggested alternative &lt;Product&gt; has
            a publisher’s suggested alternative &lt;RelatedProduct&gt;,
            which does not, however, carry the same content (cf 05 and
            06)
        VALUE_13: Epublication based on (print product) &lt;Product&gt;
            is an epublication based on printed product
            &lt;RelatedProduct&gt;. The related product is the source of
            any print-equivalent page numbering present in the
            epublication (inverse of code 27)
        VALUE_16: POD replacement for &lt;Product&gt; is a POD
            replacement for &lt;RelatedProduct&gt;.
            &lt;RelatedProduct&gt; is an out-of-print product replaced
            by a print-on-demand version under a new ISBN (inverse of
            code 17)
        VALUE_17: Replaced by POD &lt;Product&gt; is replaced by POD
            &lt;RelatedProduct&gt;. &lt;RelatedProduct&gt; is a print-
            on-demand replacement, under a new ISBN, for an out-of-print
            &lt;Product&gt; (inverse of code 16)
        VALUE_18: Is special edition of &lt;Product&gt; is a special
            edition of &lt;RelatedProduct&gt;. Used for a special
            edition (de: ‘Sonderausgabe’) with different cover, binding,
            premium content etc – more than ‘alternative format’ – which
            may be available in limited quantity and for a limited time
            (inverse of code 19)
        VALUE_19: Has special edition &lt;Product&gt; has a special
            edition &lt;RelatedProduct&gt; (inverse of code 18)
        VALUE_20: Is prebound edition of &lt;Product&gt; is a prebound
            edition of &lt;RelatedProduct&gt; (In the US, a ‘prebound’
            edition is ‘a book that was previously bound and has been
            rebound with a library quality hardcover binding. In almost
            all commercial cases, the book in question began as a
            paperback. This might also be termed ‘re-bound’) (inverse of
            code 21)
        VALUE_21: Is original of prebound edition &lt;Product&gt; is the
            regular edition of which &lt;RelatedProduct&gt; is a
            prebound edition (inverse of code 20)
        VALUE_22: Product by same author &lt;Product&gt; and
            &lt;RelatedProduct&gt; have a common author
        VALUE_23: Similar product &lt;RelatedProduct&gt; is another
            product that is suggested as similar to &lt;Product&gt; (‘if
            you liked &lt;Product&gt;, you may also like
            &lt;RelatedProduct&gt;’, or vice versa). In some markets,
            this may be termed a ‘comparison title’ or ‘comp title’
        VALUE_24: Is facsimile of &lt;Product&gt; is a facsimile edition
            of &lt;RelatedProduct&gt; (inverse of code 25)
        VALUE_25: Is original of facsimile &lt;Product&gt; is the
            original edition from which a facsimile edition
            &lt;RelatedProduct&gt; is taken (inverse of code 24)
        VALUE_26: Is license for &lt;Product&gt; is a license for a
            digital &lt;RelatedProduct&gt;, traded or supplied
            separately
        VALUE_27: Electronic version available as &lt;RelatedProduct&gt;
            is an electronic version of print &lt;Product&gt; (inverse
            of code 13)
        VALUE_28: Enhanced version available as &lt;RelatedProduct&gt;
            is an ‘enhanced’ version of &lt;Product&gt;, with additional
            content. Typically used to link an enhanced e-book to its
            original ‘unenhanced’ equivalent, but not specifically
            limited to linking e-books – for example, may be used to
            link non-illustrated and illustrated print books, original
            and enlarged editions etc. &lt;Product&gt; and
            &lt;RelatedProduct&gt; should share the same
            &lt;ProductForm&gt; (inverse of code 29)
        VALUE_29: Basic version available as &lt;RelatedProduct&gt; is a
            basic version of &lt;Product&gt;. &lt;Product&gt; and
            &lt;RelatedProduct&gt; should share the same
            &lt;ProductForm&gt; (inverse of code 28)
        VALUE_30: Product in same collection &lt;RelatedProduct&gt; and
            &lt;Product&gt; are part of the same collection (eg two
            products in same series or set, whether ordered or
            unordered) (is own inverse)
        VALUE_31: Has alternative in a different market sector
            &lt;RelatedProduct&gt; is an alternative product in another
            sector (of the same geographical market). Indicates an
            alternative that carries the same content, but available to
            a different set of customers, as one or both products are
            retailer-, channel- or market sector-specific (is own
            inverse)
        VALUE_32: Has equivalent intended for a different market
            &lt;RelatedProduct&gt; is an equivalent product, often
            intended for another (geographical) market. Indicates an
            alternative that carries essentially the same content,
            though slightly adapted for local circumstances (as opposed
            to a translation – use code 11) (is own inverse)
        VALUE_33: Has alternative intended for different market
            &lt;RelatedProduct&gt; is an alternative product, often
            intended for another (geographical) market. Indicates the
            content of the alternative is identical in all respects (is
            own inverse)
        VALUE_34: Cites &lt;Product&gt; cites &lt;RelatedProduct&gt;
            (inverse of code 35)
        VALUE_35: Is cited by &lt;Product&gt; is the object of a
            citation in &lt;RelatedProduct&gt; (inverse of code 34)
        VALUE_37: Is signed version of &lt;Product&gt; is a signed copy
            of &lt;RelatedProduct&gt;. Use where signed copies are given
            a distinct product identifier and can be ordered separately,
            but are otherwise identical (inverse of code 38)
        VALUE_38: Has signed version &lt;Product&gt; is an unsigned copy
            of &lt;RelatedProduct&gt;. Use where signed copies are given
            a distinct product identifier and can be ordered separately,
            but are otherwise identical (inverse of code 37)
        VALUE_39: Has related student material &lt;Product&gt; is
            intended for teacher use, and the related product is for
            student use
        VALUE_40: Has related teacher material &lt;Product&gt; is
            intended for student use, and the related product is for
            teacher use
        VALUE_41: Some content shared with &lt;Product&gt; includes some
            content shared with &lt;RelatedProduct&gt;. Note the shared
            content does not form the whole of either product. Compare
            with the ‘includes’ / ‘is part of’ relationship pair (codes
            01 and 02), where the shared content forms the whole of one
            of the products, and with the ‘alternative format’
            relationship (code 06), where the shared content forms the
            whole of both products (code 41 is own inverse)
        VALUE_42: Is later edition of first edition &lt;Product&gt; is a
            later edition of &lt;RelatedProduct&gt;, where the related
            product is the first edition
        VALUE_43: Adapted from &lt;Product&gt; is an adapted
            (dramatized, abridged, novelized etc) version of
            &lt;RelatedProduct&gt; (inverse of code 44). Only for use in
            ONIX 3.0 or later
        VALUE_44: Adapted as &lt;Product&gt; is the original from which
            &lt;RelatedProduct&gt; is adapted (dramatized etc) (inverse
            of code 43). Only for use in ONIX 3.0 or later
        VALUE_45: Has linked product offer Purchases of &lt;Product&gt;
            may qualify for one or more copies of &lt;RelatedProduct&gt;
            either free of charge or at a reduced price (inverse of code
            48). This may be dependent on retailer participation, upon
            price and upon the quantity of the &lt;Product&gt;
            purchased. Only for use in ONIX 3.0 or later
        VALUE_46: May be substituted by If ordered, &lt;Product&gt; may
            (at the supplier’s discretion) be substituted and the
            &lt;RelatedProduct&gt; supplied instead (inverse of code
            47). Only for use in ONIX 3.0 or later
        VALUE_47: May be substituted for If ordered,
            &lt;RelatedProduct&gt; may (at the supplier’s discretion) be
            substituted and the &lt;Product&gt; supplied instead
            (inverse of code 46). Only for use in ONIX 3.0 or later
        VALUE_48: Is linked product offer Purchases of
            &lt;RelatedProduct&gt; may qualify for one or more copies of
            &lt;Product&gt; either free of charge or at a reduced price
            (inverse of code 45). This may be dependent on retailer
            participation, upon price and upon the quantity of the
            &lt;RelatedProduct&gt; purchased. Only for use in ONIX 3.0
            or later
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
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_34 = "34"
    VALUE_35 = "35"
    VALUE_37 = "37"
    VALUE_38 = "38"
    VALUE_39 = "39"
    VALUE_40 = "40"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_44 = "44"
    VALUE_45 = "45"
    VALUE_46 = "46"
    VALUE_47 = "47"
    VALUE_48 = "48"
