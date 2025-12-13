from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .market_refname import MarketRefname
from .market_shortname import MarketShortname
from .sales_restriction import SalesRestriction
from .territory import Territory

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Market:
    """
    Details of a ‘market’ or distribution territory, primarily its geographical
    extent but any sales restrictions applicable within that area.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "name": "Territory",
            "type": "Element",
            "required": True,
        },
    )
    sales_restriction: list[SalesRestriction] = field(
        default_factory=list,
        metadata={
            "name": "SalesRestriction",
            "type": "Element",
        },
    )
    refname: Optional[MarketRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[MarketShortname] = field(
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
