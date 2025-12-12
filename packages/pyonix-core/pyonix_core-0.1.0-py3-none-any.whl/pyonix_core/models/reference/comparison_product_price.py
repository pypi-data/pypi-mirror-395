from dataclasses import dataclass, field
from typing import Optional

from .comparison_product_price_refname import ComparisonProductPriceRefname
from .comparison_product_price_shortname import ComparisonProductPriceShortname
from .currency_code import CurrencyCode
from .list3 import List3
from .price_amount import PriceAmount
from .price_type import PriceType
from .product_identifier import ProductIdentifier

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ComparisonProductPrice:
    """
    ● Added at revision 3.0 (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    product_identifier: list[ProductIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ProductIdentifier",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    price_type: Optional[PriceType] = field(
        default=None,
        metadata={
            "name": "PriceType",
            "type": "Element",
        },
    )
    price_amount: Optional[PriceAmount] = field(
        default=None,
        metadata={
            "name": "PriceAmount",
            "type": "Element",
            "required": True,
        },
    )
    currency_code: Optional[CurrencyCode] = field(
        default=None,
        metadata={
            "name": "CurrencyCode",
            "type": "Element",
        },
    )
    refname: Optional[ComparisonProductPriceRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ComparisonProductPriceShortname] = field(
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
