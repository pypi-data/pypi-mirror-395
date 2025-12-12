from dataclasses import dataclass, field
from typing import Optional

from .discount_amount import DiscountAmount
from .discount_percent import DiscountPercent
from .discount_refname import DiscountRefname
from .discount_shortname import DiscountShortname
from .discount_type import DiscountType
from .list3 import List3
from .quantity import Quantity
from .to_quantity import ToQuantity

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class Discount:
    """
    Details of the trade discount offered by the supplier, as a percentage of the
    price or an absolute amount per copy ● Added &lt;ToQuantity&gt; at revison
    3.0.2.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    discount_type: Optional[DiscountType] = field(
        default=None,
        metadata={
            "name": "DiscountType",
            "type": "Element",
        },
    )
    quantity: Optional[Quantity] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
        },
    )
    to_quantity: Optional[ToQuantity] = field(
        default=None,
        metadata={
            "name": "ToQuantity",
            "type": "Element",
        },
    )
    discount_percent: Optional[DiscountPercent] = field(
        default=None,
        metadata={
            "name": "DiscountPercent",
            "type": "Element",
            "required": True,
        },
    )
    discount_amount: list[DiscountAmount] = field(
        default_factory=list,
        metadata={
            "name": "DiscountAmount",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    refname: Optional[DiscountRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[DiscountShortname] = field(
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
