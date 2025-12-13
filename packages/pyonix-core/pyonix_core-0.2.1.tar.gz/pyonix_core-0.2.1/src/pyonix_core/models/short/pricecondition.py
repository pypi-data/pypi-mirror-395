from dataclasses import dataclass, field
from typing import Optional

from .list3 import List3
from .pricecondition_refname import PriceconditionRefname
from .pricecondition_shortname import PriceconditionShortname
from .priceconditionquantity import Priceconditionquantity
from .productidentifier import Productidentifier
from .x463 import X463

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/short"


@dataclass
class Pricecondition:
    """
    Details of condition that must be met to qualify for a particular price (eg
    ownership of a hardcover to qualify for purchase of an e-book at an
    advantageous price) ● Added &lt;ProductIdentifier&gt; at revision 3.0.2.
    """

    class Meta:
        name = "pricecondition"
        namespace = "http://ns.editeur.org/onix/3.0/short"

    x463: Optional[X463] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    priceconditionquantity: list[Priceconditionquantity] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    productidentifier: list[Productidentifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    refname: Optional[PriceconditionRefname] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shortname: Optional[PriceconditionShortname] = field(
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
