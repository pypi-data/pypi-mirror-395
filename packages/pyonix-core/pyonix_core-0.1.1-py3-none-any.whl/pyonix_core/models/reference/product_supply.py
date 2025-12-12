from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .market import Market
from .market_publishing_detail import MarketPublishingDetail
from .product_supply_refname import ProductSupplyRefname
from .product_supply_shortname import ProductSupplyShortname
from .supply_detail import SupplyDetail

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class ProductSupply:
    """Container for data describing a market, and specific publishing and supplier
    details of the product in that market.

    Note Block 6 consists of all &lt;ProductSupply&gt; containers
    together ● Modified cardinality of &lt;SupplyDetail at revision 3.0
    (2010)
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    market: list[Market] = field(
        default_factory=list,
        metadata={
            "name": "Market",
            "type": "Element",
        },
    )
    market_publishing_detail: Optional[MarketPublishingDetail] = field(
        default=None,
        metadata={
            "name": "MarketPublishingDetail",
            "type": "Element",
        },
    )
    supply_detail: list[SupplyDetail] = field(
        default_factory=list,
        metadata={
            "name": "SupplyDetail",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[ProductSupplyRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductSupplyShortname] = field(
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
