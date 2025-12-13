from dataclasses import dataclass, field
from typing import Optional

from .batch_bonus_refname import BatchBonusRefname
from .batch_bonus_shortname import BatchBonusShortname
from .batch_quantity import BatchQuantity
from .free_quantity import FreeQuantity
from .list3 import List3

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class BatchBonus:
    """
    Details of bonus copies supplied (to the reseller) with a certain order
    quantity.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    batch_quantity: Optional[BatchQuantity] = field(
        default=None,
        metadata={
            "name": "BatchQuantity",
            "type": "Element",
            "required": True,
        },
    )
    free_quantity: Optional[FreeQuantity] = field(
        default=None,
        metadata={
            "name": "FreeQuantity",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[BatchBonusRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[BatchBonusShortname] = field(
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
