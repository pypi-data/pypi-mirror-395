from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .price_constraint_limit import PriceConstraintLimit
from .price_constraint_refname import PriceConstraintRefname
from .price_constraint_shortname import PriceConstraintShortname
from .price_constraint_status import PriceConstraintStatus
from .price_constraint_type import PriceConstraintType

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


@dataclass
class PriceConstraint:
    """
    Details of a constraint on use of a product when purchased at a specific price
    ● Added at revision 3.0.3.
    """

    class Meta:
        namespace = "http://ns.editeur.org/onix/3.0/reference"

    price_constraint_type: Optional[PriceConstraintType] = field(
        default=None,
        metadata={
            "name": "PriceConstraintType",
            "type": "Element",
            "required": True,
        },
    )
    price_constraint_status: Optional[PriceConstraintStatus] = field(
        default=None,
        metadata={
            "name": "PriceConstraintStatus",
            "type": "Element",
            "required": True,
        },
    )
    price_constraint_limit: list[PriceConstraintLimit] = field(
        default_factory=list,
        metadata={
            "name": "PriceConstraintLimit",
            "type": "Element",
        },
    )
    refname: Optional[PriceConstraintRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PriceConstraintShortname] = field(
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
