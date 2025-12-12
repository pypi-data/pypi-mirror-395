from dataclasses import dataclass, field
from typing import Optional

from .cbo import Cbo
from .list3 import List3
from .location_identifier import LocationIdentifier
from .location_name import LocationName
from .on_hand import OnHand
from .on_order import OnOrder
from .on_order_detail import OnOrderDetail
from .proximity import Proximity
from .reserved import Reserved
from .stock_quantity_coded import StockQuantityCoded
from .stock_refname import StockRefname
from .stock_shortname import StockShortname
from .velocity import Velocity

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Stock:
    """
    Details of a supplier’s stock holding ● Added &lt;Reserved&gt; and adjacent
    &lt;Proximity&gt; at revision 3.0.4 ● Modified cardinality of
    &lt;LocationIdentifier&gt;, &lt;LocationName&gt; at revision 3.0.3 ● Added
    &lt;Proximity&gt;, &lt;Velocity&gt; at revision 3.0.2 ● Modified cardinality of
    &lt;StockQuantityCoded&gt; at revision 3.0.2.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    location_identifier: list[LocationIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "LocationIdentifier",
            "type": "Element",
        },
    )
    location_name: list[LocationName] = field(
        default_factory=list,
        metadata={
            "name": "LocationName",
            "type": "Element",
        },
    )
    stock_quantity_coded: list[StockQuantityCoded] = field(
        default_factory=list,
        metadata={
            "name": "StockQuantityCoded",
            "type": "Element",
        },
    )
    on_hand: Optional[OnHand] = field(
        default=None,
        metadata={
            "name": "OnHand",
            "type": "Element",
        },
    )
    proximity: list[Proximity] = field(
        default_factory=list,
        metadata={
            "name": "Proximity",
            "type": "Element",
            "max_occurs": 4,
        },
    )
    reserved: Optional[Reserved] = field(
        default=None,
        metadata={
            "name": "Reserved",
            "type": "Element",
        },
    )
    on_order: Optional[OnOrder] = field(
        default=None,
        metadata={
            "name": "OnOrder",
            "type": "Element",
        },
    )
    cbo: Optional[Cbo] = field(
        default=None,
        metadata={
            "name": "CBO",
            "type": "Element",
        },
    )
    on_order_detail: list[OnOrderDetail] = field(
        default_factory=list,
        metadata={
            "name": "OnOrderDetail",
            "type": "Element",
        },
    )
    velocity: list[Velocity] = field(
        default_factory=list,
        metadata={
            "name": "Velocity",
            "type": "Element",
        },
    )
    refname: Optional[StockRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[StockShortname] = field(
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
