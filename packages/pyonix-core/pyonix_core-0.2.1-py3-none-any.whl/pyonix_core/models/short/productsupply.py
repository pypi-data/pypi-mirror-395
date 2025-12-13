from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .market import Market
from .marketpublishingdetail import Marketpublishingdetail
from .productsupply_refname import ProductsupplyRefname
from .productsupply_shortname import ProductsupplyShortname
from .supplydetail import Supplydetail

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Productsupply:
    """Container for data describing a market, and specific publishing and supplier
    details of the product in that market.

    Note Block 6 consists of all &lt;ProductSupply&gt; containers
    together ● Modified cardinality of &lt;SupplyDetail at revision 3.0
    (2010)
    """

    class Meta:
        name = "productsupply"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    market: list[Market] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    marketpublishingdetail: Optional[Marketpublishingdetail] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    supplydetail: list[Supplydetail] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    refname: Optional[ProductsupplyRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[ProductsupplyShortname] = field(
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
