from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .price_condition_quantity_refname import PriceConditionQuantityRefname
from .price_condition_quantity_shortname import PriceConditionQuantityShortname
from .price_condition_quantity_type import PriceConditionQuantityType
from .quantity import Quantity
from .quantity_unit import QuantityUnit

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class PriceConditionQuantity:
    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    price_condition_quantity_type: Optional[PriceConditionQuantityType] = (
        field(
            default=None,
            metadata={
                "name": "PriceConditionQuantityType",
                "type": "Element",
                "required": True,
            },
        )
    )
    quantity: Optional[Quantity] = field(
        default=None,
        metadata={
            "name": "Quantity",
            "type": "Element",
            "required": True,
        },
    )
    quantity_unit: Optional[QuantityUnit] = field(
        default=None,
        metadata={
            "name": "QuantityUnit",
            "type": "Element",
            "required": True,
        },
    )
    refname: Optional[PriceConditionQuantityRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PriceConditionQuantityShortname] = field(
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
