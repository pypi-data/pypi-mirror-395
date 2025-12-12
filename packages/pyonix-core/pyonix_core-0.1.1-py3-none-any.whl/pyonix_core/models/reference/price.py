from dataclasses import dataclass, field
from typing import Optional

from .batch_bonus import BatchBonus
from .comparison_product_price import ComparisonProductPrice
from .currency_code import CurrencyCode
from .currency_zone import CurrencyZone
from .discount import Discount
from .discount_coded import DiscountCoded
from .epub_license import EpubLicense
from .epub_technical_protection import EpubTechnicalProtection
from .list3 import List3
from .minimum_order_quantity import MinimumOrderQuantity
from .position_on_product import PositionOnProduct
from .price_amount import PriceAmount
from .price_coded import PriceCoded
from .price_condition import PriceCondition
from .price_constraint import PriceConstraint
from .price_date import PriceDate
from .price_identifier import PriceIdentifier
from .price_per import PricePer
from .price_qualifier import PriceQualifier
from .price_refname import PriceRefname
from .price_shortname import PriceShortname
from .price_status import PriceStatus
from .price_type import PriceType
from .price_type_description import PriceTypeDescription
from .printed_on_product import PrintedOnProduct
from .tax import Tax
from .tax_exempt import TaxExempt
from .territory import Territory
from .unpriced_item_type import UnpricedItemType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


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
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    price_identifier: list[PriceIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "PriceIdentifier",
            "type": "Element",
        },
    )
    price_type: Optional[PriceType] = field(
        default=None,
        metadata={
            "name": "PriceType",
            "type": "Element",
        },
    )
    price_qualifier: Optional[PriceQualifier] = field(
        default=None,
        metadata={
            "name": "PriceQualifier",
            "type": "Element",
        },
    )
    epub_technical_protection: list[EpubTechnicalProtection] = field(
        default_factory=list,
        metadata={
            "name": "EpubTechnicalProtection",
            "type": "Element",
        },
    )
    price_constraint: list[PriceConstraint] = field(
        default_factory=list,
        metadata={
            "name": "PriceConstraint",
            "type": "Element",
        },
    )
    epub_license: Optional[EpubLicense] = field(
        default=None,
        metadata={
            "name": "EpubLicense",
            "type": "Element",
        },
    )
    price_type_description: list[PriceTypeDescription] = field(
        default_factory=list,
        metadata={
            "name": "PriceTypeDescription",
            "type": "Element",
        },
    )
    price_per: Optional[PricePer] = field(
        default=None,
        metadata={
            "name": "PricePer",
            "type": "Element",
        },
    )
    price_condition: list[PriceCondition] = field(
        default_factory=list,
        metadata={
            "name": "PriceCondition",
            "type": "Element",
        },
    )
    minimum_order_quantity: Optional[MinimumOrderQuantity] = field(
        default=None,
        metadata={
            "name": "MinimumOrderQuantity",
            "type": "Element",
        },
    )
    batch_bonus: list[BatchBonus] = field(
        default_factory=list,
        metadata={
            "name": "BatchBonus",
            "type": "Element",
        },
    )
    discount_coded: list[DiscountCoded] = field(
        default_factory=list,
        metadata={
            "name": "DiscountCoded",
            "type": "Element",
        },
    )
    discount: list[Discount] = field(
        default_factory=list,
        metadata={
            "name": "Discount",
            "type": "Element",
        },
    )
    price_status: Optional[PriceStatus] = field(
        default=None,
        metadata={
            "name": "PriceStatus",
            "type": "Element",
        },
    )
    price_amount: Optional[PriceAmount] = field(
        default=None,
        metadata={
            "name": "PriceAmount",
            "type": "Element",
        },
    )
    price_coded: Optional[PriceCoded] = field(
        default=None,
        metadata={
            "name": "PriceCoded",
            "type": "Element",
        },
    )
    tax: list[Tax] = field(
        default_factory=list,
        metadata={
            "name": "Tax",
            "type": "Element",
        },
    )
    tax_exempt: Optional[TaxExempt] = field(
        default=None,
        metadata={
            "name": "TaxExempt",
            "type": "Element",
        },
    )
    unpriced_item_type: Optional[UnpricedItemType] = field(
        default=None,
        metadata={
            "name": "UnpricedItemType",
            "type": "Element",
        },
    )
    currency_code: Optional[CurrencyCode] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
        },
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "name": "Territory",
            "type": "Element",
        },
    )
    currency_zone: Optional[CurrencyZone] = field(
        default=None,
        metadata={
            "name": "CurrencyZone",
            "type": "Element",
        },
    )
    comparison_product_price: list[ComparisonProductPrice] = field(
        default_factory=list,
        metadata={
            "name": "ComparisonProductPrice",
            "type": "Element",
        },
    )
    price_date: list[PriceDate] = field(
        default_factory=list,
        metadata={
            "name": "PriceDate",
            "type": "Element",
        },
    )
    printed_on_product: Optional[PrintedOnProduct] = field(
        default=None,
        metadata={
            "name": "PrintedOnProduct",
            "type": "Element",
        },
    )
    position_on_product: Optional[PositionOnProduct] = field(
        default=None,
        metadata={
            "name": "PositionOnProduct",
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
