from dataclasses import dataclass, field
from typing import Optional

from .expected_date import ExpectedDate
from .list3 import List3
from .on_order import OnOrder
from .on_order_detail_refname import OnOrderDetailRefname
from .on_order_detail_shortname import OnOrderDetailShortname
from .proximity import Proximity

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class OnOrderDetail:
    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    on_order: Optional[OnOrder] = field(
        default=None,
        metadata={
            "name": "OnOrder",
            "type": "Element",
            "required": True,
        },
    )
    proximity: Optional[Proximity] = field(
        default=None,
        metadata={
            "name": "Proximity",
            "type": "Element",
        },
    )
    expected_date: Optional[ExpectedDate] = field(
        default=None,
        metadata={
            "name": "ExpectedDate",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[OnOrderDetailRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[OnOrderDetailShortname] = field(
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
