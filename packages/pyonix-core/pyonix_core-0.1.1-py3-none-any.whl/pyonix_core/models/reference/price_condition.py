from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .price_condition_quantity import PriceConditionQuantity
from .price_condition_refname import PriceConditionRefname
from .price_condition_shortname import PriceConditionShortname
from .price_condition_type import PriceConditionType
from .product_identifier import ProductIdentifier

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class PriceCondition:
    """
    Details of condition that must be met to qualify for a particular price (eg
    ownership of a hardcover to qualify for purchase of an e-book at an
    advantageous price) ● Added &lt;ProductIdentifier&gt; at revision 3.0.2.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    price_condition_type: Optional[PriceConditionType] = field(
        default=None,
        metadata={
            "name": "PriceConditionType",
            "type": "Element",
            "required": True,
        },
    )
    price_condition_quantity: list[PriceConditionQuantity] = field(
        default_factory=list,
        metadata={
            "name": "PriceConditionQuantity",
            "type": "Element",
        },
    )
    product_identifier: list[ProductIdentifier] = field(
        default_factory=list,
        metadata={
            "name": "ProductIdentifier",
            "type": "Element",
        },
    )
    refname: Optional[PriceConditionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PriceConditionShortname] = field(
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
