from dataclasses import dataclass, field
from typing import Optional

from .batchbonus import Batchbonus
from .comparisonproductprice import Comparisonproductprice
from .discount import Discount
from .discountcoded import Discountcoded
from .epublicense import Epublicense
from .j151 import J151
from .j152 import J152
from .j192 import J192
from .j239 import J239
from .j261 import J261
from .j262 import J262
from .j263 import J263
from .j266 import J266
from .list3 import List3
from .price_refname import PriceRefname
from .price_shortname import PriceShortname
from .pricecoded import Pricecoded
from .pricecondition import Pricecondition
from .priceconstraint import Priceconstraint
from .pricedate import Pricedate
from .priceidentifier import Priceidentifier
from .tax import Tax
from .territory import Territory
from .x301 import X301
from .x313 import X313
from .x317 import X317
from .x462 import X462
from .x475 import X475
from .x546 import X546

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Price:
    """
    Details of a price applied to the product ● Added &lt;TaxExempt&gt; at revision
    3.0.5 ● Added &lt;EpubTechnicalProtection&gt; and &lt;EpubLicense&gt; at
    revision 3.0.4 ● Added &lt;UnpricedItemType&gt;, &lt;PriceConstraint&gt;, &lt;
    at revision 3.0.3 ● Added &lt;PriceIdentifier&gt; at revision 3.0.2 ● Modified
    cardinality of &lt;PriceTypeDescription&gt; at revision 3.0.1 ● Added
    &lt;PriceCoded&gt;, &lt;ComparisonProductPrice&gt; at revision 3.0 (2010)
    """

    class Meta:
        name = "price"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    priceidentifier: list[Priceidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x462: Optional[X462] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j261: Optional[J261] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x317: list[X317] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    priceconstraint: list[Priceconstraint] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    epublicense: Optional[Epublicense] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j262: list[J262] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j239: Optional[J239] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    pricecondition: list[Pricecondition] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j263: Optional[J263] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    batchbonus: list[Batchbonus] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    discountcoded: list[Discountcoded] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    discount: list[Discount] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    j266: Optional[J266] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j151: Optional[J151] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    pricecoded: Optional[Pricecoded] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    tax: list[Tax] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x546: Optional[X546] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j192: Optional[J192] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    j152: Optional[J152] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x475: Optional[X475] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    comparisonproductprice: list[Comparisonproductprice] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    pricedate: list[Pricedate] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    x301: Optional[X301] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    x313: Optional[X313] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[PriceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PriceShortname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    datestamp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"(19|20)\d\d(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-8])(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|(19|20)\d\d(0[13-9]|1[0-2])(29|30)(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|(19|20)\d\d(0[13578]|1[02])31(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|19(0[48]|[13579][26]|[2468][048])0229(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?|20(0[048]|[13579][26]|[2468][048])0229(T([01][0-9]|2[0-3])[0-5][0-9]([0-5][0-9])?(Z|[+\-](0[0-9]|1[0-2])(00|15|30|45))?)?",
        },
    )
    sourcename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"\S(.*\S)?",
        },
    )
    sourcetype: Optional[List3] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
